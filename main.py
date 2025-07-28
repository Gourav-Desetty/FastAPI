from fastapi import FastAPI
from enum import Enum
app = FastAPI()

class Available_Cuisines(str, Enum):
    indian = "indian",
    american = "american",
    italian = "italian"

food_items = {
    'indian' : [ "Samosa", "Dosa" ],
    'american' : [ "Hot Dog", "Apple Pie"],
    'italian' : [ "Ravioli", "Pizza"]
}

@app.get("/get_items/{cuisine}")
async def greet(cuisine:Available_Cuisines):
    # if cuisine not in food_items.keys():
    #     return f"available cuisines are {food_items.keys()}"
    return food_items.get(cuisine)


coupon_code = {
    1: "10%",
    2: "20%",
    3: "30%"
}

@app.get("/get_coupon/{code}")
async def get_coupon(code: int): 
    return {"discount amount": coupon_code.get(code)}