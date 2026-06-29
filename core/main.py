from fastapi import FastAPI, Query, status, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import random
from typing import Annotated

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello"}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)

# Or => uvicorn main:app --reload --host 0.0.0.0 --port 8082
# --reload is only for development

# Uvicorn is a async server (ASGI Server) that runs our app and retrieves HTTP requests from client and brings it 
# back To Our App And Gives Responses of app to Client

game_list = [
    {"id": 1, "name": "Grand Theft Auto VI"},
    {"id": 2, "name": "Marvel Wolverine"},
    {"id": 3, "name": "Assassin's Creed Black Flag"},
    {"id": 4, "name": "Grand Theft Auto VI Ultimate"},
]

@app.get("/get_all")
def get_all():
    return JSONResponse(content= game_list, status_code= status.HTTP_200_OK)

@app.get("/names/{name_id}")
def get_single_item(name_id: int):
    for game in game_list:
        if game["id"] == name_id:
            return game 

    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)

@app.get("/names")
def search_items(q: Annotated[str | None, Query(min_length=2, max_length=50)] = None):

    if q:
        return [item for item in game_list if q in item["name"]]
    return game_list

@app.post("/names", status_code= status.HTTP_201_CREATED)
def create_item(name):
    new_item = {"id": random.randint(4, 100), "name": name}
    game_list.append(new_item)

    return {"detail": "Created"}


@app.put("/names/{name_id}")
def get_single_item(name_id: int, name:str):
    for game in game_list:
        if game["id"] == name_id:
            game["name"] = name
            return game
        
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)

@app.delete("/names/{name_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_item(name_id: int):
    for game in game_list:
        if game["id"] == name_id:
            game_list.remove(game)
            return JSONResponse(content= {"detail": "Item Deleted"}, status_code= status.HTTP_200_OK)
        
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)