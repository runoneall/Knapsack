def check(uId:str):
    import os
    Knapsack_path = f"./Knapsack/{uId}.json"
    if not os.path.exists(Knapsack_path):
        with open(Knapsack_path, 'w', encoding='utf-8') as json_file:
            json_file.write('{}')