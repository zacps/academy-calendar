import time
import html
import logging
from datetime import datetime, timedelta

from ics import Calendar, Event
import requests
import bs4
import js2py
import pytz


logger = logging.getLogger(__name__)
logger.setLevel("INFO")

with open('calendar.ics', 'w') as f:
    f.write('')


def get_data():
  # Request homepage
    page = requests.get('https://www.academycinemas.co.nz/#', timeout=5)
    page.raise_for_status()
    # Parse HTML
    soup = bs4.BeautifulSoup(page.content, features="html.parser")
    # Extract the script we need
    data = soup.find(lambda tag: tag.name == "script" and "movieData" in tag.text).text[43:]
    
    # Evaluate JS to get the data out
    context = js2py.EvalJs({})
    context.execute(data)
    parsed_releases = context.movieData.to_dict()
    
    return parsed_releases


def build_calendar(parsed_releases):
    cal = Calendar()
    timezone = pytz.timezone('Pacific/Auckland')
    
    for date, films in parsed_releases.items():
        for film in films:
            for time in film['times']:
                start_time = datetime.strptime(f"{date} {time['time']}", "%Y-%m-%d %H:%M%p")
                start_time.replace(tzinfo=timezone)
                duration = timedelta(minutes=int(film['duration'][:-5]))
                event = Event(
                    name=film['title'],
                    begin=start_time,
                    end=f"{start_time + duration}",
                    location=f"Academy Cinemas",
                    url=html.unescape(time['bookingLink']),
                    categories=[f"FILM"],
                    description=time['bookingLink']
                )
                cal.events.add(event)

    return cal


def fetch_data():
    logger.info("Fetching data")
    releases = get_data()
    calendar = build_calendar(releases)
    with open('calendar.ics', 'w') as f:
        f.write(str(calendar))
    logger.info("Successfully fetched data")


if __name__ == "__main__":
    while True:
        fetch_data()
        time.sleep(60*60)