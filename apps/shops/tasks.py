# import json
#
# categories = ["watches", "straps"]
#
# category_json = [
#     {
#         "model" : "shops.categories",
#         "pk": ind+1,
#         "fields": {
#             "name" : category,
#         }
#     }
#     for ind, category in enumerate(categories)
# ]
# with open("fixtures/categories.json", "w") as f:
#     json.dump(category_json, f, indent=4)
#
# print(category_json)


import json
import random

# Ma'lumotlar
# categories = [1, 2]  # Misol uchun kategoriya ID'lar
# colors = ['Black', 'Silver', 'Gold', 'Blue', 'Green']
# dial_designs = ['Minimalist', 'Sporty', 'Luxury', 'Casual', 'Classic']
# strap_designs = ['Leather', 'Rubber', 'Metal', 'Nylon']
# movements = ['Quartz', 'Automatic', 'Solar', 'Smart']
#
# # 100 ta mahsulot yaratish
# data = []
# for i in range(1, 101):
#     product = {
#         "model": "shops.watches",
#         "pk": i,
#         "fields": {
#             "name": f"Watch Model {i}",
#             "category": random.choice(categories),
#             "about": f"This is the description for Watch Model {i}.",
#             "price": round(random.uniform(50.00, 500.00), 2),
#             "case_color": random.choice(colors),
#             "dial_design": random.choice(dial_designs),
#             "strap_design": random.choice(strap_designs),
#             "image": f"products/{2024}/{11}/{18}/watch_{i}.jpg",
#             "specification": {
#                 "keys": f"Material {i}",
#                 "coating": random.choice(['PVD coating', 'Matte finish']),
#                 "glass": random.choice(['Sapphire crystal', 'Mineral crystal']),
#                 "straps": random.choice(['Leather straps', 'Rubber straps']),
#                 "case_size": f"{random.randint(36, 45)}mm",
#                 "case_color": random.choice(colors),
#                 "dial_color": random.choice(colors),
#                 "water_resistance": f"{random.randint(3, 20)} ATM",
#                 "straps_type": random.choice(['Leather', 'Rubber', 'Metal']),
#                 "movement": random.choice(movements),
#                 "instantaneous_rate": f"+/- {random.randint(1, 15)} seconds per day",
#                 "standard_battery_life": f"{random.randint(1, 5)} years"
#             }
#         }
#     }
#     data.append(product)
#
# # JSON faylga yozish
# with open('fixtures/watches_fixture.json', 'w') as f:
#     json.dump(data, f, indent=4)
#
# print("Fixture file 'watches_fixture.json' created successfully!")
