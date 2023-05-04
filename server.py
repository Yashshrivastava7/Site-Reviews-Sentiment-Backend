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
