import streamlit as st
import time
from datetime import datetime
import plotly.express as px
import pandas as pd
import os
from utils import generate_otp, send_otp, verify_otp, format_phone_number, generate_pdf_receipt
from config import MOVIES, SEAT_LAYOUT, TICKET_PRICE, PAYMENT_OPTIONS, FOOD_MENU
from features import (
    calculate_seat_price, get_available_offers, calculate_discount,
    get_movie_recommendations, get_seat_availability,
    get_movie_details
)

# File to store booking logs
BOOKING_LOGS_FILE = 'booking_logs.csv'

def load_booking_logs():
    """Load booking logs from CSV file"""
    if os.path.exists(BOOKING_LOGS_FILE):
        try:
            df = pd.read_csv(BOOKING_LOGS_FILE)
            return df.to_dict('records')
        except Exception as e:
            st.error(f"Error loading booking logs: {str(e)}")
            return []
    return []

def save_booking_logs(logs):
    """Save booking logs to CSV file"""
    try:
        df = pd.DataFrame(logs)
        df.to_csv(BOOKING_LOGS_FILE, index=False)
    except Exception as e:
        st.error(f"Error saving booking logs: {str(e)}")

# Initialize session state variables
if 'phone_verified' not in st.session_state:
    st.session_state.phone_verified = False
if 'phone_otp' not in st.session_state:
    st.session_state.phone_otp = None
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
if 'selected_show' not in st.session_state:
    st.session_state.selected_show = None
if 'selected_seats' not in st.session_state:
    st.session_state.selected_seats = []
if 'num_tickets' not in st.session_state:
    st.session_state.num_tickets = 1
if 'payment_method' not in st.session_state:
    st.session_state.payment_method = None
if 'payment_verified' not in st.session_state:
    st.session_state.payment_verified = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'booking_history' not in st.session_state:
    st.session_state.booking_history = []
if 'booking_logs' not in st.session_state:
    st.session_state.booking_logs = load_booking_logs()
if 'show_receipt' not in st.session_state:
    st.session_state.show_receipt = False
if 'current_receipt' not in st.session_state:
    st.session_state.current_receipt = None
if 'food_order' not in st.session_state:
    st.session_state.food_order = {}
if 'show_payment' not in st.session_state:
    st.session_state.show_payment = False

def generate_receipt(user_info, movie_info, seats, payment_info, ticket_amount, food_total, final_amount):
    """Generate a receipt for the booking"""
    # Format the receipt with better styling
    receipt = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                              🎬 MOVIE TICKET RECEIPT                        ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  📱 CUSTOMER INFORMATION                                                    ║
║  ────────────────────────────────────────────────────────────────────────── ║
║  Name: {user_info['name']:<50} ║
║  Age: {user_info['age']:<50} ║
║  Phone: {user_info['phone']:<50} ║
║                                                                             ║
║  🎥 MOVIE INFORMATION                                                       ║
║  ────────────────────────────────────────────────────────────────────────── ║
║  Movie: {movie_info['title']:<50} ║
║  Language: {movie_info['language']:<50} ║
║  Show Time: {movie_info['show_time']:<50} ║
║  Date: {datetime.now().strftime('%Y-%m-%d'):<50} ║
║                                                                             ║
║  🎫 BOOKING DETAILS                                                         ║
║  ────────────────────────────────────────────────────────────────────────── ║
║  Number of Tickets: {len(seats):<50} ║
║  Seats: {', '.join(seats):<50} ║
║  Base Ticket Amount: ₹{ticket_amount:<50} ║
║  Ticket Discount: {calculate_discount(get_available_offers(movie_info['show_time'], user_info))*100:.0f}%                                              ║
║  Discounted Ticket Amount: ₹{ticket_amount:<50} ║
║                                                                             ║
║  🎫 FOOD & BEVERAGES DETAILS                                                  ║
║  ────────────────────────────────────────────────────────────────────────── ║
║  Food & Beverages Amount: ₹{food_total:<50} ║
║                                                                             ║
║  💳 PAYMENT INFORMATION                                                     ║
║  ────────────────────────────────────────────────────────────────────────── ║
║  Payment Method: {payment_info['method']:<50} ║
║  Transaction ID: {payment_info['transaction_id']:<50} ║
║  Payment Status: Successful                                                 ║
║                                                                             ║
║  📝 IMPORTANT INFORMATION                                                   ║
║  ────────────────────────────────────────────────────────────────────────── ║
║  • Please arrive at least 30 minutes before the show time                   ║
║  • Keep this receipt for entry                                             ║
║  • No refunds or exchanges allowed                                         ║
║  • Outside Food and beverages are not allowed inside the theater              ║
║                                                                             ║
║  🎉 Thank you for booking with us!                                         ║
║  Enjoy your movie! 🍿                                                      ║
║                                                                             ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    return receipt

