# GhLink Compensation Converter Pro

Professional Flask web app for converting GhIPSS / PowerCARD Compensation Details PDF reports into an Excel settlement workbook.

## Features

- Multiple PDF upload
- POS settlement extraction
- Terminal filter for RBGP transactions
- Duplicate removal
- Summary sheet
- File processing log
- Downloadable Excel output
- SQLite processing history
- Ready for Render deployment

## Local run

```bash
pip install -r requirements.txt
python app.py
```

Open: http://localhost:5000

## Render deployment

Use these settings:

```text
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

## GitHub upload

Upload all files and folders in this project root to your GitHub repository.
Do not upload the ZIP file itself.


## Upload Limit

The app supports multiple PDF uploads and enforces a maximum of 60 PDFs per conversion by default. To change it on Render, add an environment variable named `MAX_PDF_FILES`.
