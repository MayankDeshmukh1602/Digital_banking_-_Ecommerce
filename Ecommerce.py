from flask import Flask, request
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
def users():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            email VARCHAR UNIQUE,
            password_hash VARCHAR,
            role VARCHAR,
            created_at VARCHAR
        )
    ''')
    connect.commit()
    connect.close()

@app.route('/')
def home():
    return "E-commerce API is running"
@app.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    hashed_password = generate_password_hash(password)
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        INSERT INTO users
        (name, email, password_hash, role, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        name,
        email,
        hashed_password,
        'customer',
        datetime.now()
    ))
    connect.commit()
    connect.close()
    return {"message": "User registered successfully"}

@app.route('/all_users', methods=['GET'])
def all_users():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    connect.close()
    return {"users": users}

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        SELECT * FROM users
        WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()
    connect.close()
    if user:
        stored_password_hash = user[3]
        if check_password_hash(stored_password_hash, password):
            return {
                "message": "Login successful...",
                "user_id": user[0],
                "role": user[4]
            }
    return {
        "message": "Invalid email or password."
    }

def address():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS addresses(
            address_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            line1 VARCHAR,
            city VARCHAR,
            state VARCHAR,
            postal_code INT
        )
    ''')
    connect.commit()
    connect.close()

@app.route('/addresses', methods=['POST'])
def addresses():
    user_id = request.json.get('user_id')
    line1 = request.json.get('line1')
    city = request.json.get('city')
    state = request.json.get('state')
    postal_code = request.json.get('postal_code')
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        INSERT INTO addresses
        (user_id, line1, city, state, postal_code)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        user_id,
        line1,
        city,
        state,
        postal_code
    ))
    connect.commit()
    connect.close()
    return {
        "message": "Address added successfully"}

@app.route('/Show_address', methods=['GET'])
def Show_address():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM addresses')
    addresses = cursor.fetchall()
    connect.close()
    return {"addresses": addresses}

def product():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            description VARCHAR,
            price INT,
            stock INT
        )
    ''')
    connect.commit()
    connect.close()
    return {
        "message": "Table created successfully"}

@app.route('/products', methods=['POST'])
def products():
    name = request.json.get('name')
    description = request.json.get('description')
    price = request.json.get('price')
    stock = request.json.get('stock')
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        INSERT INTO products
        (name, description, price, stock)
        VALUES (?, ?, ?, ?)
    ''', (
        name,
        description,
        price,
        stock
    ))
    connect.commit()
    connect.close()
    return {
        "message": "Product added successfully"}

@app.route('/Show_products', methods=['GET'])
def Show_products():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    connect.close()
    return {"products": products}

def manage_inventory():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory(
            product_id INT,
            available_qty INT,
            reserved_qty INT,
            version INT
        )
    ''')
    connect.commit()
    connect.close()
    return {
        "message": "Table created successfully"}

@app.route('/inventory', methods=['POST'])
def inventory():
    product_id = request.json.get('product_id')
    available_qty = request.json.get('available_qty')
    reserved_qty = request.json.get('reserved_qty')
    version = request.json.get('version')
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        INSERT INTO inventory
        (product_id, available_qty, reserved_qty, version)
        VALUES (?, ?, ?, ?)
    ''', (
        product_id,
        available_qty,
        reserved_qty,
        version
    ))
    connect.commit()
    connect.close()
    return {
        "message": "Item successfully added to inventory"}

@app.route('/show_inventory', methods=['GET'])
def show_inventory():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM inventory')
    inventory = cursor.fetchall()
    connect.close()
    return {"inventory": inventory}

def create_cart():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart(
            user_id INT,
            product_id INT,
            quantity INT
        )
    ''')
    connect.commit()
    connect.close()
    return {
        "message": "Table created successfully"}

@app.route('/cart', methods=['POST'])
def cart():
    user_id = request.json.get('user_id')
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        INSERT INTO cart
        (user_id, product_id, quantity)
        VALUES (?, ?, ?)
    ''', (
        user_id,
        product_id,
        quantity
    ))
    connect.commit()
    connect.close()
    return {
        "message": "Item successfully added to cart"
    }

