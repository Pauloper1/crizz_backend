import os
import pandas as pd
import json

root_path = "backend\outputFile.json"
json_paths = [os.path.join(root_path, data) for data in os.listdir(root_path)]

def calculateTotalScoresForAnInnings(inning_data):
    total_runs_in_innings = 0
    for over_data in inning_data:
        total_runs_in_over = sum(delivery_data["runs"]["total"] for delivery_data in over_data["deliveries"])
        total_runs_in_innings += total_runs_in_over
    return total_runs_in_innings

def getDataForJSONFile(json_data):
    data = []
    teamAScore = calculateTotalScoresForAnInnings(json_data[0])
    teamBScore = calculateTotalScoresForAnInnings(json_data[1])
    teamChasingWinning = teamBScore > teamAScore
    
    overs_left = 20
    for over_number, over_data in enumerate(json_data[1], 1):
        total_runs_in_over = sum(delivery_data["runs"]["total"] for delivery_data in over_data["deliveries"])
        wickets_lost = len(set(delivery_data["batter"] for delivery_data in over_data["deliveries"])) + len(set(delivery_data["non_striker"] for delivery_data in over_data["deliveries"]))
        runs_needed = teamAScore - total_runs_in_over if teamAScore - total_runs_in_over >= 0 else 0
        data.append([overs_left - over_number, total_runs_in_over, wickets_lost, runs_needed, teamChasingWinning])
    
    return data

total_data = []
for data_path in json_paths:
    with open(data_path) as match_data:
        match_json = json.load(match_data)
        transformed_data = getDataForJSONFile([match_json['innings'][0]['overs'], match_json['innings'][1]['overs']])
        total_data.extend(transformed_data)

# Convert to DataFrame
columns = ['Overs Left', 'Total Runs in Over', 'Wickets Lost', 'Runs Needed', 'Team Chasing Winning']
dataframe = pd.DataFrame(total_data, columns=columns)

# Save to CSV
dataframe.to_csv("output.csv", index=False)
