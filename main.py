import google.generativeai as genai
from flask import Flask, request, jsonify, send_file
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

# Initialize Flask app
app = Flask(__name__)

GOOGLE_API_KEY = "AIzaSyB7rmrMrhCUgVQjJly7fzYv9ZplZFEmrWI"
genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/summary')
def summary():
    try:
        # Read the transcript
        with open("output.txt") as f:
            content = f.read()
        
        # Create prompt
        prompt = f"Give me the summary in 300 words of the transcript: {content}"
        
        # Generate summary
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        
        # Create PDF
        pdf_path = "summary.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create story (content) for PDF
        story = [
            Paragraph("Transcript Summary", styles['Title']),
            Paragraph(response.text, styles['Normal'])
        ]
        
        # Build PDF
        doc.build(story)
        
        # Return PDF file
        return send_file(pdf_path, as_attachment=True, download_name='summary.pdf')
    
    except Exception as e:
        # Return an error response if something goes wrong
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)

