import json
from ip2geotools.databases.noncommercial import DbIpCity
# from geopy.distance import distance

# crea una lista de diccionarios con cada instancia de stock


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
        
        if "source" in stock_item:
            dict_data["source"] = stock_item["source"]
        else:
            dict_data["source"] = "No Source"

        list_data.append(dict_data)

    return list_data


def get_location(ip):
    res = DbIpCity.get(ip, api_key="free")
    return f"Location: {res.city}, {res.region}, {res.country}"
