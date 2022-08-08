import html
from datetime import datetime, timedelta
from functools import lru_cache

from flask import Flask, Response
from ics import Calendar, Event
import requests
import bs4
import js2py
import pytz

from rottentomatoes import rottentomatoes as rt


app = Flask(__name__)


def get_data():
  # Request homepage
    page = requests.get('https://www.academycinemas.co.nz/#')
    # Parse HTML
    soup = bs4.BeautifulSoup(page.content)
    # Extract the script we need
    data = soup.find_all('script')[13].text[43:]
    
    # Evaluate JS to get the data out
    context = js2py.EvalJs({})
    context.execute(data)
    parsed_releases = context.movieData.to_dict()
    
    return parsed_releases


@lru_cache
def rotten_tomatoes_details(name: str) -> str:
    try:
        return str(rt.Film(name))
    except Exception as e:
        print(e)
        return "Failed to fetch details from rotten tomatoes"


def build_calendar(parsed_releases):
    cal = Calendar()
    timezone = pytz.timezone('Pacific/Auckland')

    for date, films in parsed_releases.items():
        for film in films:
            for time in film['times']:
                try:
                    details = rotten_tomatoes_details(film['title'])

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
                        description=f"{details}\n\n{html.unescape(time['bookingLink'])}"
                    )
                    cal.events.add(event)
                except Exception as e:
                    print(f"Failed to process details for film: {e}")
                    print(film)

    return cal


@app.route("/academy-cinemas")
def calendar():
    releases = get_data()
    cal = build_calendar(releases)
    
    return Response(str(cal), mimetype='text/calendar')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)