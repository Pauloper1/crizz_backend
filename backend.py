from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from estimator import CricketMatchPredictor
import pandas as pd
import math 

app = Flask(__name__)
CORS(app)  
app.config['MONGO_URI'] = 'mongodb://localhost:27017/crizz'

df = pd.read_csv('output.csv')
predictor = CricketMatchPredictor(df)
predictor.train_models()
predictor.evaluate_models()

# Overs remaining,Runs Scored,Wickets Remaining,Runs required

mongo = PyMongo(app)

@app.route('/api/getScenario/', methods=["GET"])
def getScenarios(scenarioDetails, probability):

    numberScenrio = 5
    winScenario = round(numberScenrio*probability)
    loseScenario = round(numberScenrio-winScenario)

    print(winScenario)
    print(loseScenario)
    # teamA ='Sunrisers Hyderabad'
    # teamB = 'Royal Challengers Bangalore'
    # print("details")
    # print(scenarioDetails)
    chasing_team = scenarioDetails['chasing_team']
    defending_team = scenarioDetails['defending_team']

    matchs = mongo.db.matches
    
    base_query = {
        'chasing_team': chasing_team,
        'defending_team': defending_team,

    }
    
    win_query = base_query.copy() 
    win_query['winner'] = 1 
    
    lose_query = base_query.copy()
    lose_query['winner'] = 0 

    winResults = list(matchs.find(win_query).limit(winScenario))
    loseResult = list(matchs.find(lose_query).limit(loseScenario))
    
    output = []
    for obj in winResults:
        output.append({
            'id': obj.get('id'),
            'chasing_team': obj.get('chasing_team', ''),
            'defending_team': obj.get('defending_team', ''),
            'winner': obj.get('winner'),
            'target_run': obj.get('target_run'),
            '2nd_inning':obj.get('2nd_inning'),
        })

    for obj in loseResult:
        output.append({
            'id': obj.get('id'),
            'chasing_team': obj.get('chasing_team', ''),
            'defending_team': obj.get('defending_team', ''),
            'winner': obj.get('winner'),
            'target_run': obj.get('target_run'),
            '2nd_inning':obj.get('2nd_inning'),
        })
    

    print(output) 
    return output

@app.route('/api/matches/', methods=['GET'])
def get_all_matches():
    matchs = mongo.db.matches
    all_objects = list(matchs.find().limit(100))

    output = []
    for obj in all_objects:
        output.append({
            'id': obj.get('id'),
            'chasing_team': obj.get('chasing_team', ''),
            'defending_team': obj.get('defending_team', ''),
            'winner': obj.get('winner'),
            'target_run': obj.get('target_run'),
            '2nd_inning':obj.get('2nd_inning'),
        })

    print(output) 
    return jsonify({'objects': output})



@app.route('/api/hello/', methods=['GET'])
def hello():
    return jsonify({'message': "hello"})

@app.route('/api/estimate/', methods=['POST'])
def estimate():
    data = request.get_json()
    if (data['battingTeam'] == data['teamA']):
        chasing_team = data['teamB']
        defending_team = data['teamA']
    else:
        defending_team = data['teamB']
        chasing_team = data['teamA']
    
    print(chasing_team)
    print(defending_team)
    winner = data['battingTeam']
    remainingOver = 20 - int(data['currentOver'])
    remainingWicket = 10 - int(data['currentWicket'])
    runsScored = int(data['currentRun'])
    requiredRuns = int(data['runsToScore'])
    #Overs remaining,Runs Scored,Wickets Remaining,Runs required,Match Boolean
    print(remainingOver)
    print(remainingWicket)
    print(runsScored)
    print(requiredRuns)
    print(data)
    predictions = predictor.predict([remainingOver, runsScored, remainingWicket, requiredRuns])
    probabilities = predictions[1]

# Calculating the average of the second element of the probabilities for each model
    average_second_element = {model: probs[1] for model, probs in probabilities.items()}

# Calculate the overall average of the second elements
    overall_average = sum(average_second_element.values()) / len(average_second_element)
    print(overall_average)
    output = getScenarios(
        {
            'chasing_team':chasing_team, 
            'defending_team':defending_team, 
            'winner':winner, 
            'currentOver':data['currentOver'], 
            'currentWicket':data['currentWicket'],
            'requiredRun':data['runsToScore']
         }, 
         overall_average)
    
    return jsonify(
        {
            'probability': overall_average,
            'scenario': output
        })
    

if __name__ == '__main__':
    app.run(debug=True, port=8000)