@app.route('/show_cart', methods=['GET'])
def show_cart():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM cart')
    cart = cursor.fetchall()
    connect.close()
    return {"cart": cart}

def order():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders(
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            status VARCHAR,
            totals FLOAT
        )
    ''')
    connect.commit()
    connect.close()
    return {
        "message": "Orders table created successfully"}

@app.route('/create_order', methods=['POST'])
def orders():
    user_id = request.json.get('user_id')
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE user_id = ?',
        (user_id,)
    )
    user = cursor.fetchone()
    if user is None:
        connect.close()
        return {
            "message": "User does not exists"}
    cursor.execute('''
        INSERT INTO orders
        (user_id, status, totals)
        VALUES (?, ?, ?)
    ''', (
        user_id,
        'pending',
        0
    ))
    connect.commit()
    order_id = cursor.lastrowid
    connect.close()
    return {
        "message": "order created successfully",
        "order_id": order_id,
        "user_id": user_id,
        "status": "pending",
        "totals": 0
    }

@app.route('/show_orders', methods=['GET'])
def show_orders():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    connect.close()
    return {"orders": orders}

def accounts():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bank_account(
            user_id INTEGER PRIMARY KEY,
            provider_ref VARCHAR,
            masked_number VARCHAR,
            status VARCHAR
        )
    ''')
    connect.commit()
    connect.close()
    return {
        "message": "Table created successfully"}

@app.route('/bank_account', methods=['POST'])
def bank_account():
    user_id = request.json.get('user_id')
    provider_ref = request.json.get('provider_ref')
    masked_number = request.json.get('masked_number')
    status = request.json.get('status')
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        INSERT INTO bank_account
        (user_id, provider_ref, masked_number, status)
        VALUES (?, ?, ?, ?)
    ''', (
        user_id,
        provider_ref,
        masked_number,
        status
    ))
    connect.commit()
    connect.close()
    return {
        "message": "Bank account linked successfully"}

@app.route('/fetch_account', methods=['GET'])
def fetch_accounts():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM bank_account')
    bank_account = cursor.fetchall()
    connect.close()
    return {
        "bank_accounts": bank_account
    }

def wallets():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallet(
            user_id INTEGER PRIMARY KEY,
            balance FLOAT,
            currency VARCHAR,
            version INTEGER
        )
    ''')
    connect.commit()
    connect.close()
    return {
        "message": "Table created successfully"}

@app.route('/wallet', methods=['POST'])
def wallet():
    user_id = request.json.get('user_id')
    balance = request.json.get('balance')
    currency = request.json.get('currency')
    version = request.json.get('version')
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        INSERT INTO wallet
        (user_id, balance, currency, version)
        VALUES (?, ?, ?, ?)
    ''', (
        user_id,
        balance,
        currency,
        version
    ))
    connect.commit()
    connect.close()
    return {
        "message": "wallet linked successfully"}

@app.route('/show_wallet', methods=['GET'])
def show_wallet():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM wallet')
    wallet = cursor.fetchall()
    connect.close()
    return {
        "wallet": wallet}

def payment():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments(
            order_id INTEGER PRIMARY KEY,
            amount FLOAT,
            method VARCHAR,
            status VARCHAR,
            idempotency_key VARCHAR
        )
    ''')
    connect.commit()
    connect.close()
    return {
        "message": "Table created successfully"}

@app.route('/payments', methods=['POST'])
def payments():
    order_id = request.json.get('order_id')
    amount = request.json.get('amount')
    method = request.json.get('method')
    status = request.json.get('status')
    idempotency_key = request.json.get('idempotency_key')
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        INSERT INTO payments
        (order_id, amount, method, status, idempotency_key)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        order_id,
        amount,
        method,
        status,
        idempotency_key
    ))
    connect.commit()
    connect.close()
    return {
        "message": "payment success"}

@app.route('/show_payments', methods=['GET'])
def show_payments():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM payments')
    payments = cursor.fetchall()
    connect.close()
    return {
        "payments": payments}

