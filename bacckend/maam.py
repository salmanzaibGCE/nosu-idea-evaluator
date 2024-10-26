from flask import Flask, request, jsonify, session, redirect, url_for
from flask_pymongo import PyMongo
from flask_cors import CORS  # Import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import cohere
import os
import logging
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Flask application
# Initialize Flask app
app = Flask(__name__)


CORS(app, resources={r"/evaluate": {"origins": "http://localhost:8501"}})  # Allow requests from your Streamlit app


# Catch MongoDB URI from environment variables
mongo_ur = os.getenv("mongo_url")
logging.info(f"MongoDB URI: {mongo_ur}")

# Add the MongoDB URI to the app configuration
if mongo_ur:
    app.config['MONGO_URI'] = mongo_ur
else:
    raise ValueError("MONGO_URI not found in environment variables")

# Needed for session management
app.config['SECRET_KEY'] = os.getenv("secjwt_keyy")

# MongoDB setup
mongo = PyMongo(app)

# Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Setup Cohere API
cohere_api = os.getenv("cohere_api_key")
cohere_client = cohere.Client(cohere_api)

# Logging setup
logging.basicConfig(level=logging.INFO)

# User model for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(str(user_data["_id"]), user_data["username"], user_data["email"])
    return None


# User signup route
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]

    # Check if user already exists
    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create new user in MongoDB
    try:
        # Create new user in MongoDB
        user_id = mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        }).inserted_id

        # Log the user in after signup
        user = User(str(user_id), username, email)
        login_user(user)

        return jsonify({"message": "User signed up and logged in successfully"}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred while creating the user."}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    logging.info(f"Received data: {data}")
    email = data["email"].strip()
    password = data["password"]

    #print(f"Attempting to find user with email: '{email}'")  # Debugging line
    user = mongo.db.users.find_one({"email": email})

    # Debugging output
   # print(f"User found: {user}")

    # Check if user exists and password is correct
    if user:
       # print(f"Stored hashed password: {user['password']}")
        #print(f"Provided password: {password}")

        if bcrypt.check_password_hash(user["password"], password):
            user_obj = User(str(user["_id"]), user["username"], user["email"])
            login_user(user_obj)
            
            return jsonify({"message": "Login successful"}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/verify_session", methods=["GET"])
@login_required  # Ensure this route requires login
def verify_session():
    session_cookie = request.cookies.get('session')
    app.logger.info(f"Received session cookie: {session_cookie}")
    return jsonify({"logged_in": True}), 200












# Business idea submission and evaluation route
@app.route("/evaluate", methods=["POST"])
@login_required
def evaluate_idea():
    # Log the received session cookie for debugging
    session_cookie = request.cookies.get('session')
    if session_cookie:
        logging.info(f"Received session cookie: {session_cookie}")
    else:
        logging.warning("No session cookie received")

    logging.info("Received request to evaluate idea")
    data = request.get_json()
    
    if data:
        logging.info(f"Data received: {data}")
        idea = data["idea"]
    else:
        logging.error("No data received!")

    # Validate the idea length
    if len(idea) < 10:
        return jsonify({"error": "Idea must be at least 10 characters long"}), 400

    try:
        # Analyze the business idea using Cohere API
        prompt = f"""#You are an expert business consultant. A student has presented the following business idea: "{idea}."""
        
        response = cohere_client.generate(
            model="command-light",
            prompt=prompt,
            max_tokens=12000,
        )

        feedback = response.generations[0].text.strip()

        # Store the idea and feedback in MongoDB
        mongo.db.ideas.insert_one({
            "user_id": current_user.id,
            "idea": idea,
            "feedback": feedback,
        })

        # Return the feedback to the user
        return jsonify({"feedback": feedback,"idea": idea}), 200

    except Exception as e:
        logging.error(f"Error analyzing business idea: {e}", exc_info=True)
    return jsonify({"error": "Error analyzing business idea"}), 500

  
    



# User logout route
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    
    return jsonify({"message": "Logged out successfully"}), 200


# Test database connection 
@app.route("/test_db", methods=["GET"])
def test_db():
    try:
        # Check if the MongoDB object is initialized correctly
        if mongo is None or mongo.db is None:
            return jsonify({"error": "MongoDB not initialized"}), 500

        # Query users
        users = mongo.db.users.find()  # Assuming you have a 'users' collection
        user_list = []
        for user in users:
            user_list.append({
                "_id": str(user["_id"]),
                "username": user.get("username"),
                "email": user.get("email")
            })
        return jsonify(user_list), 200
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        return jsonify({"error": str(e)}), 500

# Running the Flask application
if __name__ == "__main__":
    app.run(debug=True)