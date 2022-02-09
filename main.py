import json
from datetime import datetime

import flask
import requests
from bs4 import BeautifulSoup

app = flask.Flask(__name__)

URL = "https://www.foodandco.dk/besog-os-her/restauranter/ku/norre-campus/"
WEEKDAYS = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag"]


def fetch_menu(day: int):
    """
    Reads the html content of the menu webpage and selects the meals for the day.
    """
    html_content = requests.get(URL).text
    soup = BeautifulSoup(html_content, "html.parser")

    nbi_kanteen = soup.find_all("div", {"class": "ContentBlock"})[-1]
    elements = nbi_kanteen.find_all("p")
    content = []
    save = False
    for e in elements:
        if e.find("strong"):
            save = e.get_text() == WEEKDAYS[day]
            continue

        if save:
            content.append(e.get_text())
    return content


@app.route("/")
def main():

    # Get the contents and parse them into a string.
    content = fetch_menu(datetime.today().weekday())
    msg = "--- \n #### Today's Menu \n"
    msg += "\n".join(content).replace("\u00a0", "")

    # Format the response to be a json with the appropiate style.
    response = dict(response_type="in_channel", text=msg)
    json_str = json.dumps(response)

    # Send response with the correct header.
    r = flask.make_response(json_str)
    r.mimetype = "application/json"
    return r
