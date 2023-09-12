from flask import Flask, request, jsonify, send_file, make_response
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from translation_functions import translate
from reportlab.lib.styles import getSampleStyleSheet
import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('HindiFont', 'Fonts/Hind-Regular.ttf'))
pdfmetrics.registerFont(TTFont('GujaratiFont', 'Fonts/Gujarati.ttf'))
pdfmetrics.registerFont(TTFont('BengaliFont', 'Fonts/Bengali.ttf'))
pdfmetrics.registerFont(TTFont('MarathiFont', 'Fonts/Marathi.ttf'))
pdfmetrics.registerFont(TTFont('TamilFont', 'Fonts/Tamil.ttf'))
pdfmetrics.registerFont(TTFont('TeluguFont', 'Fonts/Telugu.ttf'))

app = Flask(__name__)

# Define a mapping of languages to font names
language_to_font = {
    'hi': 'HindiFont',
    'gu':'GujaratiFont',
    'mr':'MarathiFont',
    'ta':'TamilFont',
    'te':'TeluguFont',
    'bn':'BengaliFont'
}

@app.route("/translate-pdf", methods=["POST"])
def translate_pdf_route():
    try:
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            # Read the file content
            pdf_content = uploaded_file.read()
            
            # Get target languages from user input
            target_languages = request.form.get("target_language")
            if not target_languages:
                return jsonify({"error": "Target languages not provided."}), 400
            target_languages = target_languages.split(',')  # Split into a list
            
            # Perform translation for each target language using your function and pass the content
            translated_texts = translate(pdf_content, target_languages)  # Call the translation function
            
            # Create a PDF for each translated text with the appropriate font
            pdf_streams = {}
            for lang, text in translated_texts.items():
                pdf_stream = BytesIO()
                doc = SimpleDocTemplate(pdf_stream, pagesize=letter)
                styles = getSampleStyleSheet()
                style = styles["Normal"]
                # Set the font based on the language
                if lang in language_to_font:
                    style.fontName = language_to_font[lang]
                translated_paragraph = Paragraph(text, style)
                story = [translated_paragraph]
                doc.build(story)
                pdf_streams[lang] = pdf_stream
            
            # Set appropriate headers for ZIP file
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
