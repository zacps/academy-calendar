from flask import Flask, Response


app = Flask(__name__)


@app.route("/academy-cinemas")
def calendar():
    with open('calendar.ics') as f:
        cal = f.read()
    
    return Response(cal, mimetype='text/calendar')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)