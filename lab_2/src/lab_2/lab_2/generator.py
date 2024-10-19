import pandas as pd
import numpy as np

def generate_boolean(p):
    return int(np.random.rand() < p)

def calculate_target(row):
    score = (row['Play_music'] * 0.1 +
             (1-row['Play_video_games']) * 0.1 +
             row['Like_cooking'] * 0.1 +
             row['Like_sports'] * 0.12 +

             row['Handsome'] * 0.25 +
             row['Generous'] * 0.15 +

             row['Rich'] * 0.08 +
             (1-row['Married']) * 0.11 +

             (row['Age'] >= 18 and row['Age'] <= 21) * (0.1) +
             (row['Age'] >= 22 and row['Age'] <= 25) * (0.2) +
             (row['Age'] >= 26 and row['Age'] <= 35) * (0.3) +
             (row['Age'] >= 36 and row['Age'] <= 45) * (0.1) +
             (row['Age'] >= 46 and row['Age'] <= 55) * (-0) +
             (row['Age'] >= 56 and row['Age'] <= 65) * (-0.1) +
             (row['Age'] >= 66 and row['Age'] <= 80) * (-0.2) +
             (row['Age'] >= 81) * (-0.3)
             )

    return generate_boolean(score)

def main():
    np.random.seed(42)
    size=50000
    data = {
        'Play_music': np.random.choice([1, 0], size=size),
        'Play_video_games': np.random.choice([1, 0], size=size),
        'Like_sports': np.random.choice([1, 0], size=size),
        'Like_cooking': np.random.choice([1, 0], size=size),
        'Handsome': np.random.choice([1, 0], size=size),
        'Generous': np.random.choice([1, 0], size=size),
        'Rich': np.random.choice([1, 0], size=size),
        'Married': np.random.choice([1, 0], size=size),
        'Age': np.random.randint(18, 90, size=size)
    }

    df = pd.DataFrame(data)
    df['Result'] = df.apply(calculate_target, axis=1)

    df.to_csv('results/train_set.csv', index=None)

if __name__ == "__main__":
   main()