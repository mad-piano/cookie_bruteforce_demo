from flask import Flask, request, render_template, redirect, url_for, flash, make_response
import random
import time


app = Flask(__name__)
app.secret_key = "SuperSecretKey"

# Dummy user data for authentication
users = [

    {"username": "Adam", "password": "admin"},
    {"username": "Chris", "password": "root"},
]

valid_sessions = []

#cookie is eaisly bruteforced
def generate_session_id():
    for _ in range(1000000):
        valid_sessions.append(str(random.randint(10000, 99999)))

generate_session_id()

# Choose a specific session ID to be static (manually)
static_session_id = random.choice(valid_sessions)  # Replace with an actual session ID from valid_sessions

# Store login attempts and locked out users for each session ID
login_attempts = {}
locked_users = {}

def is_valid_session_id(session_id):
    return session_id in valid_sessions

@app.route('/')
def index():
    session_id = static_session_id

    response = make_response(render_template('login.html'))
    response.set_cookie('session_id', session_id)

    return response

@app.route('/login', methods=['POST'])
def login():
    session_id = request.cookies.get('session_id')
    username = request.form.get('username')
    password = request.form.get('password')

    login_success = False
    session_validity = False

    # Check if the session ID is valid
    if is_valid_session_id(session_id):
        session_validity = True

    # Check if the user is temporarily locked out based on the session ID
    if session_id in locked_users and locked_users[session_id] >= time.time():
        return "Account temporarily locked. Try again later."

    # Check if the user has exceeded login attempts based on the session ID
    if session_id in login_attempts and login_attempts[session_id] >= 10:
        locked_users[session_id] = time.time() + 3600  # Lock the user out for 1 hour
        return "Account temporarily locked. Try again later."

    for user in users:
        if user['username'] == username and user['password'] == password:
            # Successful login
            login_success = True
        else:
            # Increment login attempts for the session ID
            if session_id in login_attempts:
                login_attempts[session_id] += 1
            else:
                login_attempts[session_id] = 1

    if login_success:
        flash('Login successful!', 'success')
    else:
        flash('Incorrect username or password.', 'error')

    if not session_validity:
        flash('Invalid session', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
