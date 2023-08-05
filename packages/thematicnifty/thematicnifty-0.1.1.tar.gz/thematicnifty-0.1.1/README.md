# Package niftythematic
Date: 10-Apr-2022

## Installation

Use the following for importing: ```from thematicnifty import tn```

## Prerequisites
The ```pandas```  package will be imported as ```pd```.

## Features
This is a comprehensive app that will allow you to get the list of stocks in National Stock Exchange (NSE) India that is belonging to different groups of main themes such as Broad Market Indices (```bmi```), or Sectorial Indices (```secti```), Strategy Indices (```strati```) or Thematic Indices (```themei```). From each of the group theme, you can pull different list of stocks from different groups.

For example, from the ```bmi``` theme, you can get the stocks of the usual groups such as **NIFTY_50**, **NIFTY_100**, **NIFTY_200**, etc. These are the sub-themes of the main ```bmi``` theme. A complete list of themes under ```bmi``` group is provided at the end of this document.


From ```secti```, you can get the stocks belonging to different sectors such as **NIFTY_AUTO**, **NIFTY_IT**, **NIFTY_PHARMA**, **NIFTY_FMCG**, etc. These are the sub-themes of the main ```secti``` theme. A complete list of themes under ```secti``` group is provided at the end of this document.

From ```strati```, you can you can extract stocks belonging to the groups such as **NIFTY50_EQUAL_WEIGHT**, **NIFTY50_VALUE_20**, **NIFTY_ALPHA_50**, etc. These are the sub-themes of the main ```strati``` theme. A complete list of themes under ```strati``` group is provided at the end of this document.

Finally, from ```themei```, you can fetch stocks belonging to groups such as **NIFTY100_LIQUID_15**, **NIFTY_CPSE**, **NIFTY_MIDCAP_LIQUID_15**, **NIFTY_MNC**, etc. These are the sub-themes of the main ```themei``` theme. A complete list of themes under ```themei``` group is provided at the end of this document.

# Method Design
This is designed to be simple, and there is a single method with three parameters.

```getThematicNiftyStocks(main_item, sub_item, return_output)```

## Description of the Method
The ```getThematicNiftyStocks()``` method takes just 3 string inputs:

*   group_name
*   group_item
*   return_type

Description of each of the above is given hereunder.

### group_name
The main item can be one of the following four - ```bmi_group``` (default), ```secti_group```, ```strati_group``` or ```themei_group```. As already indicated, ```bmi``` stands for *Broad Market Indices*, ```secti``` stands for *Sectorial Indices*, ```strati``` stands for *Strategic Indices*, and ```themei``` stands for *Thematic Indices*.

### group_item
The sub_items are different for different main_item. For ```bmi```, the sub_item can be one of the following 16. The default value is 'NIFTY_50'.

1.  NIFTY_MIDSMALLCAP_400
2.  NIFTY_200
3.  NIFTY_LARGEMIDCAP_250
4.  NIFTY_TOTAL_MARKET
5.  *NIFTY_50*           (default)
6.  NIFTY_SMALLCAP_50
7.  NIFTY_SMALLCAP_250
8.  NIFTY_SMALLCAP_100
9.  NIFTY_100
10. NIFTY_MIDCAP_150
11. NIFTY_MIDCAP_SELECT
12. NIFTY_NEXT_50
13. NIFTY500_MULTICAP_50_25_25
14. NIFTY_MICROCAP_250
15. NIFTY_MIDCAP_50
16. NIFTY_MIDCAP_100'


For ```secti```, the sub_item can be one of the following 16: The default value is 'NIFTY_BANK'.

1.  NIFTY_PHARMA
2.  *NIFTY_BANK* (default)
3.  NIFTY_PSU_BANK
4.  NIFTY_FMCG
5.  NIFTY_CONSUMER_DURABLES
6.  NIFTY_PRIVATE_BANK
7.  NIFTY_AUTO
8.  NIFTY_HEALTHCARE_INDEX
9.  NIFTY_ENERGY
10. NIFTY_METAL
11. NIFTY_OIL_and_GAS
12. NIFTY_REALTY
13. NIFTY_FINANCIAL_SERVICES_25_50
14. NIFTY_FINANCIAL_SERVICES
15. NIFTY_MEDIA
16. NIFTY_IT


For ```strati```, the sub_item can be one of the following 10: The default is 'NIFTY_ALPHA_50'.

