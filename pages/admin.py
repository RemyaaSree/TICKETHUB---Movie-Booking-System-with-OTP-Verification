import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Admin credentials (in a real app, this would be in a secure database)
ADMIN_CREDENTIALS = {
    'admin': 'admin123'
}

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

def admin_login():
    """Admin login interface"""
    st.title("🎬 Admin Dashboard")
    
    if 'admin_verified' not in st.session_state:
        st.session_state.admin_verified = False
    if 'login_time' not in st.session_state:
        st.session_state.login_time = None
    
    if not st.session_state.admin_verified:
        st.header("Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
                st.session_state.admin_verified = True
                st.session_state.login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
        return False
    
    return True

def display_booking_logs():
    """Display booking logs in a table format"""
    st.header("Booking Logs")
    
    # Display login time if available
    if st.session_state.login_time:
        st.info(f"Logged in since: {st.session_state.login_time}")
    
    # Load existing logs from file
    if 'booking_logs' not in st.session_state:
        st.session_state.booking_logs = load_booking_logs()
    
    if st.session_state.booking_logs:
        # Convert logs to DataFrame
        df = pd.DataFrame(st.session_state.booking_logs)
        
        # Rename columns for better display
        column_names = {
            'ticket_id': 'Ticket ID',
            'customer_name': 'Customer Name',
            'phone': 'Phone Number',
            'movie': 'Movie',
            'show_time': 'Show Time',
            'seats': 'Selected Seats',
            'amount': 'Amount (₹)',
            'date': 'Booking Date',
            'payment_method': 'Payment Method'
        }
        df = df.rename(columns=column_names)
        
        # Display filters
        col1, col2 = st.columns(2)
        with col1:
            date_filter = st.date_input("Filter by Date")
        with col2:
            movie_filter = st.selectbox("Filter by Movie", ['All'] + list(df['Movie'].unique()))
        
        # Apply filters
        if date_filter:
            df = df[df['Booking Date'] == date_filter.strftime('%Y-%m-%d')]
        if movie_filter != 'All':
            df = df[df['Movie'] == movie_filter]
        
        # Display statistics
        st.subheader("Booking Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Bookings", len(df))
        with col2:
            st.metric("Total Revenue", f"₹{df['Amount (₹)'].sum():,.2f}")
        with col3:
            st.metric("Average Booking Value", f"₹{df['Amount (₹)'].mean():,.2f}")
        
        # Display booking logs
        st.subheader("Booking Details")
        st.dataframe(df)
        
        # Export functionality
        if st.button("Export to CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"booking_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.info("No booking logs available")

def main():
    if admin_login():
        display_booking_logs()

if __name__ == "__main__":
    main() 
