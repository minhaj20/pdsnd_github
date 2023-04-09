import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = [ 'january', 'february', 'march', 'april', 'may' , 'june', 'all']

DAYS = [ 'monday', 'tuesday', 'wednessday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city, month, day = None, None, None
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = getInputAndValidate(city, CITY_DATA, 'Type the name of a city (chicago, new york city, washington)')
    month = getInputAndValidate(month, MONTHS, 'Type the name of a month (all, january, february, ... , june)')
    day = getInputAndValidate(day, DAYS, 'Type the name of a day (all, monday, tuesday, ... sunday)')

    print('-'*40)
    return city, month, day

def getInputAndValidate(item, coll, txtPrompt):
    while item not in coll:
        item = str(input(f'{txtPrompt}: ')).lower()
        if item not in coll: print('Unrecognized value.')
    return item

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
    df = pd.read_csv(CITY_DATA[city], keep_default_na=False)
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    df['hour'] = df['Start Time'].dt.hour
    df['common'] = df['Start Station'] + ' => ' + df['End Station']
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('most common month: {}'.format(MONTHS[df['month'].mode()[0]-1]).title())    

    # TO DO: display the most common day of week
    
    print('most common day of week: {}'.format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    

    # find the most popular hour
    print('most popular hour: {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
   
    print('most commonly used start station: {}'.format( df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    
    print('most commonly used end station: {}'.format( df['End Station'].mode()[0]))
        
    # TO DO: display most frequent combination of start station and end station trip
    
    print('most frequent combination of start station and end station trip: {}'.format(df['common'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    
    print('total travel time: {} seconds'.format(int(df['Trip Duration'].sum())))

    # TO DO: display mean travel time
    
    print('mean travel time: {} seconds'.format(int(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
   
    print('counts of user types:\n{}'.format( df['User Type'].value_counts().to_string()))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print('\ncounts of gender:\n{}'.format( df[df['User Type'] != 'Customer']['Gender'].value_counts().to_string()))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df['BirthYear'] = pd.to_numeric(df[df['User Type'] != 'Customer']['Birth Year'])

        print('earliest year of birth: {}'.format( int(df['BirthYear'].min())))
        print('most recent year of birth: {}'.format( int(df['BirthYear'].max())))
        print('most common year of birth: {}'.format( int(df['BirthYear'].median())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        #city, month, day = 'new york city', 'february', 'tuesday'
        #city, month, day = 'washington', 'june', 'sunday'
        #city, month, day = 'chicago', 'march', 'friday'
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        r = 0
        for r in range(0,df.size,5):
            disp_5rows = str(input('\nWould you like to see 5 lines of raw data? Enter yes or no: ')).lower()
            if disp_5rows.lower() != 'no':
                print(df.iloc[r:r+5])
            else:
                break

        restart = str(input('\nWould you like to restart? Enter yes or no: ')).lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()