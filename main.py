from fastapi import FastAPI
from routers import cards, decks

app = FastAPI(
    title="Yu-Gi-Oh Deck Builder",
    description="An API for building and managing Yu-Gi-Oh decks.",
    version="1.0.0",
)

#register routers
app.include_router(cards.router)
app.include_router(decks.router)

@app.get("/")
def home():
    return {"message": "Yu-Gi-Oh Deck Builder!"}