/**
 * Express server for DocuGener frontend.
 * Serves static files and proxies API calls to Python backend.
 */
const express = require('express');
const cors = require('cors');
const path = require('path');
const axios = require('axios');

const app = express();
const PORT = 5100;
const BACKEND_URL = 'http://localhost:5000';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Proxy API requests to Python backend
app.use('/api', async (req, res) => {
  try {
    // req.path includes the full path, so for /api/captures, req.path is /captures
    // We need to add /api back when forwarding
    const backendPath = `/api${req.path}`;
    const response = await axios({
      method: req.method,
      url: `${BACKEND_URL}${backendPath}`,
      data: req.body,
      params: req.query,
      responseType: req.path.includes('/captures/') && req.method === 'GET' && !req.path.endsWith('/context') 
        ? 'arraybuffer' 
        : 'json',
    });
    
    if (response.data instanceof Buffer) {
      res.set('Content-Type', 'image/png');
      res.send(response.data);
    } else {
      res.json(response.data);
    }
  } catch (error) {
    console.error('API proxy error:', error.message);
    console.error('Request path:', req.path);
    res.status(error.response?.status || 500).json({
      error: error.message || 'Internal server error'
    });
  }
});

// Serve index.html for all routes (SPA)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Frontend server running on http://localhost:${PORT}`);
  console.log(`Backend API expected at ${BACKEND_URL}`);
});

