import json

categories = ["watches", "straps"]

category_json = [
    {
        "model" : "shops.categories",
        "pk": ind+1,
        "fields": {
            "name" : category,
        }
    }
    for ind, category in enumerate(categories)
]
with open("fixtures/categories.json", "w") as f:
    json.dump(category_json, f, indent=4)

print(category_json)