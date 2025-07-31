// get data and get summarised trends of each indicator
const express = require('express');
const { getCountrySummaryTrends } = require('../services/analysis');
const {fetchCountries} = require ('../services/worldBank');
const { INDICATOR_NAMES } = require('../utils/indicators');

const router = express.Router();

router.get('/trend', async (req, res) => {
  const country = req.query.country || 'USA';
  const start = parseInt(req.query.startYear || '2015');
  const end = parseInt(req.query.endYear || '2024');
  const indicators = req.query.indicators 
    ? req.query.indicators.split(',') 
    : Object.keys(INDICATOR_NAMES)


  try {
    const summary = await getCountrySummaryTrends(country, start, end, indicators);
    res.json(summary);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

router.get('/countries', async (req, res)=> {
  try {
    const data = await fetchCountries();
    res.json(data)
  } catch (e){
    res.status(500).json({error: e.message});
  }
})

module.exports = router;
