'use client';

import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

type IndicatorDataPoint = {
  year: number;
  value: number;
};

type IndicatorChartProps = {
  title: string;
  data: IndicatorDataPoint[];
};

export default function IndicatorChart({ title, data }: IndicatorChartProps) {
  const chartData = {
    labels: data.map(d => d.year),
    datasets: [
      {
        label: title,
        data: data.map(d => d.value),
        borderWidth: 2,
        fill: false,
      },
    ],
  };

  return (
    <div style={{ maxWidth: '700px', marginBottom: '2rem' }}>
      <Line data={chartData} />
    </div>
  );
}
