# 🎙️ VHF Communication Recording & Search System using AI

> **An AI-powered Air Traffic Control (ATC) communication search system that converts VHF voice recordings into searchable text using Whisper AI, enabling rapid retrieval of conversations by flight callsign, keywords, and timestamps.**

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Audio%20Processing-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# 📖 Overview

Air Traffic Control (ATC) VHF communications are continuously recorded for operational, safety, and investigation purposes. During an incident or operational review, controllers often need to manually listen through lengthy recordings to locate a specific conversation, which is both time-consuming and inefficient.

This project develops an **AI-powered VHF Communication Recording & Search System** that automatically transcribes recorded ATC communications into searchable text using **OpenAI Whisper**, detects aircraft callsigns, stores transcripts in a database, and enables instant retrieval using keywords or flight numbers.

This project is designed as a practical prototype for **Airport CNS (Communication, Navigation & Surveillance)** applications.

---

# 🚀 Problem Statement

Finding a specific ATC communication from hours of recorded VHF audio is a manual process that requires listening through entire recordings.

### Current Challenges

* Manual searching of long audio recordings
* Time-consuming incident investigations
* No searchable transcript database
* Difficulty locating communications by flight number
* Increased workload during operational reviews

---

# 💡 Proposed Solution

The application automatically:

* Uploads recorded VHF audio
* Converts speech into text using Whisper AI
* Detects aircraft callsigns
* Stores transcripts with timestamps
* Enables keyword-based searching
* Displays matching conversations instantly

---

# ✨ Features

## 🎤 Speech-to-Text Conversion

* AI-powered transcription using OpenAI Whisper
* Supports noisy VHF radio recordings
* Generates readable transcripts

---

## ⏱ Timestamp Generation

Every recognized sentence is associated with its recording timestamp.

| Timestamp | Transcript                               |
| --------- | ---------------------------------------- |
| 10:15:23  | Air India 612, cleared to land Runway 27 |
| 10:15:35  | Wind 260 at 12 knots                     |

---

## ✈ Flight Callsign Detection

Automatically extracts aircraft callsigns using Regular Expressions.

Supported examples:

* AI612
* 6E521
* SG234
* IX194
* VTI903

---

## 🔍 Intelligent Search

Search transcripts using:

* Flight Number
* Runway
* Taxi
* Pushback
* Landing
* Departure
* Hold Position
* Cleared to Land
* Emergency
* Mayday
* Pan Pan

Results include:

* Transcript
* Timestamp
* Recording Name

---

## 📂 Recording Management

* Upload multiple recordings
* Store historical transcripts
* Search across all recordings
* Filter by recording date

---

# 🏗️ System Architecture

```text
                  VHF Audio Recording
                           │
                           ▼
                  Audio Preprocessing
                       (FFmpeg)
                           │
                           ▼
                 Whisper AI Speech-to-Text
                           │
                           ▼
              Flight Callsign Detection
                     (Regex Engine)
                           │
                           ▼
                   SQLite Database
                           │
                           ▼
                Flask Search Interface
                           │
                           ▼
      Search Results with Timestamp & Flight Details
```

---

# 🛠 Technology Stack

| Category              | Technology                  |
| --------------------- | --------------------------- |
| Programming Language  | Python                      |
| AI Speech Recognition | OpenAI Whisper              |
| Web Framework         | Flask                       |
| Database              | SQLite                      |
| Audio Processing      | FFmpeg                      |
| Flight Detection      | Regular Expressions (Regex) |
| Frontend              | HTML, CSS, Bootstrap        |
| IDE                   | Visual Studio Code          |
| Version Control       | Git                         |

---

# 📁 Project Structure

```text
VHF_Communication_Search_System/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── database.py
│   ├── models.py
│   └── atc.db
│
├── modules/
│   ├── transcribe.py
│   ├── regex_detector.py
│   ├── keyword_detector.py
│   ├── audio_converter.py
│   ├── diarization.py          # Future Enhancement
│   └── utils.py
│
├── uploads/
├── transcripts/
│
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── upload.html
│   ├── results.html
│   └── history.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── logs/
    └── application.log
```

---

# ⚙️ Workflow

```text
Upload Audio
      │
      ▼
FFmpeg Audio Conversion
      │
      ▼
Whisper AI Transcription
      │
      ▼
Regex Flight Detection
      │
      ▼
SQLite Database
      │
      ▼
Search Interface
      │
      ▼
Search Results
```

---

# 🗄 Database Schema

## Recording Table

| Field         | Type    |
| ------------- | ------- |
| id            | INTEGER |
| filename      | TEXT    |
| upload_date   | TEXT    |
| transcript    | TEXT    |
| flight_number | TEXT    |

---

## Timestamp Table

| Field        | Type                        |
| ------------ | --------------------------- |
| id           | INTEGER                     |
| recording_id | INTEGER                     |
| start_time   | TEXT                        |
| end_time     | TEXT                        |
| transcript   | TEXT                        |
| speaker      | TEXT *(Future Enhancement)* |

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/VHF_Communication_Search_System.git
```

Move into the project folder

```bash
cd VHF_Communication_Search_System
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

---

# 📋 Software Requirements

* Python 3.11+
* Flask
* OpenAI Whisper
* SQLite
* FFmpeg
* Visual Studio Code

---

# 💻 Hardware Requirements

* Windows / Linux
* 8 GB RAM or higher
* Multi-core Processor
* Internet connection (for installation only)
* Recorded VHF audio files

---

# 📌 Expected Output

### Search Keyword

```
AI612
```

Output

| Timestamp | Transcript                              |
| --------- | --------------------------------------- |
| 10:15:23  | Air India 612 cleared to land Runway 27 |
| 10:22:41  | Air India 612 vacate via Taxiway Alpha  |

---

# 🎯 Objectives

* Convert recorded ATC communications into text
* Generate timestamped transcripts
* Detect aircraft callsigns
* Build a searchable transcript database
* Reduce investigation time
* Improve retrieval of historical ATC communications

---

# 📈 Advantages

* Faster investigation of ATC communications
* Eliminates manual audio searching
* Searchable communication history
* Low-cost implementation using open-source tools
* Modular architecture for future expansion
* Suitable for airport CNS applications

---

# 🔮 Future Enhancements

* 🎙 Real-time transcription
* 👥 Speaker Diarization (ATC vs Pilot)
* 🚨 Emergency phrase detection
* 📊 Communication analytics dashboard
* 📄 Export transcripts to PDF/CSV
* 🌐 Multi-frequency support
* 🤖 AI-generated communication summaries
* ☁ Cloud database integration

---

# 🎓 Learning Outcomes

This project demonstrates practical implementation of:

* Artificial Intelligence
* Speech Recognition
* Audio Processing
* Database Management
* Web Development
* Aviation Communication Analysis
* Python Programming
* Software Engineering

---

# ✈️ Airport CNS Relevance

This project is specifically designed for **Communication, Navigation & Surveillance (CNS)** environments. It assists in indexing and retrieving archived VHF communications for training, operational review, and incident investigation. It processes recorded audio only and does **not** interface with or control live ATC communications.

---

# 👨‍💻 Author

**Utkarsh Goyal**
**Mehul Lashkari**

Electronics & Communication Engineering (ECE)

AI-Based Airport CNS Project

---

## ⭐ If you find this project useful, consider giving it a star on GitHub!
