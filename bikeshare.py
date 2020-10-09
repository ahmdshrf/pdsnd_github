import time
import pandas as pd
import numpy as np
import datetime as dt
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']

days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True :
        city = input("\nFor what city(ies) do you want do select data, "
                      "New York City, Chicago or Washington? Use commas "
                      "to list the names.\n>").lower()
        if city == "chicago" or city == "new york city" or city == 'washington':
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        decsion = input("Would you like to filter the data by month, day, both, or not all all? Type \"none\" for no time filter.\n>").lower()
        if decsion == 'day' or decsion == 'month' or decsion == 'both':
            break
    if decsion == 'month':
        while True:
            month = input("\nFrom January to June, for what month(s) do you "
                       "want do filter data? Use commas to list the names.\n>").lower()
            if month in months:
                break
        day = days
    elif decsion =='day':
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            day = input("\nFor what weekday(s) do you want do filter bikeshare "
                     "data? Use commas to list the names.\n>").lower()
            if day in days:
                break
        month = months
    elif decsion == 'both':
        while True:
            month = input("\nFrom January to June, for what month(s) do you "
                       "want do filter data? Use commas to list the names.\n>").lower()
            if month in months:
                break
        while True:
            day = input("\nFor what weekday(s) do you want do filter bikeshare "
                     "data? Use commas to list the names.\n>").lower()
            if day in days:
                break
    else:
        return


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)
        # reorganize DataFrame columns after a city concat
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] ==
                                            (months.index(month) + 1)], month))
    else:
        df = df[df['Month'] == (months.index(month) + 1)]
    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] ==
                                          (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]
    print('-' * 40)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months_index = df['Month']
    most_com_month = months_index.mode()[0]
    print('The month with the most travels is: ' +
          str(months[most_com_month - 1]).title() + '.')

    # TO DO: display the most common day of week
    days_index = df['Weekday']
    most_com_day = days_index.mode()[0]
    print('The day with the most travels is: ' +
          str(most_com_day) + '.')

    # TO DO: display the most common start hour
    most_com_hour = df['Start Hour'].mode()[0]
    print('The most common start hour is: ' +
          str(most_com_hour).title() + '.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_com_start_station = df['Start Station'].mode()[0]
    print('The most common start station is: {}.'.format(str(most_com_start_station)))

    # TO DO: display most commonly used end station
    most_com_end_station = df['End Station'].mode()[0]
    print('The most common end station is: {}.'.format(str(most_com_end_station)))


    # TO DO: display most frequent combination of start station and end station trip
    df['Start - End station'] = df['Start Station'] + '-' + df['End Station']
    most_com_start_end_station = df['Start - End station'].mode()[0]
    print('The most common start - end station is: {}.'.format(str(most_com_start_end_station)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    total_time = (str(int(total_time // 86400)) + 'd ' + str(int((total_time % 86400) // 3600)) +
     'h ' + str(int(((total_time % 86400) % 3600) // 60)) + 'm ' + str(int(((total_time % 86400) % 3600) % 60)) + 's')
    print('The total travel time: {}.'.format(str(total_time)))


    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_time = (str(int(mean_time // 60)) + 'm ' +
                        str(int(mean_time % 60)) + 's')
    print("The mean of travel time: {}.".format(mean_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_counts = df['User Type'].value_counts().to_string()
    print('Distribution for user types:{}.'.format(user_counts))

    # TO DO: Display counts of gender
    try:
        gender_counter = df['Gender'].value_counts().to_string()
        print("\nDistribution for each gender:{}".format(gender_counter))
    except KeyError:
        print("We're sorry! There is no data of user genders for {}."
              .format(city.title()))


    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nFor the selected filter, the oldest person to ride one "
              "bike was born in: {}".format(earliest_birth_year))
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("For the selected filter, the youngest person to ride one "
              "bike was born in: {}".format(most_recent_birth_year))
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("For the selected filter, the most common birth year amongst "
              "riders is: {}".format(most_common_birth_year))
    except:
        print("We're sorry! There is no data of birth year for {}."
              .format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):

    count = 0

    while True:
        answer = input('Would you like to see 5 lines of raw data? Enter yes or no: ')
        # Check if response is yes, print the raw data and increment count by 5
        if answer == 'yes':
            for i in range(count, len(df.index)):
                print("\n")
                print(df.iloc[count:count+5].to_string())
                print("\n")
                count += 5

                if input("Do you want to keep printing raw data?"
                      "\n\n[y]Yes\n[n]No\n\n>").lower() == 'y':
                    continue
                else:
                    break
        # otherwise break while True:
        else:
            break  


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        while True:
            select_data = input("\nPlease select the information you would "
                                 "like to obtain.\n\n [ts] Time Stats\n [ss] "
                                 "Station Stats\n [tds] Trip Duration Stats\n "
                                 "[us] User Stats\n [rd] Display Raw Data\n [r] Restart\n\n>").lower()
            if select_data == 'ts':
                time_stats(df)
            elif select_data == 'ss':
                station_stats(df)
            elif select_data == 'tds':
                trip_duration_stats(df)
            elif select_data == 'us':
                user_stats(df, city)
            elif select_data == 'rd':
                raw_data(df)
            elif select_data == 'r':
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
