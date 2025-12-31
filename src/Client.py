from flask import Flask, render_template, redirect, url_for, request, flash
from Server import Server
from Crypto.Hash import MD5, SHA256
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages
server = Server()
global index
index = 1


def hash_password(password: str, algorithm: str = "SHA256") -> str:
    """
    Hashes a password using the specified algorithm.

    Args:
        password (str): The password to be hashed.
        algorithm (str): The hashing algorithm to use ('SHA256' or 'MD5').

    Returns:
        str: The hashed password in hexadecimal format.
    """

    password_bytes = bytes(password, 'utf-8')

    if algorithm.upper() == "SHA256":
        hash_obj = SHA256.new(password_bytes)
    elif algorithm.upper() == "MD5":
        hash_obj = MD5.new(password_bytes)
    else:
        raise ValueError("Unsupported algorithm! Choose 'SHA256' or 'MD5'.")

    return hash_obj.hexdigest()

def hash_otp(seed: str, n: int = 100) -> list:
    """
    Generates a chain of OTPs (One-Time Passwords) using SHA256.

    Args:
        seed (str): The initial seed for the OTP chain.
        n (int): The number of OTPs to generate.

    Returns:
        list: A list of OTPs in reverse order.
    """
    # Start with the raw bytes of the seed
    chain = []
    current_hash = bytes(seed, 'utf-8')

    for index1 in range(n):
        # Hash the current hash value (still in raw byte form)
        hash_obj = SHA256.new(current_hash)
        current_hash = hash_obj.digest()
        chain.append(current_hash.hex())  # Hex string format
    last_otp_utf8 = current_hash.hex()
    chain[-1] = last_otp_utf8
    return chain[::-1]

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles the user registration process.

    This function is mapped to the '/register' route and supports both GET and POST methods.
    When accessed via GET, it renders the registration form.
    When accessed via POST, it processes the form data to register a new user.

    POST:
        - Extracts 'username' and 'password' from the form data.
        - Validates the 'username' to ensure it only contains letters.
        - Validates the 'password' to ensure it is longer than 6 characters.
        - Hashes the password using the specified hashing algorithm.
        - Generates a chain of OTPs (One-Time Passwords) using the hashed password.
        - Attempts to register the user with the server using the username, hashed password, and the first OTP.
        - If registration is successful, flashes a success message and redirects to the login page.
        - If registration fails (e.g., username already exists), flashes an error message.

    Returns:
        - Renders the registration form template ('register.html') with appropriate flash messages.
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not re.match("^[A-Za-z]+$", username):
            flash("Username should only contain letters.")
            return render_template('register.html')
        if len(password) <= 6:
            flash("Password must be longer than 6 characters.")
            return render_template('register.html')

        hashed_password = hash_password(password)  # Password hashed using raw bytes
        otp_chain = hash_otp(password,int(server.otp_mod+1))  # OTP chain generated with raw bytes
        result = server.register_user(username, hashed_password, otp_chain[0])

        if result:
            flash("User registered successfully.")
            return redirect(url_for('login'))
        flash("Username already exists.")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the user login process.

    This function is mapped to the '/login' route and supports both GET and POST methods.
    When accessed via GET, it renders the login form.
    When accessed via POST, it processes the form data to log in the user.

    POST:
        - Extracts 'username' and 'password' from the form data.
        - Hashes the password using the specified hashing algorithm.
        - Verifies the username and hashed password with the server.
        - If verification is successful:
            - Retrieves the OTP counter for the user.
            - Generates a chain of OTPs (One-Time Passwords) using the hashed password.
            - Validates the OTP token with the server.
            - If OTP validation is successful, flashes a success message and redirects to the welcome page.
            - If OTP validation fails, flashes an error message.
        - If verification fails, flashes an error message.

    Returns:
        - Renders the login form template ('login.html') with appropriate flash messages.
    """


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        if server.verify_login(username, hashed_password):
            try:

                otp_chain = hash_otp(password,int(server.otp_mod+1))

                global index
                if (index % (server.otp_mod + 1) == 0):
                    index = 1
                otp_token_index = index

                otp_token = otp_chain[otp_token_index]

                if server.validate_otp(username, otp_token):
                    flash("Login successful.")

                    index+=1
                    return redirect(url_for('welcome', username=username))
                flash("OTP verification failed.")
            except Exception as e:
                raise(e)
                flash(f"An error occurred: {str(e)}")
        else:
            flash("Invalid username or password.")
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    """
    Renders the welcome page.

    This function is mapped to the '/welcome' route and renders the 'welcome.html' template.

    Returns:
        - Renders the welcome page template ('welcome.html').
    """

    return render_template('welcome.html')

@app.route('/')
def main_screen():
    """
    Redirects the user to the login page.

    This function is mapped to the root route ('/') and redirects the user to the '/login' route.

    Returns:
        - A redirect response to the login page.
    """

    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
