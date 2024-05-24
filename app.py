from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_httpauth import HTTPBasicAuth
from gensim.models import Word2Vec
import os
import csv


app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["UPLOAD_FOLDER"] = "uploads"
model = None
window = 40
min_count = 1
sg = 0
hs = 1
negative = 10
workers = 2
seed = 34

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

@app.route("/tune", methods=["GET", "POST"])
@auth.login_required
def tune_model():
    global window, min_count, sg, hs, negative, workers, seed
    if request.method == "POST":
        window = int(request.form["window"])
        min_count = int(request.form["min_count"])
        sg = int(request.form["sg"])
        hs = int(request.form["hs"])
        negative = int(request.form["negative"])
        workers = int(request.form["workers"])
        seed = int(request.form["seed"])
        flash("Model parameters updated successfully. Do not forget to re-train.", "success")
        return redirect(url_for("index"))
    return render_template("tune_model.html", username=auth.username(), window=window, min_count=min_count, sg=sg, hs=hs, negative=negative, workers=workers, seed=seed)

@app.route("/train/<filename>")  # Ensure this route is correctly defined
@auth.login_required
def train_file(filename):
    global model, window, min_count, sg, hs, negative, workers, seed
    with open(app.config["UPLOAD_FOLDER"]+"/"+filename, 'r') as file:
        reader = csv.reader(file)
        data = [[item.strip() for item in row] for row in reader]
        model = Word2Vec(data, window=window ,min_count=min_count,sg=sg,hs=hs, negative=negative, workers=workers, seed=seed)
        flash(f"Model trained on {filename}", "success")
        return redirect(url_for("index"))


@app.route("/api/alikes")
@auth.login_required
def api_get_alikes():
    if model is None:
        return jsonify({"error": "Model not trained yet. Choose your dataset to train model on."}), 400
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400 
    else:
        related_items = find_related_items(query)
        return jsonify({"related_items": related_items})

def find_related_items(prompt):
    global model
    if prompt not in model.wv:
        return []
    similar_words = model.wv.most_similar(prompt, topn=5)
    # Return only the words, not their similarity scores
    return [word for word, similarity in similar_words]

if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(debug=False)
