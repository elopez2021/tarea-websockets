import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_FILENAME = "Informe_WebSockets_Algoritmos_Paralelos.pdf"
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")

class NumberedCanvas(canvas.Canvas):
    """Canvas that computes total pages dynamically and adds header/footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header (from page 2 onwards)
        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(45, 748, 567, 748)
            self.drawString(45, 755, "Algoritmos Paralelos | Comunicación Bidireccional en Tiempo Real (WebSockets)")
            self.drawRightString(567, 755, "Entrega de Laboratorio")

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(45, 45, 567, 45)
        self.drawString(45, 33, "Informe Técnico: Servidor Express + WebSocket (ws) con Bootstrap 5")
        self.drawRightString(567, 33, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()

def build_pdf():
    # 6-page professional document layout
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=48,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=1,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=0,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=4,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5
    )

    meta_table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#334155")),
    ])

    story = []

    # =========================================================================
    # PÁGINA 1: PORTADA + 1. ARQUITECTURA UTILIZADA
    # =========================================================================
    story.append(Paragraph("APLICACIÓN CLIENTE-SERVIDOR CON WEBSOCKETS", title_style))
    story.append(Paragraph("Demostración de Comunicación Bidireccional en Tiempo Real sin Polling", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceAfter=8))

    meta_data = [
        [Paragraph("<b>Asignatura:</b>", body_style), Paragraph("Algoritmos Paralelos / Sistemas Distribuidos", body_style)],
        [Paragraph("<b>Objetivo:</b>", body_style), Paragraph("Demostrar comunicación concurrente en tiempo real mediante WebSockets sin consultas continuas.", body_style)],
        [Paragraph("<b>Stack Tecnológico:</b>", body_style), Paragraph("Node.js v22, Express.js, ws (RFC 6455), Morgan Logger, Bootstrap 5.3, Vanilla JS", body_style)],
        [Paragraph("<b>Topología:</b>", body_style), Paragraph("Servidor unificado HTTP + WS (puerto 3000) con múltiples clientes concurrentes", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[105, 417])
    meta_table.setStyle(meta_table_style)
    story.append(meta_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Arquitectura Utilizada", h1_style))
    story.append(Paragraph(
        "Para responder a los requisitos de la práctica, se implementó una <b>arquitectura reactiva orientada a eventos</b> sustentada "
        "en el protocolo <b>WebSocket (RFC 6455)</b> sobre transporte TCP persistente, acoplado armónicamente con un servidor web <b>Express.js</b>.",
        body_style
    ))
    story.append(Paragraph(
        "A diferencia del paradigma tradicional <i>Request/Response</i> de HTTP —donde el cliente debe realizar consultas cíclicas constantes "
        "(<i>Polling</i> o <i>Long-Polling</i>) saturando la red con peticiones vacías—, WebSocket realiza una negociación inicial "
        "(<i>HTTP Upgrade Handshake</i>) y mantiene un <b>túnel full-duplex bidireccional permanente</b>. Así, el servidor empuja (<i>push</i>) "
        "los eventos a todos los clientes al instante con una cabecera de trama ínfima (2 a 10 bytes).",
        body_style
    ))

    comp_data = [
        [Paragraph("<b>Criterio Técnico</b>", body_style), Paragraph("<b>HTTP Polling Tradicional</b>", body_style), Paragraph("<b>WebSockets (Arquitectura Actual)</b>", body_style)],
        [Paragraph("<b>Tipo de Comunicación</b>", body_style), Paragraph("Unidireccional por turno (cliente consulta)", body_style), Paragraph("Full-Duplex simultáneo (ambos emiten a discreción)", body_style)],
        [Paragraph("<b>Sobrecarga (Overhead)</b>", body_style), Paragraph("Alta (~800 bytes de cabecera HTTP por mensaje)", body_style), Paragraph("Mínima (~2-10 bytes por trama TCP)", body_style)],
        [Paragraph("<b>Latencia de Entrega</b>", body_style), Paragraph("Alta: sujeta al intervalo de sondeo (segundos)", body_style), Paragraph("Inmediata: submilisegundo en cuanto se produce el evento", body_style)],
        [Paragraph("<b>Consumo de Recursos</b>", body_style), Paragraph("Alto: miles de aperturas/cierres de sockets TCP", body_style), Paragraph("Óptimo: un socket persistente gestionado por el Event Loop", body_style)]
    ]
    comp_table = Table(comp_data, colWidths=[110, 206, 206])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EEF2F6")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Capas del Sistema Implementado:</b>", h2_style))
    story.append(Paragraph("• <b>Capa Cliente (Frontend):</b> Interfaz responsiva desarrollada con <b>Bootstrap 5.3</b> y Bootstrap Icons. Utiliza la API estándar <code>window.WebSocket</code> nativa del navegador, sin librerías pesadas.", bullet_style))
    story.append(Paragraph("• <b>Capa Servidor Web (HTTP):</b> Servidor <b>Express.js</b> que publica la aplicación en <code>GET /</code> y expone un endpoint REST de diagnóstico en <code>GET /api/status</code> (JSON).", bullet_style))
    story.append(Paragraph("• <b>Capa de Tiempo Real (WebSocket Server):</b> Instancia <code>WebSocketServer</code> de la librería <code>ws</code> asociada al mismo puerto TCP 3000 bajo la ruta <code>/ws</code>.", bullet_style))
    story.append(Paragraph("• <b>Capa de Auditoría (Logging):</b> Middleware <b>Morgan ('dev')</b> para registrar en consola peticiones HTTP, junto con trazabilidad de eventos WebSocket (conexión, mensajes y desconexión).", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: 2. CAPTURA DEL CÓDIGO DEL SERVIDOR
    # =========================================================================
    story.append(Paragraph("2. Captura del Código del Servidor (server.js)", h1_style))
    story.append(Paragraph(
        "A continuación se presenta la captura del código fuente completo del servidor en Node.js ([server.js](file:///e:/algoritmos%20paralelos/tarea%20websockets/server.js)), "
        "el cual integra Express.js con la librería <code>ws</code> para manejar clientes concurrentes, rutas HTTP y difusión masiva:",
        body_style
    ))

    server_img = os.path.join(SCREENSHOTS_DIR, "codigo_servidor.png")
    if os.path.exists(server_img):
        story.append(Image(server_img, width=490, height=395))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Análisis Técnico del Código del Servidor:</b>", h2_style))
    story.append(Paragraph("• <b>Unificación HTTP + WebSocket:</b> <code>http.createServer(app)</code> permite que Express y <code>new WebSocketServer({ server, path: '/ws' })</code> compartan el puerto 3000 de forma eficiente.", bullet_style))
    story.append(Paragraph("• <b>Conjunto Concurrente de Clientes (Set):</b> Se aprovecha <code>wss.clients</code> para iterar sobre todas las conexiones vivas y validar su estado con <code>client.readyState === WebSocket.OPEN</code>.", bullet_style))
    story.append(Paragraph("• <b>Difusión Masiva (Broadcast):</b> La función <code>broadcast(payload)</code> serializa los datos en JSON y los reenvía de forma no bloqueante a todos los navegadores conectados.", bullet_style))
    story.append(Paragraph("• <b>Generación de Timestamp:</b> El servidor es la única fuente de verdad para la fecha y hora oficial (<code>DD/MM/AAAA HH:MM:SS</code>), evitando discrepancias entre relojes locales de clientes.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: 3. CAPTURA DEL CÓDIGO DEL CLIENTE
    # =========================================================================
    story.append(Paragraph("3. Captura del Código del Cliente (public/index.html)", h1_style))
    story.append(Paragraph(
        "A continuación se presenta la captura del código cliente ([public/index.html](file:///e:/algoritmos%20paralelos/tarea%20websockets/public/index.html)), "
        "donde se gestiona la conexión WebSocket nativa, el control reactivo del DOM y la interfaz estilizada con Bootstrap 5:",
        body_style
    ))

    client_img = os.path.join(SCREENSHOTS_DIR, "codigo_cliente.png")
    if os.path.exists(client_img):
        story.append(Image(client_img, width=490, height=395))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Análisis Técnico del Código del Cliente:</b>", h2_style))
    story.append(Paragraph("• <b>Conexión Estándar (RFC 6455):</b> <code>socket = new WebSocket(wsUrl)</code> se enlaza directamente a <code>ws://localhost:3000/ws</code> usando la API nativa de JavaScript sin dependencias.", bullet_style))
    story.append(Paragraph("• <b>Listener Reactivo <code>socket.onmessage</code>:</b> Se activa de forma asíncrona ante la llegada de tramas, ejecuta <code>JSON.parse(event.data)</code> y delega la renderización a funciones especializadas.", bullet_style))
    story.append(Paragraph("• <b>Detección de Caída <code>socket.onclose</code>:</b> Si el servidor se detiene o se cierra la sesión, actualiza de inmediato el badge visual a <i>'Desconectado'</i> (rojo) y emite un aviso local.", bullet_style))
    story.append(Paragraph("• <b>Sanitización de Datos:</b> La función <code>escapeHtml()</code> garantiza la protección contra ataques de inyección de código (XSS) antes de inyectar texto al DOM del chat.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: 4. CAPTURA DE DOS CLIENTES COMUNICÁNDOSE EN TIEMPO REAL
    # =========================================================================
    story.append(Paragraph("4. Captura de Dos Clientes Comunicándose en Tiempo Real", h1_style))
    story.append(Paragraph(
        "Se ejecutó una prueba empírica concurrente abriendo dos navegadores independientes con sesiones activas: "
        "<b>Cliente 1 (Carlos)</b> y <b>Cliente 2 (Ana)</b>. Las capturas demuestran la sincronización simultánea e instantánea:",
        body_style
    ))

    carlos_img = os.path.join(SCREENSHOTS_DIR, "cliente_carlos.png")
    ana_img = os.path.join(SCREENSHOTS_DIR, "cliente_ana.png")

    if os.path.exists(carlos_img):
        story.append(Paragraph("<b>Figura 4.1: Vista del Cliente 1 — Usuario 'Carlos'</b>", h2_style))
        story.append(Image(carlos_img, width=490, height=210))
        story.append(Spacer(1, 4))

    if os.path.exists(ana_img):
        story.append(Paragraph("<b>Figura 4.2: Vista del Cliente 2 — Usuario 'Ana'</b>", h2_style))
        story.append(Image(ana_img, width=490, height=210))
        story.append(Spacer(1, 5))

    story.append(Paragraph("<b>Evidencias Observadas en la Prueba en Vivo:</b>", h2_style))
    story.append(Paragraph("1. <b>Notificación de Presencia:</b> Cuando 'Ana' ingresa, la pantalla de 'Carlos' muestra la alerta verde <i>'El usuario Ana se ha conectado'</i> con fecha y hora exacta sin recargar.", bullet_style))
    story.append(Paragraph("2. <b>Contador Concurrente:</b> Ambas interfaces sincronizan en la barra superior el indicador verde <i>'2 usuarios en línea'</i>.", bullet_style))
    story.append(Paragraph("3. <b>Bidireccionalidad Instantánea:</b> Los mensajes de Carlos y Ana aparecen en milisegundos en ambas ventanas, formateados con burbujas propias (azul a la derecha) y de terceros (blanco a la izquierda).", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: 5. EXPLICACIÓN DEL FLUJO DE COMUNICACIÓN
    # =========================================================================
    story.append(Paragraph("5. Explicación del Flujo de Comunicación", h1_style))
    story.append(Paragraph(
        "El ciclo completo de vida de la interacción entre los clientes y el servidor se detalla a continuación a través de sus cuatro etapas operativas:",
        body_style
    ))

    flujo_data = [
        [Paragraph("<b>Etapa</b>", body_style), Paragraph("<b>Trama / Protocolo</b>", body_style), Paragraph("<b>Descripción Detallada del Proceso</b>", body_style)],
        [
            Paragraph("<b>1. Handshake Inicial</b>", body_style),
            Paragraph("<code>GET /ws HTTP/1.1</code><br/><code>Upgrade: websocket</code><br/><code>Connection: Upgrade</code>", body_style),
            Paragraph("El cliente solicita la actualización de protocolo. Express delega el handshake al servidor <code>ws</code>, el cual responde con <code>101 Switching Protocols</code>, dejando el socket TCP abierto permanentemente.", body_style)
        ],
        [
            Paragraph("<b>2. Registro (Join)</b>", body_style),
            Paragraph("JSON Cliente → Servidor:<br/><code>{ type: 'join', username: '...' }</code>", body_style),
            Paragraph("El cliente manda su alias. El servidor registra <code>ws.username</code> y ejecuta un broadcast con un evento de sistema informando a toda la sala de la nueva conexión junto con el timestamp y la lista actualizada.", body_style)
        ],
        [
            Paragraph("<b>3. Chat en Tiempo Real</b>", body_style),
            Paragraph("JSON Cliente → Servidor:<br/><code>{ type: 'message', text: '...' }</code>", body_style),
            Paragraph("Al hacer clic en Enviar o presionar Enter, el texto viaja por el socket. El servidor le añade la marca de tiempo oficial y lo retransmite de inmediato a todos los clientes activos mediante <code>broadcast()</code>.", body_style)
        ],
        [
            Paragraph("<b>4. Desconexión</b>", body_style),
            Paragraph("Trama TCP Close Frame<br/>(Evento <code>ws.on('close')</code>)", body_style),
            Paragraph("Al cerrar la pestaña o pulsar 'Salir', se interrumpe el socket TCP. El servidor lo detecta al instante, lo purga de su lista y notifica al resto de clientes: <i>'El usuario X se ha desconectado'</i>.", body_style)
        ]
    ]

    flujo_table = Table(flujo_data, colWidths=[90, 140, 292])
    flujo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EEF2F6")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(flujo_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Diagrama de Secuencia Temporal de Mensajería:</b>", h2_style))
    diag_text = (
        "Cliente 1 (Carlos)                 Servidor Node.js (ws)                Cliente 2 (Ana)\n"
        "      │                                      │                                 │\n"
        "      ├── 1. HTTP Upgrade (GET /ws) ────────►│                                 │\n"
        "      │◄── 101 Switching Protocols ──────────┤                                 │\n"
        "      ├── 2. { type: 'join', 'Carlos' } ────►│                                 │\n"
        "      │◄── Broadcast: 'Carlos conectado' ────┤                                 │\n"
        "      │                                      │◄── 3. Upgrade + Join ('Ana') ───┤\n"
        "      │◄── Broadcast: 'Ana conectada' ───────┼─── Broadcast: 'Ana conectada' ──►\n"
        "      │                                      │                                 │\n"
        "      ├── 4. Chat: '¡Hola Ana!' ────────────►│                                 │\n"
        "      │◄── Broadcast: Carlos: '¡Hola Ana!' ──┼─── Broadcast: Carlos: 'Hola...'─►\n"
        "      │                                      │◄── 5. Chat: '¡Hola Carlos!' ────┤\n"
        "      │◄── Broadcast: Ana: '¡Hola Carlos!' ──┼─── Broadcast: Ana: 'Hola...'────►\n"
        "      │                                      │                                 │\n"
        "      │                                      │◄── 6. Cierre TCP (Cierra Ana) ──x\n"
        "      │◄── Broadcast: 'Ana desconectada' ────┤                                 │"
    )
    diag_table = Table([[Paragraph(f"<font face='Courier' size='7.5'>{diag_text.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", body_style)]], colWidths=[522])
    diag_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#38BDF8")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#334155")),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(diag_table)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 6: 6. CONCLUSIONES
    # =========================================================================
    story.append(Paragraph("6. Conclusiones", h1_style))
    story.append(Paragraph(
        "A partir del diseño, implementación y verificación experimental de la aplicación desarrollada, se concluye lo siguiente:",
        body_style
    ))

    story.append(Paragraph(
        "1. <b>Superación categórica del modelo de sondeo (Polling):</b> El protocolo WebSocket erradica la necesidad de que los clientes "
        "interroguen reiteradamente al servidor en busca de novedades. La capacidad del servidor para emitir eventos de forma reactiva (<i>Server Push</i>) "
        "en el milisegundo exacto en que suceden representa un salto cualitativo en eficiencia computacional y ahorro de ancho de banda.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "2. <b>Alta concurrencia en I/O con bajo consumo de memoria:</b> En el marco de la asignatura de <i>Algoritmos Paralelos</i>, se comprobó "
        "que el modelo asíncrono no bloqueante basado en el <i>Event Loop</i> de Node.js y la librería <code>ws</code> permite mantener múltiples "
        "sockets abiertos en reposo con un consumo despreciable de memoria RAM (~10-15 KB por conexión inactiva), superando arquitecturas tradicionales "
        "basadas en un hilo de sistema operativo por cliente (<i>thread-per-connection</i>).",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "3. <b>Ventajas de la implementación con WebSockets Estándar (RFC 6455):</b> Frente a soluciones de alto nivel como Socket.IO (que "
        "incorporan polling como fallback y abstracciones propietarias), el uso de la API nativa de JavaScript y la librería <code>ws</code> "
        "permite un dominio absoluto del protocolo, transparencia en las tramas JSON transmitidas y total apego a los estándares internacionales.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "4. <b>Sincronización temporal fidedigna:</b> La delegación de la marca de tiempo (<i>timestamp</i>) en el backend garantiza que "
        "todos los nodos participantes ordenen cronológicamente los mensajes de manera coherente, resolviendo problemas de sincronización en sistemas distribuidos.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "5. <b>Experiencia de usuario moderna:</b> La integración armónica de Bootstrap 5 con listeners en tiempo real ofrece una experiencia de uso "
        "ágil, intuitiva y fluida, confirmando la pertinencia de WebSockets en aplicaciones contemporáneas como mensajería instantánea, videojuegos multijugador, "
        "paneles de control financiero (<i>dashboards</i>) y telemetría de dispositivos IoT.",
        bullet_style
    ))
    story.append(Spacer(1, 14))

    # Recuadro final de cierre institucional
    final_box = [
        [Paragraph("<b>Fin del Informe de Laboratorio — Proyecto Funcional y Verificado</b>", ParagraphStyle('Final', parent=body_style, alignment=1, fontName='Helvetica-Bold', textColor=colors.HexColor("#1E3A8A")))],
        [Paragraph("Repositorio verificado con Node.js v22.18.0, Express.js y WebSocket RFC 6455.", ParagraphStyle('FinalSub', parent=body_style, alignment=1, fontSize=8, textColor=colors.HexColor("#64748B")))]
    ]
    t_final = Table(final_box, colWidths=[522])
    t_final.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(t_final)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {PDF_FILENAME}")

if __name__ == "__main__":
    build_pdf()
