const express = require('express');
const router = express.Router();
const fetch = require('node-fetch');

const FASTAPI_URL = 'http://localhost:8001';

router.post('/', async (req, res) => {
  try {
    const { query } = req.body;

    if (!query) {
      return res.status(400).json({ 
        error: 'Query is required',
        success: false 
      });
    }

    
    const response = await fetch(`${FASTAPI_URL}/finance_chatbot`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query }),
      timeout: 40000 
    });

    if (!response.ok) {
      throw new Error(`FastAPI responded with status: ${response.status}`);
    }

    const data = await response.json();
    res.json(data);

  } catch (error) {
    console.error('Error calling FastAPI:', error.message);
    

    if (error.name === 'FetchError') {
      if (error.code === 'ECONNREFUSED') {
        return res.status(503).json({
          error: 'FastAPI service is not available',
          success: false
        });
      }
      if (error.type === 'request-timeout') {
        return res.status(504).json({
          error: 'Request timeout',
          success: false
        });
      }
    }

    res.status(500).json({
      error: 'Internal server error',
      success: false
    });
  }
});

module.exports = router;