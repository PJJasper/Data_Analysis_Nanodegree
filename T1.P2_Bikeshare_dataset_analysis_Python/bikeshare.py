import csv
import time
import datetime
from collections import Counter
import pprint
import calendar
import sys

## Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'


def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
        'Would you like to see data for Chicago, New York, or Washington?\n').lower()

    while city not in ['chicago', 'new york', 'washington']:
        print("\nInvalid input: " + city)
        city = input('Please enter Chicago, New York, or Washington.\n').lower()

    print('You have selected ' + city.title())
    if city == 'new york':
        city = 'new_york_city'
    #Could use return eval(city) instead.
    return globals()[city]


def get_time_period():
    '''Asks the user for a time period of month, day or none and returns the
    specified filter.  Assumption is that a filter on day will be a day within
    a particular month.
    Displays a message to show the user which time filter is being applied.

    Args:
        none.
    Returns:
        (str) Time filter - month, day or none .
    '''
    time_period = input('\nWould you like to filter the data by month, day, or not at'
                    ' all? Type "none" for no time filter.\n').lower()
    while time_period not in ['month', 'day', 'none']:
        print("\nInvalid input: " + time_period)
        time_period = input('Please enter month, day or none.\n').lower()
    if time_period == 'none':
        print('You have selected to run statistics on the whole data set')
    else:
        print('You have selected to filter on ' + time_period)
    return time_period



