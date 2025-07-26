from fastapi import FastAPI, Query
from typing import List, Optional
import wbdata
import datetime
import pandas as pd

app = FastAPI()

@app.get("/api/gdp")
def get_gdp(
    country: str = Query(..., description="ISO-3 country code (e.g., USA, IND, CHN)"),
    start_year: int = Query(2018, description="Start year"),
    end_year: int = Query(2024, description="End year"),
    indicators: str = Query(
        "NY.GDP.MKTP.CD,FP.CPI.TOTL.ZG,SL.UEM.TOTL.ZS",
        description="Comma-separated list of indicator codes"
    )
):
    try:
        
        indicator_codes = indicators.split(",")
        indicator_map = {
        'NY.GDP.MKTP.CD': 'GDP (current US$)',
        'FP.CPI.TOTL.ZG': 'Inflation, consumer prices (annual %)',
        'SL.UEM.TOTL.ZS': 'Unemployment, total (% of total labor force)',
        'GC.DOD.TOTL.GD.ZS': 'Government Debt (% of GDP)',
        'NE.EXP.GNFS.CD': 'Exports (current US$)',
        'NE.IMP.GNFS.CD': 'Imports (current US$)',
        'SP.POP.TOTL': 'Population, total',
        'NY.GDP.PCAP.CD': 'GDP per capita (current US$)',
        'FP.CPI.TOTL': 'Consumer Price Index (2010 = 100)'
    }


        selected_indicators = {code: indicator_map.get(code, code) for code in indicator_codes}

        # Date range
        start_date = datetime.datetime(start_year, 1, 1)
        end_date = datetime.datetime(end_year, 1, 1)

        # Fetch data
        df = wbdata.get_dataframe(
            selected_indicators,
            country,
            date=(start_date, end_date),
            parse_dates=True
        )

        df.reset_index(inplace=True)
        df.rename(columns={'date': 'Year'}, inplace=True)
        df['Year'] = df['Year'].dt.year

        return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}
