from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os

# Flask app setup
app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
app.config["SECRET_KEY"] = "your_secret_key"

# Database and authentication setup
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirect to login if not authenticated

# ------------------ User Model ------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)  # Store last login time

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ Routes ------------------

@app.route("/")
def home():
    return render_template("index.html")  # Home page

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)  # Keep user logged in
            user.last_login = datetime.now()  # Update last login timestamp
            db.session.commit()  # Ensure commit after updating timestamp

            flash(f"Welcome, {user.username}! Login successful.", "success")
            return redirect(url_for("dashboard.html"))  # Redirect to dashboard
        else:
            flash("Invalid username or password!", "danger")

    return render_template("login.html")  # Corrected login page

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "warning")
            return redirect(url_for("signup"))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()  # Ensure data is saved

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

# Ensure direct access to /dashboard.html redirects correctly
@app.route("/dashboard.html")
@login_required
def dashboard_html():
    return redirect(url_for("dashboard"))

# ------------------ Admin Panel Route ------------------
@app.route("/admin")
@login_required  # Restrict access to logged-in users only
def admin():
    return render_template("admin.html", user=current_user)

# Ensure direct access to /admin.html redirects correctly
@app.route("/admin.html")
@login_required
def admin_html():
    return redirect(url_for("admin"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# ------------------ Run Flask App ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure database is created before running
    app.run(debug=True)
