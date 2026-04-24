import os
from io import BytesIO

import pandas as pd
import pdfplumber
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

MAX_FILE_SIZE_MB = 20
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE_MB * 1024 * 1024


def pdf_to_dataframe(pdf_stream: BytesIO) -> pd.DataFrame:
    """Extract tables from each page and merge into one DataFrame."""
    all_tables: list[pd.DataFrame] = []

    with pdfplumber.open(pdf_stream) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            for table in page_tables or []:
                if not table or len(table) < 2:
                    continue

                header = table[0]
                rows = table[1:]
                frame = pd.DataFrame(rows, columns=header)
                all_tables.append(frame)

    if not all_tables:
        raise ValueError("No tables were detected in the PDF.")

    return pd.concat(all_tables, ignore_index=True)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return {"status": "ok"}, 200


@app.post("/convert")
def convert_pdf_to_excel():
    uploaded_file = request.files.get("pdf_file")

    if not uploaded_file or uploaded_file.filename == "":
        return render_template("index.html", error="Please select a PDF file first."), 400

    safe_name = secure_filename(uploaded_file.filename)

    try:
        input_stream = BytesIO(uploaded_file.read())
        dataframe = pdf_to_dataframe(input_stream)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            dataframe.to_excel(writer, index=False, sheet_name="InvoiceData")
        output.seek(0)

        excel_name = f"{safe_name.rsplit('.', 1)[0]}_converted.xlsx"
        return send_file(
            output,
            as_attachment=True,
            download_name=excel_name,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as exc:  # pragma: no cover
        return render_template("index.html", error=f"Conversion failed: {exc}"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=False)
