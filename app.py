from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import json

import os

# Get the absolute path of the directory where app.py is located
basedir = os.path.abspath(os.path.dirname(__file__))

from functools import wraps

app = Flask(__name__, 
            static_folder=os.path.join(basedir, 'static'),
            template_folder=os.path.join(basedir, 'templates'))
app.secret_key = "DBMS_PROJECT_SECRET_KEY"

# --- Security Decorator ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            if request.path.startswith('/api/'):
                return jsonify({"error": "Admin access required"}), 401
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# --- MongoDB Configuration ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://danyl:74syaqNd.4PyXfp@cluster0.lchfsrt.mongodb.net/?appName=Cluster0")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["event_portal_db"]
    # Check connection
    client.server_info()
    print(f"✅ Successfully connected to MongoDB: {MONGO_URI}")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
    # In-memory Fallback for Demo (Optional)
    # db = None

# ----------------- Helper Functions -----------------
def serialize(doc):
    if not doc: return None
    doc["_id"] = str(doc["_id"])
    if "date" in doc and isinstance(doc["date"], datetime):
        doc["date"] = doc["date"].strftime("%Y-%m-%d")
    return doc

# ----------------- Routes: Frontend -----------------
@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/event/<event_id>')
def event_details_page(event_id):
    return render_template('event_details.html', event_id=event_id)

@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin.html')

@app.route('/register/<event_id>')
def registration_page(event_id):
    return render_template('register.html', event_id=event_id)

@app.route('/login')
def login_page():
    return render_template('login.html')

# ----------------- API Routes: Events (CRUD) -----------------
@app.route('/api/events', methods=['GET'])
def get_events():
    events = list(db.events.find().sort("date", 1))
    return jsonify([serialize(e) for e in events])

@app.route('/api/events/<event_id>', methods=['GET'])
def get_event(event_id):
    try:
        event = db.events.find_one({"_id": ObjectId(event_id)})
        return jsonify(serialize(event)) if event else (jsonify({"error": "Event not found"}), 404)
    except:
        return jsonify({"error": "Invalid ID"}), 400

@app.route('/api/events', methods=['POST'])
@admin_required
def create_event():
    data = request.json
    # MongoDB Advantage: Flexible Schema
    # We can accept any additional metadata!
    new_event = {
        "name": data.get("name"),
        "club_name": data.get("club_name"),
        "date": datetime.strptime(data.get("date"), "%Y-%m-%d"),
        "time": data.get("time"),
        "location": data.get("location"),
        "description": data.get("description"),
        "total_seats": int(data.get("total_seats", 0)),
        "seats_filled": 0,
        "category": data.get("category"),
        "metadata": data.get("metadata", {}) # This is our flexible part
    }
    result = db.events.insert_one(new_event)
    return jsonify({"message": "Event created", "_id": str(result.inserted_id)}), 201

@app.route('/api/events/<event_id>', methods=['PUT'])
@admin_required
def update_event(event_id):
    data = request.json
    update_fields = {}
    if "name" in data: update_fields["name"] = data["name"]
    if "date" in data: update_fields["date"] = datetime.strptime(data["date"], "%Y-%m-%d")
    # ... other standard fields ...
    if "metadata" in data: update_fields["metadata"] = data["metadata"] # Flexible updates

    db.events.update_one({"_id": ObjectId(event_id)}, {"$set": update_fields})
    return jsonify({"message": "Event updated"})

@app.route('/api/events/<event_id>', methods=['DELETE'])
@admin_required
def delete_event(event_id):
    db.events.delete_one({"_id": ObjectId(event_id)})
    return jsonify({"message": "Event deleted"})

# ----------------- API Routes: Auth & Users -----------------
@app.route('/api/auth/login', methods=['POST'])
def admin_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    # 1. Check Admin Collection
    admin = db.admins.find_one({"email": email, "password": password})
    if admin:
        session['user_id'] = str(admin["_id"])
        session['role'] = "admin"
        return jsonify({"message": "Admin Login Success", "role": "admin"})
        
    # 2. Check Student Collection (Optional: expand if needed)
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/auth/logout')
def logout():
    session.clear()
    return redirect(url_for('home_page'))

# ----------------- API Routes: Registrations (Students Table) -----------------
@app.route('/api/register', methods=['POST'])
def register_student():
    data = request.json
    event_id = data.get("event_id")
    ktu_id = data.get("ktu_id")

    # 1. Verify Event
    event = db.events.find_one({"_id": ObjectId(event_id)})
    if not event: return jsonify({"error": "Event not found"}), 404
    if event["seats_filled"] >= event["total_seats"]:
        return jsonify({"error": "Event is full!"}), 400

    # 2. Prevent duplicate registration
    existing = db.registrations.find_one({"event_id": event_id, "ktu_id": ktu_id})
    if existing: return jsonify({"error": "You are already registered"}), 400

    # 3. MONGODB ADVANTAGE: Update/Create Student Profile (Students Table)
    # This upserts the student record while registering
    db.students.update_one(
        {"ktu_id": ktu_id},
        {"$set": {
            "name": data.get("full_name"),
            "email": data.get("email"),
            "branch": data.get("branch"),
            "year": data.get("year"),
            "last_active": datetime.utcnow()
        }},
        upsert=True
    )

    # 4. Create Registration (Registrations Table)
    reg_doc = {
        "event_id": event_id,
        "ktu_id": ktu_id,
        "status": "registered",
        "timestamp": datetime.utcnow()
    }
    db.registrations.insert_one(reg_doc)

    # 5. Atomic seat increment (Events Table)
    db.events.update_one({"_id": ObjectId(event_id)}, {"$inc": {"seats_filled": 1}})

    return jsonify({"message": "Successfully registered!"}), 201

@app.route('/api/events/<event_id>/registrations', methods=['GET'])
def get_event_registrations(event_id):
    regs = list(db.registrations.find({"event_id": event_id}))
    # Enhance with student names from Students table (manual join for demo)
    for r in regs:
        r["_id"] = str(r["_id"])
        student = db.students.find_one({"ktu_id": r["ktu_id"]})
        r["student_name"] = student["name"] if student else "Unknown"
    return jsonify(regs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
