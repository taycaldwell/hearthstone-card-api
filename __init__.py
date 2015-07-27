
from flask import Flask, url_for, request, jsonify, Response
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)

client = MongoClient()
db = client.database
card_db = db.card_db

locale_list = ["deDE", "enGB", "enUS", "esES", "esMX", "frFR", "itIT", "koKR", "plPL", "ptBR", "ptPT", "ruRU", "zhCN", "zhTW"]
card_set_list = ["Basic", "Classic", "Reward", "Missions", "System", "Debug", "Promotion", "Curse of Naxxramas", "Goblin vs Gnomes", "Blackrock Mountain", "Credits"]
card_type_list = ["Hero", "Minion", "Spell", "Enchantment", "Weapon", "Hero Power"]
class_list = ["Developer", "Druid", "Hunter", "Mage", "Paladin", "Priest", "Rogue", "Shaman", "Warlock", "Warrior", "Dream"]
race_list = ["Murloc", "Demon", "Mechanical", "Beast", "Totem", "Pirate", "Dragon"]
faction_list = ["Horde", "Alliance", "Neutral"]
rarity_list = ["Developer", "Common", "Free", "Rare", "Epic", "Legendary"]

# Endpoint - Get cards
# Defaults - locale: enUS, cardSet: all, cardType: all
@app.route('/v1.0/cards/', methods=['GET'])
def cards():
    card_filter = {'locale' : 'enUS'}
    if not handle_query_parameters(card_filter, request):
        return bad_request()
    cards = card_db.find(card_filter)
    cards_dict = {}
    for card in cards:
        index = card['cardName']
        if 'dataById' in request.args:
            if request.args['dataById'].lower() == 'true':
                index = card['id']
            elif request.args['dataById'].lower() == 'false':
                pass
            else:
                return bad_request()
        cards_dict[index] = card
        del cards_dict[index]['_id']
    if not cards_dict:
        return not_found()
    return Response(json_util.dumps(cards_dict), mimetype='application/json')

# Endpoint - Get a card by its name
@app.route('/v1.0/cards/by-name/<name>', methods=['GET'])
def card_by_name(name=None):
    if name:
        card_filter = {'locale' : 'enUS', 'cardName' : name}
        if not handle_query_parameters(card_filter, request):
            return bad_request()
        cards = card_db.find(card_filter)
        cards_dict = {}
        for card in cards:
            del card['_id']
            cards_dict[card['id']] = card
        if not cards_dict:
            return not_found()
        return Response(json_util.dumps(cards_dict), mimetype='application/json')
    return not_found()

# Endpoint - Get a card by its ID
@app.route('/v1.0/cards/by-id/<id>', methods=['GET'])
def card_by_id(id=None):
    if id:
        card_filter = {'locale' : 'enUS', 'id' : id}
        if not handle_query_parameters(card_filter, request):
            return bad_request()
        cards = card_db.find(card_filter)
        cards_dict = {}
        for card in cards:
            del card['_id']
            cards_dict[card['id']] = card
        if not cards_dict:
            return not_found()
        return Response(json_util.dumps(cards_dict), mimetype='application/json')
    return not_found()

# Error Handler - Not Found (404)
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

# Error Handler - Bad Request (400)
@app.errorhandler(400)
def bad_request(error=None):
    message = {
        'status': 400,
        'message': 'Bad Request'
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp

# Error Handler - Internal Server Error (500)
@app.errorhandler(500)
def internal_server_error(error=None):
    message = {
        'status': 500,
        'message': 'Internal server error'
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp

def handle_query_parameters(card_filter, request):
    if 'locale' in request.args:
        if request.args['locale'] not in locale_list:
            return False
        card_filter['locale'] = request.args['locale']
    if 'cardSet' in request.args:
        if request.args['cardSet'] not in card_set_list:
            return False
        card_filter['cardSet'] = request.args['cardSet']
    if 'cardType' in request.args:
        if request.args['cardType'] not in card_type_list:
            return False
        card_filter['cardType'] = request.args['cardType']
    if 'rarity' in request.args:
        if request.args['rarity'] not in rarity_list:
            return False
        card_filter['rarity'] = request.args['rarity']
    if 'class' in request.args:
        if request.args['class'] not in class_list:
            return False
        card_filter['class'] = request.args['class']
    if 'race' in request.args:
        if request.args['race'] not in race_list:
            return False
        card_filter['race'] = request.args['race']
    if 'faction' in request.args:
        if request.args['faction'] not in faction_list:
            return False
        card_filter['faction'] = request.args['faction']
    if 'collectible' in request.args:
        if request.args['collectible'].lower() == 'true': # Note - we need to check for both booleans independently (including the spelling)
            card_filter['collectible'] = True             # so random incorrect strings like "dasdasd" don't default to false,
        elif request.args['elite'].lower() == 'false':    # as would happen if we just returned arg.lower() == 'true'
            card_filter['elite'] = False
        else:
            return False
    if 'elite' in request.args:
        if request.args['elite'].lower() == 'true':
            card_filter['elite'] = True
        elif request.args['elite'].lower() == 'false':
            card_filter['elite'] = False
        else:
            False
    return True

if __name__ == '__main__':
    app.run(debug = True)
                     