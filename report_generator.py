from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report(patient_name, scan_type, disease, confidence):

    file_name = "report.pdf"

    c = canvas.Canvas(file_name, pagesize=letter)

    y = 750

    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, y, "HealNet AI Clinical Report")

    y -= 50
    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Patient Name: {patient_name}")

    y -= 30
    c.drawString(50, y, f"Scan Type: {scan_type}")

    y -= 30
    c.drawString(50, y, f"Primary Screening: {disease}")

    y -= 30
    c.drawString(50, y, f"AI Confidence: {confidence:.2f}%")

    y -= 40
    c.drawString(50, y, "⚠ AI-assisted system. Doctor confirmation required.")

    c.save()