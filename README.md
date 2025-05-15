# TICKETHUB - Movie Booking System with OTP Verification

TICKETHUB is a modern, user-friendly movie ticket booking system  built with Streamlit that brings together ease, security, and interactivity into one web application. It enables users to search through a carefully curated list of movies in various languages such as Tamil, Hindi, English, and Malayalam, so it can be used by a broad range of people.

With its intuitive interface, customers can pick desired showtimes, pick favorite seats from a live interactive floor plan, and make multiple payments including Debit Card, Credit Card, and UPI — all while being secured through phone OTP verification during login and payment phases.

## Features

- Phone OTP verification for login and payment
- Browse movies by language (Tamil, Hindi, English, Malayalam)
- Show time selection
- Interactive seat selection with different pricing tiers
- Available offers and discounts
- Offers Food and Beverages section
- Multiple payment options (Debit Card, Credit Card, UPI)
- PDF receipt generation
- Admin dashboard for booking management
- Movie recommendations based on booking history
- Seat availability visualization

## Prerequisites

- Python 3.7+
- Streamlit
- Required Python packages (listed in requirements.txt)

## Setup

1. Clone the repository:
```bash
git clone <"https://www.github.com/RemyaaSree/TICKETHUB-Movie-Booking-System-with-OTP-Verification">
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run main.py
```

The application will be available at http://localhost:8501

## Usage

1. **Phone Verification**
   - Enter your 10-digit phone number
   - Receive OTP (displayed in console for testing)
   - Verify OTP to proceed

2. **User Information**
   - Enter your name and age
   - This information is used for personalized offers

3. **Movie Selection**
   - Browse movies by language
   - View movie details including ratings and reviews
   - Select a movie to book

4. **Show Time Selection**
   - Choose from available show times
   - View seat availability visualization

5. **Seat Selection**
   - Select number of tickets
   - Choose seats from the interactive layout
   - Different seat classes with varying prices
   - View available offers and discounts

6. **Food and Beverages**
   - Select snacks and drinks to add to your booking
   - Items are added to your order summary

7. **Payment**
   - Choose payment method (Debit Card, Credit Card, UPI)
   - Enter payment details
   - Verify payment with OTP
   - Complete the booking

8. **Receipt**
   - Download PDF receipt
   - Receipt includes:
     - Customer information
     - Movie details
     - Booking information
     - Payment details
     - Important terms and conditions

## Admin Dashboard

Access the admin dashboard by clicking the "Admin Login" button in the sidebar.

Admin credentials:
- Username: admin
- Password: admin123

Features:
- View booking logs
- Filter bookings by date and movie
- View booking statistics
- Export booking data

## Project Structure

```
movie-booking-system/
├── main.py              # Main application file
├── admin.py            # Admin dashboard
├── utils.py            # Utility functions
├── config.py           # Configuration and constants
├── features.py         # Business logic and features
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Dependencies

- streamlit==1.31.1
- pandas==2.2.0
- pillow==10.2.0
- python-dotenv==1.0.0
- plotly==5.18.0
- numpy==1.26.3
- scikit-learn==1.4.0
- secure-smtplib==0.1.1
- requests==2.31.0
- reportlab==4.1.0

## Author

**Remyaa**  
Pre-final Year Student, SRM Institute of Science and Technology  
Passionate about solving real-time problems through technology and innovation.  

- [LinkedIn](https://www.linkedin.com/in/remyaa-sree/)  
- [GitHub](https://github.com/RemyaaSree)  
