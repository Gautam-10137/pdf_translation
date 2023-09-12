from io import BytesIO
from deep_translator import GoogleTranslator
import PyPDF2
import textwrap
from nltk.tokenize import sent_tokenize

def translate(pdf_content):
    def translate_extracted(Extracted):
        """Wrapper for Google Translate with upload workaround."""
        translate = GoogleTranslator(source='auto', target='hi').translate
        sentences = sent_tokenize(Extracted)
        translated_text = ''
        source_text_chunk = ''
        for sentence in sentences:
            if len(sentence.encode('utf-8')) + len(source_text_chunk.encode('utf-8')) < 5000:
                source_text_chunk += ' ' + sentence
            else:
                translated_text += ' ' + translate(source_text_chunk)
                if len(sentence.encode('utf-8')) < 5000:
                    source_text_chunk = sentence
                else:
                    message = '<<Omitted Word longer than 5000bytes>>'
                    translated_text += ' ' + translate(message)
                    source_text_chunk = ''
        if translate(source_text_chunk) is not None:
            translated_text += ' ' + translate(source_text_chunk)
        return translated_text

    try:
        # Create a PyPDF2 PDF object from the binary data
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
        # Extract text from each page of the PDF
        extracted_text = ""
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            extracted_text += page.extract_text()

        # Translate the extracted text
        translated_text = translate_extracted(extracted_text)

        # Return the translated text
        return translated_text
    except Exception as e:
        return str(e)+"gautam"

# Example usage:
# pdf_content = ...  # Binary PDF content
# translated_text = translate_pdf(pdf_content)
