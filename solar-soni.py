import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def convert_to_datetime(year, doy, ms):
    """
    Convert year, day of year, and milliseconds to a datetime object
    """
    base_date = datetime(year, 1,1)
    doy = int(doy)
    ms = int(ms)

    delta = (timedelta(days = doy-1, milliseconds = ms))
    return base_date + delta

column_specs = [
    (0, 4),    # YEAR
    (5, 9),    # DOY
    (10, 18),  # MS
    (19, 30),  # LOBT
    (31, 40),  # PH1
    (41, 50),  # PH2
    (51, 60),  # PH3
    (61, 70),  # PH4
    (71, 80),  # PH5
    (81, 90),  # PH6
    (91, 100), # PH7
    (101, 110),# PH8
    (111, 120),# PH9
    (121, 130),# PH10
    (131, 140),# AH1
    (141, 150),# AH2
    (151, 160),# AH3
    (161, 170),# AH4
    (171, 180),# AH5
    (181, 190),# AH6
    (191, 200),# AH7
    (201, 210),# AH8
    (211, 220),# AH9
    (221, 230),# AH10
    (231, 236),# PHC1
    (237, 242),# PHC2
    (243, 248),# PHC3
    (249, 254),# PHC4
    (255, 260),# PHC5
    (261, 266),# PHC6
    (267, 272),# PHC7
    (273, 278),# PHC8
    (279, 284),# PHC9
    (285, 290),# PHC10
    (291, 296),# AHC1
    (297, 302),# AHC2
    (303, 308),# AHC3
    (309, 314),# AHC4
    (315, 320),# AHC5
    (321, 326),# AHC6
    (327, 332),# AHC7
    (333, 338),# AHC8
    (339, 344),# AHC9
    (345, 350),# AHC10
    (351, 359),# INT
    (360, 368),# ED2
    (369, 377),# ED3
    (378, 387),# HEDl
    (388, 397),# HEDi
    (398, 407),# HEDh
    (408, 417),# Hpr3sr
    (418, 427),# Hpr1sr
]


column_names = [
        'YEAR', 'DOY', 'MS', 'LOBT', 'PH1', 'PH2', 'PH3', 'PH4', 'PH5', 'PH6', 'PH7',
    'PH8', 'PH9', 'PH10', 'AH1', 'AH2', 'AH3', 'AH4', 'AH5', 'AH6', 'AH7', 'AH8',
    'AH9', 'AH10', 'PHC1', 'PHC2', 'PHC3', 'PHC4', 'PHC5', 'PHC6', 'PHC7', 'PHC8',
    'PHC9', 'PHC10', 'AHC1', 'AHC2', 'AHC3', 'AHC4', 'AHC5', 'AHC6', 'AHC7', 'AHC8',
    'AHC9', 'AHC10', 'INT', 'ED2', 'ED3', 'HEDl', 'HEDi', 'HEDh', 'Hpr3sr', 'Hpr1sr'

]


def read_file(file_path): 
    df = pd.read_fwf(file_path, colspecs=column_specs, header=None)
    df.columns = column_names

    # Create a datetime column
    df['datetime'] = df.apply(lambda row: convert_to_datetime(row['YEAR'], row['DOY'], row['MS']), axis=1)

    return df

files_dir = 'HED-SL2-data'
file_paths = [os.path.join(files_dir, file) for file in os.listdir(files_dir) if file.endswith('.SL2')]

combined_data = pd.concat([read_file(file_path) for file_path in file_paths])

# Select columns for sonification (example: PH1 and PH2 intensity columns)
#selected_data = combined_data[['PH1', 'PH2']]  # Modify as needed
#selected_data = combined_data

# Export the selected data to a CSV file
#selected_data.to_csv('exported_data_for_sonification.csv', index=False)

all_data = combined_data
all_data.set_index('datetime', inplace=True)

# Sort data by datetime (if a datetime column is created)
all_data = all_data.sort_values('datetime')

# Function to plot each column with datetime on x-axis
def plot_columns(data):
    for column in data.columns:
        if column != 'YEAR' and column != 'DOY' and column != 'MS':  # Exclude the original date columns
            plt.figure(figsize=(10, 4))
            plt.plot(data.index, data[column])
            plt.title(column)
            plt.xlabel('Time')
            plt.ylabel('Value')
            plt.xticks(rotation=45)  # Rotate dates for better readability
            plt.tight_layout()  # Adjust layout
            plt.show()

# Plotting all columns
plot_columns(all_data)