def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        (str) The month to filter the bikeshare data on.
        TODO: fill out return type and description (see get_city for an example)
    '''
    month = input('\nWhich month? January, February, March, April, May, or June?\n').lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
        print("\nInvalid input: " + month)
        month = input('\nPlease enter month: January, February, March, April, May, or June.\n').lower()
    return month


def get_day(month):
    '''Asks the user for a day and returns the specified day.

    Args:
        (str) the month which the day is in.
    Returns:
        (int) The day of the specified month to filter the Bikeshare data on.
    '''
    # 2017 was not a leap year so Feb has 28 days
    cal_dict = {'january':31, 'february':28, 'march':31, 'april':30, 'may':31, 'june':30}
    day = int(float(input('\nWhich day? Please type your response as an integer.\n')))
    while day > cal_dict[month]:
        msg = '\nInvalid input for {}. {} has {} days'.format \
            (month.title(), month.title(), cal_dict[month])
        print(msg)
        day = int(float(input('Please enter the day for your specified month as an integer.\n')))
    return day


def popular_month(city_file, time_period='none'):
    '''
    Takes a list containing the data from the .csv file for the city and returns the month
    with the greatest number of journeys (based on number of start times)
    This function operates over a whole dataset and cannot be filtered.
    Throws a ValueException if bad date format.

    Args:
        (list) the data for the chosen city.
        (str) the time period filtered on by the user. This variable is not required
        for this function.  It has been given a default value of none

    Returns:
        (str) the month with the most journeys

    Question: What is the most popular month for start time?

    '''
    #This function will only be called if there is no time period filter
    month_counts = {'January':0, 'February':0, 'March':0, 'April':0, 'May':0, 'June':0}

    for row in city_file:
        try:
            d = datetime.datetime.strptime(row['Start Time'], "%Y-%m-%d %H:%M:%S")
            #d = datetime.datetime.strptime(row['Start Time'], "%d/%m/%Y %H:%M")
        except ValueError as ve:
            print("WARNING! ", ve)
            print("Please fix the format according to your date settings and rerun program.")
            break
        else:
            month_counts[calendar.month_name[d.month]] += 1
    return max(month_counts, key=lambda key: month_counts[key])


def popular_day(city_file, time_period):
    '''
    Takes a list containing the data from the .csv file for the city and returns the day
    with the greatest number of journeys (based on number of start times)
    This function can be filtered on month or can operate over the whole dataset.

    Args:
        (list) the data for the chosen city.
        (str) the time period filtered on by the user. Either an empty string or a month

    Returns:
        (str) the day on which most jouneys are taken

    Question: What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    '''
    day_counts = {'Monday':0, 'Tuesday':0, 'Wednesday':0, 'Thursday':0, 'Friday':0, 'Saturday':0, 'Sunday':0}

    for row in city_file:
        ftr = filter_for_month(time_period, row, 'Start Time')
        if not ftr: #date didn't match the filter
            continue
            day_counts[ftr.strftime('%A')] += 1
    return max(day_counts, key=lambda key: day_counts[key])


def popular_hour(city_file, month, day):
    '''
    Takes a list containing the data from the .csv file for the city and returns the hour
    of the day with the greatest number of journeys (based on number of start times)
    This function can operate over the whole dataset or can be filtered by month or days
    within a month.
    Question: What is the most popular hour of day for start time?

    Args:
        (list) the data for the chosen city.
        (str) the month filtered on by the user. Empty string if the user is not filtering
        (int) the day of the month filtered on by the user. Empty string if the user is not
              filtering the data, or is only filtering by month.
    Returns:
        (int) the hour of the day when the greatest number of journeys are taken in 24h format
    '''
    #a list with an element for each hour of the day
    hour_counts = [0] * 24
    for row in city_file:
        ftr = filter_for_day_in_month(month, day, row, 'Start Time')
        if ftr: # the date meets the filter or no filter
            # count the hours
            hour_counts[int(ftr.strftime('%H'))] += 1

    #return the position of the max value as this is the hour
    if sum(hour_counts) == 0: #means this day is not in the data
        return "no data"
    return hour_counts.index(max(hour_counts))

def trip_duration(city_file, month, day):
    '''
    Takes a list containing the data from the .csv file for the city and returns the total
    and average trip duration .
    This function can operate over the whole dataset or can be filtered by month or day
    within a month.
    Question: What is the total trip duration and average trip duration?

    Args:
        (list) the data for the chosen city.
        (str) the month filtered on by the user. Empty string if the user is not filtering
        (int) the day of the month filtered on by the user. Empty string if the user is not
              filtering the data, or is only filtering by month.

    Returns:
        (int) the total duration of all journeys in seconds.
        (float) the average duration fo a journey to 2dp. The total / number of journeys
    '''
    total = 0
    row_count = 0
    for row in city_file:
        ftr = filter_for_day_in_month(month, day, row, 'Start Time')
        if ftr:
            # do the calculations now
            total += int(float(row['Trip Duration']))
            row_count += 1
    avg = round(float(total/row_count),2)
    return total, avg


def popular_stations(city_file, month, day):
    '''
    Takes a list containing the data from the .csv file for the city and returns the MOST
    popular start station
    This function can operate over the whole dataset or can be filtered by month or days
    within a month.
    Question: What is the most popular start station and most popular end station?

    Args:
        (list) the data for the chosen city.
        (str) the month filtered on by the user. Empty string if the user is not filtering
        (int) the day of the month filtered on by the user. Empty string if the user is not
              filtering the data, or is only filtering by month.

    Returns:
        (str) the station with the largest number of starting journeys
        (str) the station with the largest number of end journeys
    '''
    start_stations = {}
    end_stations = {}
    for row in city_file:
        ftr = filter_for_day_in_month(month, day, row, 'Start Time')
        if ftr:
            if not row['Start Station'] in start_stations:
                start_stations[row['Start Station']] = 1
            else:
                start_stations[row['Start Station']] += 1
            if not row['End Station'] in end_stations:
                end_stations[row['End Station']] = 1
            else:
                end_stations[row['End Station']] += 1

    max_start = max(start_stations, key=lambda key: start_stations[key])
    max_end = max(end_stations, key=lambda key: end_stations[key])
    return max_start, max_end




def popular_trip(city_file, month, day):
    '''
    Takes a list containing the data from the .csv file for the city and returns the MOST
    popular start station
    This function can operate over the whole dataset or can be filtered by month or days
    within a month.
    Question: What is the most popular trip?

    Args:
        (list) the data for the chosen city.
        (str) the month filtered on by the user. Empty string if the user is not filtering
        (int) the day of the month filtered on by the user. Empty string if the user is not
              filtering the data, or is only filtering by month.

    Returns:
        (str) the common trip, consisting of the start station and the end station

    Question: What is the most popular trip?
    '''
    trips = {}
    for row in city_file:
        trip_str = row['Start Station']+' to '+row['End Station']

        ftr = filter_for_day_in_month(month, day, row, 'Start Time')
        if ftr:
            if not trip_str in trips:
                trips[trip_str] = 1
            else:
                trips[trip_str] += 1
    return max(trips, key=lambda key: trips[key])




def users(city_file, month, day):
    '''
    Takes a list containing the data from the .csv file for the city and returns the
    counts of each user type.
    This function can operate over the whole dataset or can be filtered by month or days
    within a month.
    Question: What are the counts of each user type?

    Args:
        (list) the data for the chosen city.
        (str) the month filtered on by the user. Empty string if the user is not filtering
        (int) the day of the month filtered on by the user. Empty string if the user is not
              filtering the data, or is only filtering by month.

    Returns:
        (dict) user type and count for each user type found in the dataset.

    '''
    user_list = []
    user_types = {}
    for row in city_file:
        ftr = filter_for_day_in_month(month, day, row, 'Start Time')
        if ftr:
            user_list.append(row['User Type'])

    for value in user_list:
        if value == '':
            value = 'Blank'
        if not value in user_types:
            user_types[value] = 1
        else:
            user_types[value] +=1

    return user_types



def gender(city_file, month, day):
    '''
    Takes a list containing the data from the .csv file for the city and returns the
    counts of each Gender
    This function can operate over the whole dataset or can be filtered by month or days
    within a month.
    Question: What are the counts of gender?

    Args:
        (list) the data for the chosen city.
        (str) the month filtered on by the user. Empty string if the user is not filtering
        (int) the day of the month filtered on by the user. Empty string if the user is not
              filtering the data, or is only filtering by month.

    Returns:
        (int) the count of males
        (int) the count of females
        (int) the count of unknowns
    '''
    gender_list = []
    genders = {}
    for row in city_file:
        ftr = filter_for_day_in_month(month, day, row, 'Start Time')
        if ftr:
            gender_list.append(row['Gender'])

    males = len(list(filter(lambda x: x == 'Male', gender_list)))
    females = len(list(filter(lambda x: x == 'Female', gender_list)))
    unknown = len(gender_list)-(males + females)
    return males, females, unknown


def birth_years(city_file, month, day):
    '''
    Takes a list containing the data from the .csv file for the city and returns the
    year of birth for the oldest person, the youngest person and the most most_common
    year of both
    This function can operate over the whole dataset or can be filtered by month or days
    within a month.
    Question: What are the earliest (i.e. oldest user), most recent (i.e. youngest user),
    and most popular birth years?

    Args:
        (list) the data for the chosen city.
        (str) the month filtered on by the user. Empty string if the user is not filtering
        (int) the day of the month filtered on by the user. Empty string if the user is not
              filtering the data, or is only filtering by month.

    Returns:
        (int) the birth year of the oldest person in the dataset
        (int) the birth year of the youngest person in the dataset
        (int) the most frequently occurring birth year.
    '''
    dobs = []
    for row in city_file:
        ftr = filter_for_day_in_month(month, day, row, 'Start Time')
        if ftr:
            # remove blanks
            if len(row['Birth Year']) >0:
                dobs.append(int(float(row['Birth Year'])))
    oldest = min(dobs)
    youngest = max(dobs)
    most_freq = Counter(dobs).most_common(1)[0][0]
    return oldest, youngest, most_freq


def display_data(city_file):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        (list) the data for the chosen city.
    Returns:
        None
    '''
    display = input('\nWould you like to view individual trip data?'
                    ' Type \'yes\' or \'no\'.\n')

    while display not in ['yes', 'no']:
        print("\nInvalid input: " + display)
        display = input('Please enter yes or no.\n').lower()
    iter_list = iter(city_file)
    while display.lower() == 'yes':
        count = 1
        for val in iter_list:
            pprint.pprint(val)
            if count == 5:
                display = input('\nWould you like to view individual trip data?'
                        ' Type \'yes\' or \'no\'.\n')
                while display not in ['yes', 'no']:
                    print("\nInvalid input: " + display)
                    display = input('Please enter yes or no.\n').lower()
                break
            count += 1


