from flask import Flask, request, render_template_string
import requests

# Initialize Flask app
app = Flask(__name__)

# Target URL where you want to send login info
TARGET_URL = 'https://clients.hostwinds.com/dologin.php'

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

@app.route('/')
def index():
    # Render the login form
    return render_template_string(HTML_FORM)

@app.route('/login', methods=['POST'])
def login():
    # Extract username and password from the form
    username = request.form['username']
    password = request.form['password']
    
    # Create the login data dictionary
    login_data = {
        'username': username,
        'password': password,
        # This field might vary depending on the website's form
        'action': 'login'  # Replace with correct action if needed
    }

    # Start a session to persist cookies and headers
    with requests.Session() as session:
        # Send POST request to the target login URL
        response = session.post(TARGET_URL, data=login_data)

        # Check if the login attempt was successful (or just return the content for debugging)
        if response.status_code == 200:
            return response.content  # Forward the target page content
        else:
            return "Login failed! Please check your credentials."

if __name__ == '__main__':
    # Run the Flask app on local server
    app.run(debug=True, host='0.0.0.0', port=5000)
