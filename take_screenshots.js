const path = require('path');
const fs = require('fs');
const puppeteer = require('puppeteer-core');

require('./server.js');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

async function run() {
  const outputDir = path.join(__dirname, 'screenshots');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  await new Promise(r => setTimeout(r, 800));

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    defaultViewport: { width: 950, height: 780 },
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page1 = await browser.newPage();
  page1.on('console', msg => console.log('PAGE1 LOG:', msg.text()));
  page1.on('pageerror', err => console.log('PAGE1 ERR:', err));

  const page2 = await browser.newPage();
  page2.on('console', msg => console.log('PAGE2 LOG:', msg.text()));
  page2.on('pageerror', err => console.log('PAGE2 ERR:', err));

  console.log('Navigating to http://localhost:3000...');
  await page1.goto('http://localhost:3000');
  await page2.goto('http://localhost:3000');

  console.log('Submitting login for Carlos...');
  await page1.evaluate(() => {
    document.getElementById('usernameInput').value = 'Carlos';
    document.getElementById('loginForm').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
  });

  console.log('Submitting login for Ana...');
  await page2.evaluate(() => {
    document.getElementById('usernameInput').value = 'Ana';
    document.getElementById('loginForm').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
  });

  await new Promise(r => setTimeout(r, 800));

  console.log('Sending message 1...');
  await page1.evaluate(() => {
    document.getElementById('messageInput').value = '¡Hola Ana! ¿Cómo estás? Probando WebSockets en tiempo real.';
    document.getElementById('messageForm').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
  });

  await new Promise(r => setTimeout(r, 600));

  console.log('Sending message 2...');
  await page2.evaluate(() => {
    document.getElementById('messageInput').value = '¡Hola Carlos! Todo excelente, los mensajes llegan al instante sin recargar la página.';
    document.getElementById('messageForm').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
  });

  await new Promise(r => setTimeout(r, 600));

  console.log('Sending message 3...');
  await page1.evaluate(() => {
    document.getElementById('messageInput').value = '¡Genial! Además cada mensaje incluye la fecha y hora exacta del servidor.';
    document.getElementById('messageForm').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
  });

  await new Promise(r => setTimeout(r, 1000));

  console.log('Saving screenshots...');
  await page1.screenshot({ path: path.join(outputDir, 'cliente_carlos.png') });
  await page2.screenshot({ path: path.join(outputDir, 'cliente_ana.png') });

  console.log('Screenshots saved successfully!');
  await browser.close();
  process.exit(0);
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