def read_file(filename):
    '''
    Loads a csv file containing the Bikeshare data for Chicago,
    New York City or Washington. The data is loaded into a DictReader iterator
    and is converted into a list of dictionaries

    Args:
        (string) the filename of the Bikeshare data to be read.

    Returns:
        (list of dictionaries) the data of the specified file

    Question: What is the most popular month for start time?

    '''
    print("Opening", filename, "...")
    data = []
    with open(filename, newline='') as f:
        data = list(csv.DictReader(f))
    return data

def filter_for_month(month, row, column):
    '''
    Helper function to provide a filter which filters data by  month.
    Throws a ValueException and exits the program if date format is not correct.
    Code has been implemented in this way in case UK date settings cause a prolem
    with a review in the US.

    Args:
        (str) the month to be filtered on.  Empty string if no filter.
        (iterator) the line of data
        (string) the name of the column where the date filter will be applied.

    Returns:
        (datetime) if the datetime meets the filter condition, empty string if it
        doesn't
    '''
    try:
        #d = datetime.datetime.strptime(row[column], "%d/%m/%Y %H:%M")
        d = datetime.datetime.strptime(row['Start Time'], "%Y-%m-%d %H:%M:%S")
    except ValueError as ve:
        print("WARNING! ", ve)
        print("Please fix the format according to your settings and rerun program.")
        sys.exit(0)
    else:
        if d.strftime('%B').lower() == month or month == '':
            return d
        else:
            return ''


