from fastapi import APIRouter, HTTPException, Query
import httpx

router = APIRouter(
    prefix="/cards",
    tags=["cards"],
)

@router.get("/")
async def search_cards(name: str = Query(..., description="The name of the card to search for")):
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={name}"
    async with httpx.AsyncClient() as clients:
        r = await clients.get(url)

    if r.status_code != 200:
        raise HTTPException(status_code=404, detail="Card not found")

    data = r.json()
    cards = [{
        "id": card["id"],
        "name": card["name"],
        "type": card["type"],
        "desc": card["desc"],
        "image_url": card["card_images"][0]["image_url"]
    } for card in data.get("data", [])]
    return {"cards": cards}