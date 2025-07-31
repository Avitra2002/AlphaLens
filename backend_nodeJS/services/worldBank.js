const fetch = require('node-fetch');
const { INDICATOR_NAMES } = require('../utils/indicators');

const BASE = 'http://localhost:8000/api';

async function fetchAll(country, start, end, indicators) {
  const url = `${BASE}/gdp?country=${country}&start_year=${start}&end_year=${end}&indicators=${indicators.join(',')}`;
  
  const res = await fetch(url);
  const data = await res.json();
  console.log("✅ Raw data from FastAPI:", data);

  if (!Array.isArray(data)) return {};

  const results = {};

  for (let code of indicators) {
    const Name = INDICATOR_NAMES[code] || code;

    const values = data
      .map(d => ({
        year: d.Year,
        value: d[code] ?? null
      }))
      .sort((a, b) => a.year - b.year);

    const allNull = values.every(entry => entry.value === null);
    if (allNull) continue;

    results[code] = values; 
  }

  return results;
}


async function fetchCountries(){
  const url = `${BASE}/get_countries`;
  const res= await fetch(url);
  const data = await res.json();
  return data.sort((a, b) => a.name.localeCompare(b.name));
}

module.exports = { fetchAll, fetchCountries };
