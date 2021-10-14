import streamlit as st
import requests
import pandas as pd
import plotly.express as px

@st.cache
def request_ticker(source):
    URL="http://127.0.0.1:8000/api/stocks/{}".format(source)
    data=requests.get(URL)
    return data.json()


@st.cache
def request_source():
    URL="http://127.0.0.1:8000/api/sources"
    data=requests.get(URL)
    return data.json()


@st.cache
def request_prices(src,tic,tf="daily"):
    URL="http://127.0.0.1:8000/api/prices/{}/{}/{}".format(src,tic,tf)
    data = requests.get(URL)
    data=data.json()
    df=pd.DataFrame.from_dict(data[0]["data"])
    df["symbol"]=data[0]["symbol"]
    return df
def update():
    ticker=st.session_state.ticker
    source=st.session_state.src
    time_frame=st.session_state.tf
    df=request_prices(source,ticker,time_frame)
    fig  = px.line(df, x="timestamp",y= ['open' ,'close'],hover_name="symbol",title="Daily Open-Close",markers=True)
    fig1 = px.line(df,x="timestamp",y= ['low','high'],hover_name="symbol",title="Daily Low-High",markers=True)
    
    
    chart1.plotly_chart(fig,key="fig1")
    chart2.plotly_chart(fig1,key="fig2")

srcs=pd.DataFrame(request_source())
tick=pd.DataFrame(request_ticker(srcs["source_id"].iloc[0]))
#header
st.header("Trading-app")
#sidebar
sources=st.sidebar.selectbox("Data-Source",srcs,on_change=update,key="src")
timeframe=st.sidebar.radio("Timeframe",("daily","hourly","minute"),on_change=update,key="tf")
tickers=st.sidebar.selectbox("Tickers",tick["ticker"],on_change=update,key='ticker')

#figures
df=request_prices(srcs["source_id"].iloc[0], tick["ticker"].iloc[0])
fig  = px.line(df, x="timestamp",y= ['open' ,'close'],hover_name="symbol",title="Daily Open-Close",markers=True)
fig2 = px.line(df,x="timestamp",y= ['low','high'],hover_name="symbol",title="Daily Low-High",markers=True)

chart1=st.plotly_chart(fig,key="fig1")
chart2=st.plotly_chart(fig2,key="fig2")



