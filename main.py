from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models import Produit, ProduitUpdate
from database import db
from blockchain import enregistrer_sur_blockchain
import uuid

app = FastAPI(
    title="GestionStock API",
    description="API CRUD de gestion de stock — Projet EFREI M1",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def interface():
    return FileResponse("static/index.html")

@app.post("/produits", status_code=201)
def creer_produit(produit: Produit):
    produit_id = str(uuid.uuid4())
    produit_data = produit.dict()
    produit_data["id"] = produit_id
    db[produit_id] = produit_data
    tx_hash = enregistrer_sur_blockchain(produit_id, "creation")
    produit_data["blockchain_tx"] = tx_hash
    return {"message": "Produit créé avec succès", "produit": produit_data}

@app.get("/produits")
def lister_produits():
    return {"produits": list(db.values()), "total": len(db)}

@app.get("/produits/{produit_id}")
def obtenir_produit(produit_id: str):
    if produit_id not in db:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return db[produit_id]

@app.put("/produits/{produit_id}")
def modifier_produit(produit_id: str, mise_a_jour: ProduitUpdate):
    if produit_id not in db:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    produit_actuel = db[produit_id]
    donnees_maj = mise_a_jour.dict(exclude_unset=True)
    produit_actuel.update(donnees_maj)
    db[produit_id] = produit_actuel
    enregistrer_sur_blockchain(produit_id, "modification")
    return {"message": "Produit mis à jour", "produit": produit_actuel}

@app.delete("/produits/{produit_id}")
def supprimer_produit(produit_id: str):
    if produit_id not in db:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    produit_supprime = db.pop(produit_id)
    enregistrer_sur_blockchain(produit_id, "suppression")
    return {"message": "Produit supprimé", "produit": produit_supprime}
