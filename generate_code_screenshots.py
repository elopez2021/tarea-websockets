import os
from pygments import highlight
from pygments.lexers import JavascriptLexer, HtmlLexer
from pygments.formatters import ImageFormatter

screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(screenshots_dir, exist_ok=True)

# 1. Leer server.js
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

# Generar captura de server.js
server_img_path = os.path.join(screenshots_dir, 'codigo_servidor.png')
formatter_server = ImageFormatter(
    style='monokai',
    line_numbers=True,
    font_size=13,
    line_number_bg='#272822',
    line_number_fg='#75715e',
    image_pad=14
)
with open(server_img_path, 'wb') as f:
    f.write(highlight(server_code, JavascriptLexer(), formatter_server))

print(f"Generated: {server_img_path}")

# 2. Leer parte JavaScript principal de index.html
with open('public/index.html', 'r', encoding='utf-8') as f:
    client_code = f.read()

# Extraer el bloque del script y formulario relevante para la captura
start_idx = client_code.find('<!-- Client-Side WebSocket Logic -->')
if start_idx != -1:
    relevant_client_code = client_code[start_idx:start_idx + 3200]
else:
    relevant_client_code = client_code[:3000]

client_img_path = os.path.join(screenshots_dir, 'codigo_cliente.png')
formatter_client = ImageFormatter(
    style='monokai',
    line_numbers=True,
    font_size=13,
    line_number_bg='#272822',
    line_number_fg='#75715e',
    image_pad=14
)
with open(client_img_path, 'wb') as f:
    f.write(highlight(relevant_client_code, JavascriptLexer(), formatter_client))

print(f"Generated: {client_img_path}")
