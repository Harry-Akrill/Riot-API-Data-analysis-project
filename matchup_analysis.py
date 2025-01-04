import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from scipy.stats import spearmanr
from pathlib import Path

data_dir = Path(r"D:\Projects\riot_api_work\akkers_example_code\data")

eu_files = [
    "Odoamne_DATA",
    "septico1_DATA",
    "Spoodersussi v3_DATA",
    "TheShackledOne_DATA"
]

kr_files = [
    "God Thunder_DATA",
    "해 태_DATA",
    "wnrflach_DATA",
    "This game canwin_DATA",
    "아리마 카나_DATA",
    "dydwns7667_DATA",
    "emo jian ke_DATA",
    "Kingen_DATA",
    "강하다 별_DATA",
    "天下 第一_DATA",
    "Casting_DATA"
]

def combine_csv_files(file_list, data_dir):
    data_frames = [pd.read_csv(data_dir / file) for file in file_list]
    return pd.concat(data_frames, ignore_index=True)

eu_df = combine_csv_files(eu_files, data_dir)
eu_df.to_csv(data_dir / "COMBINED_EUW_DATA.csv", index=False)

kr_df = combine_csv_files(kr_files, data_dir)
kr_df.to_csv(data_dir / "COMBINED_KR_DATA.csv", index=False)

total_df = pd.concat([eu_df, kr_df], ignore_index=True)
total_df.to_csv(data_dir / "COMBINED_OVERALL_DATA.csv", index=False)

def plot_logistic_regression(data, feature_col, target_col):
 
    X = data[[feature_col]] 
    y = data[target_col]    
    
    model = LogisticRegression()
    model.fit(X, y)
    
    X_range = np.linspace(data[feature_col].min(), data[feature_col].max(), 300).reshape(-1, 1)
    
    predicted_probabilities = model.predict_proba(X_range)[:, 1] 
    
    plt.figure(figsize=(8, 6))
    
    sns.scatterplot(x=feature_col, y=target_col, data=data, s=100, color='blue', label='Actual Data')
    
    plt.plot(X_range, predicted_probabilities, color='red', label='Logistic Regression')
    
    plt.xlabel(f'{feature_col}')
    plt.ylabel(f'{target_col} (1 = Win, 0 = Loss)')
    plt.title(f'Logistic Regression: {feature_col} vs {target_col}')

    plt.legend()
    plt.show()

#example usage
plot_logistic_regression(kr_df, 'golddiff14min', 'win')

def spearmansRank(df,stat1,stat2):

    corr, p_value = spearmanr(df[stat1], df[stat2])

    print(f'Spearman correlation: {corr:.3f}, p-value: {p_value:.3f}')

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=stat1, y=stat2, data=df, s=100, color='blue')
    plt.xlabel(stat1)
    plt.ylabel(stat2)
    plt.title(f'Scatter Plot: ' + stat1 + ' vs '  + stat2 + '\nSpearman Correlation: {corr:.3f}')
    plt.show()

    df[stat1 + '_rank'] = df[stat1].rank()
    df[stat2 + '_rank'] = df[stat2].rank()

    plt.figure(figsize=(8, 6))
    sns.lineplot(x=stat1 + '_rank', y=stat2 + '_rank', data=df, marker="o")
    plt.xlabel('Rank of ' + stat1)
    plt.ylabel('Rank of ' + stat2)
    plt.title(f'Rank Plot:  ' + stat1 + ' vs '  + stat2 + '\nSpearman Correlation: {corr:.3f}')
    plt.show()

def matchup_analysis(df, champX, champY):
    champion_x = champX
    champion_y = champY

    matchup_data = df[(df['champion'] == champion_x) & (df['opponentChampion'] == champion_y)]

    if len(matchup_data) > 0:
        avg_csdiff14 = matchup_data['csdiff14min'].mean()
        avg_golddiff14 = matchup_data['golddiff14min'].mean()
        avg_xpdiff14 = matchup_data['xpDiff14'].mean()
        win_rate = matchup_data['win'].mean()  

        print(f"Matchup: {champion_x} vs {champion_y}")
        print(f"Number of times Matchup played: {len(matchup_data)}")
        print(f"Average CS Difference at 14 min: {avg_csdiff14}")
        print(f"Average Gold Difference at 14 min: {avg_golddiff14}")
        print(f"Average XP Difference at 14 min: {avg_xpdiff14}")
        print(f"Win Rate for {champion_x} in this matchup: {win_rate * 100:.2f}%")

        plt.figure(figsize=(8, 6))
        sns.barplot(x=['CS Difference', 'Gold Difference', 'XP Difference'], 
                    y=[avg_csdiff14, avg_golddiff14, avg_xpdiff14])
        plt.title(f'Early-Game Advantage for {champion_x} vs {champion_y}')
        plt.ylabel('Average Difference at 14 minutes')
        plt.show()

    else:
        print(f"No data available for the matchup {champion_x} vs {champion_y}.")

#example usage
matchup_analysis(total_df, 'KSante', 'Rumble')