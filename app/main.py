from datetime import datetime, timedelta

from flask import Flask
from ics import Calendar, Event
import requests
import bs4
import js2py
import pytz


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
                    url=time['bookingLink'],
                    categories=[f"FILM"],
                    description=time['bookingLink']
                )
                cal.events.add(event)

    return cal


@app.route("/academy-cinemas")
def calendar():
    releases = get_data()
    cal = build_calendar(releases)
    
    return str(cal)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)