from flask import Flask
from flask import render_template, session,request, flash, make_response
from datetime import datetime
import json
from cribbage_utilities import *
from cribbage_utilities import init_score_lookup
import re

app = Flask(__name__, static_folder="static")
app.debug = True
app.config['SECRET_KEY'] = 'xyzzy'

score_lookup_4, score_lookup_5 = init_score_lookup()
player_deals = True

@app.route("/")
def home():
    session['id'] = '12345'
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
    player_deals = player_is_dealer

    flash ('player is dealer' + str(player_is_dealer))
    if player_is_dealer:
        # who = 'Player'
        
        who = 'You deal' + session['id']
    else:
        who = 'Computer deals'

    resp = make_response(render_template(
        "start_game.html",
        player_cardFileName="static/CardDeck/" + player_cardname,
        computer_cardFileName="static/CardDeck/" + computer_cardname,
        who_deals=who))
    resp.set_cookie('dealer_is', who)
    
    
    return resp

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

@app.route("/select_cards",methods=['GET','POST'])
def select_cards():

    h = Hands()
    random.seed(2)
    h.deal_hands()

    player_hand = h.get_player_hand()
    print (player_hand)
    player_cardnames = [card_lookup[cn] for cn in player_hand]
    computer_hand = h.get_computer_hand()
    print (computer_hand)
    starter = h.get_starter_card()
    print ('request method is ' +str(request.method))

    if request.method == 'POST':
        print ('in post')
        cardlist = [1,2,3]
        cardlist = request.form.getlist("cardNumber")
        print (cardlist)

        if len(cardlist) != 2:
            print (len(cardlist))
            flash ('Select 2 cards for crib..')

        print (cardlist)



        
    resp = make_response (render_template(
        "select_cards.html",
        #player_cardFileName="static/CardDeck/" + player_cardname,
        blank = "static/" + "card_back.svg",
        transparent = "static/" + "transparent.svg",
        pcn0 = "static/CardDeck/" + player_cardnames[0],
        pcn1 = "static/CardDeck/" + player_cardnames[1],
        pcn2 = "static/CardDeck/" + player_cardnames[2],
        pcn3 = "static/CardDeck/" + player_cardnames[3],
        pcn4 = "static/CardDeck/" + player_cardnames[4],
        pcn5 = "static/CardDeck/" + player_cardnames[5],
        pc0 = player_hand[0],
        pc1 = player_hand[1],
        pc2 = player_hand[2],
        pc3 = player_hand[3],
        pc4 = player_hand[4],
        pc5 = player_hand[5]
      )
    )
    ph = json.dumps(player_hand.tolist())
    ch = json.dumps(computer_hand.tolist())
    resp.set_cookie('playerhand',ph)
    resp.set_cookie('computerhand',ch)      
    return resp

@app.route("/crib", methods=['GET', 'POST'])
def crib():
    print ("in crib")
    if request.method == 'POST':
        print ('in post')
        
        cardlist = request.form.getlist("cardNumber")
        print (cardlist)

    return render_template("crib.html")

@app.route("/test", methods=['GET','POST']) 
def test(): 
    if request.method == 'POST':
        print (request.form.getlist('chkbox'))    
    return render_template("test.html")    

if __name__ == '__main__':
    app.run()