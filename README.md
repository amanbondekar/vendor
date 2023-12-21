# vendor# Vendor Management System

This is a Django-based Vendor Management System that includes API endpoints for managing vendors, purchase orders, and evaluating vendor performance.

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Contributing](#contributing)

## Setup Instructions

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/vendor-management-system.git
    cd vendor-management-system
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Load initial data (optional):**

    ```bash
    python manage.py loaddata initial_data
    ```

## API Endpoints

### Vendor Management:

- **Create a new vendor:**
  - Endpoint: `POST /api/vendors/`
  - Request Body:
    ```json
    {
      "name": "Vendor1",
      "contact_details": "Contact1",
      "address": "Address1",
      "vendor_code": "V1"
    }
    ```
- **List all vendors:**
  - Endpoint: `GET /api/vendors/`

- **Retrieve a specific vendor's details:**
  - Endpoint: `GET /api/vendors/{vendor_id}/`

- **Update a vendor's details:**
  - Endpoint: `PUT /api/vendors/{vendor_id}/`
  - Request Body:
    ```json
    {
      "name": "UpdatedVendorName"
    }
    ```

- **Delete a vendor:**
  - Endpoint: `DELETE /api/vendors/{vendor_id}/`

### Purchase Order Tracking:

- **Create a purchase order:**
  - Endpoint: `POST /api/purchase_orders/`
  - Request Body:
    ```json
    {
      "po_number": "PO123",
      "vendor": 1,
      "order_date": "2023-01-01",
      "delivery_date": "2023-02-01",
      "items": {"item1": 5, "item2": 10},
      "quantity": 15,
      "status": "pending"
    }
    ```

- **List all purchase orders:**
  - Endpoint: `GET /api/purchase_orders/`

- **Retrieve details of a specific purchase order:**
  - Endpoint: `GET /api/purchase_orders/{po_id}/`

- **Update a purchase order:**
  - Endpoint: `PUT /api/purchase_orders/{po_id}/`
  - Request Body:
    ```json
    {
      "status": "completed"
    }
    ```

- **Delete a purchase order:**
  - Endpoint: `DELETE /api/purchase_orders/{po_id}/`

### Vendor Performance Evaluation:

- **Retrieve a vendor's performance metrics:**
  - Endpoint: `GET /api/vendors/{vendor_id}/performance/`

## Running Tests

To run the test suite, use the following command:

```bash
python manage.py test
