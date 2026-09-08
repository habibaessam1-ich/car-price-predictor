import io
import json
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Car Price Predictor Pro - Ultimate Edition",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Comprehensive Car Database (All Brands, Models, and Engine Options)
CAR_MODELS = {
    "Toyota": {
        "Corolla": {
            "engines": ["1.6L Normal", "1.8L Hybrid"],
            "base_price": 1600000,
            "body": "Sedan",
            "hp": 120,
        },
        "Yaris": {
            "engines": ["1.5L Normal"],
            "base_price": 1000000,
            "body": "Hatchback",
            "hp": 118,
        },
        "Fortuner": {
            "engines": ["2.7L Normal", "4.0L V6"],
            "base_price": 3800000,
            "body": "SUV",
            "hp": 234,
        },
        "C-HR": {
            "engines": ["1.2L Turbo", "1.8L Hybrid"],
            "base_price": 1750000,
            "body": "SUV",
            "hp": 113,
        },
        "Belta": {
            "engines": ["1.5L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 103,
        },
        "RAV4": {
            "engines": ["2.5L Hybrid"],
            "base_price": 2800000,
            "body": "SUV",
            "hp": 219,
        },
        "Land Cruiser": {
            "engines": ["3.3L Twin-Turbo V6", "4.0L V6"],
            "base_price": 7500000,
            "body": "SUV",
            "hp": 409,
        },
    },
    "Nissan": {
        "Sunny": {
            "engines": ["1.5L Normal"],
            "base_price": 800000,
            "body": "Sedan",
            "hp": 108,
        },
        "Sentra": {
            "engines": ["1.6L Normal"],
            "base_price": 1100000,
            "body": "Sedan",
            "hp": 118,
        },
        "Qashqai": {
            "engines": ["1.3L Turbo"],
            "base_price": 1650000,
            "body": "SUV",
            "hp": 148,
        },
        "Juke": {
            "engines": ["1.0L Turbo"],
            "base_price": 1300000,
            "body": "SUV",
            "hp": 114,
        },
        "Patrol": {
            "engines": ["5.6L V8"],
            "base_price": 6800000,
            "body": "SUV",
            "hp": 400,
        },
    },
    "Hyundai": {
        "Elantra": {
            "engines": ["1.6L Normal"],
            "base_price": 1300000,
            "body": "Sedan",
            "hp": 127,
        },
        "Tucson": {
            "engines": ["1.6L Turbo"],
            "base_price": 1900000,
            "body": "SUV",
            "hp": 180,
        },
        "Accent": {
            "engines": ["1.4L Normal"],
            "base_price": 900000,
            "body": "Sedan",
            "hp": 100,
        },
        "Creta": {
            "engines": ["1.5L Normal"],
            "base_price": 1400000,
            "body": "SUV",
            "hp": 113,
        },
        "i10": {
            "engines": ["1.2L Normal"],
            "base_price": 700000,
            "body": "Hatchback",
            "hp": 84,
        },
        "Santa Fe": {
            "engines": ["2.5L Normal", "1.6L Turbo Hybrid"],
            "base_price": 2700000,
            "body": "SUV",
            "hp": 194,
        },
        "Sonata": {
            "engines": ["2.5L Normal"],
            "base_price": 2100000,
            "body": "Sedan",
            "hp": 191,
        },
    },
    "Kia": {
        "Cerato / K3": {
            "engines": ["1.6L Normal"],
            "base_price": 1350000,
            "body": "Sedan",
            "hp": 130,
        },
        "Sportage": {
            "engines": ["1.6L Turbo"],
            "base_price": 1950000,
            "body": "SUV",
            "hp": 177,
        },
        "Pegas": {
            "engines": ["1.4L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 95,
        },
        "Seltos": {
            "engines": ["1.4L Turbo", "1.5L Normal"],
            "base_price": 1500000,
            "body": "SUV",
            "hp": 140,
        },
        "Sorento": {
            "engines": ["2.5L Normal", "1.6L Turbo Hybrid"],
            "base_price": 2900000,
            "body": "SUV",
            "hp": 191,
        },
        "Carnival": {
            "engines": ["3.5L V6"],
            "base_price": 3200000,
            "body": "Van",
            "hp": 290,
        },
    },
    "MG": {
        "MG 5": {
            "engines": ["1.5L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 118,
        },
        "MG 6": {
            "engines": ["1.5L Turbo"],
            "base_price": 1200000,
            "body": "Sedan",
            "hp": 169,
        },
        "MG ZS": {
            "engines": ["1.5L Normal"],
            "base_price": 1050000,
            "body": "SUV",
            "hp": 119,
        },
        "MG RX5": {
            "engines": ["1.5L Turbo"],
            "base_price": 1400000,
            "body": "SUV",
            "hp": 171,
        },
        "MG 4 EV": {
            "engines": ["Electric EV"],
            "base_price": 1350000,
            "body": "Hatchback",
            "hp": 170,
        },
        "MG Whale": {
            "engines": ["2.0L Turbo"],
            "base_price": 1600000,
            "body": "SUV",
            "hp": 231,
        },
    },
    "Chery": {
        "Arrizo 5": {
            "engines": ["1.5L Normal"],
            "base_price": 750000,
            "body": "Sedan",
            "hp": 114,
        },
        "Tiggo 3": {
            "engines": ["1.6L Normal"],
            "base_price": 880000,
            "body": "SUV",
            "hp": 126,
        },
        "Tiggo 7": {
            "engines": ["1.5L Turbo"],
            "base_price": 1100000,
            "body": "SUV",
            "hp": 145,
        },
        "Tiggo 8 Pro": {
            "engines": ["1.5L Turbo", "1.6L Turbo"],
            "base_price": 1450000,
            "body": "SUV",
            "hp": 145,
        },
        "Arrizo 8": {
            "engines": ["1.6L Turbo"],
            "base_price": 1250000,
            "body": "Sedan",
            "hp": 194,
        },
    },
    "BYD": {
        "F3": {
            "engines": ["1.5L Normal"],
            "base_price": 620000,
            "body": "Sedan",
            "hp": 108,
        },
        "Song Plus Hybrid": {
            "engines": ["1.5L Hybrid"],
            "base_price": 1600000,
            "body": "SUV",
            "hp": 197,
        },
        "Yuan Plus": {
            "engines": ["Electric EV"],
            "base_price": 1700000,
            "body": "SUV",
            "hp": 201,
        },
    },
    "Changan": {
        "Alsvin": {
            "engines": ["1.4L Normal", "1.5L Normal"],
            "base_price": 650000,
            "body": "Sedan",
            "hp": 107,
        },
        "CS35 Plus": {
            "engines": ["1.4L Turbo"],
            "base_price": 1150000,
            "body": "SUV",
            "hp": 158,
        },
        "CS55 Plus": {
            "engines": ["1.5L Turbo"],
            "base_price": 1350000,
            "body": "SUV",
            "hp": 185,
        },
        "Uni-K": {
            "engines": ["2.0L Turbo"],
            "base_price": 1950000,
            "body": "SUV",
            "hp": 233,
        },
        "Uni-T": {
            "engines": ["1.5L Turbo"],
            "base_price": 1450000,
            "body": "SUV",
            "hp": 177,
        },
    },
    "Geely": {
        "Emgrand": {
            "engines": ["1.5L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 102,
        },
        "Coolray": {
            "engines": ["1.5L Turbo"],
            "base_price": 1300000,
            "body": "SUV",
            "hp": 175,
        },
        "Okavango": {
            "engines": ["1.5L Hybrid"],
            "base_price": 1650000,
            "body": "SUV",
            "hp": 190,
        },
        "Monjaro": {
            "engines": ["2.0L Turbo"],
            "base_price": 2200000,
            "body": "SUV",
            "hp": 235,
        },
    },
    "Skoda": {
        "Octavia": {
            "engines": ["1.4L Turbo", "2.0L Turbo"],
            "base_price": 1850000,
            "body": "Sedan",
            "hp": 150,
        },
        "Kodiaq": {
            "engines": ["1.4L Turbo", "2.0L Turbo"],
            "base_price": 2600000,
            "body": "SUV",
            "hp": 150,
        },
        "Karoq": {
            "engines": ["1.4L Turbo"],
            "base_price": 2100000,
            "body": "SUV",
            "hp": 150,
        },
        "Scala": {
            "engines": ["1.6L Normal"],
            "base_price": 1300000,
            "body": "Hatchback",
            "hp": 110,
        },
        "Superb": {
            "engines": ["1.4L Turbo", "2.0L Turbo"],
            "base_price": 2300000,
            "body": "Sedan",
            "hp": 150,
        },
    },
    "BMW": {
        "3 Series (320i)": {
            "engines": ["2.0L Turbo"],
            "base_price": 3500000,
            "body": "Sedan",
            "hp": 184,
        },
        "5 Series (520i)": {
            "engines": ["2.0L Turbo"],
            "base_price": 4800000,
            "body": "Sedan",
            "hp": 184,
        },
        "X1": {
            "engines": ["1.5L Turbo"],
            "base_price": 2900000,
            "body": "SUV",
            "hp": 140,
        },
        "X5": {
            "engines": ["3.0L Turbo"],
            "base_price": 6200000,
            "body": "SUV",
            "hp": 340,
        },
        "7 Series": {
            "engines": ["3.0L Turbo Hybrid"],
            "base_price": 8500000,
            "body": "Sedan",
            "hp": 380,
        },
        "X3": {
            "engines": ["2.0L Turbo"],
            "base_price": 4100000,
            "body": "SUV",
            "hp": 252,
        },
    },
    "Mercedes-Benz": {
        "C-Class (C180 / C200)": {
            "engines": ["1.5L Turbo", "2.0L Turbo"],
            "base_price": 4200000,
            "body": "Sedan",
            "hp": 170,
        },
        "E-Class (E200)": {
            "engines": ["2.0L Turbo"],
            "base_price": 5800000,
            "body": "Sedan",
            "hp": 197,
        },
        "GLC": {
            "engines": ["2.0L Turbo"],
            "base_price": 5900000,
            "body": "SUV",
            "hp": 204,
        },
        "A-Class": {
            "engines": ["1.3L Turbo"],
            "base_price": 2700000,
            "body": "Hatchback",
            "hp": 136,
        },
        "S-Class": {
            "engines": ["3.0L Turbo", "4.0L V8"],
            "base_price": 9500000,
            "body": "Sedan",
            "hp": 435,
        },
        "GLE": {
            "engines": ["2.0L Turbo", "3.0L Turbo"],
            "base_price": 6800000,
            "body": "SUV",
            "hp": 255,
        },
    },
    "Audi": {
        "A4": {
            "engines": ["2.0L Turbo"],
            "base_price": 2800000,
            "body": "Sedan",
            "hp": 190,
        },
        "A6": {
            "engines": ["2.0L Turbo"],
            "base_price": 3900000,
            "body": "Sedan",
            "hp": 245,
        },
        "Q3": {
            "engines": ["1.4L Turbo"],
            "base_price": 2500000,
            "body": "SUV",
            "hp": 150,
        },
        "Q7": {
            "engines": ["3.0L Turbo"],
            "base_price": 4900000,
            "body": "SUV",
            "hp": 340,
        },
        "Q8": {
            "engines": ["3.0L Turbo"],
            "base_price": 5800000,
            "body": "SUV",
            "hp": 340,
        },
    },
    "Chevrolet": {
        "Optra": {
            "engines": ["1.5L Normal"],
            "base_price": 750000,
            "body": "Sedan",
            "hp": 110,
        },
        "Captiva": {
            "engines": ["1.5L Turbo"],
            "base_price": 1500000,
            "body": "SUV",
            "hp": 148,
        },
        "Aveo": {
            "engines": ["1.5L Normal"],
            "base_price": 600000,
            "body": "Sedan",
            "hp": 105,
        },
        "Groove": {
            "engines": ["1.5L Normal"],
            "base_price": 1000000,
            "body": "SUV",
            "hp": 110,
        },
        "Trailblazer": {
            "engines": ["1.3L Turbo"],
            "base_price": 1350000,
            "body": "SUV",
            "hp": 155,
        },
    },
    "Renault": {
        "Megane": {
            "engines": ["1.6L Normal", "1.3L Turbo"],
            "base_price": 1400000,
            "body": "Sedan",
            "hp": 115,
        },
        "Logan": {
            "engines": ["1.6L Normal"],
            "base_price": 650000,
            "body": "Sedan",
            "hp": 110,
        },
        "Duster": {
            "engines": ["1.6L Normal"],
            "base_price": 1200000,
            "body": "SUV",
            "hp": 115,
        },
        "Sandero Stepway": {
            "engines": ["1.6L Normal"],
            "base_price": 850000,
            "body": "Hatchback",
            "hp": 110,
        },
        "Austral": {
            "engines": ["1.3L Turbo Hybrid"],
            "base_price": 1750000,
            "body": "SUV",
            "hp": 200,
        },
    },
    "Fiat": {
        "Tipo": {
            "engines": ["1.4L Normal", "1.6L Normal"],
            "base_price": 1050000,
            "body": "Sedan",
            "hp": 110,
        },
        "500": {
            "engines": ["1.4L Normal"],
            "base_price": 1100000,
            "body": "Hatchback",
            "hp": 100,
        },
    },
    "Peugeot": {
        "301": {
            "engines": ["1.6L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 115,
        },
        "508": {
            "engines": ["1.6L Turbo"],
            "base_price": 1800000,
            "body": "Sedan",
            "hp": 165,
        },
        "2008": {
            "engines": ["1.2L Turbo"],
            "base_price": 1450000,
            "body": "SUV",
            "hp": 130,
        },
        "3008": {
            "engines": ["1.6L Turbo"],
            "base_price": 1950000,
            "body": "SUV",
            "hp": 180,
        },
        "5008": {
            "engines": ["1.6L Turbo"],
            "base_price": 2200000,
            "body": "SUV",
            "hp": 180,
        },
    },
    "Suzuki": {
        "Swift": {
            "engines": ["1.2L Normal"],
            "base_price": 750000,
            "body": "Hatchback",
            "hp": 84,
        },
        "Ciaz / Dzire": {
            "engines": ["1.2L Normal", "1.5L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 104,
        },
        "Ertiga": {
            "engines": ["1.5L Normal"],
            "base_price": 950000,
            "body": "Van",
            "hp": 103,
        },
        "Grand Vitara": {
            "engines": ["1.5L Hybrid"],
            "base_price": 1550000,
            "body": "SUV",
            "hp": 103,
        },
        "Jimny": {
            "engines": ["1.5L Normal"],
            "base_price": 1400000,
            "body": "SUV",
            "hp": 102,
        },
    },
    "Volkswagen": {
        "Golf": {
            "engines": ["1.4L Turbo"],
            "base_price": 1600000,
            "body": "Hatchback",
            "hp": 150,
        },
        "Passat": {
            "engines": ["1.4L Turbo", "2.0L Turbo"],
            "base_price": 1900000,
            "body": "Sedan",
            "hp": 150,
        },
        "Tiguan": {
            "engines": ["1.4L Turbo", "2.0L Turbo"],
            "base_price": 2200000,
            "body": "SUV",
            "hp": 150,
        },
        "Touareg": {
            "engines": ["3.0L V6 Turbo"],
            "base_price": 4200000,
            "body": "SUV",
            "hp": 340,
        },
    },
    "Mazda": {
        "Mazda 3": {
            "engines": ["1.5L Normal", "2.0L Normal"],
            "base_price": 1350000,
            "body": "Sedan",
            "hp": 155,
        },
        "Mazda CX-3": {
            "engines": ["1.5L Normal"],
            "base_price": 1400000,
            "body": "SUV",
            "hp": 110,
        },
        "Mazda CX-5": {
            "engines": ["2.5L Normal"],
            "base_price": 1900000,
            "body": "SUV",
            "hp": 188,
        },
    },
    "Ford": {
        "Focus": {
            "engines": ["1.5L Turbo", "1.5L Normal"],
            "base_price": 1200000,
            "body": "Sedan",
            "hp": 182,
        },
        "Kuga": {
            "engines": ["1.5L Turbo"],
            "base_price": 1750000,
            "body": "SUV",
            "hp": 182,
        },
        "Explorer": {
            "engines": ["2.3L Turbo", "3.0L V6"],
            "base_price": 4500000,
            "body": "SUV",
            "hp": 300,
        },
    },
    "Mitsubishi": {
        "Lancer (Puma)": {
            "engines": ["1.6L Normal"],
            "base_price": 750000,
            "body": "Sedan",
            "hp": 117,
        },
        "Eclipse Cross": {
            "engines": ["1.5L Turbo"],
            "base_price": 1650000,
            "body": "SUV",
            "hp": 150,
        },
        "Xpander": {
            "engines": ["1.5L Normal"],
            "base_price": 1150000,
            "body": "Van",
            "hp": 104,
        },
        "Outlander": {
            "engines": ["2.4L Normal"],
            "base_price": 2000000,
            "body": "SUV",
            "hp": 167,
        },
    },
    "Jeep": {
        "Renegade": {
            "engines": ["1.4L Turbo", "1.3L Turbo"],
            "base_price": 1550000,
            "body": "SUV",
            "hp": 140,
        },
        "Grand Cherokee": {
            "engines": ["5.7L V8", "3.6L V6"],
            "base_price": 4800000,
            "body": "SUV",
            "hp": 290,
        },
        "Wrangler": {
            "engines": ["2.0L Turbo", "3.6L V6"],
            "base_price": 4300000,
            "body": "SUV",
            "hp": 270,
        },
    },
    "Porsche": {
        "Cayenne": {
            "engines": ["3.0L V6 Turbo", "4.0L V8 Twin-Turbo"],
            "base_price": 7500000,
            "body": "SUV",
            "hp": 348,
        },
        "Macan": {
            "engines": ["2.0L Turbo", "2.9L V6"],
            "base_price": 5500000,
            "body": "SUV",
            "hp": 265,
        },
        "Panamera": {
            "engines": ["2.9L V6 Twin-Turbo"],
            "base_price": 8800000,
            "body": "Sedan",
            "hp": 348,
        },
        "911 Carrera": {
            "engines": ["3.0L Twin-Turbo H6"],
            "base_price": 11000000,
            "body": "Coupe",
            "hp": 379,
        },
    },
    "Land Rover": {
        "Range Rover Evoque": {
            "engines": ["2.0L Turbo"],
            "base_price": 4100000,
            "body": "SUV",
            "hp": 200,
        },
        "Range Rover Sport": {
            "engines": ["3.0L Turbo", "4.4L V8"],
            "base_price": 8200000,
            "body": "SUV",
            "hp": 360,
        },
        "Defender": {
            "engines": ["2.0L Turbo", "3.0L Turbo", "5.0L V8"],
            "base_price": 7200000,
            "body": "SUV",
            "hp": 296,
        },
    },
    "Alfa Romeo": {
        "Giulia": {
            "engines": ["2.0L Turbo"],
            "base_price": 2700000,
            "body": "Sedan",
            "hp": 280,
        },
        "Stelvio": {
            "engines": ["2.0L Turbo"],
            "base_price": 3100000,
            "body": "SUV",
            "hp": 280,
        },
    },
    "Subaru": {
     