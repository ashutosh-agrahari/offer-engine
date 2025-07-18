

# Offer Engine API

A backend service that processes Flipkart’s payment page offers, stores them, and calculates the highest applicable discount for users based on payment details.
Built with **FastAPI**, **SQLite**, and **SQLAlchemy**.

---

## Features

* Extract and store offers from Flipkart’s offer API response.
* Query the highest applicable discount for a given amount, bank, and payment instrument.
* Support for different payment instruments like Credit Card, Debit Card, EMI, UPI.
* REST API with Swagger UI for testing.

---

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/ashutosh-agrahari/offer-engine.git
   cd offer-engine
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate    # For Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**

   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access API docs (Swagger UI)**

   ```
   http://localhost:8000/docs
   ```

---

## Folder Structure

```
offer-engine/
├── app/
│   ├── __init__.py
│   ├── main.py                # Main FastAPI application with endpoints
│   ├── models.py              # SQLAlchemy models for Offer table
│   ├── schemas.py             # Pydantic schemas for request validation
│   └── database.py            # Database connection and session setup
├── sample_flipkart_response.json   # Sample Flipkart API response for testing POST /offer
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── offers.db                  # SQLite database file (created after first run)
├── venv/                      # Virtual environment folder (created locally)

```
## API Endpoints

### 1. POST `/offer`

* **Description:** Accepts Flipkart offer API response and stores all identified offers in the database.
* **Request Body Example:**
  Use the `sample_flipkart_response.json` provided in the project root.

  ```json
  {
    "flipkartOfferApiResponse": { ... }
  }
  ```
* **Response Example:**

  ```json
  {
    "noOfOffersIdentified": 10,
    "noOfNewOffersCreated": 10
  }
  ```

---

### 2. GET `/offers`

* **Description:** Retrieves all stored offers from the database.
* **Use this to verify if the POST `/offer` has stored your data correctly.**

---

### 3. GET `/highest-discount`

* **Query Parameters:**

  * `amountToPay` — Transaction amount.
  * `bankName` — Bank name (e.g., IDFC, HDFC).
  * `paymentInstrument` — Payment method (e.g., CREDIT CARD, UPI).

* **Example Request:**

  ```
  http://localhost:8000/highest-discount?amountToPay=5000&bankName=IDFC&paymentInstrument=CREDIT%20CARD
  ```

* **Response Example:**

  ```json
  {
    "highestDiscountAmount": 500
  }
  ```

---

## How to Test the API

1. Start the server.
2. Use **Swagger UI** at `http://localhost:8000/docs` for easy API testing.
3. First, POST the `sample_flipkart_response.json` payload using `/offer` endpoint.
4. Check stored offers using `/offers` endpoint.
5. Test discount calculation with `/highest-discount` by passing query parameters.

---

## Assumptions Made

* Only one payment instrument is applicable per offer (extracted from offer description).
* If payment instrument is not specified, the offer is assumed to be applicable for all.
* Minimum transaction value is applied before any discount is considered.
* Discount is extracted based on fixed keywords like “Save ₹…”, “up to ₹…”, or percentage offers.
* Flat cashback and percentage discounts are both supported.

---

## Design Choices

* **FastAPI**: Quick development of REST APIs with automatic documentation.
* **SQLite**: Lightweight database suitable for this use case.
* **SQLAlchemy**: ORM for easy database interaction.
* Regex-based extraction of discounts and minimum transaction values for flexibility.

---

## Scaling Considerations for `/highest-discount`

To handle **1000+ requests per second**:

* Implement caching (e.g., Redis) for frequently accessed queries.
* Add database indexes on `bank_name` and `payment_instruments`.
* Use asynchronous database drivers.
* Deploy behind a load balancer with horizontal scaling.
* Move to a production-grade database (e.g., PostgreSQL).

---

## Future Improvements

* Add unit tests with pytest.
* Implement offer update logic instead of delete-and-insert.
* Add user authentication and API key management.
* Containerize with Docker.
* Add pagination support for `/offers`.
* Integrate Redis caching for hot queries.

---

## Requirements

```
fastapi==0.116.1
uvicorn==0.35.0
SQLAlchemy==2.0.41
pydantic==2.11.7
```
---

