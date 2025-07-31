'use client';

import { useEffect, useState } from "react";
import { TrendingUp, TrendingDown, BarChart3, Globe, Calendar, Activity, AlertTriangle } from "lucide-react";

// Import your actual IndicatorChart component
import IndicatorChart from '../../components/IndicatorChart';

type IndicatorDataPoint = {
  year: number;
  value: number;
};

type IndicatorDetails = {
  data: IndicatorDataPoint[];
  trend: string;
  anomalies: string[];
};

type SummaryResponse = {
  country: string;
  start: number;
  end: number;
  indicators: {
    [indicatorName: string]: IndicatorDetails;
  };
};

type CountryOption = {
  id: string;
  name: string;
};

const availableIndicators = [
  { code: "NY.GDP.MKTP.CD", name: "GDP (current US$)", icon: "💰" },
  { code: "FP.CPI.TOTL.ZG", name: "Inflation (%)", icon: "📈" },
  { code: "SL.UEM.TOTL.ZS", name: "Unemployment (%)", icon: "👥" },
  { code: "GC.DOD.TOTL.GD.ZS", name: "Government Debt (% of GDP)", icon: "🏛️" },
  { code: "NE.EXP.GNFS.CD", name: "Exports (US$)", icon: "🚢" },
  { code: "NE.IMP.GNFS.CD", name: "Imports (US$)", icon: "📦" },
  { code: "SP.POP.TOTL", name: "Population", icon: "🌍" },
  { code: "NY.GDP.PCAP.CD", name: "GDP per capita (US$)", icon: "💵" },
];

