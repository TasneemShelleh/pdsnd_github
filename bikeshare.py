import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
valid_months = ['january', 'february', 'march', 'april','may', 'june', 'all']
valid_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','all']

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
    while True:
        city = input("Enter city (chicago, new york city, washington): ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Try again.")


    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter month (january ... june or all): ").strip().lower()
        if month in valid_months:
            break
        else:
            print("Invalid month. Try again.")


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter day (sunday ... saturday or all): ").strip().lower()
        if day in valid_days:
            break
        else:
            print("Invalid day. Try again.")


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        month_index = valid_months.index(month) + 1
        df = df[df['month'] == month_index]
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print("Most Common Month: ",common_month)


    # TO DO: display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    common_day = df['day'].mode()[0]
    print("Most Common Day Of Week: ",common_day)


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("Most Common Start Hour is: ",common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
# Index(['Start Time', 'End Time', 'Trip Duration', 'Start Station',
#        'End Station', 'User Type', 'Gender', 'Birth Year'],
#       dtype='object')
    # TO DO: display most commonly used start station
    comon_start_station = df['Start Station'].mode()[0]
    print("Most Commonly Used Start Station: ",comon_start_station)


    # TO DO: display most commonly used end station
    comon_end_station = df['End Station'].mode()[0]
    print("Most Commonly Used End Station: ",comon_end_station)


    # TO DO: display most frequent combination of start station and end station trip
    freq_comb = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("Most Frequent Combination Of Start Station and End Station Trip",freq_comb)
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total Travel time: ",total_time)


    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Mean Tavel Time: ", mean_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts Of User types:")
    print(user_types)
    print("\n")


    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print("Counts Of Gender:")
        print(gender)


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nEarliest Year Of Birth:", int(df['Birth Year'].min()))
        print("Most Recent Year Of Birth:", int(df['Birth Year'].max()))
        print("Most Common Year Of Birth:",int(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def display_data(df):
    """Display 5 rows of raw data from the filtered DataFrame at a time."""
    start_row = 0
    while True:
        ans = input("Would you like to see 5 lines of raw data? Enter yes or no: ").strip().lower()
        
        if ans == "yes":
            if start_row >= len(df):
               print("No more data to show.")
               break 
            print(df.iloc[start_row:start_row + 5])
            start_row += 5
        elif ans == "no":
            break
        else:
            print("Invalid input. Please enter yes or no.")
        
def main():
    """Main function to run the bikeshare data analysis."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        if df.empty:
            print("No data available for the selected filters. Please try different filters.")
            continue

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
