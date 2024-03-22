import Pyro4
import logging

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
# Get the URI from the server
uri = input("Enter the Pyro URI of the server: ").strip()

# Create a proxy to the server
arithmetic_service = Pyro4.Proxy(uri)

# Ask if user wants to register or login
choice = input("Do you want to register (r) or login (l)? ").strip()

if choice.lower() == 'r':
    # Register a new user
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    print(arithmetic_service.register(username, password))
    logging.info("Registered")
    try:
        auth_result = arithmetic_service.authenticate(username, password)
        if auth_result == "Authenticated successfully":
            logging.info("Authenticated")
        else:
            logging.error("Authentication failed")
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
elif choice.lower() == 'l':
    # Perform authentication
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    try:
        auth_result = arithmetic_service.authenticate(username, password)
        if auth_result == "Authenticated successfully":
            logging.info("Authenticated")
        else:
            logging.error("Authentication failed")
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
else:
    logging.error("Invalid choice")

# Perform operations only if authenticated
if arithmetic_service.is_authenticated():
    try:
        print(arithmetic_service.add(3, 4))
        print(arithmetic_service.subtract(10, 5))
        print(arithmetic_service.multiply(2, 3))
        print(arithmetic_service.divide(10, 2))
        print(arithmetic_service.factorial(5))
    except Exception as e:
        logging.error(f"Error: {e}")
else:
    logging.error("User not authenticated")