export default function TrendsAIPage() {
  const [summary, setSummary] = useState<SummaryResponse | null>(null);
  const [countries, setCountries] = useState<CountryOption[]>([]);
  const [loading, setLoading] = useState(false);
  const [showIndicatorDropdown, setShowIndicatorDropdown] = useState(false);

  const [selectedCountry, setSelectedCountry] = useState("USA");
  const [startYear, setStartYear] = useState(2015);
  const [endYear, setEndYear] = useState(2024);
  const [selectedIndicators, setSelectedIndicators] = useState<string[]>(["NY.GDP.MKTP.CD", "SL.UEM.TOTL.ZS"]);

  useEffect(() => {
    fetchCountries();
    // Initial fetch with default values
    fetchSummary();
  }, []);

  useEffect(() => {
    // Close dropdown when clicking outside
    const handleClickOutside = (event: MouseEvent) => {
      if (!(event.target as Element).closest('.indicator-dropdown')) {
        setShowIndicatorDropdown(false);
      }
    };
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const fetchCountries = async () => {
    try {
      const res = await fetch("http://localhost:4000/api/summary/countries");
      const data = await res.json();
      setCountries(data);
    } catch (err) {
      console.error("Error fetching countries:", err);
    }
  };

  const fetchSummary = async () => {
    setLoading(true);
    try {
      const indicatorsParam = selectedIndicators.join(',');
      const url = `http://localhost:4000/api/summary/trend?country=${selectedCountry}&startYear=${startYear}&endYear=${endYear}&indicators=${indicatorsParam}`;
      const res = await fetch(url);
      const data = await res.json();
      setSummary(data);
    } catch (err) {
      console.error("❌ Error fetching summary:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = () => {
    fetchSummary();
  };

  const getTrendIcon = (trend: string) => {
    if (trend.toLowerCase().includes('upward') || trend.toLowerCase().includes('growth')) {
      return <TrendingUp className="w-5 h-5 text-green-500" />;
    } else if (trend.toLowerCase().includes('declining') || trend.toLowerCase().includes('down')) {
      return <TrendingDown className="w-5 h-5 text-red-500" />;
    }
    return <Activity className="w-5 h-5 text-blue-500" />;
  };

  const getIndicatorName = (code: string) => {
    const indicator = availableIndicators.find(ind => ind.code === code);
    return indicator?.name || code;
  };

  const getIndicatorIcon = (code: string) => {
    const indicator = availableIndicators.find(ind => ind.code === code);
    return indicator?.icon || "📊";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Economic Dashboard</h1>
              <p className="text-sm text-gray-600">Real-time economic indicators and trends</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Control Panel */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Globe className="w-5 h-5 text-blue-600" />
            Analysis Parameters
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Country</label>
              <select 
                value={selectedCountry} 
                onChange={e => setSelectedCountry(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                {countries.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700 flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                Start Year
              </label>
              <input 
                type="number" 
                value={startYear} 
                onChange={e => setStartYear(Number(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700 flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                End Year
              </label>
              <input 
                type="number" 
                value={endYear} 
                onChange={e => setEndYear(Number(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">Indicators</label>
              <div className="relative indicator-dropdown">
                <div 
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500 bg-white cursor-pointer min-h-[42px]"
                  onClick={() => setShowIndicatorDropdown(!showIndicatorDropdown)}
                >
                  <div className="flex flex-wrap gap-1">
                    {selectedIndicators.length === 0 ? (
                      <span className="text-gray-500 text-sm">Select indicators...</span>
                    ) : (
                      selectedIndicators.map(code => {
                        const indicator = availableIndicators.find(ind => ind.code === code);
                        return (
                          <span key={code} className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-md">
                            <span>{indicator?.icon}</span>
                            <span className="max-w-20 truncate">{indicator?.name}</span>
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                setSelectedIndicators(prev => prev.filter(i => i !== code));
                              }}
                              className="ml-1 text-blue-600 hover:text-blue-800"
                            >
                              ×
                            </button>
                          </span>
                        );
                      })
                    )}
                  </div>
                </div>
                
                {showIndicatorDropdown && (
                  <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-64 overflow-y-auto">
                    {availableIndicators.map(ind => (
                      <label key={ind.code} className="flex items-center gap-2 p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0">
                        <input
                          type="checkbox"
                          checked={selectedIndicators.includes(ind.code)}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setSelectedIndicators(prev => [...prev, ind.code]);
                            } else {
                              setSelectedIndicators(prev => prev.filter(i => i !== ind.code));
                            }
                          }}
                          className="text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="text-sm flex items-center gap-2">
                          <span>{ind.icon}</span>
                          <span>{ind.name}</span>
                        </span>
                      </label>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="mt-6">
            <button 
              onClick={handleSubmit}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Updating...
                </>
              ) : (
                <>
                  <Activity className="w-4 h-4" />
                  Update Analysis
                </>
              )}
            </button>
          </div>
        </div>

        {/* Data Display */}
        {!summary ? (
          <div className="bg-white rounded-xl shadow-sm border p-12 text-center">
            <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-600 text-lg">Loading economic data...</p>
          </div>
        ) : (
          <div className="space-y-8">
            {/* Summary Header */}
            <div className="bg-white rounded-xl shadow-sm border p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                    📍 {summary.country}
                  </h2>
                  <p className="text-gray-600 mt-1">
                    Analysis Period: {summary.start} - {summary.end}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500">Data Points</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {Object.keys(summary.indicators || {}).length}
                  </p>
                </div>
              </div>
            </div>

            {/* Indicators Grid */}
            {summary?.indicators ? (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {Object.entries(summary.indicators).map(([indicator, details]) => (
                  <div key={indicator} className="bg-white rounded-xl shadow-sm border overflow-hidden">
                    {/* Indicator Header */}
                    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 border-b">
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                          <div className="text-2xl">
                            {getIndicatorIcon(indicator)}
                          </div>
                          <div>
                            <h3 className="text-lg font-semibold text-gray-900">
                              {getIndicatorName(indicator)}
                            </h3>
                            <div className="flex items-center gap-2 mt-1">
                              {getTrendIcon(details.trend)}
                              <span className="text-sm font-medium text-gray-700">
                                {details.trend}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Chart */}
                    <div className="p-6">
                      <IndicatorChart title={indicator} data={details.data} />
                    </div>

                    {/* Anomalies */}
                    {details.anomalies && details.anomalies.length > 0 && (
                      <div className="px-6 pb-6">
                        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
                          <div className="flex items-start gap-2">
                            <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
                            <div>
                              <h4 className="font-medium text-amber-800 mb-1">Notable Anomalies</h4>
                              <ul className="text-sm text-amber-700 space-y-1">
                                {details.anomalies.map((anomaly, idx) => (
                                  <li key={idx} className="flex items-start gap-1">
                                    <span className="w-1 h-1 bg-amber-600 rounded-full mt-2 flex-shrink-0"></span>
                                    {anomaly}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-white rounded-xl shadow-sm border p-12 text-center">
                <div className="text-gray-400 mb-4">
                  <BarChart3 className="w-16 h-16 mx-auto" />
                </div>
                <p className="text-gray-600 text-lg">No indicator data available.</p>
                <p className="text-gray-500 text-sm mt-2">Try selecting different parameters or check your data source.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}