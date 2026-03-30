from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# --- Configuration ---
MONGO_URI = "mongodb+srv://danyl:74syaqNd.4PyXfp@cluster0.lchfsrt.mongodb.net/?appName=Cluster0" 

def seed():
    try:
        client = MongoClient(MONGO_URI)
        db = client["event_portal_db"]
        
        # Clear existing
        db.events.delete_many({})
        db.registrations.delete_many({})
        db.students.delete_many({})
        db.admins.delete_many({})

        # Sample Admin (For Login)
        db.admins.insert_one({
            "email": "admin@mec.in",
            "password": "admin123", # For demo, no hashing
            "name": "Super Admin"
        })

        # Sample Events
        events = [
            {
                "name": "Generative AI Hackathon",
                "club_name": "TinkerHub",
                "date": datetime.now() + timedelta(days=10),
                "time": "09:00 AM",
                "location": "Main Auditorium",
                "description": "A 24-hour hackathon to build amazing things using Generative AI. Teams of 2-4 allowed. Free pizza and swag!",
                "total_seats": 50,
                "seats_filled": 12,
                "category": "Hackathon",
                "metadata": {
                    "team_size": "2-4",
                    "laptop_required": True,
                    "prizes": "$1000 Cash Prize + Internships"
                }
            },
            {
                "name": "Full Stack Mastery Workshop",
                "club_name": "IEEE CS",
                "date": datetime.now() + timedelta(days=5),
                "time": "10:30 AM",
                "location": "IT Lab 1",
                "description": "Learn how to build end-to-end web applications using Flask and MongoDB. Perfect for beginners entering the world of web development.",
                "total_seats": 30,
                "seats_filled": 28,
                "category": "Workshop",
                "metadata": {
                    "prerequisites": "Basic Python knowledge",
                    "certification": "IEEE Participation Certificate",
                    "guest_speaker": "Sarah Jenkins (Senior Dev @ Google)"
                }
            },
            {
                "name": "MEC Startup Summit 2026",
                "club_name": "IEDC MEC",
                "date": datetime.now() + timedelta(days=20),
                "time": "02:00 PM",
                "location": "Seminar Hall",
                "description": "Bringing together founders, investors and students for an afternoon of networking and insightful sessions about startup culture.",
                "total_seats": 200,
                "seats_filled": 45,
                "category": "Seminar",
                "metadata": {
                    "networking_session": True,
                    "lunch_included": False,
                    "speaker": "John Doe (Founder of TechX)"
                }
            },
            {
                "name": "Cyber Security Bootcamp",
                "club_name": "ACM Student Chapter",
                "date": datetime.now() + timedelta(days=3),
                "time": "09:00 AM",
                "location": "Online (Zoom)",
                "description": "Deep dive into ethical hacking, network security and modern defense strategies with hands-on labs.",
                "total_seats": 100,
                "seats_filled": 98,
                "category": "Workshop",
                "metadata": {
                    "platform": "Zoom",
                    "recording_available": True,
                    "difficulty": "Intermediate"
                }
            }
        ]

        # In MongoDB, we can insert the raw list of dictionaries
        db.events.insert_many(events)
        print("Successfully seeded 4 events into MongoDB.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        print("Make sure MongoDB is running on localhost:27017")

if __name__ == "__main__":
    seed()
