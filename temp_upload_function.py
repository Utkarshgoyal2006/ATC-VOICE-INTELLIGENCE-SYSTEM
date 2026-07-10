# @app.route("/upload", methods=["GET", "POST"])
# @login_required
# def upload():

#     if request.method == "POST":

#         if "audio" not in request.files:
#             flash("No file selected")
#             return redirect(request.url)

#         file = request.files["audio"]

#         if file.filename == "":
#             flash("No file selected")
#             return redirect(request.url)

#         if file and allowed_file(file.filename):

#             filename = secure_filename(file.filename)

#             audio_path = os.path.join(
#                 app.config["UPLOAD_FOLDER"],
#                 filename
#             )

#             file.save(audio_path)

#             processed_audio = None
#             clean_audio = None

#             try:

#                 # -------------------------
#                 # Audio Processing
#                 # -------------------------

#                 processed_audio = preprocess_audio(audio_path)

#                 clean_audio = reduce_noise(processed_audio)

#                 # -------------------------
#                 # Whisper Transcription
#                 # -------------------------

#                 result = transcribe_audio(clean_audio) 

#                 print("=" * 50)
#                 print("Whisper Input File:")
#                 print(clean_audio)
#                 print("=" * 50)

#                 transcript_text = result["text"]

#                 transcript_text = correct_atc_text(transcript_text)

#                 transcript_text = convert_numbers_to_words(transcript_text)

#                 segments = result["segments"]

#                 duration = segments[-1]["end"] if segments else 0

#                 stats = calculate_statistics(
#                     transcript_text,
#                     duration
#                 )

#                 # -------------------------
#                 # Flight Detection
#                 # -------------------------

#                 flights = detect_flight_numbers(transcript_text)

#                 flight = flights[0] if flights else None

#                 runway = detect_runway(transcript_text)

#                 # -------------------------
#                 # Save Recording
#                 # -------------------------

#                 recording = Recording(

#                     filename=filename,

#                     flight_number=flight,

#                     runway=runway

#                 )

#                 db.session.add(recording)

#                 db.session.commit()

#                 # -------------------------
#                 # Save Transcript
#                 # -------------------------

#                 transcript = Transcript(

#                     recording_id=recording.id,

#                     transcript=transcript_text

#                 )

#                 db.session.add(transcript)
                
#                 # -------------------------
#                 # Save Timestamped Segments
#                 # -------------------------

#                 for segment in segments:

#                     corrected_segment = correct_atc_text(
#                         segment["text"]
#                     )

#                     corrected_segment = convert_numbers_to_words(
#                         corrected_segment
#                     )

#                     db.session.add(

#                         TranscriptSegment(

#                             recording_id=recording.id,

#                             start_time=segment["start"],

#                             end_time=segment["end"],

#                             text=corrected_segment

#                         )

#                     )

#                 db.session.commit()

#                 # -------------------------
#                 # Debug Output
#                 # -------------------------

#                 print("\nFinal Transcript\n")

#                 print(transcript_text)

#                 print("\nTimestamped Segments\n")

#                 for segment in segments:

#                     corrected_segment = correct_atc_text(
#                         segment["text"]
#                     )

#                     corrected_segment = convert_numbers_to_words(
#                         corrected_segment
#                     )

#                     print(
#                         f"[{segment['start']:.2f} - {segment['end']:.2f}] "
#                         f"{corrected_segment}"
#                     )

#                 flash("File uploaded successfully!")

#                 return redirect(url_for("dashboard"))

#             finally:

#                 # -------------------------
#                 # Delete Temporary Files
#                 # -------------------------

#                 if processed_audio and os.path.exists(processed_audio):
#                     os.remove(processed_audio)

#                 if clean_audio and os.path.exists(clean_audio):
#                     os.remove(clean_audio)

#         flash("Only MP3 and WAV files are allowed.")

#     return render_template("upload.html")
