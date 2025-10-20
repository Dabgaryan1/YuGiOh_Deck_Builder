from fastapi import APIRouter, HTTPException
import sqlite3
from pydantic import BaseModel

router = APIRouter(prefix="/decks",tags=["decks"])

#Deck model
class Deck(BaseModel):
    name: str
    description: str | None = None

DB_PATH = "decks.db"

#helper function to get db connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

#create decks table if not exists
with get_db_connection() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS decks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    """)
    conn.commit()

#create a new deck
@router.post("/", response_model=Deck)
def create_deck(deck: Deck):
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
            "INSERT INTO decks (name, description) VALUES (?, ?)",
            (deck.name, deck.description)
        )
        conn.commit()
        return {"message": f"Deck '{deck.name}' created successfully."}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Deck could not be created.")

#get all decks
@router.get("/")
def get_decks():
    try:
        with get_db_connection() as conn:
            decks = conn.execute("SELECT * FROM decks").fetchall()
        return {"decks": [dict(deck) for deck in decks]}
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Could not retrieve decks.")

#get one deck
@router.get("/{deck_id}")
def get_deck(deck_id: int):
    try:
        with get_db_connection() as conn:
            deck = conn.execute("SELECT * FROM decks WHERE id = ?", (deck_id,)).fetchone()
        if deck is None:
            raise HTTPException(status_code=404, detail="Deck not found")
        return {"deck": dict(deck)}
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Could not retrieve the deck.")

#delete a deck
@router.delete("/{deck_id}")
def delete_deck(deck_id: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Deck not found")
        return {"message": f"Deck with id {deck_id} deleted successfully."}
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Could not delete the deck.")

#update a deck
@router.put("/{deck_id}", response_model=Deck)
def update_deck(deck_id: int, deck: Deck):
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
            "UPDATE decks SET name = ?, description = ? WHERE id = ?",
            (deck.name, deck.description, deck_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Deck not found")
        return {"message": f"Deck with id {deck_id} updated successfully."}
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Could not update the deck.")
