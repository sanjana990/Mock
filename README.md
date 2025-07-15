# MockDb API

A Flask-based REST API for managing mock test listings and orders, backed by a MySQL database.

## Features
- CRUD operations for mock test listings
- CRUD operations for mock test orders
- Admin endpoint for creating listings
- Query available slots and listings by date

## Requirements
- Python 3.7+
- MySQL database

## Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd MockDb
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables
Create a `.env` file in the project root with the following variables:
```
DB_HOST=your_mysql_host
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
DB_PORT=3306
```

## Running the API
```bash
python api.py
```
The API will start on `http://localhost:5000` by default.

## API Endpoints

### Orders
- `GET /getOrderList` — List all orders
- `GET /orders/<order_uuid>` — Get order by UUID
- `POST /CreateOrderItem` — Create a new order
- `PUT /orders/<order_uuid>` — Update an order
- `DELETE /orders/<order_uuid>` — Delete an order

### Listings
- `GET /getListingList` — List all listings
- `GET /listing/<listing_id>` — Get listing by ID
- `POST /CreateListingItem` — Create a new listing
- `PUT /listing/<listing_id>` — Update a listing
- `DELETE /listing/<listing_id>` — Delete a listing

### Admin & Advanced
- `POST /CreateMockListingItemByAdmin` — Create a listing as admin
- `GET /getMockAllListedList` — List all mock listings
- `GET /getMockAllListedListByDate?date=YYYY-MM-DD` — List all mock listings for a specific date
- `GET /getAvailableSlotsofNext30Days` — Get available slots for the next 30 days

## Example: Create a Mock Listing (Admin)
POST `/CreateMockListingItemByAdmin`
```json
{
  "Mock_Listing_Title": "Sample Mock Test June",
  "Mock_Created_DateTime": "2024-06-01 10:00:00",
  "DateOfMock": "2024-06-15",
  "Mock_Start_Hrs": "09:00:00",
  "Mock_End_Hrs": "12:00:00",
  "Mock_Cost": 499,
  "Total_Slot_Seats": 30,
  "Filled_Seats": 0,
  "Remaining_Seats": 30,
  "isSlotOPEN": "Y",
  "Total_Slots_of_Day": 1
}
```

## Notes
- Ensure your MySQL database and tables are set up as expected by the API.
- All time fields should be in `HH:MM:SS` format.
- Date fields should be in `YYYY-MM-DD` format.

## License
MIT
