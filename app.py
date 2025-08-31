import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def home():
    """Show home screen"""
    return render_template("home.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Show Option for anyone to upload edit and download photos"""
    if request.method == "POST":
        # Handle file upload and editing here
        if 'userPhoto' not in request.files:
            flash("File not supported")
            return redirect(request.url)

        file = request.files["userPhoto"]
        if file:
            # Save the file and perform editing
            filepath = os.path.join("static/uploads", file.filename)
            file.save(filepath)
            return redirect(url_for("edit", fileName=file.filename))
        else:
            flash("No file selected.")
    else:
        return render_template("upload.html")
    
@app.route("/edit", methods=["GET", "POST"])
def edit():
    """Show Option for anyone to edit and download photos"""
    fileName = request.args.get("fileName")
    if request.method == "POST":
        # Handle file editing here
        pass
    else:
        return render_template("edit.html", fileName=fileName)

@app.route("/gallery")
def gallery():
    """If the user is logged, the user can see their saved edit and photos (MAX 1 GB of photos)"""
    return render_template("error.html")

@app.route("/about")
def about():
    """Tell the user about the creator of the application"""
    return render_template("error.html")

@app.route("/login")
def login():
    """Log the user in"""
    return render_template("error.html")

@app.route("/logout")
def logout():
    """Log the user out"""
    return render_template("error.html")

@app.route("/register")
def register():
    """Register a new user"""
    return render_template("error.html")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
