import random
from datetime import datetime, timedelta

# Seat pricing based on class
SEAT_PRICES = {
    'Premium': 250,
    'Executive': 200,
    'Normal': 150,
    'Economy': 100,
    'Budget': 80
}

# Special offers and discounts
OFFERS = {
    'WEEKEND_SPECIAL': {
        'discount': 0.15,  # 15% off
        'description': 'Weekend Special - 15% off on all tickets'
    },
    'EARLY_BIRD': {
        'discount': 0.20,  # 20% off
        'description': 'Early Bird - 20% off on morning shows'
    },
    'STUDENT': {
        'discount': 0.25,  # 25% off
        'description': 'Student Discount - 25% off with valid ID'
    },
    'SENIOR_CITIZEN': {
        'discount': 0.30,  # 30% off
        'description': 'Senior Citizen - 30% off'
    }
}

# Movie ratings and reviews
MOVIE_RATINGS = {
    'Captain Miller': {'rating': 4.5, 'reviews': 1200},
    'Ayalaan': {'rating': 4.2, 'reviews': 800},
    'Fighter': {'rating': 4.7, 'reviews': 1500},
    'Wonka': {'rating': 4.3, 'reviews': 900},
    'Malaikottai Vaaliban': {'rating': 4.4, 'reviews': 1100}
}

def calculate_seat_price(seat_class):
    """Calculate price based on seat class"""
    return SEAT_PRICES.get(seat_class, 150)

def get_available_offers(show_time, user_info):
    """Get available offers based on show time and user info"""
    offers = []
    
    # Weekend special
    if datetime.now().weekday() >= 5:  # Saturday or Sunday
        offers.append('WEEKEND_SPECIAL')
    
    # Early bird
    show_hour = int(show_time.split(':')[0])
    if show_hour < 12:  # Morning shows
        offers.append('EARLY_BIRD')
    
    # Student discount
    if user_info.get('age', 0) < 25:
        offers.append('STUDENT')
    
    # Senior citizen
    if user_info.get('age', 0) >= 60:
        offers.append('SENIOR_CITIZEN')
    
    return offers

def calculate_discount(offers):
    """Calculate total discount from available offers"""
    if not offers:
        return 0
    
    # Apply the highest discount
    max_discount = max(OFFERS[offer]['discount'] for offer in offers)
    return max_discount

def get_movie_recommendations(user_history):
    """Get movie recommendations based on user history"""
    # This would typically use a recommendation algorithm
    # For now, return random movies
    return random.sample(list(MOVIE_RATINGS.keys()), 3)

def get_seat_availability(show_time, date):
    """Get seat availability for a show"""
    # This would typically check a database
    # For now, return random availability
    return {
        'Premium': random.randint(5, 20),
        'Executive': random.randint(10, 30),
        'Normal': random.randint(15, 40),
        'Economy': random.randint(20, 50),
        'Budget': random.randint(25, 60)
    }

def get_movie_details(movie_title):
    """Get detailed movie information"""
    return {
        'rating': MOVIE_RATINGS.get(movie_title, {}).get('rating', 0),
        'reviews': MOVIE_RATINGS.get(movie_title, {}).get('reviews', 0),
        'duration': f"{random.randint(120, 180)} minutes",
        'genre': random.choice(['Action', 'Drama', 'Comedy', 'Thriller', 'Romance']),
        'language': random.choice(['Tamil', 'Hindi', 'English', 'Malayalam']),
        'release_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
    } 