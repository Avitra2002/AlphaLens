const dfd = require('danfojs');
const { fetchAll } = require('./worldBank');

function analyzeTrend(data) {
  if (!data.length) return "Not enough data.";
  const delta = data.at(-1).value - data[0].value;
  if (delta > 0) return `Increased from ${data[0].value} to ${data.at(-1).value}`;
  if (delta < 0) return `Decreased from ${data[0].value} to ${data.at(-1).value}`;
  return "Remained stable.";
}

const {INDICATOR_THRESHOLDS} = require ('../utils/indicators')

function detectAnomalies(data, code) {
  const anomalies = [];
  const threshold = INDICATOR_THRESHOLDS[code] || 10; // Default to 10% if not defined

  for (let i = 1; i < data.length; i++) {
    const prev = data[i - 1].value;
    const curr = data[i].value;

    if (prev == null || curr == null) continue;

    const percentChange = Math.abs((curr - prev) / prev) * 100;

    if (percentChange > threshold) {
      anomalies.push(`Year ${data[i].year}: ${percentChange.toFixed(2)}% change`);
    }
  }

  return anomalies;
}

async function getCountrySummaryTrends(country, start, end, indicators) {
  const rawData = await fetchAll(country, start, end, indicators);
  const summary = {};

  for (let [key, data] of Object.entries(rawData)) {
    summary[key] = {
      data,
      trend: analyzeTrend(data),
      anomalies: detectAnomalies(data, key)
    };
  }

  return { country, start, end, indicators: summary };
}

module.exports = { getCountrySummaryTrends };
