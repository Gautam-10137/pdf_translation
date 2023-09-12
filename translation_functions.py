from io import BytesIO
from deep_translator import GoogleTranslator
import PyPDF2
import textwrap
from nltk.tokenize import sent_tokenize
import nltk

nltk.download('punkt')

def translate(pdf_content, target_languages):
    def translate_extracted(Extracted, target_language):
        """Wrapper for Google Translate with upload workaround."""
        translate = GoogleTranslator(source='auto', target=target_language).translate
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

        # Translate the extracted text for each target language
        translated_texts = {}
        for target_language in target_languages:
            translated_texts[target_language] = translate_extracted(extracted_text, target_language)

        # Return the translated texts
        return translated_texts
    except Exception as e:
        return str(e) + "gautam"

# Example usage:
# pdf_content = ...  # Binary PDF content
# target_languages = ['hi', 'fr', 'es']  # List of target languages
# translated_texts = translate(pdf_content, target_languages)
