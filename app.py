import os
import uuid
from werkzeug.utils import secure_filename
from flask import Flask, flash, redirect, render_template, request, send_file, url_for

from converter import convert_pdfs
from db import add_job, dashboard_stats, find_job, init_db, recent_jobs

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "storage", "outputs")
ALLOWED_EXTENSIONS = {"pdf"}
MAX_PDF_FILES = int(os.environ.get("MAX_PDF_FILES", "60"))

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")
app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_UPLOAD_MB", "100")) * 1024 * 1024

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
init_db()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html", stats=dashboard_stats(), jobs=recent_jobs(10), max_pdf_files=MAX_PDF_FILES)


@app.route("/convert", methods=["POST"])
def convert():
    files = request.files.getlist("pdf_files")
    valid_files = [f for f in files if f and f.filename and allowed_file(f.filename)]
    if len(valid_files) > MAX_PDF_FILES:
        flash(f"Maximum upload limit is {MAX_PDF_FILES} PDF files per conversion. You selected {len(valid_files)}.", "danger")
        return redirect(url_for("index"))

    if not valid_files:
        flash("Please upload at least one PDF file.", "danger")
        return redirect(url_for("index"))

    job_id = uuid.uuid4().hex[:12]
    job_upload_dir = os.path.join(UPLOAD_DIR, job_id)
    os.makedirs(job_upload_dir, exist_ok=True)

    pdf_paths = []
    original_names = []
    for file in valid_files:
        filename = secure_filename(file.filename)
        original_names.append(filename)
        path = os.path.join(job_upload_dir, filename)
        file.save(path)
        pdf_paths.append(path)

    output_file = f"STAR_OIL_GHLINK_COMPENSATION_{job_id}.xlsx"
    output_path = os.path.join(OUTPUT_DIR, output_file)

    try:
        result = convert_pdfs(pdf_paths, output_path)
        summary = result["summary"]
        status = "OK" if summary["failed_files"] == 0 else "PARTIAL"
        add_job({
            "job_id": job_id,
            "original_files": ", ".join(original_names),
            "output_file": output_file,
            "pdf_count": summary["pdf_count"],
            "row_count": summary["row_count"],
            "duplicate_count": summary["duplicate_count"],
            "total_credit": summary["total_credit"],
            "status": status,
            "error": "",
        })
        return render_template("result.html", job_id=job_id, summary=summary, file_stats=result["file_stats"])
    except Exception as exc:
        add_job({
            "job_id": job_id,
            "original_files": ", ".join(original_names),
            "output_file": output_file,
            "pdf_count": len(pdf_paths),
            "row_count": 0,
            "duplicate_count": 0,
            "total_credit": 0,
            "status": "FAILED",
            "error": str(exc),
        })
        flash(f"Conversion failed: {exc}", "danger")
        return redirect(url_for("index"))


@app.route("/download/<job_id>")
def download(job_id):
    job = find_job(job_id)
    if not job:
        flash("Report not found.", "danger")
        return redirect(url_for("index"))
    output_path = os.path.join(OUTPUT_DIR, job["output_file"])
    if not os.path.exists(output_path):
        flash("Output file is missing on the server.", "danger")
        return redirect(url_for("index"))
    return send_file(output_path, as_attachment=True, download_name=job["output_file"])


@app.route("/history")
def history():
    return render_template("history.html", jobs=recent_jobs(100), stats=dashboard_stats())


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
