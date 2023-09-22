import json
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.distance import distance
# stock_data = {"stocks":"[{\"symbol\":\"AAPL\",\"shortName\":\"Apple Inc.\",\"price\":180.19,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"},{\"symbol\":\"AMZN\",\"shortName\":\"Amazon.com, Inc.\",\"price\":133.14,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"},{\"symbol\":\"TSLA\",\"shortName\":\"Tesla, Inc.\",\"price\":238.82,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"},{\"symbol\":\"MSFT\",\"shortName\":\"Microsoft Corporation\",\"price\":323.7,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"},{\"symbol\":\"NFLX\",\"shortName\":\"Netflix, Inc.\",\"price\":418.06,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"},{\"symbol\":\"GOOGL\",\"shortName\":\"Alphabet Inc.\",\"price\":131.01,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"},{\"symbol\":\"NVDA\",\"shortName\":\"NVIDIA Corporation\",\"price\":468.35,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"},{\"symbol\":\"META\",\"shortName\":\"Meta Platforms, Inc.\",\"price\":290.26,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"},{\"symbol\":\"WMT\",\"shortName\":\"Walmart Inc.\",\"price\":158.72,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"},{\"symbol\":\"SHEL\",\"shortName\":\"Shell PLC\",\"price\":61.42,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"},{\"symbol\":\"LTMAY\",\"shortName\":\"LATAM AIRLINES GROUP SA SPONS A\",\"price\":0.6699,\"currency\":\"USD\",\"source\":\"Delayed Quote\"},{\"symbol\":\"COMP\",\"shortName\":\"Compass, Inc.\",\"price\":3.32,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"},{\"symbol\":\"MA\",\"shortName\":\"Mastercard Incorporated\",\"price\":407.44,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"},{\"symbol\":\"PG\",\"shortName\":\"Procter & Gamble Company (The)\",\"price\":153.78,\"currency\":\"USD\",\"source\":\"Delayed Quote\"},{\"symbol\":\"AVGO\",\"shortName\":\"Broadcom Inc.\",\"price\":861.08,\"currency\":\"USD\",\"source\":\"Nasdaq Real Time Price\"}]","stocks_id":"d294d73e-25da-41b0-9371-e0d6a9fc1a12","datetime":"2023-08-28T23:42:57.319Z"}


#crea una lista de diccionarios con cada instancia de stock
def create_list_from_stock_data(stock_data):
    list_data = []
    stock_data = json.loads(stock_data)
    stocks_list = stock_data["stocks"]
    stocks_id = stock_data["stocks_id"]
    datetime_value = stock_data["datetime"]
    stocks_list = json.loads(stocks_list)
    
            
    for stock_item in stocks_list:
        dict_data = {}
        dict_data["stocks_id"] = stocks_id
        dict_data["datetime"] = datetime_value  
        dict_data["symbol"] = stock_item["symbol"]
        dict_data["shortName"] = stock_item["shortName"]
        dict_data["price"] = stock_item["price"]
        dict_data["currency"] = stock_item["currency"]
        dict_data["source"] = stock_item["source"]

        list_data.append(dict_data)

 
    return list_data

def get_location(ip):
    res = DbIpCity.get(ip , api_key="free")
    return f"Location: {res.city}, {res.region}, {res.country}"