import random
import string

def generate_short_url(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_geolocation(ip_address):
    # Simulando uma localização básica para fins de desenvolvimento
    return {"country": "Unknown", "city": "Unknown"} if ip_address == "127.0.0.1" else {"country": "US", "city": "New York"}
