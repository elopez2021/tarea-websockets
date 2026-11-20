# Aplicación Cliente-Servidor con WebSockets y Express.js

Esta aplicación demuestra el funcionamiento de la **comunicación bidireccional en tiempo real** utilizando **WebSockets**, **Express.js (Node.js)** y una interfaz moderna con **Bootstrap 5**.

A diferencia del modelo tradicional basado en *Polling* (donde el cliente consulta repetidamente al servidor por novedades), WebSockets mantiene una conexión TCP persistente y abierta que permite al servidor enviar datos instantáneamente al cliente (push) en el momento en que ocurre un evento.

---

## 🚀 Características Implementadas

- **Servidor web con Express:** Sirve de forma limpia y directa la interfaz de usuario en la carpeta `public/`.
- **Conexión de múltiples clientes simultáneos:** Varios navegadores o pestañas pueden conectarse a la vez.
- **Detección de conexión:** Se notifica a todos los clientes cuándo un usuario ingresa al chat.
- **Detección de desconexión:** Se notifica a todos cuándo un usuario cierra la pestaña o sale.
- **Mensajes en tiempo real:** Los mensajes enviados se reciben al instante sin recargar la página.
- **Fecha y hora:** Cada mensaje y evento del sistema incluye su marca temporal exacta (`DD/MM/AAAA HH:MM:SS`).
- **Interfaz con Bootstrap 5:**
  - Campo para ingresar el nombre de usuario.
  - Caja de texto para redactar mensajes.
  - Botón de envío (y soporte para la tecla Enter).
  - Área con scroll automático para visualizar todos los mensajes.
  - Contador de usuarios conectados en vivo.

---

## 📋 Requisitos Previos

- [Node.js](https://nodejs.org/) instalado (versión 16 o superior).

---

## 🛠️ Instalación y Ejecución

1. Abre una terminal en la carpeta del proyecto e instala las dependencias:
   ```bash
   npm install
   ```

2. Inicia el servidor:
   ```bash
   npm start
   ```
   *(o ejecutando directamente: `node server.js`)*

3. Abre en tu navegador la siguiente dirección:
   [http://localhost:3000](http://localhost:3000)

4. **Para probar la concurrencia:**
   - Abre **dos o más pestañas** (o ventanas en modo incógnito) en `http://localhost:3000`.
   - Ingresa un nombre distinto en cada una (por ejemplo: *Carlos* y *Ana*).
   - Observa cómo se notifica la entrada de cada participante con fecha y hora.
   - Envía mensajes y comprueba cómo llegan instantáneamente entre ambas pantallas sin recargar la página.
   - Cierra una pestaña y comprueba la notificación de desconexión en la otra.

---

## 📂 Estructura del Proyecto

```text
├── node_modules/       # Dependencias instaladas (express, ws)
├── package.json        # Configuración de dependencias y scripts de Node.js
├── package-lock.json   # Árbol de dependencias bloqueado
├── server.js           # Servidor Express + WebSocket Server (ws)
├── public/
│   └── index.html      # Interfaz de usuario estilizada con Bootstrap 5 y cliente WebSocket
└── README.md           # Documentación del proyecto
```
