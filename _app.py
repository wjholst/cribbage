from flask import Flask
from flask import render_template
from datetime import datetime
from cribbage_utilities import *
from cribbage_utilities import init_score_lookup
import re

app = Flask(__name__, static_folder="static")

score_lookup_4, score_lookup_5 = init_score_lookup()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/Start")
def startGame():
    # Choose two cards at random.
    # First card is player, second card is computer.
    # Evaluate winner.  If tied, choose two new cards.
    # Return card file names.  First card is player, second card is computer.
    # Return "Computer" or "You" for who is dealer.
    # Send cookie "Computer" or "Player" identifying dealer.

    player_is_dealer, player_card, computer_card = determine_dealer ()
    player_cardname = card_lookup [player_card]
    computer_cardname = card_lookup[computer_card]
    if player_is_dealer:
        # who = 'Player'
        who = 'You'
    else:
        who = 'Computer'
    return render_template(
        "start_game.html",
        player_cardFileName="static/CardDeck/" + player_cardname,
        computer_cardFileName="static/CardDeck/" + computer_cardname,
        who_deals=who
    )

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run()