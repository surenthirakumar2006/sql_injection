import sqlite3
import re
from flask import Flask, request, render_template, redirect, url_for, session, g

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For demonstration only – do not use in production!
DATABASE = "users.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Function to validate email format
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

@app.route("/", methods=["GET", "POST"])
def login():
    error = None  # Set to None initially, so it doesn't show on first load

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate email format for username
        if not is_valid_email(username):
            error = "Invalid Credentials"
            return render_template("login.html", error=error)

        try:
            cur = get_db().cursor()
            
            # Secure query for username (prevents injection)
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cur.fetchone()
            
            # Vulnerable query for password (allows injection)
            if user:
                query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
                cur.execute(query)
                user = cur.fetchone()
                
                if user:
                    session["user"] = user[1]  # Store username in session
                    return redirect(url_for("home"))
        except Exception:
            pass  # Avoid exposing errors

        error = "Invalid Credentials"  # Show error only after a failed attempt

    return render_template("login.html", error=error)

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", user=session["user"])

if __name__ == "__main__":
    app.run(debug=True)
