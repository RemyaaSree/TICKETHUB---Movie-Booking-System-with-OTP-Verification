import random
import time
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

# Store OTPs in memory (in a real app, this would be in a database)
otp_store = {}

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def format_phone_number(phone_number):
    """Format phone number to standard format"""
    # Remove any spaces or special characters
    phone = ''.join(filter(str.isdigit, phone_number))
    
    # If number starts with +91 or 91, remove it
    if phone.startswith('91') and len(phone) == 12:
        phone = phone[2:]
    
    # Ensure number is 10 digits
    if len(phone) != 10:
        raise ValueError("Phone number must be 10 digits")
    
    return phone

def send_otp(phone_number, otp):
    """Mock function to simulate sending OTP"""
    try:
        # Format the phone number
        formatted_phone = format_phone_number(phone_number)
        
        # Store OTP with timestamp
        otp_store[formatted_phone] = {
            'otp': otp,
            'timestamp': time.time(),
            'attempts': 0
        }
        
        # In a real app, this would send an SMS
        # For now, we'll just print it to the console
        print(f"\n{'='*50}")
        print(f"OTP for {formatted_phone}: {otp}")
        print(f"{'='*50}\n")
        return True
    except Exception as e:
        print(f"Error in mock OTP system: {str(e)}")
        return False

def verify_otp(phone_number, otp):
    """Verify the OTP for a phone number"""
    formatted_phone = format_phone_number(phone_number)
    
    # Check if OTP exists and is not expired
    if formatted_phone in otp_store:
        stored_data = otp_store[formatted_phone]
        
        # Check if OTP is expired (5 minutes)
        if time.time() - stored_data['timestamp'] > 300:
            print(f"OTP expired for {formatted_phone}")
            return False
        
        # Check if too many attempts
        if stored_data['attempts'] >= 3:
            print(f"Too many attempts for {formatted_phone}")
            return False
        
        # Increment attempts
        stored_data['attempts'] += 1
        
        # Check if OTP matches
        if stored_data['otp'] == otp:
            # Remove OTP after successful verification
            del otp_store[formatted_phone]
            return True
    
    return False

def generate_pdf_receipt(user_info, movie_info, seats, payment_info, ticket_amount, food_total, final_amount):
    """Generate a PDF receipt for the booking"""
    # Create a BytesIO buffer to store the PDF
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Create the content
    content = []
    
    # Title
    content.append(Paragraph("🎬 MOVIE TICKET RECEIPT", title_style))
    content.append(Spacer(1, 20))
    
    # Customer Information
    content.append(Paragraph("📱 CUSTOMER INFORMATION", styles['Heading2']))
    customer_data = [
        ["Name:", user_info['name']],
        ["Age:", str(user_info['age'])],
        ["Phone:", user_info['phone']]
    ]
    customer_table = Table(customer_data, colWidths=[2*inch, 4*inch])
    customer_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(customer_table)
    content.append(Spacer(1, 20))
    
    # Movie Information
    content.append(Paragraph("🎥 MOVIE INFORMATION", styles['Heading2']))
    movie_data = [
        ["Movie:", movie_info['title']],
        ["Language:", movie_info['language']],
        ["Show Time:", movie_info['show_time']],
        ["Date:", time.strftime('%Y-%m-%d')]
    ]
    movie_table = Table(movie_data, colWidths=[2*inch, 4*inch])
    movie_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(movie_table)
    content.append(Spacer(1, 20))
    
    def get_available_offers(show_time, user_info):
        """
        Mock function to get available offers based on show time and user info.
        Returns a list of offers, each offer is a dict with 'discount' as decimal fraction.
        Example: [{'discount': 0.1}, {'discount': 0.05}]
    """
        # For simplicity, let's say if show time is evening, 10% discount; else 5%
        if "18:" in show_time or "19:" in show_time or "20:" in show_time:
            return [{'discount': 0.10}]
        else:
            return [{'discount': 0.05}]

    def calculate_discount(offers):
        """
        Calculate the maximum discount from the list of offers.
        """
        if not offers:
            return 0.0
        return max(offer.get('discount', 0) for offer in offers)

    # Booking Details
    content.append(Paragraph("🎫 BOOKING DETAILS", styles['Heading2']))
    booking_data = [
        ["Number of Tickets:", str(len(seats))],
        ["Seats:", ', '.join(seats)],
        ["Base Ticket Amount:", f"₹{ticket_amount}"],
        ["Ticket Discount:", f"{calculate_discount(get_available_offers(movie_info['show_time'], user_info))*100:.0f}%"],
        ["Discounted Ticket Amount:", f"₹{ticket_amount}"]
    ]
    booking_table = Table(booking_data, colWidths=[2*inch, 4*inch])
    booking_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(booking_table)
    content.append(Spacer(1, 20))
    
    # Food & Beverages Details
    if food_total > 0:
        content.append(Paragraph("🍿 FOOD & BEVERAGES DETAILS", styles['Heading2']))
        food_data = [
            ["Food & Beverages Amount:", f"₹{food_total}"]
        ]
        food_table = Table(food_data, colWidths=[2*inch, 4*inch])
        food_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        content.append(food_table)
        content.append(Spacer(1, 20))
    
    # Payment Information
    content.append(Paragraph("💳 PAYMENT INFORMATION", styles['Heading2']))
    payment_data = [
        ["Payment Method:", payment_info['method']],
        ["Transaction ID:", payment_info['transaction_id']],
        ["Payment Status:", "Successful"],
        ["Final Amount:", f"₹{final_amount}"]
    ]
    payment_table = Table(payment_data, colWidths=[2*inch, 4*inch])
    payment_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(payment_table)
    content.append(Spacer(1, 20))
    
    # Important Information
    content.append(Paragraph("📝 IMPORTANT INFORMATION", styles['Heading2']))
    important_info = [
        "• Please arrive at least 30 minutes before the show time",
        "• Keep this receipt for entry",
        "• No refunds or exchanges allowed",
        "• Food and beverages will be available at the counter"
    ]
    for info in important_info:
        content.append(Paragraph(info, styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Thank you message
    content.append(Paragraph("🎉 Thank you for booking with us!", styles['Heading2']))
    content.append(Paragraph("Enjoy your movie! 🍿", styles['Normal']))
    
    # Build the PDF
    doc.build(content)
    
    # Get the value of the BytesIO buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf 