land = 80
tomatoes_area = potatoes_area = cabbage_area = sunflower_area = sugarcane_area = land / 5
yield_of_tomatoes = (30 / 100 * tomatoes_area * 10) + (70 / 100 * tomatoes_area * 12)
yield_of_potatoes = 10 * potatoes_area
yield_of_cabbage = 14 * cabbage_area
yield_of_sunflower = 0.7 * sunflower_area
yield_of_sugarcane = 45 * sugarcane_area
selling_price_tomato = 7
selling_price_potatoes = 20
selling_price_cabbage = 24
selling_price_sunflower = 200
selling_price_sugarcane = 4000
sales_achieved = yield_of_tomatoes * selling_price_tomato + yield_of_potatoes * selling_price_potatoes + yield_of_cabbage + selling_price_cabbage + yield_of_sunflower * selling_price_sunflower + yield_of_sugarcane * selling_price_sugarcane
print(f"sales after converting to chemical-free : {sales_achieved}")