1.  NIFTY100_LOW_VOLATILITY_30
2.  NIFTY100_QUALITY_30
3.  NIFTY50_VALUE_20
4.  NIFTY_MIDCAP150_QUALITY_50
5.  *NIFTY_ALPHA_50* (default)
6.  NIFTY200_QUALITY_30
7.  NIFTY100_EQUAL_WEIGHT
8.  NIFTY_ALPHA_LOW_VOLATILITY_30
9.  NIFTY200_MOMENTUM_30
10. NIFTY_DIVIDEND_OPPORTUNITIES_50


Finally, for ```themei```, the sub_item can be one of the following 10: The default value is 'NIFTY100_LIQUID_15'.

1.  NIFTY100_ESG
2.  NIFTY_INDIA_CONSUMPTION
3.  NIFTY_SERVICES_SECTOR
4.  NIFTY_INFRASTRUCTURE
5.  NIFTY_INDIA_DIGITAL
6.  NIFTY_PSE
7.  *NIFTY100_LIQUID_15* (default)
8.  NIFTY_INDIA_MANUFACTURING
9.  NIFTY_CPSE
10. NIFTY_MIDCAP_LIQUID_15
11. NIFTY_GROWTH_SECTORS_15
12. NIFTY_COMMODITIES
13. NIFTY_MNC'


### return_type
As indicated earlier, return_type can take one of the following options:

1.   ```'as_list'```
2.   ```'as_list_with_NS'```
3.   ```'as_text'```
4.   ```'as_text_with_NS'``` (default)

### Default values for the method parameters
The method has been designed with the following default parameters:

1.   group_name = ```'bmi_group'```
2.   group_item = ```'NIFTY_50'```
3.   return_type = ```'as_text_with_NS'```


# Method Usage
## Example for ```bmi_group```

If you run the following method,

```getThematicNiftyStocks('bmi_group', 'NIFTY_50', 'as_text_with_ns')```

the output will be the following:

Output: ```NTPC.NS INDUSINDBK.NS BPCL.NS SBIN.NS POWERGRID.NS HDFCBANK.NS HDFCLIFE.NS ADANIPORTS.NS BAJAJ-AUTO.NS COALINDIA.NS SHREECEM.NS M&M.NS BAJFINANCE.NS HDFC.NS KOTAKBANK.NS ONGC.NS TATACONSUM.NS TATAMOTORS.NS MARUTI.NS LT.NS UPL.NS HINDUNILVR.NS WIPRO.NS BAJAJFINSV.NS ICICIBANK.NS AXISBANK.NS DRREDDY.NS ASIANPAINT.NS EICHERMOT.NS TATASTEEL.NS BRITANNIA.NS ULTRACEMCO.NS NESTLEIND.NS JSWSTEEL.NS TCS.NS RELIANCE.NS HCLTECH.NS GRASIM.NS ITC.NS BHARTIARTL.NS SUNPHARMA.NS INFY.NS HINDALCO.NS TITAN.NS CIPLA.NS APOLLOHOSP.NS DIVISLAB.NS TECHM.NS SBILIFE.NS HEROMOTOCO.NS```

## Example for ```secti_group```

```getThematicNiftyStocks(group_name='secti_group', group_item='NIFTY_IT', return_type='as_text')```

Output: ```WIPRO TCS LTTS HCLTECH INFY LTI MINDTREE TECHM MPHASIS COFORGE```


## Example for ```strati_group```

```getThematicNiftyStocks(group_name='strati_group', group_item='NIFTY50_VALUE_20', return_type='as_list_with_NS')```

Output: ```['NTPC.NS', 'BPCL.NS', 'POWERGRID.NS', 'COALINDIA.NS', 'BAJAJ-AUTO.NS', 'ONGC.NS', 'HINDUNILVR.NS', 'WIPRO.NS', 'LT.NS', 'UPL.NS', 'BRITANNIA.NS', 'GRASIM.NS', 'TCS.NS', 'HCLTECH.NS', 'JSWSTEEL.NS', 'ITC.NS', 'INFY.NS', 'HINDALCO.NS', 'TECHM.NS', 'HEROMOTOCO.NS']```


## Example for ```themei_group```

```getThematicNiftyStocks(group_name='themei_group', group_item='NIFTY_MIDCAP_LIQUID_15', return_type='as_list')```

Output: ```['FEDERALBNK', 'RECLTD', 'BEL', 'IRCTC', 'AUBANK', 'ZEEL', 'SRTRANSFIN', 'TATAPOWER', 'AUROPHARMA', 'ASHOKLEY', 'TVSMOTOR', 'GODREJPROP', 'BHARATFORG', 'MPHASIS', 'BALKRISIND']```

