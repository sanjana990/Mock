from flask import Flask, request, jsonify
import mysql.connector
from datetime import timedelta, datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=os.getenv('DB_PORT')
    )

def timedelta_to_str(td):
    if isinstance(td, timedelta):
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return td

@app.route('/getOrderList', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM MOCKS_BOOKING_ORDERS_TBL")
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(orders)

@app.route('/orders/<order_uuid>', methods=['GET'])
def get_order(order_uuid):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM MOCKS_BOOKING_ORDERS_TBL WHERE Mock_Order_UUID = %s", (order_uuid,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()
    if order:
        return jsonify(order)
    else:
        return jsonify({'error': 'Order not found'}), 404

@app.route('/CreateOrderItem', methods=['POST'])
def add_order():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = ("INSERT INTO MOCKS_BOOKING_ORDERS_TBL "
           "(Mock_Order_UUID, Mock_Listing_UUID, Mock_Ordered_User_EmailId, Mock_Order_DateTime, "
           "isOrderComboOfMockNFullCourse_Boolean, ORDER_Payment_UUID, Mock_Order_PGW_Status, "
           "Mock_Order_Status, hasUserAttendedTheMock_Boolean, MOCK_ORDER_VALUE_Cost, MOCK_ORDER_QTY) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    values = (
        data['Mock_Order_UUID'],
        data['Mock_Listing_UUID'],
        data['Mock_Ordered_User_EmailId'],
        data['Mock_Order_DateTime'],
        data['isOrderComboOfMockNFullCourse_Boolean'],
        data['ORDER_Payment_UUID'],
        data['Mock_Order_PGW_Status'],
        data['Mock_Order_Status'],
        data['hasUserAttendedTheMock_Boolean'],
        data['MOCK_ORDER_VALUE_Cost'],
        data['MOCK_ORDER_QTY']
    )
    try:
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({'message': 'Order added successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/orders/<order_uuid>', methods=['PUT'])
def update_order(order_uuid):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = ("UPDATE MOCKS_BOOKING_ORDERS_TBL SET "
           "Mock_Listing_UUID=%s, Mock_Ordered_User_EmailId=%s, Mock_Order_DateTime=%s, "
           "isOrderComboOfMockNFullCourse_Boolean=%s, ORDER_Payment_UUID=%s, Mock_Order_PGW_Status=%s, "
           "Mock_Order_Status=%s, hasUserAttendedTheMock_Boolean=%s, MOCK_ORDER_VALUE_Cost=%s, MOCK_ORDER_QTY=%s "
           "WHERE Mock_Order_UUID=%s")
    values = (
        data['Mock_Listing_UUID'],
        data['Mock_Ordered_User_EmailId'],
        data['Mock_Order_DateTime'],
        data['isOrderComboOfMockNFullCourse_Boolean'],
        data['ORDER_Payment_UUID'],
        data['Mock_Order_PGW_Status'],
        data['Mock_Order_Status'],
        data['hasUserAttendedTheMock_Boolean'],
        data['MOCK_ORDER_VALUE_Cost'],
        data['MOCK_ORDER_QTY'],
        order_uuid
    )
    try:
        cursor.execute(sql, values)
        conn.commit()
        if cursor.rowcount:
            return jsonify({'message': 'Order updated successfully'})
        else:
            return jsonify({'error': 'Order not found'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/orders/<order_uuid>', methods=['DELETE'])
def delete_order(order_uuid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM MOCKS_BOOKING_ORDERS_TBL WHERE Mock_Order_UUID = %s", (order_uuid,))
    conn.commit()
    result = cursor.rowcount
    cursor.close()
    conn.close()
    if result:
        return jsonify({'message': 'Order deleted successfully'})
    else:
        return jsonify({'error': 'Order not found'}), 404

# --- LISTING CRUD ENDPOINTS ---

@app.route('/getListingList', methods=['GET'])
def get_listings():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM MOCKS_LISTING_TBL")
    listings = cursor.fetchall()
    for listing in listings:
        if 'Mock_Start_Hrs' in listing:
            listing['Mock_Start_Hrs'] = timedelta_to_str(listing['Mock_Start_Hrs'])
        if 'Mock_End_Hrs' in listing:
            listing['Mock_End_Hrs'] = timedelta_to_str(listing['Mock_End_Hrs'])
    cursor.close()
    conn.close()
    return jsonify(listings)

@app.route('/listing/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM MOCKS_LISTING_TBL WHERE Mock_Listing_ID = %s", (listing_id,))
    listing = cursor.fetchone()
    if listing:
        if 'Mock_Start_Hrs' in listing:
            listing['Mock_Start_Hrs'] = timedelta_to_str(listing['Mock_Start_Hrs'])
        if 'Mock_End_Hrs' in listing:
            listing['Mock_End_Hrs'] = timedelta_to_str(listing['Mock_End_Hrs'])
        cursor.close()
        conn.close()
        return jsonify(listing)
    else:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Listing not found'}), 404

@app.route('/CreateListingItem', methods=['POST'])
def add_listing():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = ("INSERT INTO MOCKS_LISTING_TBL "
           "(Mock_Listing_Title, Mock_Created_DateTime, DateOfMock, Mock_Start_Hrs, Mock_End_Hrs, "
           "Mock_Cost, Total_Slot_Seats, Filled_Seats, Remaining_Seats, isSlotOPEN, Total_Slots_of_Day) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    values = (
        data['Mock_Listing_Title'],
        data['Mock_Created_DateTime'],
        data['DateOfMock'],
        data['Mock_Start_Hrs'],
        data['Mock_End_Hrs'],
        data['Mock_Cost'],
        data['Total_Slot_Seats'],
        data.get('Filled_Seats', 0),
        data.get('Remaining_Seats', 0),
        data['isSlotOPEN'],
        data['Total_Slots_of_Day']
    )
    try:
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({'message': 'MOCK Listing Added Successfully', 'Mock_Listing_ID': cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/listing/<int:listing_id>', methods=['PUT'])
def update_listing(listing_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = ("UPDATE MOCKS_LISTING_TBL SET "
           "Mock_Listing_Title=%s, Mock_Created_DateTime=%s, DateOfMock=%s, Mock_Start_Hrs=%s, Mock_End_Hrs=%s, "
           "Mock_Cost=%s, Total_Slot_Seats=%s, Filled_Seats=%s, Remaining_Seats=%s, isSlotOPEN=%s, Total_Slots_of_Day=%s "
           "WHERE Mock_Listing_ID=%s")
    values = (
        data['Mock_Listing_Title'],
        data['Mock_Created_DateTime'],
        data['DateOfMock'],
        data['Mock_Start_Hrs'],
        data['Mock_End_Hrs'],
        data['Mock_Cost'],
        data['Total_Slot_Seats'],
        data['Filled_Seats'],
        data['Remaining_Seats'],
        data['isSlotOPEN'],
        data['Total_Slots_of_Day'],
        listing_id
    )
    try:
        cursor.execute(sql, values)
        conn.commit()
        if cursor.rowcount:
            return jsonify({'message': 'Listing updated successfully'})
        else:
            return jsonify({'error': 'Listing not found'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/listing/<int:listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM MOCKS_LISTING_TBL WHERE Mock_Listing_ID = %s", (listing_id,))
    conn.commit()
    result = cursor.rowcount
    cursor.close()
    conn.close()
    if result:
        return jsonify({'message': 'Listing deleted successfully'})
    else:
        return jsonify({'error': 'Listing not found'}), 404

@app.route('/CreateMockListingItemByAdmin', methods=['POST'])
def create_mock_listing_by_admin():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = ("INSERT INTO MOCKS_LISTING_TBL "
           "(Mock_Listing_Title, Mock_Created_DateTime, DateOfMock, Mock_Start_Hrs, Mock_End_Hrs, "
           "Mock_Cost, Total_Slot_Seats, Filled_Seats, Remaining_Seats, isSlotOPEN, Total_Slots_of_Day) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    values = (
        data['Mock_Listing_Title'],
        data['Mock_Created_DateTime'],
        data['DateOfMock'],
        data['Mock_Start_Hrs'],
        data['Mock_End_Hrs'],
        data['Mock_Cost'],
        data['Total_Slot_Seats'],
        data.get('Filled_Seats', 0),
        data.get('Remaining_Seats', 0),
        data['isSlotOPEN'],
        data['Total_Slots_of_Day']
    )
    try:
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({'message': 'MockSlot added successfully', 'Mock_Listing_ID': cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/getMockAllListedList', methods=['GET'])
def get_mock_all_listed_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM MOCKS_LISTING_TBL")
    listings = cursor.fetchall()
    for listing in listings:
        if 'Mock_Start_Hrs' in listing:
            listing['Mock_Start_Hrs'] = timedelta_to_str(listing['Mock_Start_Hrs'])
        if 'Mock_End_Hrs' in listing:
            listing['Mock_End_Hrs'] = timedelta_to_str(listing['Mock_End_Hrs'])
    cursor.close()
    conn.close()
    return jsonify(listings)

@app.route('/getMockAllListedListByDate', methods=['GET'])
def get_mock_all_listed_list_by_date():
    date = request.args.get('date')
    if not date:
        return jsonify({'error': 'Missing date parameter'}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM MOCKS_LISTING_TBL WHERE DateOfMock = %s", (date,))
    listings = cursor.fetchall()
    for listing in listings:
        if 'Mock_Start_Hrs' in listing:
            listing['Mock_Start_Hrs'] = timedelta_to_str(listing['Mock_Start_Hrs'])
        if 'Mock_End_Hrs' in listing:
            listing['Mock_End_Hrs'] = timedelta_to_str(listing['Mock_End_Hrs'])
    cursor.close()
    conn.close()
    return jsonify(listings)

@app.route('/getAvailableSlotsofNext30Days', methods=['GET'])
def get_available_slots_of_next_30_days():
    today = datetime.now().date()
    future_date = today + timedelta(days=30)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT DateOfMock, Mock_Start_Hrs, Mock_End_Hrs FROM MOCKS_LISTING_TBL WHERE isSlotOPEN = 'Y' AND DateOfMock >= %s AND DateOfMock < %s", (today, future_date))
    slots = cursor.fetchall()
    for slot in slots:
        if 'Mock_Start_Hrs' in slot:
            slot['Mock_Start_Hrs'] = timedelta_to_str(slot['Mock_Start_Hrs'])
        if 'Mock_End_Hrs' in slot:
            slot['Mock_End_Hrs'] = timedelta_to_str(slot['Mock_End_Hrs'])
    # Group by DateOfMock
    result = {}
    for slot in slots:
        date_key = str(slot['DateOfMock'])
        slot_info = {
            'Date': date_key,
            'Mock_Start_Hrs': slot['Mock_Start_Hrs'],
            'Mock_End_Hrs': slot['Mock_End_Hrs']
        }
        if date_key not in result:
            result[date_key] = []
        result[date_key].append(slot_info)
    cursor.close()
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 