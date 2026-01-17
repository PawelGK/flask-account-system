import pymysql
import bcrypt
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mini_secret_key"

DB_CONFIG = {
    "host": "localhost",
    "user": "miniuser",
    "passwd": "minipass",
    "db": "minidb"
}

def get_db():
    return pymysql.connect(**DB_CONFIG)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT password FROM accounts WHERE username=%s", (username,))
        result = cur.fetchone()
        db.close()

        if not result:
            return render_template("login.html", error="User does not exist")

        if bcrypt.checkpw(password.encode(), result[0].encode()):
            session["user"] = username
            return redirect(url_for("profile"))
        else:
            return render_template("login.html", error="Incorrect password")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "INSERT INTO accounts (username, password, created_at) VALUES (%s, %s, %s)",
                (username, hashed, datetime.now())
            )
            db.commit()
        except:
            db.close()
            return render_template("signup.html", error="Username already taken")

        db.close()
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT username, created_at FROM accounts WHERE username=%s",
        (session["user"],)
    )
    user = cur.fetchone()
    db.close()

    return render_template("profile.html", user=user)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)