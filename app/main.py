
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
    db.query(models.Offer).delete()
    db.commit()  # Commit the deletion to persist changes

    offer_items = payload.flipkartOfferApiResponse.get('paymentOptions', {}).get('items', [])

    total_offers = 0
    new_offers = 0

    for item in offer_items:
        if item.get('type') == 'OFFER_LIST':
            offer_list = item.get('data', {}).get('offers', {}).get('offerList', [])
            for offer in offer_list:
                print(f"Processing offer: {offer}")
                offer_id = offer.get('offerDescription', {}).get('id')
                offer_text = offer.get('offerText', {}).get('text')
                description = offer.get('offerDescription', {}).get('text')
                providers = offer.get('provider', []) or ['ALL_BANKS']
                instruments = offer.get('paymentInstrument', []) or []

                total_offers += len(providers)

                for bank in providers:
                    # Delete old offers for the same offer_id and bank_name
                  
                    print(f"Description: {description}")
                    # Add new offer
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

    def extract_discount(text, description):
        if not text:
            return 0
        print(f"Extracting discount from text: {text}")
        print(f"Description: {description}")
        percentage_match = re.search(r'(\d+)%\s*off', description, re.IGNORECASE)
        print(f"percentage_match: {percentage_match}")
        max_discount_amount = re.search(r'Save\s*₹\s*([\d,]+)', text, re.IGNORECASE)
        print(f"amount_match: {max_discount_amount}")
        min_txn_match = re.search(r'Min Txn Value:\s*₹\s*([\d,]+)', description, re.IGNORECASE)
        min_txn_value = int(min_txn_match.group(1).replace(',', '')) if min_txn_match else 0
        print(f"Min Txn Value: {min_txn_value}")
        if amountToPay < min_txn_value:
            print(f"Amount to pay ({amountToPay}) is less than Min Txn Value ({min_txn_value}). Discount not applicable.")
            return 0
        if percentage_match:
             percentage = int(percentage_match.group(1))
             return (percentage / 100) * amountToPay  
        elif max_discount_amount:
            return int(max_discount_amount.group(1).replace(',', ''))  # Return the amount discount

        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 0

    max_discount = 0

    for offer in offers:
        if not offer.payment_instruments or paymentInstrument in offer.payment_instruments:
            discount = extract_discount(offer.offer_text, offer.description)
            print(f"Calculated discount for offer {offer.offer_id}: {discount}")
            if discount > max_discount:
                max_discount = discount

    return {"highestDiscountAmount": max_discount}



