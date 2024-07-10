






def preprocess_record(data):
    preprocessed_data = {}

    # Basic info extraction
    info = data.get('info', {})
    preprocessed_data['match_number'] = info.get('event', {}).get('match_number')
    preprocessed_data['teams'] = info.get('teams')
    preprocessed_data['toss_winner'] = info.get('toss', {}).get('winner')
    preprocessed_data['toss_decision'] = info.get('toss', {}).get('decision')
    preprocessed_data['winner'] = info.get('outcome', {}).get('winner')

    # Second innings cumulative runs calculation
    second_inning = data.get('innings', [])[1]  # Assuming there are always at least 2 innings
    if second_inning:
        preprocessed_data['target_run'] = second_inning.get('target', {}).get('runs')
        preprocessed_data['2nd_inning'] = {}

        for over_data in second_inning.get('overs', []):
            over_number = over_data.get('over')
            cumulative_runs = 0
            for delivery in over_data.get('deliveries', []):
                cumulative_runs += delivery.get('runs', {}).get('total', 0)
            preprocessed_data['2nd_inning'][over_number] = cumulative_runs

    return preprocessed_data


root_path = r'D:\Documents\Luap\Career\5_Sciative\Study\Assessment\Cricket Match Winning Probability Estimator\ipl_male_json'

import os

def preprocessJsonFile():
    for file in os.listdir(root_path):
        if file.endswith('.json'):
            open_file = os.path.join(root_path,file)
            with open(open_file, 'r') as f:
                pass

sample_file = r'D:\Documents\Luap\Career\5_Sciative\Study\Assessment\Cricket Match Winning Probability Estimator\ipl_male_json\335982.json'
print(preprocess_record(sample_file))