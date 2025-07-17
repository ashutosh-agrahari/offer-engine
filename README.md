# Offer Engine API

A backend service to store offers and calculate the best discount based on bank and payment instrument.
Built with **FastAPI** and **SQLite**.

---

## Features

* Store offers from Flipkart’s offer API
* Fetch the highest applicable discount
* Filter by bank and payment instrument
* REST API with Swagger UI

---

## Setup Instructions

```bash
# Clone the repo
git clone https://github.com/yourusername/offer-engine.git
cd offer-engine

# Create virtual environment
python -m venv venv
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload
```

---

## API Endpoints

### POST `/offer`

* Stores offers from Flipkart’s API response.
* **Request Body:**

```json
{
  "flipkartOfferApiResponse": { ... }
}
```

* **Response:**

```json
{
  "noOfOffersIdentified": 5,
  "noOfNewOffersCreated": 3
}
```

---

### GET `/highest-discount`

* Retrieves the highest discount based on bank and payment instrument.
* **Example:**

```
GET /highest-discount?amountToPay=10000&bankName=AXIS&paymentInstrument=CREDIT
```

* **Response:**

```json
{
  "highestDiscountAmount": 750
}
```

---

## Assumptions

* Payment instrument may be empty; in that case, offers are treated as applicable to all.
* Discount is extracted as the first integer from the offer text.
* SQLite is used for simplicity.

---

## Design Choices

* **FastAPI** for rapid REST API development.
* **SQLAlchemy ORM** for database operations.
* **SQLite** for ease of local setup (easily switchable to PostgreSQL or MySQL).
* Modular structure with clear separation of concerns.

---

## Scaling Considerations for `/highest-discount`

To handle **1,000+ requests per second**:

* Implement caching for frequent queries (e.g., Redis).
* Add indexes on `bank_name` and `payment_instruments` columns.
* Use asynchronous database operations with connection pooling.
* Deploy behind a load balancer with horizontal scaling.

---

## Potential Improvements with More Time

* Write unit tests using pytest.
* Implement pagination for listing offers.
* Add authentication and rate limiting.
* Integrate Redis for caching frequently accessed data.
* Containerize with Docker for production deployment.

---

## License

For educational use only — Flipkart APIs should be used responsibly.
