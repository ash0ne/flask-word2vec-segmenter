from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_httpauth import HTTPBasicAuth
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["UPLOAD_FOLDER"] = "uploads"

# Environment variables for user credentials
APP_USER = os.environ.get("APP_USER", "admin")
APP_PASSWORD = os.environ.get("APP_PASSWORD", "adminpass")

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    return username == APP_USER and password == APP_PASSWORD


@app.route("/")
@auth.login_required
def index():
    files = [f for f in os.listdir(app.config["UPLOAD_FOLDER"]) if f.endswith(".csv")]
    return render_template("index.html", username=auth.username(), files=files)


@app.route("/upload", methods=["GET", "POST"])
@auth.login_required
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)
            flash("File successfully uploaded and processed", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid file format. Please upload a .csv file.", "danger")
    return render_template("upload.html", username=auth.username())


@app.route("/delete/<filename>")
@auth.login_required
def delete_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f"File {filename} deleted", "success")
    else:
        flash("File not found", "danger")
    return redirect(url_for("index"))


@app.route("/train/<filename>")  # Ensure this route is correctly defined
@auth.login_required
def train_file(filename):
    # Add your training logic here
    flash(f"Model trained on {filename}", "success")
    return redirect(url_for("index"))


@app.route("/api/substitutes")
@auth.login_required
def api_get_first_file_contents():
    query = request.args.get("query")  # Get the query parameter from the request
    files = [f for f in os.listdir(app.config["UPLOAD_FOLDER"]) if f.endswith(".csv")]
    if files:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], files[0])
        with open(file_path, "r") as file:
            contents = file.read()
        return jsonify({"query": query, "file_contents": contents})
    else:
        return jsonify({"error": "No .csv files found in the uploads directory"})


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(debug=False)
