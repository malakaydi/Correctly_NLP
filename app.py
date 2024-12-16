from flask import Flask, render_template, request, jsonify, send_file
from english import process_english_text
from arabic import process_arabic_text
from translation import process_translation
import langdetect
import PyPDF2
from fpdf import FPDF
import os
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to process text correction
@app.route('/spell', methods=['POST'])
def process_text():
    text = request.form.get('text', '')
    selected_language = request.form.get('language', 'english')

    detected_lang = langdetect.detect(text)
    
    if (selected_language == 'english' and detected_lang != 'en') or (selected_language == 'arabic' and detected_lang != 'ar'):
        return jsonify({
            'warning_message': "Warning: The detected language does not match the selected language. Please select the correct language.",
            'corrected_text': ""
        })
    else:
        if selected_language == 'english':
            corrected_text = process_english_text(text)
        elif selected_language == 'arabic':
            corrected_text = process_arabic_text(text)
        else:
            corrected_text = "Unsupported language selection."

        return jsonify({
            'corrected_text': corrected_text
        })

# Route for translation
@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()

    print(f"Received data: {data}")

    text = data.get('text', '').strip()
    target_language = data.get('target_language', '').lower()

    if not text:
        print("Error: No text provided")
        return jsonify({"error": "No text provided"}), 400

    if target_language not in ['english', 'arabic']:
        print("Error: Unsupported target language")
        return jsonify({"error": "Unsupported target language"}), 400

    print(f"Translating text: {text} to {target_language}")

    translated_text = process_translation(text, target_language)

    print(f"Translated text: {translated_text}")

    return jsonify({"translated_text": translated_text})

# Route to upload and correct PDF
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file uploaded"}), 400

    file = request.files['pdf']
    if file.filename == '':
        return jsonify({"error": "No PDF file selected"}), 400

    # Save the uploaded PDF temporarily
    pdf_path = os.path.join('uploads', file.filename)
    file.save(pdf_path)

    # Extract text from the PDF
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()

    # Detect the language
    detected_lang = langdetect.detect(text)
    if detected_lang not in ['en', 'ar']:
        os.remove(pdf_path)
        return jsonify({"error": "Unsupported language detected in the PDF"}), 400

    # Process text correction
    if detected_lang == 'en':
        corrected_text = process_english_text(text)
    elif detected_lang == 'ar':
        corrected_text = process_arabic_text(text)

    # Create a corrected PDF
    corrected_pdf_path = os.path.join('uploads', 'corrected_' + file.filename)
    pdf = FPDF()
    pdf.add_page()
    
    if detected_lang == 'en':
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)
    else:  # Arabic
        pdf.add_font('Arial', '', 'arial.ttf', uni=True)
        pdf.set_font('Arial', '', 12)

    # Split the text into lines
    lines = corrected_text.split('\n')
    
    for line in lines:
        if detected_lang == 'ar':
            # Reshape Arabic text
            reshaped_text = arabic_reshaper.reshape(line)
            bidi_text = get_display(reshaped_text)
            pdf.multi_cell(0, 10, bidi_text)
        else:
            pdf.multi_cell(0, 10, line)

    pdf.output(corrected_pdf_path)

    # Remove the original PDF
    os.remove(pdf_path)

    # Send the corrected PDF to the user
    return send_file(corrected_pdf_path, as_attachment=True)

if __name__ == '__main__':
    # Ensure the uploads folder exists
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
