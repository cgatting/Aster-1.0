import eel
import edge_tts
import tracemalloc
import requests
import datetime
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import json

tracemalloc.start()

eel.init('web')

@eel.expose
def tts(text):
    text = str(text)
    communicate = edge_tts.Communicate(text, "en-IE-EmilyNeural")
    communicate.save_sync("output.mp3")

@eel.expose
def get_weather():
    api_key = "213e8f92dc45c1bd6681848984a1f5d2"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    # You might want to get the city dynamically, but for this example we'll use a fixed city
    city = "Cheltenham"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # For Celsius
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        weather_data = response.json()
        result = {
            "city": weather_data["name"],
            "temperature": int(round(weather_data["main"]["temp"], 0)),
            "description": weather_data["weather"][0]["description"],
            "humidity": weather_data["main"]["humidity"],
            "icon": weather_data["weather"][0]["icon"]
        }
        result["icon_url"] = f"http://openweathermap.org/img/wn/{result['icon']}@2x.png"
        return result
    else:
        error_message = {"error": "Unable to fetch weather data"}
        print(f"Error fetching weather data: {error_message}")
        return error_message
@eel.expose
def calendar():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    time_min = now.isoformat()
    events_result = service.events().list(calendarId='primary', timeMin=time_min,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_time = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
        if start_time > now + datetime.timedelta(minutes=10):
            event_date = start_time.strftime("%B %d, %Y")
            event_time = start_time.strftime("%I:%M %p")
            
            return {
                'summary': f"Next event: {event['summary']}",
                'start': f"Date: {event_date}, Time: {event_time}",
                'link': f"Calendar link: {event.get('htmlLink', '')}"
            }
    
    return 'No events found starting more than 10 minutes from now.'

@eel.expose

def display_user_message():
    with open('user_settings.json', 'r') as file:
        user_settings = json.load(file)
    return f"Hello, {user_settings['firstname']}!"
def run_eel():
    eel.start('index.html', size=(800, 600))

if __name__ == "__main__":
    run_eel()
