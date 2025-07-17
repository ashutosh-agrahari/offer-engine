from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, SessionLocal
from app.schemas import OfferRequest
import re

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Offer Engine API is running"}

@app.post("/offer")
def create_offers(payload: OfferRequest, db: Session = Depends(get_db)):
    offer_items = payload.flipkartOfferApiResponse.get('paymentOptions', {}).get('items', [])

    total_offers = 0
    new_offers = 0

    for item in offer_items:
        if item.get('type') == 'OFFER_LIST':
            offer_list = item.get('data', {}).get('offers', {}).get('offerList', [])
            for offer in offer_list:
                offer_id = offer.get('offerDescription', {}).get('id')
                offer_text = offer.get('offerText', {}).get('text')
                description = offer.get('offerDescription', {}).get('text')
                providers = offer.get('provider', []) or ['ALL_BANKS']
                instruments = offer.get('paymentInstrument', []) or []

                total_offers += len(providers)

                for bank in providers:
                    existing_offer = db.query(models.Offer).filter_by(offer_id=offer_id, bank_name=bank).first()
                    if not existing_offer:
                        new_entry = models.Offer(
                            offer_id=offer_id,
                            bank_name=bank,
                            offer_text=offer_text,
                            description=description,
                            payment_instruments=instruments
                        )
                        db.add(new_entry)
                        new_offers += 1

    db.commit()

    return {
        "noOfOffersIdentified": total_offers,
        "noOfNewOffersCreated": new_offers
    }

@app.get("/highest-discount")
def get_highest_discount(amountToPay: float, bankName: str, paymentInstrument: str, db: Session = Depends(get_db)):
    offers = db.query(models.Offer).filter(models.Offer.bank_name == bankName).all()

    if not offers:
        return {"highestDiscountAmount": 0}

    def extract_discount(text):
        if not text:
            return 0
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 0

    max_discount = 0

    for offer in offers:
        if not offer.payment_instruments or paymentInstrument in offer.payment_instruments:
            discount = extract_discount(offer.offer_text)
            if discount > max_discount:
                max_discount = discount

    return {"highestDiscountAmount": max_discount}


