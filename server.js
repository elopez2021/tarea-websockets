const express = require('express');
const http = require('http');
const path = require('path');
const morgan = require('morgan');
const { WebSocketServer, WebSocket } = require('ws');

const app = express();
const server = http.createServer(app);

// WebSocket Server explicitly mounted on the '/ws' path
const wss = new WebSocketServer({ server, path: '/ws' });

const PORT = process.env.PORT || 3000;

// HTTP request logger middleware for Express (prints requests, status codes, and latency in console)
app.use(morgan('dev'));

// Serve static assets (CSS, JS, images) from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// ==========================================
// HTTP ROUTES (Express)
// ==========================================

// Route 1: Main chat web page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Route 2: Health/diagnostic endpoint (inspect connected users and server state in JSON)
app.get('/api/status', (req, res) => {
  res.json({
    status: 'online',
    connectedUsersCount: getConnectedUsers().length,
    users: getConnectedUsers(),
    timestamp: getFormattedDateTime()
  });
});

// ==========================================
// HELPER FUNCTIONS
// ==========================================

// Returns current timestamp formatted as (DD/MM/YYYY HH:MM:SS)
function getFormattedDateTime() {
  const now = new Date();
  const date = now.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
  const time = now.toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
  return `${date} ${time}`;
}

// Broadcasts a JSON payload to all actively connected WebSocket clients
function broadcast(payload) {
  const json = JSON.stringify(payload);
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(json);
    }
  });
}

// Returns an array of usernames for all currently connected users
function getConnectedUsers() {
  return [...wss.clients]
    .filter((client) => client.readyState === WebSocket.OPEN && client.username)
    .map((client) => client.username);
}

// ==========================================
// WEBSOCKET EVENTS (Real-Time Communication)
// ==========================================

wss.on('connection', (ws) => {
  ws.username = null;

  // Handle incoming messages from this specific client
  ws.on('message', (rawMessage) => {
    try {
      const data = JSON.parse(rawMessage);

      // Event: User submits username upon joining
      if (data.type === 'join') {
        ws.username = (data.username || 'Anónimo').trim();
        console.log(`[WS Connection] User "${ws.username}" connected from browser.`);

        // Notify all clients that a new user has joined
        broadcast({
          type: 'system',
          action: 'connect',
          username: ws.username,
          text: `El usuario "${ws.username}" se ha conectado.`,
          timestamp: getFormattedDateTime(),
          users: getConnectedUsers()
        });
      }

      // Event: User sends a chat message
      else if (data.type === 'message') {
        const text = (data.text || '').trim();
        if (!text || !ws.username) return;

        console.log(`[WS Chat] ${ws.username}: "${text}"`);

        // Re-broadcast message to all connected clients in real time
        broadcast({
          type: 'chat',
          username: ws.username,
          text: text,
          timestamp: getFormattedDateTime()
        });
      }
    } catch (err) {
      console.error('Error processing incoming message:', err);
    }
  });

  // Event: Client disconnects (closes tab or browser)
  ws.on('close', () => {
    if (ws.username) {
      const departedUser = ws.username;
      console.log(`[WS Disconnection] User "${departedUser}" disconnected.`);
      broadcast({
        type: 'system',
        action: 'disconnect',
        username: departedUser,
        text: `El usuario "${departedUser}" se ha desconectado.`,
        timestamp: getFormattedDateTime(),
        users: getConnectedUsers()
      });
    }
  });

  ws.on('error', (err) => {
    console.error('WebSocket client error:', err);
  });
});

// Start the unified HTTP and WebSocket server on the configured port
server.listen(PORT, () => {
  console.log(`===================================================`);
  console.log(` Express + WebSockets Server active at:`);
  console.log(` - Web Route:       http://localhost:${PORT}/`);
  console.log(` - API Route:       http://localhost:${PORT}/api/status`);
  console.log(` - WebSocket Route: ws://localhost:${PORT}/ws`);
  console.log(`===================================================`);
});
