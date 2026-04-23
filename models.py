from pydantic import BaseModel, Field
from typing import Optional

class Produit(BaseModel):
    """Modèle d'un produit dans le stock."""
    nom: str = Field(..., example="Casque de chantier")
    categorie: str = Field(..., example="Équipement de protection")
    quantite: int = Field(..., ge=0, example=50)
    prix: float = Field(..., gt=0, example=29.99)

    class Config:
        json_schema_extra = {
            "example": {
                "nom": "Casque de chantier",
                "categorie": "Équipement de protection",
                "quantite": 50,
                "prix": 29.99
            }
        }


class ProduitUpdate(BaseModel):
    """Modèle pour la mise à jour partielle d'un produit (tous les champs sont optionnels)."""
    nom: Optional[str] = None
    categorie: Optional[str] = None
    quantite: Optional[int] = Field(None, ge=0)
    prix: Optional[float] = Field(None, gt=0)
