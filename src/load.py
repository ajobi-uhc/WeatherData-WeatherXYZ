import numpy as np
import matplotlib.pyplot as plt
import numpy.lib.recfunctions as rfn

# Function to load data from a file and calculate statistics
def load_data_and_calculate_statistics(file_path):
    # Define the data type for the structured array
    dtype = [('Date', 'U10'), ('Location', 'U50'), ('Max Temperature (C)', 'f8'), 
             ('Min Temperature (C)', 'f8'), ('Precipitation (mm)', 'f8'), 
             ('Wind Speed (km/h)', 'f8'), ('Humidity (%)', 'f8'), ('Cloud Cover (%)', 'f8')]

    # Read and parse the file
    data = []
    with open(file_path, 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            fields = line.strip().split(',')
            data.append(tuple(fields))


    # Convert the list of tuples into a structured NumPy array
    structured_array = np.array(data, dtype=dtype)
    categories = np.array([categorize_day((day['Max Temperature (C)'] + day['Min Temperature (C)']) / 2) for day in structured_array])
    structured_array = rfn.append_fields(structured_array, 'Day Category', data=categories, usemask=False)
    return structured_array


def load_paris_weather_data(file_path):
    dtype = [
        ('Date', 'U10'), 
        ('Location', 'U50'), 
        ('Max Temperature (C)', 'f8'), 
        ('Min Temperature (C)', 'f8'), 
        ('Precipitation (mm)', 'f8'), 
        ('Wind Speed (km/h)', 'f8'), 
        ('Humidity (%)', 'f8'), 
        ('Cloud Cover (%)', 'f8'),
        ('CO2 Levels (ppm)', 'f8'),
        ('Sea Level Rise (mm)', 'f8')
    ]

    data = []
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            fields = line.strip().split(',')
            data.append(tuple(fields))

    structured_array = np.array(data, dtype=dtype)
    return structured_array


def calculate_and_display_city_statistics(structured_array):
    cities = np.unique(structured_array['Location'])
    
    for city in cities:
        city_data = structured_array[structured_array['Location'] == city]
        
        # Calculating statistics
        avg_max_temp = np.mean(city_data['Max Temperature (C)'])
        avg_min_temp = np.mean(city_data['Min Temperature (C)'])
        total_precipitation = np.sum(city_data['Precipitation (mm)'])
        max_wind_speed = np.max(city_data['Wind Speed (km/h)'])
        min_wind_speed = np.min(city_data['Wind Speed (km/h)'])

        # Displaying statistics
        print(f"Statistics for {city}:")
        print(f"  Average Max Temperature: {avg_max_temp:.2f}°C")
        print(f"  Average Min Temperature: {avg_min_temp:.2f}°C")
        print(f"  Total Precipitation: {total_precipitation:.2f} mm")
        print(f"  Max Wind Speed: {max_wind_speed:.2f} km/h")
        print(f"  Min Wind Speed: {min_wind_speed:.2f} km/h")
        print("-" * 40)

def display_city_weather(structured_array, city_name, data, graph_temp, stats):
    if city_name in structured_array['Location']:
        if data == True:
            city_data = structured_array[structured_array['Location'] == city_name]
            print(f"Weather statistics for {city_name}:\n")
            print(f"{'Date':<15}{'Max Temp (C)':<15}{'Min Temp (C)':<15}{'Precipitation (mm)':<20}{'Wind Speed (km/h)':<20}{'Humidity (%)':<15}{'Cloud Cover (%)':<20}{'Day Category':<20}")
            print("-" * 150)
            for record in city_data:
                print(f"{record['Date']:<15}{record['Max Temperature (C)']:<15.2f}{record['Min Temperature (C)']:<15.2f}{record['Precipitation (mm)']:<20.2f}{record['Wind Speed (km/h)']:<20.2f}{record['Humidity (%)']:<15.2f}{record['Cloud Cover (%)']:<20.2f}{record['Day Category']:<15}")
        if graph_temp == True:
            plot_temperature_over_time(structured_array, city_name)
        if stats == True:
            find_extreme_days_by_city(structured_array, city_name)
    else:
        print(f"City '{city_name}' not found in the dataset.")

def plot_temp_vs_co2(structured_array_paris):
    dates = structured_array_paris['Date']
    plt.figure(figsize=(10, 5))
    plt.plot(dates, structured_array_paris['CO2 Levels (ppm)'], label='CO2 Levels (ppm)', marker='o')
    plt.title('CO2 Levels Over Time in Paris')
    plt.xlabel('Date')
    plt.ylabel('CO2 Levels (ppm)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.savefig('co2_levels_over_time_paris.png')
    plt.show()

    # Sea Level Rise over Time
    plt.figure(figsize=(10, 5))
    plt.plot(dates, structured_array_paris['Sea Level Rise (mm)'], label='Sea Level Rise (mm)', color='green', marker='o')
    plt.title('Sea Level Rise Over Time in Paris')
    plt.xlabel('Date')
    plt.ylabel('Sea Level Rise (mm)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.savefig('sea_level_rise_over_time_paris.png')
    plt.show()

    # Precipitation over Time
    plt.figure(figsize=(10, 5))
    plt.plot(dates, structured_array_paris['Precipitation (mm)'], label='Precipitation (mm)', color='blue', marker='o')
    plt.title('Precipitation Over Time in Paris')
    plt.xlabel('Date')
    plt.ylabel('Precipitation (mm)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.savefig('precipitation_over_time_paris.png')
    plt.show()

def calculate_correlation(structured_array, var1, var2):
    correlation_matrix = np.corrcoef(structured_array[var1], structured_array[var2])
    return correlation_matrix[0, 1]


def plot_temperature_over_time(structured_array, city):
    
        city_data = structured_array[structured_array['Location'] == city]
        dates = city_data['Date']
        max_temps = city_data['Max Temperature (C)']
        min_temps = city_data['Min Temperature (C)']

        plt.figure(figsize=(10, 5))
        plt.plot(dates, max_temps, label='Max Temperature (C)', marker='o')
        plt.plot(dates, min_temps, label='Min Temperature (C)', marker='o')
        plt.title(f'Temperature Over Time in {city}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (C)')
        plt.xticks(rotation=45)
        plt.legend()
        plt.show()

def plot_average_temperature_comparison(structured_array):
    # Compute average temperature for each city
    cities = np.unique(structured_array['Location'])
    avg_temps = []
    for city in cities:
        city_data = structured_array[structured_array['Location'] == city]
        avg_temp = np.mean((city_data['Max Temperature (C)'] + city_data['Min Temperature (C)']) / 2)
        avg_temps.append(avg_temp)

    # Plotting bar chart
    plt.figure(figsize=(10, 5))
    plt.bar(cities, avg_temps, color='skyblue')
    plt.title('Average Temperature Comparison Between Cities')
    plt.xlabel('City')
    plt.ylabel('Average Temperature (C)')
    plt.xticks(rotation=45)
    plt.show()


def categorize_each_day(structured_array):
    day_categories = {}
    for record in structured_array:
        avg_temp = (record['Max Temperature (C)'] + record['Min Temperature (C)']) / 2
        category = categorize_day(avg_temp)
        day_categories[record['Date']] = category
    return day_categories

def categorize_day(avg_temp):
    if avg_temp <= 10:
        return 'Cold'
    elif 10 < avg_temp <= 20:
        return 'Moderate'
    else:
        return 'Warm'


def categorize_days_for_all_cities(structured_array):
    cities = np.unique(structured_array['Location'])
    city_categories = {}
    for city in cities:
        city_data = structured_array[structured_array['Location'] == city]
        avg_temp = np.mean((city_data['Max Temperature (C)'] + city_data['Min Temperature (C)']) / 2)
        category = categorize_day(avg_temp)
        city_categories[city] = category
    return city_categories


def categorize_day(avg_temp):
    if avg_temp <= 10:  # Threshold for 'Cold'
        return 'Cold'
    elif 10 < avg_temp <= 20:  # Threshold for 'Moderate'
        return 'Moderate'
    else:
        return 'Warm'

def find_extreme_days_by_city(structured_array, city):
    city_data = structured_array[structured_array['Location'] == city]
    hottest_day_index = np.argmax(city_data['Max Temperature (C)'])
    coldest_day_index = np.argmin(city_data['Min Temperature (C)'])
    hottest_day = city_data[hottest_day_index]
    coldest_day = city_data[coldest_day_index]
    return {
        'Hottest Day': hottest_day,
        'Coldest Day': coldest_day
    }

def find_extreme_days_for_all_cities(structured_array):
    cities = np.unique(structured_array['Location'])
    extremes = {}
    for city in cities:
        extremes[city] = find_extreme_days_by_city(structured_array, city)
    return extremes


