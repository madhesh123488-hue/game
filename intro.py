from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "number_secret"

@app.route("/", methods=["GET", "POST"])
def index():
    if "number" not in session:
        session["number"] = random.randint(1, 50)   # Range 1 to 50
        session["attempts"] = 0
        session["limit"] = 10   # Max attempts = 10

    message = ""
    if request.method == "POST":
        guess = int(request.form["guess"])
        session["attempts"] += 1

        if guess < session["number"]:
            message = "😅 குறைவாக guess பண்ணிட்டீங்க!"
        elif guess > session["number"]:
            message = "😅 அதிகமாக guess பண்ணிட்டீங்க!"
        else:
            message = f"🎉 சரியானது! எண் {session['number']} தான். {session['attempts']} முயற்சியில் கண்டுபிடிச்சீங்க!"
            session.clear()

        if session.get("attempts") >= session.get("limit", 10):
            message = f"💔 Game Over! எண் {session['number']} தான்."
            session.clear()

    return render_template("index.html", message=message)

@app.route("/restart")
def restart():
    session.clear()
    return render_template("index.html", message="🔄 புதிய game ஆரம்பிச்சுட்டீங்க!")

if __name__ == "__main__":
    app.run(debug=True)
