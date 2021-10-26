from utils.globals import *
import os
import pandas as pd


def main():
    # get all housing files
    pums_files = [file for file in os.listdir(PUMS_CSV_FILE_DIRECTORY)
                  if 'h' in file]
    combined_df = None
    for pums_csv in pums_files:
        print(f"Analyzing {pums_csv}", end='')
        # open csv
        with open(os.path.join(PUMS_CSV_FILE_DIRECTORY, pums_csv)) as df_file:
            df = pd.read_csv(df_file, low_memory=False)
        # create a geoid from state code and puma code (leading zeros are critical here)
        geoid = df['ST'].map('{:02d}'.format) + df['PUMA'].map('{:05d}'.format)
        # move geoid column to the front
        df.insert(0, 'GEOID', geoid)
        # group by geoid and count rows
        df_count = df.groupby('GEOID').size().to_frame('size').reset_index()
        # combine dataframe with all previous dfs
        if combined_df is None:
            combined_df = df_count
        else:
            combined_df = pd.concat([combined_df, df_count], axis=0)
        print(" ... done!")
    print("Exporting to 'pums.csv'")
    # export to csv
    combined_df.to_csv(os.path.join(PUMS_CSV_FILE_DIRECTORY, 'pums.csv'), index=False)


if __name__ == '__main__':
    main()
