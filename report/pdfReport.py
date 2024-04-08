from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
def generate_pdf_report(imageToPredict, result):
    pdf_filename = os.path.join('uploads', 'report.pdf')
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    title_style = styles['Title']
    
    # Add content to the PDF
    content = []
    content.append(Paragraph("Diabetic Retinopathy Diagnosis Report", title_style))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Uploaded Image:", normal_style))
    content.append(Image(imageToPredict, width=400, height=300))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Diagnosis Result:", normal_style))
    content.append(Paragraph(result, normal_style))

    # Build the PDF
    doc.build(content)
    return pdf_filename