def ledger():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ledger_entries(
            ledger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_type VARCHAR,
            account_id INTEGER,
            direction VARCHAR,
            amount FLOAT,
            reference VARCHAR
        )
    ''')
    connect.commit()
    connect.close()
    return {
        "message": "Table created successfully"}

@app.route('/ledger_entries', methods=['POST'])
def ledger_entries():
    account_type = request.json.get('account_type')
    account_id = request.json.get('account_id')
    direction = request.json.get('direction')
    amount = request.json.get('amount')
    reference = request.json.get('reference')
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        INSERT INTO ledger_entries
        (account_type, account_id, direction, amount, reference)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        account_type,
        account_id,
        direction,
        amount,
        reference
    ))
    connect.commit()
    connect.close()
    return {
        "message": "ledger entries.."}

@app.route('/show_ledger', methods=['GET'])
def show_ledger():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM ledger_entries')
    ledger_entries = cursor.fetchall()
    connect.close()
    return {
        "ledger_entries": ledger_entries}

def refund():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS refunds(
            payment_id INTEGER PRIMARY KEY,
            amount FLOAT,
            reason VARCHAR,
            status VARCHAR
        )
    ''')
    connect.commit()
    connect.close()
    return {
        "message": "Table created successfully"}

@app.route('/refunds', methods=['POST'])
def refunds():
    payment_id = request.json.get('payment_id')
    amount = request.json.get('amount')
    reason = request.json.get('reason')
    status = request.json.get('status')
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        INSERT INTO refunds
        (payment_id, amount, reason, status)
        VALUES (?, ?, ?, ?)
    ''', (
        payment_id,
        amount,
        reason,
        status
    ))
    connect.commit()
    connect.close()
    return {
        "message": "refund initiated successfully.."}

@app.route('/show_refunds', methods=['GET'])
def show_refunds():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM refunds')
    refunds = cursor.fetchall()
    connect.close()
    return {
        "refunds": refunds}

def logs():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs(
            actor_id INTEGER,
            action VARCHAR,
            entity_type VARCHAR,
            entity_id INTEGER,
            created_at DATETIME
        )
    ''')
    connect.commit()
    connect.close()
    return {
        "message": "Table created successfully"}

@app.route('/audit_logs', methods=['POST'])
def audit_logs():
    actor_id = request.json.get('actor_id')
    action = request.json.get('action')
    entity_type = request.json.get('entity_type')
    entity_id = request.json.get('entity_id')
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    created_at = datetime.now()
    cursor.execute('''
        INSERT INTO audit_logs
        (actor_id, action, entity_type, entity_id, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        actor_id,
        action,
        entity_type,
        entity_id,
        created_at
    ))
    connect.commit()
    connect.close()
    return {
        "message": "audit logs added successfully."}

@app.route('/show_logs', methods=['GET'])
def show_logs():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM audit_logs')
    audit_logs = cursor.fetchall()
    connect.close()
    return {
        "audit_logs": audit_logs
    }

def manage_orderitems():
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items(
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price FLOAT,
            total_price FLOAT
        )
    ''')
    connect.commit()
    connect.close()
    return {"message": "Order items table created successfully"}

@app.route('/add_orderitem', methods=['POST'])
def add_orderitem():
    get = request.json
    order_id = get['order_id']
    product_id = get['product_id']
    quantity = get['quantity']
    connect = sqlite3.connect('ecommerce.db')
    cursor = connect.cursor()
    cursor.execute(
        'SELECT * FROM orders WHERE order_id = ?',
        (order_id,)
    )
    order = cursor.fetchone()
    if order is None:
        connect.close()
        return {"message": "Order does not exist"}
    cursor.execute(
        'SELECT price FROM products WHERE product_id = ?',
        (product_id,)
    )
    product = cursor.fetchone()
    if product is None:
        connect.close()
        return {"message": "Product does not exist"}
    unit_price = product[0]
    total_price = unit_price * quantity
    cursor.execute('''
        INSERT INTO order_items
        (order_id, product_id, quantity, unit_price, total_price)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        order_id,
        product_id,
        quantity,
        unit_price,
        total_price
    ))
    connect.commit()
    connect.close()
    return {
        "message": "Order item added successfully",
        "order_id": order_id,
        "product_id": product_id,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_price": total_price
    }

users()
address()
product()
manage_inventory()
create_cart()
order()
accounts()
wallets()
payment()
ledger()
refund()
logs()
manage_orderitems()

app.run(port=5005)