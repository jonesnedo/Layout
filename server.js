const http = require('http');

let employees = [];

function send(res, status, payload, headers = {}) {
  res.writeHead(status, { 'Content-Type': 'application/json', ...headers });
  res.end(JSON.stringify(payload));
}

function handler(req, res) {
  const { method, url } = req;
  if (url === '/employees' && method === 'GET') {
    return send(res, 200, employees);
  }
  if (url === '/employees' && method === 'POST') {
    let body = '';
    req.on('data', chunk => (body += chunk));
    req.on('end', () => {
      try {
        const data = JSON.parse(body || '{}');
        if (data.name && data.role) {
          const employee = { id: employees.length + 1, ...data };
          employees.push(employee);
          return send(res, 201, employee);
        }
        return send(res, 400, { error: 'Invalid employee data' });
      } catch (err) {
        return send(res, 400, { error: 'Invalid JSON' });
      }
    });
    return;
  }
  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('Not Found');
}

const server = http.createServer(handler);
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`HR API running on http://localhost:${PORT}`);
});
