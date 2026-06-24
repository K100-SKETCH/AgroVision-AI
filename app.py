from flask import Flask, render_template, request, send_file, Response

import csv
import os
import time
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
import psutil

from reportlab.platypus import (
SimpleDocTemplate,
Paragraph,
Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from predict import predict_disease
from disease_info import DISEASE_INFO

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

LAST_REPORT = {}

# ==================================================

# DATABASE

# ==================================================


def init_db():
    print("DATABASE INITIALIZED", flush=True)

    conn = sqlite3.connect("agrovision.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT,
            confidence REAL,
            image_path TEXT,
            analysis_time TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()

# ==================================================

# HOME PAGE

# ==================================================

@app.route("/")
def home():
    print("HOME PAGE OPENED", flush=True)

    return render_template(
        "index.html"
    )

# ==================================================

# MEMORY CHECK

# ==================================================

@app.route("/memory")
def memory():

    process = psutil.Process()

    return {
        "memory_mb":
        round(
            process.memory_info().rss / 1024 / 1024,
            2
        )
    }


# ==================================================

# IMAGE UPLOAD

# ==================================================

@app.route("/upload", methods=["POST"])
def upload():

    global LAST_REPORT

    print("=" * 60, flush=True)
    print("UPLOAD REQUEST RECEIVED", flush=True)

    start_time = time.time()

    try:

        image = request.files.get("leaf_image")

        if not image:
            return "No image uploaded"

        print(
            f"IMAGE RECEIVED: {image.filename}",
            flush=True
        )

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            image.filename
        )

        image.save(filepath)

        print(
            f"IMAGE SAVED: {filepath}",
            flush=True
        )

        print(
            "CALLING PREDICT_DISEASE()",
            flush=True
        )

        disease, confidence, top3_predictions = predict_disease(
            filepath
        )

        print(
            "PREDICTION RETURNED",
            flush=True
        )

        info = DISEASE_INFO.get(
            disease,
            {
                "symptoms": "Information not available",
                "treatment": "Information not available",
                "prevention": "Information not available"
            }
        )

        confidence = round(confidence, 2)

        if confidence >= 90:
            reliability = "High Confidence"

        elif confidence >= 70:
            reliability = "Medium Confidence"

        else:
            reliability = "Low Confidence"

        analysis_time = datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).strftime(
            "%d-%m-%Y %I:%M %p"
        )

        LAST_REPORT = {
            "disease": disease,
            "confidence": confidence,
            "symptoms": info["symptoms"],
            "treatment": info["treatment"],
            "prevention": info["prevention"],
            "analysis_time": analysis_time
        }

        # SAVE TO DATABASE

        conn = sqlite3.connect("agrovision.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO history
            (
                disease,
                confidence,
                image_path,
                analysis_time
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                disease,
                confidence,
                filepath,
                analysis_time
            )
        )

        conn.commit()
        conn.close()

        print(
            f"TOTAL REQUEST TIME: {round(time.time() - start_time, 2)} sec",
            flush=True
        )

        return render_template(
            "result.html",
            disease=disease,
            confidence=confidence,
            reliability=reliability,
            analysis_time=analysis_time,
            image_path=filepath,
            symptoms=info["symptoms"],
            treatment=info["treatment"],
            prevention=info["prevention"],
            top3_predictions=top3_predictions
        )

    except Exception as e:

        print(
            "ERROR IN APP.PY",
            flush=True
        )

        print(
            str(e),
            flush=True
        )

        return f"ERROR: {str(e)}"
# ==================================================

# PDF REPORT

# ==================================================

@app.route("/download-report")
def download_report():

    pdf_file = "AgroVision_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = [

        Paragraph(
            "AgroVision AI Disease Report",
            styles["Title"]
        ),

        Spacer(1, 20),

        Paragraph(
            f"Disease: {LAST_REPORT.get('disease', 'N/A')}",
            styles["Normal"]
        ),

        Paragraph(
            f"Confidence: {LAST_REPORT.get('confidence', 'N/A')}%",
            styles["Normal"]
        ),

        Paragraph(
            f"Date: {LAST_REPORT.get('analysis_time', 'N/A')}",
            styles["Normal"]
        ),

        Spacer(1, 15),

        Paragraph(
            "Symptoms",
            styles["Heading2"]
        ),

        Paragraph(
            LAST_REPORT.get(
                "symptoms",
                "N/A"
            ),
            styles["Normal"]
        ),

        Spacer(1, 10),

        Paragraph(
            "Treatment",
            styles["Heading2"]
        ),

        Paragraph(
            LAST_REPORT.get(
                "treatment",
                "N/A"
            ),
            styles["Normal"]
        ),

        Spacer(1, 10),

        Paragraph(
            "Prevention",
            styles["Heading2"]
        ),

        Paragraph(
            LAST_REPORT.get(
                "prevention",
                "N/A"
            ),
            styles["Normal"]
        )

    ]

    doc.build(content)

    return send_file(
        pdf_file,
        as_attachment=True
    )

# ==================================================

# HISTORY PAGE

# ==================================================

@app.route("/history")
def history():

    conn = sqlite3.connect(
        "agrovision.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            disease,
            confidence,
            image_path,
            analysis_time
        FROM history
        ORDER BY id DESC
        """
    )

    records = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        records=records
    )

@app.route("/download-csv")
def download_csv():

    conn = sqlite3.connect("agrovision.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            disease,
            confidence,
            image_path,
            analysis_time
        FROM history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    def generate():

        yield "Disease,Confidence,Image Path,Analysis Time\n"

        for row in rows:

            yield f"{row[0]},{row[1]},{row[2]},{row[3]}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=agrovision_history.csv"
        }
    )

# ==================================================
# DASHBOARD
# ==================================================
@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect(
        "agrovision.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            disease,
            confidence
        FROM history
        """
    )

    records = cursor.fetchall()

    conn.close()

    total_analyses = len(records)

    healthy_count = 0
    diseased_count = 0

    total_confidence = 0

    disease_stats = {}

    for disease, confidence in records:

        total_confidence += confidence

        # Disease count for pie chart
        if disease in disease_stats:

            disease_stats[disease] += 1

        else:

            disease_stats[disease] = 1

        # Healthy vs Diseased count
        if "healthy" in disease.lower():

            healthy_count += 1

        else:

            diseased_count += 1

    if total_analyses > 0:

        average_confidence = round(
            total_confidence / total_analyses,
            2
        )

    else:

        average_confidence = 0

    chart_labels = list(
        disease_stats.keys()
    )

    chart_values = list(
        disease_stats.values()
    )

    return render_template(
        "dashboard.html",
        total_analyses=total_analyses,
        healthy_count=healthy_count,
        diseased_count=diseased_count,
        average_confidence=average_confidence,
        chart_labels=chart_labels,
        chart_values=chart_values
    )

# ==================================================

# TEST

# ==================================================

@app.route("/test")
def test():
    return "Flask is working"


# ==================================================

# RUN

# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )

