import os
from dotenv import load_dotenv

load_dotenv()

# Movie Ticket Configuration
TICKET_PRICE = 150

# Payment Options
PAYMENT_OPTIONS = {
    'Debit Card': {
        'fields': ['Card Number', 'Card Holder Name', 'Expiry Date (MM/YY)', 'CVV'],
        'icon': '💳'
    },
    'Credit Card': {
        'fields': ['Card Number', 'Card Holder Name', 'Expiry Date (MM/YY)', 'CVV'],
        'icon': '💳'
    },
    'UPI': {
        'fields': ['UPI ID'],
        'icon': '📱'
    }
}

# Sample Movie Data
MOVIES = {
    'Tamil': [
        {
            'title': 'Captain Miller',
            'language': 'Tamil',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/captain-miller-et00357727-1704957101.jpg',
            'shows': ['9:30 AM', '1:30 PM', '5:30 PM', '9:00 PM']
        },
        {
            'title': 'Ayalaan',
            'language': 'Tamil',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/ayalaan-et00348588-1704967533.jpg',
            'shows': ['10:30 AM', '2:30 PM', '6:30 PM', '10:00 PM']
        },
        {
            'title': 'Merry Christmas',
            'language': 'Tamil',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/merry-christmas-et00376327-1703228611.jpg',
            'shows': ['11:30 AM', '3:30 PM', '7:30 PM']
        },
        {
            'title': 'Guntur Kaaram',
            'language': 'Tamil',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/guntur-kaaram-et00376327-1703228611.jpg',
            'shows': ['12:30 PM', '4:30 PM', '8:30 PM']
        },
        {
            'title': 'Lal Salaam',
            'language': 'Tamil',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/lal-salaam-et00376327-1703228611.jpg',
            'shows': ['9:00 AM', '1:00 PM', '5:00 PM', '9:00 PM']
        },
        {
            'title': 'Mission Chapter 1',
            'language': 'Tamil',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/mission-chapter-1-et00376327-1703228611.jpg',
            'shows': ['10:00 AM', '2:00 PM', '6:00 PM', '10:00 PM']
        },
        {
            'title': 'Ayalaan 2',
            'language': 'Tamil',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/ayalaan-2-et00376327-1703228611.jpg',
            'shows': ['11:00 AM', '3:00 PM', '7:00 PM', '10:30 PM']
        },
        {
            'title': 'Thalaivar 170',
            'language': 'Tamil',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/thalaivar-170-et00376327-1703228611.jpg',
            'shows': ['12:00 PM', '4:00 PM', '8:00 PM', '11:00 PM']
        },
        {
            'title': 'Indian 3',
            'language': 'Tamil',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/indian-3-et00376327-1703228611.jpg',
            'shows': ['1:30 PM', '5:30 PM', '9:30 PM']
        },
        {
            'title': 'Vettaiyan',
            'language': 'Tamil',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/vettaiyan-et00376327-1703228611.jpg',
            'shows': ['2:30 PM', '6:30 PM', '10:30 PM']
        }
    ],
    'Hindi': [
        {
            'title': 'Fighter',
            'language': 'Hindi',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/fighter-et00376327-1703228611.jpg',
            'shows': ['10:00 AM', '2:00 PM', '6:00 PM', '9:30 PM']
        },
        {
            'title': 'Dunki',
            'language': 'Hindi',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/dunki-et00376327-1703228611.jpg',
            'shows': ['11:00 AM', '3:00 PM', '7:00 PM', '10:30 PM']
        },
        {
            'title': '12th Fail',
            'language': 'Hindi',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/12th-fail-et00376327-1703228611.jpg',
            'shows': ['12:00 PM', '4:00 PM', '8:00 PM', '10:00 PM']
        },
        {
            'title': 'Animal',
            'language': 'Hindi',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/animal-et00376327-1703228611.jpg',
            'shows': ['1:00 PM', '5:00 PM', '9:00 PM']
        },
        {
            'title': 'Salaar',
            'language': 'Hindi',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/salaar-et00376327-1703228611.jpg',
            'shows': ['10:30 AM', '2:30 PM', '6:30 PM', '9:30 PM']
        },
        {
            'title': 'HanuMan',
            'language': 'Hindi',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/hanuman-et00376327-1703228611.jpg',
            'shows': ['11:30 AM', '3:30 PM', '7:30 PM', '10:30 PM']
        },
        {
            'title': 'Main Atal Hoon',
            'language': 'Hindi',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/main-atal-hoon-et00376327-1703228611.jpg',
            'shows': ['12:30 PM', '4:30 PM', '8:30 PM']
        },
        {
            'title': 'Teri Baaton Mein Aisa Uljha Jiya',
            'language': 'Hindi',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/teri-baaton-mein-aisa-uljha-jiya-et00376327-1703228611.jpg',
            'shows': ['1:30 PM', '5:30 PM', '9:30 PM']
        },
        {
            'title': 'Yodha',
            'language': 'Hindi',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/yodha-et00376327-1703228611.jpg',
            'shows': ['10:00 AM', '2:00 PM', '6:00 PM', '10:00 PM']
        },
        {
            'title': 'Article 370',
            'language': 'Hindi',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/article-370-et00376327-1703228611.jpg',
            'shows': ['11:00 AM', '3:00 PM', '7:00 PM', '10:30 PM']
        }
    ],
    'English': [
        {
            'title': 'Wonka',
            'language': 'English',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/wonka-et00376327-1703228611.jpg',
            'shows': ['9:30 AM', '1:30 PM', '5:30 PM', '9:00 PM']
        },
        {
            'title': 'Aquaman and the Lost Kingdom',
            'language': 'English',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/aquaman-and-the-lost-kingdom-et00376327-1703228611.jpg',
            'shows': ['10:30 AM', '2:30 PM', '6:30 PM', '10:00 PM']
        },
        {
            'title': 'Migration',
            'language': 'English',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/migration-et00376327-1703228611.jpg',
            'shows': ['11:30 AM', '3:30 PM', '7:30 PM']
        },
        {
            'title': 'Anyone But You',
            'language': 'English',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/anyone-but-you-et00376327-1703228611.jpg',
            'shows': ['12:30 PM', '4:30 PM', '8:30 PM']
        },
        {
            'title': 'The Beekeeper',
            'language': 'English',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/the-beekeeper-et00376327-1703228611.jpg',
            'shows': ['1:30 PM', '5:30 PM', '9:30 PM']
        },
        {
            'title': 'Mean Girls',
            'language': 'English',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/mean-girls-et00376327-1703228611.jpg',
            'shows': ['2:30 PM', '6:30 PM', '10:30 PM']
        },
        {
            'title': 'The Book of Clarence',
            'language': 'English',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/the-book-of-clarence-et00376327-1703228611.jpg',
            'shows': ['9:00 AM', '1:00 PM', '5:00 PM', '9:00 PM']
        },
        {
            'title': 'The Boys in the Boat',
            'language': 'English',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/the-boys-in-the-boat-et00376327-1703228611.jpg',
            'shows': ['10:00 AM', '2:00 PM', '6:00 PM', '10:00 PM']
        },
        {
            'title': 'Night Swim',
            'language': 'English',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/night-swim-et00376327-1703228611.jpg',
            'shows': ['11:00 AM', '3:00 PM', '7:00 PM', '10:30 PM']
        },
        {
            'title': 'The Color Purple',
            'language': 'English',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/the-color-purple-et00376327-1703228611.jpg',
            'shows': ['12:00 PM', '4:00 PM', '8:00 PM', '11:00 PM']
        }
    ],
    'Malayalam': [
        {
            'title': 'Malaikottai Vaaliban',
            'language': 'Malayalam',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/malaikottai-vaaliban-et00364640-1705471873.jpg',
            'shows': ['10:00 AM', '1:00 PM', '4:00 PM', '7:00 PM']
        },
        {
            'title': 'Abraham Ozler',
            'language': 'Malayalam',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/abraham-ozler-et00379480-1704461533.jpg',
            'shows': ['11:30 AM', '2:30 PM', '5:30 PM', '8:30 PM']
        },
        {
            'title': 'Bramayugam',
            'language': 'Malayalam',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/bramayugam-et00376327-1703228611.jpg',
            'shows': ['12:00 PM', '3:00 PM', '6:00 PM', '9:00 PM']
        },
        {
            'title': 'Manjummel Boys',
            'language': 'Malayalam',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/manjummel-boys-et00376327-1703228611.jpg',
            'shows': ['1:00 PM', '4:00 PM', '7:00 PM', '10:00 PM']
        },
        {
            'title': 'Aattam',
            'language': 'Malayalam',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/aattam-et00376327-1703228611.jpg',
            'shows': ['10:30 AM', '1:30 PM', '4:30 PM', '7:30 PM']
        },
        {
            'title': 'Anweshippin Kandethum',
            'language': 'Malayalam',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/anweshippin-kandethum-et00376327-1703228611.jpg',
            'shows': ['11:30 AM', '2:30 PM', '5:30 PM', '8:30 PM']
        },
        {
            'title': 'Varshangalkku Shesham',
            'language': 'Malayalam',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/varshangalkku-shesham-et00376327-1703228611.jpg',
            'shows': ['12:30 PM', '3:30 PM', '6:30 PM', '9:30 PM']
        },
        {
            'title': 'Aavesham',
            'language': 'Malayalam',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/aavesham-et00376327-1703228611.jpg',
            'shows': ['1:30 PM', '4:30 PM', '7:30 PM', '10:30 PM']
        },
        {
            'title': 'Premalu',
            'language': 'Malayalam',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/premalu-et00376327-1703228611.jpg',
            'shows': ['10:00 AM', '1:00 PM', '4:00 PM', '7:00 PM']
        },
        {
            'title': 'Thalavan',
            'language': 'Malayalam',
            'image': 'https://assets-in.bmscdn.com/iedb/movies/images/mobile/thumbnail/xlarge/thalavan-et00376327-1703228611.jpg',
            'shows': ['11:00 AM', '2:00 PM', '5:00 PM', '8:00 PM']
        }
    ]
}

