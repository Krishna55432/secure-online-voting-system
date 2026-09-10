from flask import Flask, render_template, request, redirect
import sqlite3
import random
from database import init_db
from blockchain import Blockchain

app = Flask(__name__)
init_db()

# Initialize blockchain
blockchain = Blockchain()

# Temporary storage for OTP
current_otp = None
current_user = None


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    global current_otp, current_user

    if request.method == "POST":
        voter_id = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("votes.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM voters WHERE voter_id=? AND password=?",
            (voter_id, password)
        )

        voter = cursor.fetchone()
        conn.close()

        if voter is None:
            return render_template("invalid_login.html")

        current_otp = str(random.randint(1000, 9999))
        current_user = voter_id

        print(f"[DEBUG] OTP for {voter_id}: {current_otp}")

        return render_template("otp.html")

    return render_template("login.html")


# ---------------- OTP VERIFY ----------------
@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    global current_otp, current_user

    user_otp = request.form["otp"]

    if user_otp == current_otp:
        return redirect(f"/vote/{current_user}")
    else:
        return render_template("invalid_otp.html")


# ---------------- VOTING ----------------
@app.route("/vote/<voter_id>", methods=["GET", "POST"])
def vote(voter_id):
    conn = sqlite3.connect("votes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, voted FROM voters WHERE voter_id=?", (voter_id,))
    voter = cursor.fetchone()

    if voter is None:
        conn.close()
        return "Invalid voter"

    name, voted = voter

    if voted:
        conn.close()
        return render_template("already.html")

    if request.method == "POST":
        candidate = request.form["candidate"]

        # Blockchain
        blockchain.add_block({
            "voter": voter_id,
            "vote": candidate
        })

        # Database update
        cursor.execute("UPDATE results SET votes = votes + 1 WHERE candidate=?", (candidate,))
        cursor.execute("UPDATE voters SET voted = 1 WHERE voter_id=?", (voter_id,))

        conn.commit()
        conn.close()

        return render_template("success.html")

    conn.close()
    return render_template("vote.html", username=name)


# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    conn = sqlite3.connect("votes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM voters")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM voters WHERE voted=1")
    total_votes = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM results")
    results = cursor.fetchall()

    conn.close()

    return render_template("admin.html",
                           users=total_users,
                           votes=total_votes,
                           results=results)


# ---------------- RESULT ----------------
@app.route("/result")
def result():
    conn = sqlite3.connect("votes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM results")
    data = cursor.fetchall()

    conn.close()

    total = sum([x[1] for x in data])
    percentages = [(c, v, (v/total)*100 if total else 0) for c, v in data]

    return render_template("result.html", data=percentages)


# ---------------- BLOCKCHAIN VIEW ----------------
@app.route("/chain")
def view_chain():
    valid, bad_block, stored, calculated = blockchain.is_valid()

    if valid:
        status = "✅ Blockchain Valid"
    else:
        status = f"❌ Data Tampered at Block {bad_block}"

    return render_template(
        "chain.html",
        chain=blockchain.chain,
        status=status,
        bad_block=bad_block,
        stored=stored,
        calculated=calculated
    )
@app.route("/attack")
def attack():
    blockchain.simulate_attack()
    return "⚠️ Attack simulated! Check blockchain"


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)