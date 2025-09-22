from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import json

app = Flask(__name__)

# Datenverzeichnisse
DATA_DIR = Path("data")
LOCATIONS_DIR = DATA_DIR / "locations"
PINS_FILE = DATA_DIR / "pins.json"

DATA_DIR.mkdir(exist_ok=True)
LOCATIONS_DIR.mkdir(exist_ok=True)

# ---------------- ROUTES ---------------- #

@app.route("/")
def index():
    return render_template("index.html")


@app.post("/upload/<location>/<abteil>")
def upload(location, abteil):
    """Upload Floorplan in Standort/Abteil"""
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "no file"}), 400

    dest_dir = LOCATIONS_DIR / location / abteil
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest = dest_dir / file.filename
    file.save(dest)

    # Pfad für JSON speichern
    return jsonify({"url": f"/locations/{location}/{abteil}/{file.filename}"})


@app.get("/locations/<path:filename>")
def serve_location_file(filename):
    """Serve Floorplan files"""
    return send_from_directory(LOCATIONS_DIR, filename)


@app.get("/api/pins")
def get_pins():
    if PINS_FILE.exists():
        return send_from_directory(DATA_DIR, "pins.json")
    return jsonify({"locations": {}})


@app.post("/api/pins")
def save_pins():
    payload = request.get_json(force=True)
    PINS_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
