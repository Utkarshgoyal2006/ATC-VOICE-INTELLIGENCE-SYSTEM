from database.db import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="user")

    def __repr__(self):
        return f"<User {self.username}>"

class Recording(db.Model):

    __tablename__ = "recordings"

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(255), nullable=False)

    upload_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(50),
        default="Uploaded"
    )
    flight_number = db.Column(
    db.String(100),
    nullable=True
    )
    flight_number = db.Column(db.String(20))

    runway = db.Column(db.String(20))

    frequency = db.Column(db.String(20))

    altitude = db.Column(db.String(30))

    emergency = db.Column(
    db.Boolean,
    default=False
    )
    def __repr__(self):
        return f"<Recording {self.filename}>"
    
class Transcript(db.Model):

    __tablename__ = "transcripts"

    id = db.Column(db.Integer, primary_key=True)

    recording_id = db.Column(
        db.Integer,
        db.ForeignKey("recordings.id"),
        nullable=False,
        unique=True
    )

    transcript = db.Column(
        db.Text,
        nullable=False
    )

    recording = db.relationship(
        "Recording",
        backref="transcript",
        uselist=False
    )


class TranscriptSegment(db.Model):

    __tablename__ = "transcript_segments"

    id = db.Column(db.Integer, primary_key=True)

    recording_id = db.Column(
        db.Integer,
        db.ForeignKey("recordings.id"),
        nullable=False
    )

    start_time = db.Column(db.Float)

    end_time = db.Column(db.Float)

    speaker = db.Column(
        db.String(50),
        default="Unknown"
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    recording = db.relationship(
        "Recording",
        backref="segments"
    )

    def __repr__(self):
        return f"<Segment {self.id}>"