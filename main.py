import os

from flask import Flask, jsonify, request, send_file
from werkzeug.exceptions import HTTPException
import io
from weasyprint import HTML




app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to the PDF generator app", 200


@app.route('/PDFgenerate', methods=['POST'])
def generate_pdf():
    # Get HTML content from the request body
    html = request.data.decode('utf-8')
    print("Received HTML:", html)  # Debugging: Print the HTML to verify it's correct

    # Ensure HTML is received correctly before proceeding
    if not html.strip():
        return "No HTML content received", 400

    # Create a PDF buffer
    pdf_buffer = io.BytesIO()
    HTML(string=html).write_pdf(pdf_buffer)

    # Reset buffer position to the beginning
    pdf_buffer.seek(0)

    # Send the PDF file back as a response
    pdf_buffer.seek(0)  # Reset buffer position after writing to file
    return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, download_name='output.pdf')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
