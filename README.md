# EVENT PORTAL - DBMS PROJECT
A modern, minimalist full-stack event management system for students and admins.

## 🎨 Design Philosophy: "Studio Studio"
This portal follows a premium, minimalist "Studio" aesthetic using a custom-curated palette:
- **Paper (#F6F4F1):** Primary background.
- **Stone (#E4DED2):** Surface and UI separation.
- **Coral (#F95C4B):** Primary action color.
- **Black (#000000):** Typography and high-contrast elements.

---

## 📂 Database Architecture (MongoDB)
This project leverages **MongoDB's Flexible Schema** to manage data across **4 Core Collections**:

1. **`events`**: Stores event details, seat capacity, and a dynamic `metadata` field for category-specific data (e.g., Hackathon team sizes vs. Seminar speakers).
2. **`admins`**: Manages management portal credentials and access roles (e.g., `admin@mec.in`).
3. **`students`**: Stores long-term student profiles (KTU ID, branch, name) generated or updated during registrations.
4. **`registrations`**: Acts as a junction collection linking `students` to `events` with timestamps.

### 🌟 The MongoDB Advantage
- **Embedded Metadata**: No `ALTER TABLE` needed. A "Workshop" can store a *Prerequisites* list, while a "Talk" stores *Guest Speaker* info in the same collection.
- **Atomic Bookings**: Uses the `$inc` operator to ensure seat calculations are thread-safe and never over-booked.
- **Schema Evolution**: As the college adds new types of events (e.g., "Tournaments"), the database adapts instantly without downtime.

---

## 🛠️ Tech Stack
- **Backend:** Flask (Python 3.x) + PyMongo
- **Database:** MongoDB Atlas (Cloud)
- **Frontend:** HTML5, Premium CSS3, Vanilla JS
- **API:** RESTful JSON endpoints

## 🚀 Quick Setup
1. Clone the repository.
2. Install dependencies: `pip install flask pymongo dnspython`
3. Configure `MONGO_URI` in `app.py`.
4. Seed the database: `python seed_db.py` (Default Admin: `admin@mec.in` / `admin123`)
5. Run the app: `python app.py`
