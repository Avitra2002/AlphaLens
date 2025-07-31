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
        "NY.GDP.MKTP.CD,FP.CPI.TOTL.ZG,SL.UEM.TOTL.ZS,GC.DOD.TOTL.GD.ZS,NE.EXP.GNFS.ZS,NE.IMP.GNFS.ZS,NY.GDP.PCAP.CD,FP.CPI.TOTL",
        description="Comma-separated list of indicator codes"
    )
):
    try:
        
        indicator_codes = indicators.split(",")


        selected_indicators = dict(zip(indicator_codes, indicator_codes))

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
        df=df.copy()

        df.reset_index(inplace=True)
        df.rename(columns={'date': 'Year'}, inplace=True)
        df['Year'] = df['Year'].dt.year
        print (df.head())

        return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

@app.get("/api/get_countries")
def get_countries():
    try:
        countries = wbdata.get_countries()
        # print (countries)
        return [
            {
                "id": country['id'],        # ISO-3 country code
                "name": country['name'],
                
            }
            for country in countries
        ]
    except Exception as e:
        return {"error": str(e)}
