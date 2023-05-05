from fastapi import FastAPI
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()

uri = "mongodb+srv://yashnode:yashnodejs7@cluster0.jnmzzaw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Final-Project"]
reviews_collection = db["reviews"]

class Review(BaseModel):
    sitename: str
    review: str
    
@app.get("/")
def root():
    collections = db.list_collection_names()
    return collections 

@app.post("/reviews")
def addReviews(review_data: Review):
    data_to_insert = {
        "sitename": review_data.sitename,
        "review": review_data.review
    }
    ids = reviews_collection.insert_one(data_to_insert)
    return {"message" : "Review added successfully"}

@app.get("/reviews")
def getAllReviews():
    reviews = reviews_collection.find()
    response = [[r["sitename"], r["review"]] for r in reviews]
    return response

@app.get("/reviews/{sitename}")
def getReviewForSite(sitename: str):
    review_for_site = []
    for x in reviews:
        if x.sitename == sitename:
            review_for_site.append(x)
    return review_for_site

data = {
        "sitename": "hello.com",
        "review": "Trash"
}

@app.get("/test")
def test():
    reviews_collection.insert_one(data)
    return {"message": "success!"}

@app.get("/reviews/sentiment/{sitename}")
def getSentimentForSite():
    default = 0
    if default > 0:
        return {"message": "positve"}
    elif default < 0:
        return {"message": "negative"}
    else:
        return {"message": "neutral"}

