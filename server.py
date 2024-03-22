import Pyro4
import logging
import threading
from pymongo import MongoClient
import bcrypt

# Setup logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='server.log',
                    filemode='w')

# Connect to MongoDB
uri = "<replace with your mongoDB connection URI>"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client['user_auth_db']
users = db['user_data']

# Define the arithmetic operations
@Pyro4.behavior(instance_mode="session")
class ArithmeticService:
    def __init__(self):
        self._pyroCredentials = None  # Expose _pyroCredentials attribute

    @Pyro4.expose
    def is_authenticated(self):
        return self._pyroCredentials is not None


    @Pyro4.expose
    def register(self, username, password):
        if users.find_one({"username": username}):
            raise ValueError("User already exists")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users.insert_one({"username": username, "password": hashed_password.decode('utf-8')})
        logging.info(f"Registered user: {username}")
        return "User registered successfully"
    
    @Pyro4.expose
    def authenticate(self, username, password):
        user = users.find_one({"username": username})
        if user is None or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            raise ValueError("Authentication failed")
        self._pyroCredentials = (username, password) # Set the credentials upon successful authentication
        return "Authenticated successfully"
            
    @Pyro4.expose
    def add(self, x, y):
        if not self.is_authenticated():
            raise ValueError("User not authenticated")
        return x + y

    @Pyro4.expose
    def subtract(self, x, y):
        if not self.is_authenticated():
            raise ValueError("User not authenticated")
        return x - y

    @Pyro4.expose
    def multiply(self, x, y):
        if not self.is_authenticated():
            raise ValueError("User not authenticated")
        return x * y

    @Pyro4.expose
    def divide(self, x, y):
        if not self.is_authenticated():
            raise ValueError("User not authenticated")
        if y == 0:
            raise ValueError("Division by zero is not allowed")
        return x / y

    @Pyro4.expose
    def factorial(self, n):
        if not self.is_authenticated():
            raise ValueError("User not authenticated")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if n == 0 or n == 1:
            return 1
        return n * self.factorial(n - 1)

# Create a daemon to handle requests
daemon = Pyro4.Daemon()

# Register the service
uri = daemon.register(ArithmeticService)

# Print the URI for clients to connect
print(f"Ready. Object URI = {uri}")
logging.info("Server started")

# Start the daemon
try:
    daemon.requestLoop()
except Exception as e:
    logging.error(f"Error in request loop: {e}")
finally:
    daemon.close()
    logging.info("Shutting down server")