# Seat Configuration
SEAT_LAYOUT = {
    'Premium': ['A' + str(i) for i in range(1, 11)] + ['B' + str(i) for i in range(1, 11)],
    'Executive': ['C' + str(i) for i in range(1, 11)] + ['D' + str(i) for i in range(1, 11)],
    'Normal': ['E' + str(i) for i in range(1, 11)] + ['F' + str(i) for i in range(1, 11)],
    'Economy': ['G' + str(i) for i in range(1, 11)] + ['H' + str(i) for i in range(1, 11)],
    'Budget': ['I' + str(i) for i in range(1, 11)] + ['J' + str(i) for i in range(1, 11)]
}

# Food and Beverages Menu
FOOD_MENU = {
    'Popcorn': {
        'Small': 80,
        'Medium': 120,
        'Large': 150
    },
    'Nachos': {
        'Regular': 100,
        'Large': 150
    },
    'Beverages': {
        'Soft Drink (Small)': 60,
        'Soft Drink (Large)': 80,
        'Mineral Water': 30,
        'Coffee': 70,
        'Tea': 50
    },
    'Snacks': {
        'French Fries': 80,
        'Sandwich': 100,
        'Burger': 120,
        'Hot Dog': 90
    },
    'Combo Meals': {
        'Popcorn + Soft Drink (Small)': 120,
        'Popcorn + Soft Drink (Large)': 150,
        'Nachos + Soft Drink (Large)': 180,
        'Burger + Soft Drink (Large)': 180
    }
} 