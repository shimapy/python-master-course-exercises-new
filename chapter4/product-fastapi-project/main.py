from fastapi import FastAPI,status,Path
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid


app = FastAPI()

products = [
                {
                "id":"f217cfe5-98e5-4164-afe6-80d9c54bab11",
                "name":"product1",
                "price":20  
                },
                {
                "id":"82af8342-7e0a-4fff-bdf9-8166db0dd762",
                "name":"product2",
                "price":15  
                }
            ]

class ProductsModel(BaseModel):
    name: str
    price: int
    

@app.get("/products")
async def products_list(max_price:int | None = None):
    
    if max_price is not None:
        new_products = [product for product in products if product["price"] < max_price]
        return new_products
    return products


@app.post("/products")
async def products_create(request_data: ProductsModel):
    products.append({"id":str(uuid.uuid4()),
                          "name": request_data.name,
                          "price":request_data.price})
    return JSONResponse({"detail":"product added successfully"},
                        status_code=status.HTTP_201_CREATED)

@app.get("/products/{product_id}")
async def product_detail(product_id: str=Path()):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="product not found")  

@app.put("/products/{product_id}")
async def product_update(request_data: ProductsModel, product_id: str=Path()):
    for product in products:
        if product["id"] == product_id:
            product["name"] = request_data.name
            product["price"] = request_data.price
            return product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="product not found")
    


@app.delete("/products/{product_id}")
async def product_delete(product_id: str=Path()):
    global products
    products = [product for product in products if product["id"] != product_id]
    return JSONResponse({}, status_code=status.HTTP_204_NO_CONTENT)