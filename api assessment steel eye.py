#!/usr/bin/env python
# coding: utf-8

# In[5]:



import datetime as dt
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query


# In[2]:


pip install pydantic


# In[4]:


pip install fastapi


# In[6]:


app = FastAPI()


# In[7]:


trades_db = []


# In[8]:


# Pydantic model representing a single Trade
class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")


# In[9]:


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")


# In[13]:


# Endpoint to fetch a list of trades
#This implementation provides three endpoints: /trades/ for listing trades with filtering and pagination,
#/trades/{trade_id} for retrieving a single trade by ID, and /trades/search for searching trades based on various fields.
@app.get("/trades/")
def get_trades(
    asset_class: Optional[str] = Query(None, description="Asset class of the trade."),
    end: Optional[dt.datetime] = Query(None, description="The maximum date for the tradeDateTime field."),
    max_price: Optional[float] = Query(None, description="The maximum value for the tradeDetails.price field."),
    min_price: Optional[float] = Query(None, description="The minimum value for the tradeDetails.price field."),
    start: Optional[dt.datetime] = Query(None, description="The minimum date for the tradeDateTime field."),
    trade_type: Optional[str] = Query(None, description="The tradeDetails.buySellIndicator is a BUY or SELL"),
    skip: int = Query(0, ge=0, description="Number of trades to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of trades to return for pagination")
) -> List[Trade]:
    filtered_trades = trades_db

    if asset_class:
        filtered_trades = [t for t in filtered_trades if t.asset_class == asset_class]
    if end:
        filtered_trades = [t for t in filtered_trades if t.trade_date_time <= end]
    if max_price:
        filtered_trades = [t for t in filtered_trades if t.trade_details.price <= max_price]
    if min_price:
        filtered_trades = [t for t in filtered_trades if t.trade_details.price >= min_price]
    if start:
        filtered_trades = [t for t in filtered_trades if t.trade_date_time >= start]
    if trade_type:
        filtered_trades = [t for t in filtered_trades if t.trade_details.buySellIndicator == trade_type]

    paginated_trades = filtered_trades[skip : skip + limit]

    return paginated_trades


# Endpoint to fetch a single trade by ID
@app.get("/trades/{trade_id}")
def get_trade_by_id(trade_id: str) -> Optional[Trade]:
    for trade in trades_db:
        if trade.trade_id == trade_id:
            return trade
    return None


# Endpoint for searching trades
@app.get("/trades/search")
def search_trades(
    search: str = Query(..., description="Text to search across trade fields")
) -> List[Trade]:
    matching_trades = []
    for trade in trades_db:
        if (
            search.lower() in trade.counterparty.lower()
            or search.lower() in trade.instrument_id.lower()
            or search.lower() in trade.instrument_name.lower()
            or search.lower() in trade.trader.lower()
        ):
            matching_trades.append(trade)
    return matching_trades


# In[ ]:




