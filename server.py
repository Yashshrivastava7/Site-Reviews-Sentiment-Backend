from fastapi import FastAPI

app = FastAPI()

reviews = ["Hello" , "World!"]
@app.get("/")
def root():
    return {"Server running!"}

@app.post("/reviews")
def addReviews(review_data):
    reviews.append(review_data)
    return {"message" : "Review added successfully"}

@app.get("/reviews")
def getReviews():
    return reviews
