import pandas as pd

# with open('resources/Top20k.JSON', 'r', encoding='utf-8') as file:
#     data = file.readlines()
#
# with open('resources/Top20k_valid.JSON', 'w', encoding='utf-8') as file:
#     file.write('[')
#     for line in data:
#         if line == '}\n':
#             file.write('},\n')
#         else:
#             file.write(line)
#     file.write(']')

with open('resources/Top20k_valid.JSON', 'r', encoding='utf-8') as file:
    df = pd.read_json(file)

if __name__ == '__main__':
    print(df.head())
    print(df.columns)
    print(df.shape)

    # Ten columns wit NaN values
    df.dropna(axis=1, inplace=True)
    print(df.columns)
    print(df.shape)

    # Drop rows where Bundesland is not BAW
    df = df[(df['Bundesland'] == 'BAW') | (df['Bundesland'] == '')]
    print(df.shape)

    # Only one Zulieferer
    print(df['Zulieferername'].unique())
    print(df['Zuliefererid'].unique())

    # Rename Latitude and Longitude
    df.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}, inplace=True)

    # Check rows where lat and lon are unique
    df.drop_duplicates(subset=['lat', 'lon'], inplace=True)
    print(df.shape)

    # Drop rows where Kursstrasse is not unique
    df.drop_duplicates(subset=['Kursstrasse'], inplace=True)
    print(df.shape)