import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import numpy as np
import cProfile as cP

def main():
    df_raw = pd.read_json('data\matchDetails_2024-01-22.json', convert_axes=False)
    df = df_raw.transpose() # Make Match ID the rows instead of columns

    # Create Database from first transposed entry
    df2 = pd.DataFrame([df.iloc[0][0]])

    # Add Match ID as a column
    match_id = df.iloc[0].name
    print(match_id)
    df2['match_id'] = df.iloc[0].name
    for i in range(len(df.columns) - 1):
        df2 = df2._append(df.iloc[0][i + 1], ignore_index=True)
        df2.at[i + 1, 'match_id'] = df.iloc[0].name
    # print(df2)

    # Retrieve Columns for Database Dictionary
    column_names = []
    for col in df2.columns:
        column_names.append(col)
    arr = df2[column_names].values

    dfs = []

    # Loop through the transposed database
    for i in range(80):
        match_id = df.iloc[i].name
        # print(match_id)
        add_df = pd.DataFrame(columns=column_names)
        game = df.iloc[i]
        for j in range(len(df2)):
            add_df = add_df._append(game[j], ignore_index=True)
            add_df.at[j, 'match_id'] = match_id
        # print(add_df)
        add_df = add_df.copy()
        dfs.append(add_df)

    #df_final = df2[0:0]

    df_final = pd.concat(dfs, ignore_index=True)
    df_final.to_excel("output.xlsx")

cP.run('main()', 'cProfile.prof')