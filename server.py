from fastapi import FastAPI
from textblob import TextBlob
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

@app.post("/test/sentiment")
def getSentiment(review_data: Review):
    blob = TextBlob(review_data.review)
    polarity = blob.sentiment.polarity
    return polarity
    
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
    data_to_retrieve = {
            "sitename": sitename  
    }
    result = reviews_collection.find(data_to_retrieve)
    print(result)
    response = [[r["sitename"],r["review"]] for r in result]
    return response

data = {
        "sitename": "hello.com",
        "review": "Trash"
}

@app.get("/test/{sitename}/{review}")
def test(sitename: str, review: str):
    data = {
        "sitename": sitename,
        "review": review
    }
    reviews_collection.insert_one(data)
    return {"message": "success!"}

def findSentiment(response):
    answer = 0
    iteration = 0
    for r in response :
        iteration += 1
        blob = TextBlob(r[1])
        polarity = blob.sentiment.polarity
        answer += polarity
    return (answer/iteration)

@app.get("/reviews/sentiment/{sitename}")
def getSentimentForSite(sitename: str):
    data_to_retrieve = {
            "sitename": sitename  
    }
    result = reviews_collection.find(data_to_retrieve)
    response = [[r["sitename"],r["review"]] for r in result]
    default = findSentiment(response)
    if default > 0:
        return {"message": "positve", "score": str(default)}
    elif default < 0:
        return {"message": "negative", "score": str(default)}
    else:
        return {"message": "neutral", "score": str(default)}

