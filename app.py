from flask import Flask, jsonify, render_template, request

from checker import analyze_password


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/analyze")
def analyze():
    if not request.is_json:
        return jsonify({"error": "Expected JSON request."}), 400

    payload = request.get_json(silent=True) or {}
    password = payload.get("password", "")
    if not isinstance(password, str):
        return jsonify({"error": "Password must be a string."}), 400
    if len(password) > 512:
        return jsonify({"error": "Password is too long to analyze in this demo."}), 413

    return jsonify(analyze_password(password))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
