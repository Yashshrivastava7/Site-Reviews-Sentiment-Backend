from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Review(BaseModel):
    sitename: str
    review: str
    
reviews = []
@app.get("/")
def root():
    return {"Server running!"}

@app.post("/reviews")
def addReviews(review_data: Review):
    reviews.append(review_data)
    return {"message" : "Review added successfully"}

@app.get("/reviews")
def getReviews():
    return reviews

@app.get("/reviews/{sitename}")
def getReviewForSite(sitename: str):
    review_for_site = []
    for x in reviews:
        if x.sitename == sitename:
            review_for_site.append(x)
    return review_for_site

@app.get("/reviews/sentiment/{sitename}")
def getSentimentForSite():
    default = 0
    if default > 0:
        return {"message": "positve"}
    elif default < 0:
        return {"message": "negative"}
    else:
        return {"message": "neutral"}

