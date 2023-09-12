from flask import Flask, request, jsonify, send_file, make_response
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from translation_functions import translate
from reportlab.lib.styles import getSampleStyleSheet
import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('HindiFont', 'Hind-Regular.ttf'))

app = Flask(__name__)
@app.route("/translate-pdf", methods=["POST"])
def translate_pdf_route():
    try:
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            # Read the file content
            pdf_content = uploaded_file.read()
            
            # Perform translation using your function and pass the content
            translated_text = translate(pdf_content)  # Call the translation function
           
            # Create a PDF from the translated text
            pdf_stream = BytesIO()
            doc = SimpleDocTemplate(pdf_stream, pagesize=letter)
            styles = getSampleStyleSheet()
            style = styles["Normal"]
            style.fontName = 'HindiFont'
            translated_paragraph = Paragraph(translated_text, style)
            story = [translated_paragraph]
            doc.build(story)
            
            # Set appropriate headers for PDF file
            response = make_response(pdf_stream.getvalue())
            response.headers["Content-Disposition"] = "attachment; filename=translated.pdf"
            response.headers["Content-Type"] = "application/pdf"
            
            return response
        else:
            return jsonify({"error": "No file provided."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
