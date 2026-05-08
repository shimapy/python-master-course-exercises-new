from sanic import Sanic,Request,json,exceptions
from sanic_ext import Extend,openapi
from enum import Enum
import uuid
import csv


app = Sanic("CookingApp")
Extend(app)

foods=[{
        "id":"f217cfe5-98e5-4164-afe6-80d9c54bab11",
        "title":"ghorme sabzi",
        "category":"lunch",
        "description":"it is a Iranain food",
        "estimated_time":"120 min",
        "difficulty":"medium",
        "ingredients":["vegetable","meet","beans","onion"]
    }]

class CategoryEnum(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    dessert = "dessert"
    snack = "snack"
    
class DifficultyEnum(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"    
    
class FoodModel():
    title: str
    category: CategoryEnum
    description: str
    estimated_time: str
    difficulty: DifficultyEnum
    ingredients : list
 
 
# @app.get("/recipes")
@app.get("/")
async def get_recipes(request:Request):
    return json(foods)

@app.post("/recipes")
@openapi.body(FoodModel)
async def create_recipes(request:Request):
    data = request.json
    if not data.get("title"):
        raise exceptions.BadRequest("food title conot be null!")
    if [food for food in foods if food["title"] == data.get("title")]:
        raise exceptions.BadRequest("food title exists!")
    if not data.get("category"):
        raise exceptions.BadRequest("category conot be null!")
    if not data.get("description"):
        raise exceptions.BadRequest("description conot be null!")
    if not data.get("estimated_time"):
        raise exceptions.BadRequest("estimated_time conot be null!")
    foods.append({"id":str(uuid.uuid4()),
                  "title":data.get("title"),
                  "category":data.get("category"),
                  "description":data.get("description",""),
                  "estimated_time":data.get("estimated_time"),
                  "difficulty":data.get("difficulty"),
                  "ingredients":data.get("ingredients")})
    return json({"detail":"new food recipe has been created"})

@app.get("/recipes/<food_id>")
async def recipe_detail(request:Request, food_id:str):
    for food in foods:
        if food["id"] == food_id:
            return json(food)
    return exceptions.NotFound("food recipe dosn't exists.")

@app.put("/recipes/<food_id>")
@openapi.body(FoodModel)
async def recipe_update(request:Request, food_id):
    data = request.json
    if not data.get("title"):
        raise exceptions.BadRequest("title conot be null!")
    if [food for food in foods if food["title"] == data.get("title") and food["id"] != food_id]:
        raise exceptions.BadRequest("food title exists!")
    if not data.get("category"):
        raise exceptions.BadRequest("category conot be null!")
    if not data.get("description"):
        raise exceptions.BadRequest("description conot be null!")
    if not data.get("estimated_time"):
        raise exceptions.BadRequest("estimated_time conot be null!")
    
    for food in foods:
        if food["id"] == food_id:
            food.update({"title":data.get("title"),
                         "category":data.get("category"),
                         "description":data.get("description",""),
                         "estimated_time":data.get("estimated_time"),
                         "difficulty":data.get("difficulty"),
                         "ingredients":data.get("ingredients")})
            return json({"detail":"recipe has been update"})
        
    return exceptions.NotFound("food recipe dosnt exists.")

@app.delete("/recipes/<food_id>")
async def recipe_delete(request:Request, food_id):
    global foods
    old_food = foods
    foods = [food for food in foods if food["id"] != food_id]
    if len(old_food) == len(foods):
        return exceptions.BadRequest("food recipe dosn't exist!")
    return json({"detail":"food recipe has been delete"},204)

@app.get("/recipes/export")
async def get_export(request:Request):

    header = ['ID','Title','Category','Description','Estimated_time','Difficulty','Ingredients']
    with open('foods_recipes.csv', 'w', encoding='utf8') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(header)
        for food in foods:
            csvwriter.writerow(food.values()) 
    return json({},200)

if __name__ == "__main__":
    app.run(debug=True)