const fetch = require('node-fetch');
const { INDICATORS } = require('../utils/indicators');

const BASE = 'http://localhost:8000/api';

async function fetchIndicator(country, code, start, end) {
  const url = `${BASE}/gdp?country=${country}&start_year=${start}&end_year=${end}&indicators=${code}`;
  const res = await fetch(url);
  const data = await res.json();
  if (!Array.isArray(data)) return [];

  return data.map(d => ({
    year: d.Year,
    value: d[Object.keys(d).find(k => k !== 'Year' && k !== 'country')]  // dynamically pick the value field
  })).filter(d => d.value !== null);
}

async function fetchAll(country, start, end) {
  const results = {};
  for (let [key, code] of Object.entries(INDICATORS)) {
    results[key] = await fetchIndicator(country, code, start, end);
  }
  return results;
}

module.exports = { fetchAll };