def display_movie_details(movie):
    """Display detailed movie information"""
    details = get_movie_details(movie['title'])
    
    st.subheader("Movie Details")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Rating:** ⭐ {details['rating']}/5")
        st.write(f"**Reviews:** {details['reviews']}")
        st.write(f"**Duration:** {details['duration']}")
    
    with col2:
        st.write(f"**Genre:** {details['genre']}")
        st.write(f"**Language:** {details['language']}")
        st.write(f"**Release Date:** {details['release_date']}")

def display_seat_availability(show_time):
    """Display seat availability visualization"""
    availability = get_seat_availability(show_time, datetime.now().strftime('%Y-%m-%d'))
    
    # Create a bar chart
    fig = px.bar(
        x=list(availability.keys()),
        y=list(availability.values()),
        title="Seat Availability by Class",
        labels={'x': 'Seat Class', 'y': 'Available Seats'},
        color=list(availability.values()),
        color_continuous_scale='Viridis'
    )
    
    st.plotly_chart(fig)

def main():
    st.title("🎬 Movie Booking System")
    
    # Add admin login link
    if st.sidebar.button("Admin Login"):
        st.switch_page("admin.py")
    
    # Show receipt if available
    if st.session_state.show_receipt and st.session_state.current_receipt:
        st.subheader("Booking Receipt")
        
        # Generate PDF receipt
        movie_info = {
            'title': st.session_state.selected_movie['title'],
            'language': st.session_state.selected_movie['language'],
            'show_time': st.session_state.selected_show
        }
        
        payment_info = {
            'method': st.session_state.payment_method,
            'transaction_id': f"TXN{int(time.time())}"
        }
        
        # Calculate amounts
        total_amount = sum(calculate_seat_price(seat[0]) for seat in st.session_state.selected_seats)
        offers = get_available_offers(st.session_state.selected_show, st.session_state.user_info)
        discount = calculate_discount(offers)
        final_amount = total_amount * (1 - discount)
        
        # Generate PDF
        pdf = generate_pdf_receipt(
            st.session_state.user_info,
            movie_info,
            st.session_state.selected_seats,
            payment_info,
            total_amount,
            discount,
            final_amount
        )
        
        # Add download button for PDF receipt
        st.download_button(
            label="Download PDF Receipt",
            data=pdf,
            file_name=f"movie_ticket_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
        
        if st.button("Book Another Ticket"):
            st.session_state.show_receipt = False
            st.session_state.current_receipt = None
            st.experimental_rerun()
        return

    # Phone verification section
    if not st.session_state.phone_verified:
        st.header("Phone Verification")
        st.info("Enter your 10-digit phone number (e.g., ##########)")
        phone = st.text_input("Phone Number", placeholder="1234567890")
        
        if st.button("Send OTP"):
            if phone:
                # Remove any spaces from the phone number
                phone = phone.replace(" ", "")
                
                # Validate phone number format
                if not phone.isdigit() or len(phone) != 10:
                    st.error("Please enter a valid 10-digit phone number")
                else:
                    otp = generate_otp()
                    st.session_state.phone_otp = otp
                    if send_otp(phone, otp):
                        st.success("OTP sent! Please check the console for the OTP.")
                    else:
                        st.error("Failed to send OTP. Please try again.")
            else:
                st.error("Please enter your phone number")
        
        phone_otp = st.text_input("Enter OTP", type="password")
        if st.button("Verify Phone"):
            if phone and phone_otp:
                if verify_otp(phone, phone_otp):
                    st.session_state.phone_verified = True
                    st.session_state.user_info['phone'] = phone
                    st.success("Phone verified successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid OTP. Please try again.")
            else:
                st.error("Please enter both phone number and OTP")
        return

    # User information section
    if st.session_state.phone_verified and not st.session_state.user_info.get('name'):
        st.header("User Information")
        name = st.text_input("Enter your name" , placeholder="Enter your Name")
        age = st.number_input("Enter your age", min_value=1, max_value=120)
        
        if st.button("Continue"):
            if name and age:
                st.session_state.user_info['name'] = name
                st.session_state.user_info['age'] = age
                st.experimental_rerun()
            else:
                st.error("Please fill in all fields")
        return

    # Movie selection section
    if st.session_state.phone_verified and st.session_state.user_info.get('name') and not st.session_state.selected_movie:
        st.header("Select Movie")
        
        # Show recommendations if user has booking history
        if st.session_state.booking_history:
            st.subheader("Recommended for You")
            recommendations = get_movie_recommendations(st.session_state.booking_history)
            for movie in recommendations:
                st.write(f"⭐ {movie}")
        
        # Language selection
        language = st.selectbox("Select Language", list(MOVIES.keys()))
        
        # Display movies for selected language
        col1, col2 = st.columns(2)
        for idx, movie in enumerate(MOVIES[language]):
            with col1 if idx % 2 == 0 else col2:
                st.image(movie['image'], width=200)
                st.write(f"**{movie['title']}**")
                
                # Show movie details
                if st.button(f"View Details - {movie['title']}"):
                    display_movie_details(movie)
                
                if st.button(f"Book Now - {movie['title']}"):
                    st.session_state.selected_movie = movie
                    st.experimental_rerun()
        return

    # Show time selection
    if st.session_state.selected_movie and not st.session_state.selected_show:
        st.header(f"Select Show Time - {st.session_state.selected_movie['title']}")
        
        # Display seat availability
        st.subheader("Seat Availability")
        display_seat_availability(st.session_state.selected_movie['shows'][0])
        
        shows = st.session_state.selected_movie['shows']
        
        # Display show times in a grid
        cols = st.columns(len(shows))
        for idx, show in enumerate(shows):
            with cols[idx]:
                if st.button(show):
                    st.session_state.selected_show = show
                    st.experimental_rerun()
        
        if st.button("Back to Movie Selection"):
            st.session_state.selected_movie = None
            st.experimental_rerun()
        return

    # Number of tickets and seat selection
    if st.session_state.selected_show and not st.session_state.selected_seats:
        st.header("Select Seats")
        
        # Number of tickets
        st.session_state.num_tickets = st.number_input(
            "Number of Tickets",
            min_value=1,
            max_value=10,
            value=st.session_state.num_tickets
        )
        
        # Calculate total amount with seat prices
        total_amount = sum(calculate_seat_price(seat[0]) for seat in st.session_state.selected_seats)
        st.write(f"Total Amount: ₹{total_amount}")
        
        # Show available offers
        offers = get_available_offers(st.session_state.selected_show, st.session_state.user_info)
        if offers:
            st.subheader("Available Offers")
            for offer in offers:
                st.write(f"🎉 {offer}")
        
        # Seat selection
        st.subheader("Select Your Seats")
        
        # Display screen
        st.markdown("""
        <div style='text-align: center; padding: 10px; background-color: #f0f0f0; border-radius: 5px; margin-bottom: 20px;'>
            <strong>SCREEN</strong>
        </div>
        """, unsafe_allow_html=True)
        
        for section, seats in SEAT_LAYOUT.items():
            st.write(f"\n{section} Class (₹{calculate_seat_price(section)})")
            cols = st.columns(10)
            for idx, seat in enumerate(seats):
                with cols[idx % 10]:
                    if st.button(
                        seat,
                        key=f"seat_{seat}",
                        disabled=len(st.session_state.selected_seats) >= st.session_state.num_tickets
                        and seat not in st.session_state.selected_seats
                    ):
                        if seat in st.session_state.selected_seats:
                            st.session_state.selected_seats.remove(seat)
                        else:
                            if len(st.session_state.selected_seats) < st.session_state.num_tickets:
                                st.session_state.selected_seats.append(seat)
                            else:
                                st.error("You have already selected the maximum number of seats")
        
        st.write("Selected Seats:", ", ".join(st.session_state.selected_seats))
        
        if len(st.session_state.selected_seats) == st.session_state.num_tickets:
            if st.button("Proceed to Payment"):
                st.session_state.payment_verified = False
                st.session_state.selected_seats = st.session_state.selected_seats  # Keep selected seats
                st.session_state.food_order = st.session_state.food_order  # Keep food order
                st.session_state.show_payment = True
                st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
        
        if st.button("Back to Show Selection"):
            st.session_state.selected_show = None
            st.session_state.selected_seats = []
            st.experimental_rerun()
        return

    # Food and Beverages section
    if st.session_state.selected_seats and not st.session_state.payment_verified and not st.session_state.show_payment:
        st.header("Food and Beverages")
        st.info("Would you like to add some snacks and drinks to your order?")
        
        # Display food menu
        for category, items in FOOD_MENU.items():
            st.subheader(category)
            cols = st.columns(3)
            for idx, (item, price) in enumerate(items.items()):
                with cols[idx % 3]:
                    quantity = st.number_input(
                        f"{item} (₹{price})",
                        min_value=0,
                        max_value=5,
                        value=st.session_state.food_order.get(f"{category} - {item}", 0),
                        key=f"food_{category}_{item}"
                    )
                    if quantity > 0:
                        st.session_state.food_order[f"{category} - {item}"] = quantity
                    elif f"{category} - {item}" in st.session_state.food_order:
                        del st.session_state.food_order[f"{category} - {item}"]
        
        # Calculate food total
        food_total = sum(
            FOOD_MENU[item.split(" - ")[0]][item.split(" - ")[1]] * quantity
            for item, quantity in st.session_state.food_order.items()
        )
        
        if food_total > 0:
            st.subheader("Food Order Summary")
            for item, quantity in st.session_state.food_order.items():
                category, name = item.split(" - ")
                price = FOOD_MENU[category][name]
                st.write(f"{name}: {quantity} x ₹{price} = ₹{price * quantity}")
            st.write(f"**Total Food Amount: ₹{food_total}**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Proceed to Payment"):
                st.session_state.payment_verified = False
                st.session_state.selected_seats = st.session_state.selected_seats
                st.session_state.food_order = st.session_state.food_order
                st.session_state.show_payment = True
                st.experimental_rerun()
        with col2:
            if st.button("Skip Food & Beverages"):
                st.session_state.food_order = {}
                st.session_state.payment_verified = False
                st.session_state.selected_seats = st.session_state.selected_seats
                st.session_state.show_payment = True
                st.experimental_rerun()
        return

    # Payment section
    if not st.session_state.payment_verified and st.session_state.selected_seats and st.session_state.show_payment:
        st.header("Payment")
        
        # Calculate final amount with discounts
        base_amount = sum(calculate_seat_price(seat[0]) for seat in st.session_state.selected_seats)
        offers = get_available_offers(st.session_state.selected_show, st.session_state.user_info)
        discount = calculate_discount(offers)
        ticket_amount = base_amount * (1 - discount)
        
        # Calculate food total
        food_total = sum(
            FOOD_MENU[item.split(" - ")[0]][item.split(" - ")[1]] * quantity
            for item, quantity in st.session_state.food_order.items()
        )
        
        final_amount = ticket_amount + food_total
        
        st.write(f"Base Ticket Amount: ₹{base_amount}")
        if discount > 0:
            st.write(f"Ticket Discount: {discount*100:.0f}%")
        st.write(f"Discounted Ticket Amount: ₹{ticket_amount}")
        if food_total > 0:
            st.write(f"Food & Beverages Amount: ₹{food_total}")
        st.write(f"**Final Amount: ₹{final_amount}**")
        
        # Payment method selection
        st.subheader("Select Payment Method")
        payment_method = st.radio(
            "Choose your payment method:",
            list(PAYMENT_OPTIONS.keys()),
            format_func=lambda x: f"{PAYMENT_OPTIONS[x]['icon']} {x}"
        )
        
        if payment_method:
            st.session_state.payment_method = payment_method
            
            # Display payment form based on selected method
            st.subheader(f"Enter {payment_method} Details")
            
            payment_fields = {}
            for field in PAYMENT_OPTIONS[payment_method]['fields']:
                if field == 'CVV':
                    payment_fields[field] = st.text_input(field, type="password", max_chars=4)
                elif field == 'Card Number':
                    payment_fields[field] = st.text_input(field, max_chars=16)
                elif field == 'Expiry Date (MM/YY)':
                    payment_fields[field] = st.text_input(field, placeholder="MM/YY", max_chars=5)
                else:
                    payment_fields[field] = st.text_input(field)
            
            # Phone verification for payment
            st.subheader("Verify Your Phone for Payment")
            st.info("Enter your phone number with country code for payment verification")
            phone = st.text_input("Phone Number", placeholder="+91##########")
            
            if st.button("Send Payment OTP"):
                if phone:
                    # Remove any spaces from the phone number
                    phone = phone.replace(" ", "")
                    
                    # Validate phone number format
                    if not phone.startswith('+') or not phone[1:].isdigit():
                        st.error("Please enter a valid phone number with country code (e.g., +918610395422)")
                    else:
                        otp = generate_otp()
                        st.session_state.phone_otp = otp
                        if send_otp(phone, otp):
                            st.success("OTP sent! Check the console for the OTP.")
                        else:
                            st.error("Failed to send OTP. Please try again.")
                else:
                    st.error("Please enter your phone number")
            
            phone_otp = st.text_input("Enter Payment OTP", type="password")
            if st.button("Verify and Pay"):
                if phone and phone_otp:
                    if verify_otp(phone, phone_otp):
                        # Validate payment details
                        all_fields_filled = all(payment_fields.values())
                        if all_fields_filled:
                            st.session_state.payment_verified = True
                            
                            # Generate receipt
                            movie_info = {
                                'title': st.session_state.selected_movie['title'],
                                'language': st.session_state.selected_movie['language'],
                                'show_time': st.session_state.selected_show
                            }
                            
                            payment_info = {
                                'method': payment_method,
                                'transaction_id': f"TXN{int(time.time())}"
                            }
                            
                            receipt = generate_receipt(
                                st.session_state.user_info,
                                movie_info,
                                st.session_state.selected_seats,
                                payment_info,
                                ticket_amount,
                                food_total,
                                final_amount
                            )
                            
                            # Store receipt in session state
                            st.session_state.current_receipt = receipt
                            st.session_state.show_receipt = True
                            
                            # Add to booking logs
                            booking_log = {
                                'ticket_id': payment_info['transaction_id'],
                                'customer_name': st.session_state.user_info['name'],
                                'phone': st.session_state.user_info['phone'],
                                'movie': movie_info['title'],
                                'show_time': movie_info['show_time'],
                                'seats': ', '.join(st.session_state.selected_seats),
                                'food_order': ', '.join([f"{item} x {quantity}" for item, quantity in st.session_state.food_order.items()]),
                                'amount': final_amount,
                                'date': datetime.now().strftime('%Y-%m-%d'),
                                'payment_method': payment_method
                            }
                            st.session_state.booking_logs.append(booking_log)
                            save_booking_logs(st.session_state.booking_logs)  # Save to file
                            
                            # Add to booking history
                            st.session_state.booking_history.append({
                                'movie': movie_info['title'],
                                'date': datetime.now().strftime('%Y-%m-%d'),
                                'seats': st.session_state.selected_seats,
                                'food_order': st.session_state.food_order
                            })
                            
                            st.experimental_rerun()
                        else:
                            st.error("Please fill in all payment details")
                    else:
                        st.error("Invalid OTP. Please try again.")
                else:
                    st.error("Please enter both phone number and OTP")
        
        if st.button("Back to Seat Selection"):
            st.session_state.selected_seats = []
            st.session_state.food_order = {}
            st.session_state.show_payment = False
            st.experimental_rerun()
        return

if __name__ == "__main__":
    main() 