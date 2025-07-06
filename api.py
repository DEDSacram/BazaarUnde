import requests
import json

# r = requests.get("https://api.skinport.com/v1/items", params={
#     "app_id":  252490,
#     "currency": "EUR",
#     "tradable": 0
# }).json()

filtered = []

with open('data.json', 'r') as f:
    r = json.load(f)

for item in r:
    suggested_price = item.get("suggested_price") or 0
    min_price = item.get("min_price") or 0

    if suggested_price > min_price:
        #item["suggested_price"] = suggested_price
        #item["min_price"] = min_price
        #item["diff"] = suggested_price - min_price
        #print(item["market_hash_name"])
        #print(f"suggested: {suggested_price}")
        #print(f"min: {min_price}")
        #print(f"diff: {suggested_price - min_price:.2f}")
        #print("")
        itemF = {
            "market_hash_name": item["market_hash_name"],
            "suggested_price": suggested_price,
            "min_price": min_price,
            "diff": suggested_price - min_price
        }
        
        filtered.append(itemF)

filtered.sort(key=lambda x: x["suggested_price"] - x["min_price"], reverse=True)

with open('filtered.json', 'w') as f:
    json.dump(filtered, f, indent=4)