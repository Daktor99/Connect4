from flask import Flask, render_template, request, jsonify
from Gameboard import Gameboard
from sqlite3 import Error
import logging
import db

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

game = Gameboard()

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():

    global game
    db.clear()
    db.init_db()
    game = Gameboard()

    return render_template("player1_connect.html", status='Pick a Color.')


'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    try:
        # setting player1's color
        colorPicked = request.args['color']
        game.player1 = colorPicked

        return render_template('player1_connect.html',
                               status="Color picked: " + colorPicked)
    except Exception:
        return "Error with /p1Color"


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    try:

        if game.player1 not in ["red", "yellow"]:
            return render_template("p2Join.html",
                                   status="Error, player 1 color not picked!")

        if game.player1 == "red":
            game.player2 = "yellow"
        elif game.player1 == "yellow":
            game.player2 = "red"

        game.add_move()
        return render_template("p2Join.html",
                               status="Color picked: " + game.player2)

    except Exception:
        return "Error on '/p2join'"


'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
'''


@app.route('/move1', methods=['POST'])
def p1_move():

    try:
        column = request.json['column']
        game.makeMove(column, "p1", game.player1)
        return jsonify(move=game.board,
                       invalid=False,
                       winner=game.game_result)
    except ValueError as e:
        return jsonify(move=game.board,
                       invalid=True,
                       reason=str(e),
                       winner=game.game_result)


'''
Same as '/move1' but instead process Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():

    try:
        column = request.json['column']
        game.makeMove(column, "p2", game.player2)
        return jsonify(move=game.board,
                       invalid=False,
                       winner=game.game_result)
    except ValueError as e:
        return jsonify(move=game.board,
                       invalid=True,
                       reason=str(e),
                       winner=game.game_result)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
