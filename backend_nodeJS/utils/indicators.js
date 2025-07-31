const INDICATOR_NAMES = {
  'NY.GDP.MKTP.CD': 'GDP (current US$)',
  'FP.CPI.TOTL.ZG': 'Inflation (%)',
  'SL.UEM.TOTL.ZS': 'Unemployment (%)',
  'GC.DOD.TOTL.GD.ZS': 'Government Debt (% of GDP)',
  'NE.EXP.GNFS.ZS': 'Exports (% of GDP)',
  'NE.IMP.GNFS.ZS': 'Imports (% of GDP)',
  'SP.POP.TOTL': 'Population',
  'NY.GDP.PCAP.CD': 'GDP per capita (US$)',
  'FP.CPI.TOTL': 'Consumer Price Index (2010 = 100)',
};

const INDICATOR_THRESHOLDS = {
  'NY.GDP.MKTP.CD': 10,      
  'FP.CPI.TOTL.ZG': 3,      
  'SL.UEM.TOTL.ZS': 20,     
  'GC.DOD.TOTL.GD.ZS': 15, 
  'NE.EXP.GNFS.ZS': 8,       
  'NE.IMP.GNFS.ZS': 8,       
  'SP.POP.TOTL': 2,          
  'NY.GDP.PCAP.CD': 5,       
  'FP.CPI.TOTL': 3,         
};

module.exports = { INDICATOR_NAMES, INDICATOR_THRESHOLDS };
