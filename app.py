from flask import Flask, render_template, request, flash, redirect, url_for
from ai.flight_detector import detect_flights
from ai.audio_processor import preprocess_audio
from flask_login import LoginManager, login_required
from ai.whisper_engine import transcribe_audio
from sqlalchemy import or_
from config import Config
from ai.number_converter import convert_numbers
from database.db import db
from ai.noise_reduction import reduce_noise
from database.models import User ,Recording ,Transcript

from auth.routes import register, login, logout
from flask import request, flash, redirect
import os
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("HF_TOKEN"))


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()

app.add_url_rule("/register", "register", register, methods=["GET", "POST"])

app.add_url_rule("/login", "login", login, methods=["GET", "POST"])

app.add_url_rule("/logout", "logout", logout)


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/dashboard")
@login_required
def dashboard():

    recordings = Recording.query.order_by(
        Recording.upload_date.desc()
    ).all()

    return render_template(
        "dashboard.html",
        recordings=recordings
    )

ALLOWED_EXTENSIONS = {"mp3", "wav"}

def allowed_file(filename):

    return "." in filename and \
        filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/transcript/<int:recording_id>")
@login_required
def view_transcript(recording_id):

    recording = Recording.query.get_or_404(recording_id)

    transcript = Transcript.query.filter_by(
        recording_id=recording.id
    ).first()

    return render_template(
        "transcript.html",
        recording=recording,
        transcript=transcript
    )

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():

    results = []

    if request.method == "POST":

        keyword = request.form["keyword"]

        results = Transcript.query.filter(

            Transcript.transcript.ilike(f"%{keyword}%")

        ).all()
        print("Keyword:", keyword)
        print("Results:", results)

    return render_template(
        "search.html",
        results=results
    )

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == "POST":

        if "audio" not in request.files:
            flash("No file selected")
            return redirect(request.url)

        file = request.files["audio"]

        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            audio_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(audio_path)

            processed_audio = preprocess_audio(audio_path)

            clean_audio = reduce_noise(processed_audio)

            transcript_text, segments = transcribe_audio(clean_audio)
            for segment in segments:

                print(
            f"[{segment['start']:.2f} - {segment['end']:.2f}] "
            f"{segment['text']}"
            )
            flights = detect_flights(transcript_text)
            recording = Recording(
            filename=filename,
            flight_number=", ".join(flights)
            )

            db.session.add(recording)
            db.session.commit()

            transcript = Transcript(
                recording_id=recording.id,
                transcript=transcript_text
            )

            db.session.add(transcript)
            db.session.commit()

            flash("File uploaded successfully!")

            return redirect(url_for("dashboard"))

        flash("Only MP3 and WAV files are allowed.")

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)