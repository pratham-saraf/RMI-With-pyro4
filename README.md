# Arithmetic Service with Authentication

This is a client-server application that provides an arithmetic service with user authentication. The server is built using Pyro4, and the client can connect to the server, register or log in, and then perform arithmetic operations like addition, subtraction, multiplication, division, and factorial calculation.

## Prerequisites

- Python 3.11
- Pyro4 library
- pymongo library
- bcrypt library
- MongoDB Atlas account (or a local MongoDB instance)

## Setup

1. Clone the repository or copy the `server.py` and `client.py` files to your local machine.

2. Create a virtual environment. You can do this by using the following command in your terminal:
   
```python
python3 -m venv env
```
3. Activate the virtual environment. On Windows, use:
   
```bash
.\env\Scripts\activate
```

On  Unix or MacOS use:

```bash
source env/bin/activate
```

1. Install the required packages using pip:
```bash
pip install -r requirements.txt
```

1. Update the MongoDB connection URI in the `server.py` file with your MongoDB Atlas connection string or local MongoDB instance URI.

```python
uri = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=auth-cluster"
```

## Running the Server

1. Open a terminal and navigate to the directory containing the server.py file.
2. Run the following command to start the server:

```python
python server.py
```

3. The server will print the Pyro URI for clients to connect, e.g., Ready. Object URI = PYRO:obj_b1a3b9a3a7a64e6ba5b9c7a6a5a6a5a6@localhost:51892

## Running the Client

1. Open another terminal and navigate to the directory containing the client.py file.
2. Run the following command and enter the Pyro URI printed by the server when prompted:

```python
python client.py
```

3. You will be asked if you want to register a new user or log in. Enter r for registration or l for login.
4. If registering, provide a username and password when prompted.
5. If logging in, provide your registered username and password.
6. Upon successful authentication, you can perform arithmetic operations like addition, subtraction, multiplication, division, and factorial calculation.

### Notes

1. The server logs information to a server.log file in the same directory.
2. The client logs information to the console.
3. User credentials are stored in a MongoDB database, and passwords are hashed using bcrypt for security.
4. Only authenticated users can perform arithmetic operations.
5. The server handles errors and exceptions gracefully.
