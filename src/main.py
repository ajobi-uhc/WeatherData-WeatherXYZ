import load as ld
import numpy as np
import sys


def main():
    file_path = 'data/data_temperature.txt'
    structured_array = ld.load_data_and_calculate_statistics(file_path)

    file_path = 'data/Paris_data_climate.txt'
    structured_array_paris = ld.load_paris_weather_data(file_path)
    print("Correlation between Max Temp and CO2 in Paris", ld.calculate_correlation(structured_array_paris, 'Max Temperature (C)', 'CO2 Levels (ppm)'))
    # Calculations using NumPy
    statistics = {
        'Average Max Temperature': np.mean(structured_array['Max Temperature (C)']),
        'Average Min Temperature': np.mean(structured_array['Min Temperature (C)']),
        'Total Precipitation': np.sum(structured_array['Precipitation (mm)']),
        'Max Wind Speed': np.max(structured_array['Wind Speed (km/h)']),
        'Min Wind Speed': np.min(structured_array['Wind Speed (km/h)'])
    }
    print(statistics)
    if len(sys.argv) > 1:
        city_input = sys.argv[1]
        data = False
        graph_temp = False
        stats = False            
        if len(sys.argv) > 2:
            if sys.argv[2] == 'data':
                data = True
            elif sys.argv[2] == 'graph_temp':
                graph_temp = True
            elif sys.argv[2] == 'stats':
                stats = True
        ld.display_city_weather(structured_array, city_input, data, graph_temp, stats)
    else:
        print("No city name provided as command-line argument.")
    


main()