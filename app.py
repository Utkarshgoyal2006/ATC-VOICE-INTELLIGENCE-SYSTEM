from flask import Flask, render_template, request, flash, redirect, url_for


from ai.statistics import calculate_statistics

from flask import send_from_directory

from ai.flight_detector import detect_flights

from ai.number_to_words import convert_numbers_to_words

from ai.audio_processor import preprocess_audio

from flask_login import LoginManager, login_required

from ai.whisper_engine import transcribe_audio

from ai.atc_corrector import correct_atc_text

from flask import send_file
import tempfile

from sqlalchemy import or_

from config import Config

from reportlab.platypus import SimpleDocTemplate, Paragraph

from reportlab.lib.styles import getSampleStyleSheet

from flask import send_file
import tempfile


from ai.number_converter import convert_numbers

from flask import send_from_directory

from database.db import db
from ai.noise_reduction import reduce_noise

from database.models import (
    User,
    Recording,
    Transcript,
    TranscriptSegment
)
from ai.regex_detector import detect_flight_numbers
from auth.routes import register, login, logout
from flask import request, flash, redirect

import os

from werkzeug.utils import secure_filename

from dotenv import load_dotenv

from ai.regex_detector import detect_runway
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

@app.route("/recording/<int:recording_id>")
@login_required
def recording_details(recording_id):

    recording = Recording.query.get_or_404(recording_id)

    transcript = Transcript.query.filter_by(
        recording_id=recording.id
    ).first()

    segments = TranscriptSegment.query.filter_by(
        recording_id=recording.id
    ).order_by(
        TranscriptSegment.start_time
    ).all()

    if segments:

        duration = segments[-1].end_time

        stats = calculate_statistics(
            transcript.transcript,
            duration
        )

    else:

        stats = None

    return render_template(

        "recording_details.html",

        recording=recording,

        transcript=transcript,

        segments=segments,

        stats=stats

    )
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

@app.route("/download/<int:recording_id>")
@login_required
def download_transcript(recording_id):

    recording = Recording.query.get_or_404(recording_id)

    transcript = Transcript.query.filter_by(
        recording_id=recording.id
    ).first_or_404()

    temp_pdf = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    pdf = SimpleDocTemplate(temp_pdf.name)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b><font size=18>ATC Voice Intelligence System</font></b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph("<br/><br/>", styles["Normal"])
    )

    story.append(
        Paragraph(
            f"<b>Recording :</b> {recording.filename}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Flight :</b> {recording.flight_number or 'Not Detected'}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Runway :</b> {recording.runway or '-'}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Status :</b> {recording.status}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Date :</b> {recording.upload_date.strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph("<br/><br/>", styles["Normal"])
    )

    story.append(
        Paragraph(
            "<b>Transcript</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            transcript.transcript.replace("\n", "<br/>"),
            styles["Normal"]
        )
    )

    pdf.build(story)

    return send_file(
        temp_pdf.name,
        as_attachment=True,
        download_name=f"{recording.filename}_Report.pdf",
        mimetype="application/pdf"
    )
@app.route("/delete/<int:recording_id>", methods=["POST"])
@login_required
def delete_recording(recording_id):

    recording = Recording.query.get_or_404(recording_id)

    transcript = Transcript.query.filter_by(
        recording_id=recording.id
    ).first()

    segments = TranscriptSegment.query.filter_by(
        recording_id=recording.id
    ).all()

    # Delete transcript segments
    for segment in segments:
        db.session.delete(segment)

    # Delete transcript
    if transcript:
        db.session.delete(transcript)

    # Delete audio file
    audio_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        recording.filename
    )

    if os.path.exists(audio_path):
        os.remove(audio_path)

    db.session.delete(recording)

    db.session.commit()

    flash("Recording deleted successfully.")

    return redirect(url_for("dashboard"))


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

            processed_audio = None
            clean_audio = None

            try:

                # -------------------------
                # Audio Processing
                # -------------------------

                processed_audio = preprocess_audio(audio_path)

                clean_audio = reduce_noise(processed_audio)

                # -------------------------
                # Whisper Transcription
                # -------------------------

                result = transcribe_audio(clean_audio) 

                print("=" * 50)
                print("Whisper Input File:")
                print(clean_audio)
                print("=" * 50)

                transcript_text = result["text"]

                transcript_text = correct_atc_text(transcript_text)

                transcript_text = convert_numbers_to_words(transcript_text)

                segments = result["segments"]

                duration = segments[-1]["end"] if segments else 0

                stats = calculate_statistics(
                    transcript_text,
                    duration
                )

                # -------------------------
                # Flight Detection
                # -------------------------

                flights = detect_flight_numbers(transcript_text)

                flight = flights[0] if flights else None

                runway = detect_runway(transcript_text)

                # -------------------------
                # Save Recording
                # -------------------------

                recording = Recording(

                    filename=filename,

                    flight_number=flight,

                    runway=runway

                )

                db.session.add(recording)

                db.session.commit()

                # -------------------------
                # Save Transcript
                # -------------------------

                transcript = Transcript(

                    recording_id=recording.id,

                    transcript=transcript_text

                )

                db.session.add(transcript)

                # -------------------------
                # Save Timestamped Segments
                # -------------------------

                for segment in segments:

                    corrected_segment = correct_atc_text(
                        segment["text"]
                    )

                    corrected_segment = convert_numbers_to_words(
                        corrected_segment
                    )

                    db.session.add(

                        TranscriptSegment(

                            recording_id=recording.id,

                            start_time=segment["start"],

                            end_time=segment["end"],

                            text=corrected_segment

                        )

                    )

                db.session.commit()

                # -------------------------
                # Debug Output
                # -------------------------

                print("\nFinal Transcript\n")

                print(transcript_text)

                print("\nTimestamped Segments\n")

                for segment in segments:

                    corrected_segment = correct_atc_text(
                        segment["text"]
                    )

                    corrected_segment = convert_numbers_to_words(
                        corrected_segment
                    )

                    print(
                        f"[{segment['start']:.2f} - {segment['end']:.2f}] "
                        f"{corrected_segment}"
                    )

                flash("File uploaded successfully!")

                return redirect(url_for("dashboard"))

            finally:

                # -------------------------
                # Delete Temporary Files
                # -------------------------

                if processed_audio and os.path.exists(processed_audio):
                    os.remove(processed_audio)

                if clean_audio and os.path.exists(clean_audio):
                    os.remove(clean_audio)

        flash("Only MP3 and WAV files are allowed.")

    return render_template("upload.html")

@app.route("/audio/<filename>")
@login_required
def play_audio(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )
if __name__ == "__main__":
    app.run(debug=True)