def filter_for_day_in_month(month, day, row, column):
    '''
    Helper function to provide a filter that filters datat for a specified
    day within a specified month.
    Throws a ValueException and exits the program if date format is not correct.
    Code has been implemented in this way in case UK date settings cause a prolem
    with a review in the US.

    Args:
        (str) the month to be filtered on.  Empty string if no filter.
        (str) the day to be filtered on.  Empty string if no filter.
        (iterator) the line of data
        (string) the name of the column where the date filter will be applied.

    Returns:
        (datetime) if the datetime meets the filter condition, empty string if it
        doesn't
    '''
    try:
        #d = datetime.datetime.strptime(row[column], "%d/%m/%Y %H:%M")
        d = datetime.datetime.strptime(row['Start Time'], "%Y-%m-%d %H:%M:%S")
    except ValueError as ve:
        print("WARNING! ", ve)
        print("Please fix the format according to your settings and rerun program")
        sys.exit(0)
    else:
        if day: #if filtering on day both day and month conditions much match
            #ignore everything that isn't the day and month combination
            if month != d.strftime('%B').lower():
                return ''
            else: # month does match, check on day now
                if day != int(d.strftime('%d')):
                    return ''
                elif month: #only the month needs to match
                    # ignore everything that isn't for that month
                    if month != d.strftime('%B').lower():
                        return ''
        return d


def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()

    #load the file
    city_data = read_file(city)
    print("The file has ", len(city_data), "rows of data")

    # Filter by time period (month, day, none)
    time_period = get_time_period()
    month, day = '', ''
    if time_period.lower() != 'none':
        month = get_month()
        if time_period.lower() == 'day':
            day = get_day(month)

    print('Calculating the first statistic...')

    # What is the most popular month for start time?
    if time_period == 'none':
        start_time = time.time()
        print('start time ' , start_time)
        print("\nTHE MOST POPULAR MONTH IS: ",popular_month(city_data, time_period))
        print("\nThat took %s seconds." % (time.time() - start_time))
        print("Calculating the next statistic...")

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()

        print("\nTHE MOST POPULAR DAY IS: ", popular_day(city_data, month))
        print("\nThat took %s seconds." % (time.time() - start_time))
        print("Calculating the next statistic...")

    start_time = time.time()

    # What is the most popular hour of day for start time?
    print("\nTHE MOST POPULAR HOUR IS: ", popular_hour(city_data, month, day),"h")
    print("\nThat took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    total, avg = trip_duration(city_data, month, day)
    msg = "\nTHE TOTAL TRIP DURATION IS: {} seconds. THE AVERAGE TRIP DURATION IS: {} seconds." \
        .format(total, avg)
    print(msg)
    print("In other words: ", str(datetime.timedelta(seconds = total)), \
            " and ", str(datetime.timedelta(seconds = avg)))

    print("\nThat took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    start, end = popular_stations(city_data, month, day)
    msg ="\nTHE MOST POPULAR START STATION IS {}\nTHE MOST END STATION IS {}".format(start,end)
    print(msg)
    print("\nThat took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular trip?
    print("\nTHE MOST POPULAR TRIP IS ", popular_trip(city_data, month, day))
    print("\nThat took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")

    start_time = time.time()

    # What are the counts of each user type?
    print("THE USER TYPE COUNTS ARE: ")
    user_counts = users(city_data, month, day)
    for item in user_counts:
        print(item, user_counts[item])
    print("\nThat took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")

    start_time = time.time()

    # What are the counts of gender?
    if 'Gender' in city_data[0]: # not available for all cities
        males, females, unknown = gender(city_data, month, day)
        msg = "\nCOUNT OF MALES: {}, FEMALES: {}, UNKNOWN: {}".format(males, females, unknown)
        print(msg)
        print("\nThat took %s seconds." % (time.time() - start_time))
        print("Calculating the next statistic...")
    else:
        print("No data for Gender statistic. Skipping ...")


    start_time = time.time()
    # What are the earliest (i.e. oldest user), most recent (i.e. youngest user), and
    # most popular birth years?
    if 'Birth Year' in city_data[0]: # not available for all cities
        oldest, youngest, frequent = birth_years(city_data, month, day)
        print("\nTHE BIRTH YEAR OF THE OLDEST USER IS ", oldest)
        print("\nTHE BIRTH YEAR OF THE YOUNGEST USER IS ", youngest)
        print("\nTHE MOST FREQUENTLY OCCURRING BIRTH YEAR IS ", frequent)
        print("\nThat took %s seconds." % (time.time() - start_time))
    else:
        print("No data for Birth Year statistic. Skipping ...")

    # Display five lines of data at a time if user specifies that they would like to
    display_data(city_data)

    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n').lower()
    while restart not in ['yes', 'no', 'none']:
        restart = input("\nInvalid input: Type \'yes\' or \'no\'")
    if restart.lower() == 'yes':
        statistics()
    else:
        print("Exiting")



if __name__ == "__main__":
    statistics()
