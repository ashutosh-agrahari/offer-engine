from pydantic import BaseModel
from typing import Dict, Any

class OfferRequest(BaseModel):
    flipkartOfferApiResponse: Dict[str, Any]
