from flask import Flask
from flask import render_template, session,request, flash, make_response
from datetime import datetime
import json
#import cribbage_utilities
from cribbage_utilities import *
#from cribbage_utilities import init_score_lookup
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
        
        # who = 'You deal' + session['id']
        who = 'Player deals'    
    else:
        who = 'Computer deals'

    resp = make_response(render_template(
        "start_game.html",
        player_cardFileName="static/CardDeck/" + player_cardname,
        computer_cardFileName="static/CardDeck/" + computer_cardname,
        who_deals=who))
    resp.set_cookie('dealer_is', who)
    resp.set_cookie('computer_score', '0')
    resp.set_cookie('player_score', '0')
    resp.set_cookie('narration_1', 'Play 3, pair for 2 - count is 28')
    resp.set_cookie('narration_2', 'Play 2 - go for 1')
    
    return resp

# @app.route("/hello/")
# @app.route("/hello/<name>")
# def hello_there(name = None):
#     return render_template(
#         "hello_there.html",
#         name=name,
#         date=datetime.now()
#     )

# @app.route("/api/data")
# def get_data():
#     return app.send_static_file("data.json")

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
    starter = str(starter[0])
    print ('starter is ' + str(starter))
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
        #chand,comp_crib = pick_best_hand(computer_hand,True)
        #print (chand)
    resp = make_response (render_template(
        "select_cards.html",
        #player_cardFileName="static/CardDeck/" + player_cardname,
        blank = "static/CardDeck/" + "Card-Back.svg",
        transparent = "static/CardDeck/" + "transparent.svg",
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
    resp.set_cookie('selecting_crib','y') 
    resp.set_cookie('starter',starter)       
    return resp

@app.route("/play_cards", methods=['GET', 'POST'])
def play_cards():
    print ("in play_cards")
    crib = []
    ch = []
    selecting_crib = request.cookies.get('selecting_crib')
    ph = request.cookies.get('playerhand')
    starter = int(request.cookies.get('starter'))
    who_deals = request.cookies.get('dealer_is')
    player_deals = who_deals == "Player deals"
    
    playerhand = json.loads(ph)
    playerhand = list(playerhand)
    player_hand = []
    print (playerhand)
    
    print ('selecting crib value is ' + selecting_crib)
    if request.method == 'POST':
      print ('in post')
      print ('selecting crib value is ' + selecting_crib)
      if selecting_crib=='y':  
        criblist = request.form.getlist("cardNumber")
        print (criblist)
        player_crib = [int(i) for i in criblist]

        c_hand,c_crib = pick_best_hand(computer_hand,player_deals)
        print (c_hand)
        print (c_crib)
        playerlist = list(set(playerhand).difference(set(player_crib)))
        player_hand = [int(i) for i in playerlist]
        crib_list = player_crib + c_crib
        #res = make_response()

        ch = json.dumps(c_hand)
        crib = json.dumps(crib_list)
      else:
        print ('not slecting crib')
    #print ('player hand ' + (player_hand))
    print(type(player_hand)) 
    print (type(player_hand[0]))
    player_cardnames = [card_lookup[cn] for cn in player_hand]
    starter_cardname = "static/CardDeck/" + card_lookup[starter] 
    cm_crib = "static/CardDeck/" + "Card-Back.svg"
    pl_crib = "static/CardDeck/" + "Card-Back.svg"

    if player_deals:
        starterc = "static/CardDeck/transparent.svg"
        starterp = starter_cardname
        cm_crib = "static/CardDeck/transparent.svg"
        start_msg = "Click to start play"
    else:
        starterp = "static/CardDeck/transparent.svg"
        starterc = starter_cardname
        pl_crib = "static/CardDeck/transparent.svg"
        start_msg = "Select and play"
    resp = make_response (render_template(
        "play_cards.html",
        blank = "static/CardDeck/" + "Card-Back.svg",
        pc0 = player_hand[0],
        pc1 = player_hand[1],
        pc2 = player_hand[2],
        pc3 = player_hand[3],
        pcn0 = "static/CardDeck/" + player_cardnames[0],
        pcn1 = "static/CardDeck/" + player_cardnames[1],
        pcn2 = "static/CardDeck/" + player_cardnames[2],
        pcn3 = "static/CardDeck/" + player_cardnames[3],
        ccrib = cm_crib, 
        pcrib = pl_crib,
        computer_starter = starterc,
        player_starter = starterp,
        start_msg = start_msg ))
    if selecting_crib=='y':  
        resp.set_cookie("computer_hand",value=ch)
        resp.set_cookie("crib_hand",value=crib)
        ph = json.dumps(player_hand)
        resp.set_cookie("player_hand",value=ph)

    resp.set_cookie("selecting_crib",value='n')
    return resp

@app.route("/test", methods=['GET','POST']) 
def test(): 
    if request.method == 'POST':
        print (request.form.getlist('chkbox'))    
    return render_template("test.html")    

if __name__ == '__main__':
    app.run()