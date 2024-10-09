# Python Backend Code (news_demo.py)
import eel
import asyncio
import tracemalloc

# Start tracing memory allocations
tracemalloc.start()

# Initialize the Eel app
eel.init('web')

@eel.expose
def get_news_audio():
    # Your code here to generate or provide the audio file URL
    audio_url = "news_report.mp3"  # Make sure the path to the audio file is correct
    return audio_url

# Ensure the event loop is properly managed when running the coroutine
def start_eel_app():
    eel.start('news.html', size=(800, 600))

if __name__ == "__main__":
    start_eel_app()