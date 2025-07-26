// get data and get summarised trends of each indicator
const express = require('express');
const { getCountrySummaryTrends } = require('../services/analysis');

const router = express.Router();

router.get('/', async (req, res) => {
  const country = req.query.country || 'USA';
  const start = parseInt(req.query.startYear || '2015');
  const end = parseInt(req.query.endYear || '2024');

  try {
    const summary = await getCountrySummaryTrends(country, start, end);
    res.json(summary);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

module.exports = router;
