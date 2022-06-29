# Academy Calendar

A simple docker container which scrapes Academy Cinemas showtimes and serves them as ical so they can be added to Google Calendar or any other client.

## Use

```
docker run -p $PORT:80 ghcr.io/zacps/academy-calendar:master
```

Then expose `$PORT` using your favourite proxy.

The calendar will be available at:

```
https://your.host.here/academy-cinemas
```
