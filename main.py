from typing import Optional, List
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from model.dbHandler import match_exact, match_like

app = FastAPI()


@app.get("/")
def index():
    """
    DEFAULT ROUTE
    This method will
    1. Provide usage instructions formatted as JSON
    """
    response = {"usage": "/dict?=<word>"}
    return jsonable_encoder(response)


@app.get("/dict")
def dictionary(word: str):
    """
    DEFAULT ROUTE
    This method will
    1. Accept a word from the request
    2. Try to find an exact match, and return it if found
    3. If not found, find all approximate matches and return
    """
    if not word: 
        response = {"status": "error", "word": word, "data": "word not found"}
        return jsonable_encoder(response)
    definitions = match_exact(word)
    if definitions:
        response = {"status": "success", "word": word, "data": definitions}
        return jsonable_encoder(response)
    definitions = match_like(word)
    if definitions:
        response = {"status": "partial", "word": word, "data": definitions}
        return response
    else:
        response = {"status": "error", "word": word, "data": "word not found"}
        return jsonable_encoder(response)
