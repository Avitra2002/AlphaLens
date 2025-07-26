const dfd = require('danfojs');
const { fetchAll } = require('./worldBank');

function analyzeTrend(data) {
  if (!data.length) return "Not enough data.";
  const delta = data.at(-1).value - data[0].value;
  if (delta > 0) return `Increased from ${data[0].value} to ${data.at(-1).value}`;
  if (delta < 0) return `Decreased from ${data[0].value} to ${data.at(-1).value}`;
  return "Remained stable.";
}

function detectAnomalies(data, threshold = 2.0) {
  const df = new dfd.DataFrame(data);
  const diffs = df['value'].values.map((v, i, arr) => i === 0 ? 0 : Math.abs(v - arr[i - 1]));
  return data
    .map((d, i) => diffs[i] > threshold ? `Year ${d.year}: ${diffs[i].toFixed(2)} change` : null)
    .filter(Boolean);
}

async function getCountrySummaryTrends(country, start, end) {
  const rawData = await fetchAll(country, start, end);
  const summary = {};

  for (let [key, data] of Object.entries(rawData)) {
    summary[key] = {
      data,
      trend: analyzeTrend(data),
      anomalies: detectAnomalies(data)
    };
  }

  return { country, start, end, indicators: summary };
}

module.exports = { getCountrySummary };
