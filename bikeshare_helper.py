#   Udacity Programming for Datascience with Python Nanodegree
#   Project: US bikeshare
#   By: Anuradha Pani
#   File: 'bikeshare_helper.py' contains all the helper functions
# #############################################################################

import time
import pandas as pd
import numpy as np
import dash_table
import dash_bootstrap_components as dbc
import plotly.express as px


# Global variables and data structures
# Data File Dictionary
CITY_DATA = {'chicago': 'chicago.csv',
             'nyc': 'new_york_city.csv',
             'washington': 'washington.csv'}

# City Name: required to conditionally display additional user stats
# Loaded after user filter selections
CITY = ""

# Counter to keep track of the rows of raw data to display
ROW_COUNTER = 0
ROW_ADVANCE = 5

# Main DataFrame
# Loaded after user filter selections
DF = pd.DataFrame()



# #############################################################################
# Function definitions
def load_data(city, month, weekday):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'none' to apply no month filter
        (str) weekday - name of the day of week to filter by, or 'none'to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    try:
        # Load city data into DataFrame
        df = pd.read_csv(CITY_DATA[city])

        # Convert start and end times to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])

        # Create three new columns, 'Month', 'Weekday' and 'Hour'
        # based one the 'Start Time' column
        df['Month'] = df['Start Time'].dt.month_name()
        df['Weekday'] = df['Start Time'].dt.day_name()
        df['Hour'] = df['Start Time'].dt.hour

        # Filter data depending on filter choices
        # Filter by month
        if month != 'none':
            df = df[df['Month'] == month.title()]

        # Filter by weekday
        if weekday != 'none':
            df = df[df['Weekday'] == weekday.title()]
        return df
    except Exception as e:
        print("Some error occurred in load_data(): {}".format(e))
# #############################################################################


# Create Table
"""
Creates a Dash Bootstrap Table

Args:
    (list) rows - list of rows for the dataframe
    (list) column_names - list of column names
Returns:
    (dbc.table) table - dash_bbotstrap_components table
"""
def create_dbc_table(rows, column_names):
    rdf = pd.DataFrame(rows, columns=column_names)
    # Create data table
    table = dbc.Table.from_dataframe(rdf,
                                     dark=True,
                                     striped=True,
                                     bordered=True,
                                     hover=True,
                                     style={'color': 'white'})
    return table
# #############################################################################



# TIME STATS
def time_stats(df):
    """
    Computes the time based statistics for the Time Tab display
    Args:
        (pd.DataFrame) df - dataframe used for the computations
    Returns:
        (list) output_list - output list containing return values for
                            application layout components
    """
    output_list = []
    column_names = ['Metric', 'Result', 'Count']
    rdf_rows = []

    start_time = time.time()
    # display the most common month
    most_common_month = df['Month'].mode()[0]
    month_count = df['Month'].value_counts().values[0]
    data_row = ['Most common month', most_common_month, month_count]
    rdf_rows.append(data_row)

    # display the most common day of week
    most_common_weekday = df['Weekday'].value_counts().index[0]
    day_count = df['Weekday'].value_counts().values[0]
    data_row = ['Most common weekday', most_common_weekday, day_count]
    rdf_rows.append(data_row)

    # display the most common start hour
    most_common_hour = df['Hour'].value_counts().index[0]
    hour_count = df['Hour'].value_counts().values[0]
    data_row = ['Most common hour', most_common_hour, hour_count]
    rdf_rows.append(data_row)

    # execution time
    time_taken = "This computation took {} seconds.".format(round((time.time() - start_time), 4))

    # Create a result data frame and add it to the output list
    time_table = create_dbc_table(rdf_rows, column_names)
    output_list.append("Popular Times of Travel:")
    output_list.append(time_table)
    output_list.append(time_taken)
    return output_list
# #############################################################################



# STATION STATS
def station_stats(df):
    """
    Computes statistics on the most popular stations and trips
    Args:
        (pd.DataFrame) df - dataframe used for the computations
    Returns:
        (list) output_list - output list containing return values for
                            application layout components
    """
    output_list = []
    column_names = ['Metric', 'Result', 'Count']
    rdf_rows = []

    start_time = time.time()
    # Most popular start station
    most_common_start = df['Start Station'].value_counts().index[0]
    start_count = df['Start Station'].value_counts().values[0]
    data_row = ['Most popular Start Station', most_common_start, start_count]
    rdf_rows.append(data_row)

    # display most popular end station
    most_common_end = df['End Station'].value_counts().index[0]
    end_count = df['End Station'].value_counts().values[0]
    data_row = ['Most popular End Station', most_common_end, end_count]
    rdf_rows.append(data_row)

    # display most frequent combination of start station and end station trip
    most_popular_trip = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    most_popular_start = most_popular_trip.index[0][0]
    most_popular_end = most_popular_trip.index[0][1]
    start_end_count = most_popular_trip[0]

    # execution time
    time_taken = "This computation took {} seconds.".format(round((time.time() - start_time), 4))

    data_row = ['Most popular Start & End Station Combo',
                most_popular_start + " AND " + most_popular_end,
                start_end_count]
    # Create data table
    rdf_rows.append(data_row)
    station_table = create_dbc_table(rdf_rows, column_names)

    output_list.append("Popular Stations and Trips: ")
    output_list.append(station_table)
    output_list.append(time_taken)
    return output_list
# #############################################################################


# TRIP DURATION STATS
def trip_duration_stats(df):
    """
    Computes statistics on the total and average trip duration.
    Args:
        (pd.DataFrame) df - dataframe used for the computations
    Returns:
        (list) output_list - output list containing return values for
                            application layout components
    """
    output_list = []
    column_names = ['Metric', 'Result']
    rdf_rows = []

    start_time = time.time()
    # display total travel time
    total_trip_time = df['Trip Duration'].sum()
    data_row = ['Total Trip Time',
                str(pd.to_timedelta(total_trip_time, unit='s'))
                ]
    rdf_rows.append(data_row)

    # display mean travel time
    avg_trip_time = df['Trip Duration'].mean()
    data_row = ['Average Trip Time',
                str(pd.to_timedelta(avg_trip_time, unit='s'))
                ]
    rdf_rows.append(data_row)

    # execution time
    time_taken = "This computation took {} seconds.".format(round((time.time() - start_time), 4))

    # Create data table
    trip_table = create_dbc_table(rdf_rows, column_names)

    output_list.append("Trip Durations: ")
    output_list.append(trip_table)
    output_list.append(time_taken)
    return output_list
# #############################################################################




# USER STATS
def user_stats(df):
    """
    Computes statistics on on bikeshare users.
    Args:
        (pd.DataFrame) df - dataframe used for the computations
    Returns:
        (list) output_list - output list containing return values for
                            application layout components
    """
    user_stat_list = []
    start_time = time.time()

    # Display counts of user types
    column_names = ['User Type', 'Count', '% of Total']
    user_types = df['User Type'].value_counts().index
    user_counts = df['User Type'].value_counts().values
    user_count_percentage = np.round((df['User Type'].value_counts(normalize=True) * 100).values, 2)
    rdf_rows = list(zip(user_types, user_counts, user_count_percentage))
    user_type_table = create_dbc_table(rdf_rows, column_names)
    user_stat_list.append(user_type_table)

    # Create a pie chart for user type
    pie_names = df['User Type'].unique()
    pie_data = list(zip(user_counts, pie_names))
    pie_df = pd.DataFrame(data=pie_data, columns=['count', 'user type'])
    pie_chart = px.pie(pie_df, values='count', names='user type', title="Percentage of user types: ")
    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    pie_chart.update_layout(margin=dict(l=20, r=20, t=40, b=10),
                            paper_bgcolor= 'LightSteelBlue',
                            height=300,
                            width=700,
                            title_x=0.5,
                            title_font_size=20)
    pie_chart.update_traces(textposition='inside', textinfo='percent+label',
                            marker = dict(colors=colors, line=dict(color='#000000', width=2)))

    user_stat_list.append(pie_chart)
# #############################################################################



    # Display counts of gender
    if CITY == 'washington':
        gender_na_text = "Gender data is not available for {} right now!".format(CITY.capitalize())
        birth_na_text = "Birth Year data is not available for {} right now!".format(CITY.capitalize())
        user_stat_list.append(gender_na_text)
        user_stat_list.append(birth_na_text)

    else:
        column_names = ['Gender Type', 'Count', '% of Total']
        gender_types = df['Gender'].value_counts().index
        gender_counts = df['Gender'].value_counts().values
        gender_count_percentage = np.round((df['Gender'].value_counts(normalize=True) * 100).values, 2)
        rdf_rows = list(zip(gender_types, gender_counts, gender_count_percentage))
        user_gender_table = create_dbc_table(rdf_rows, column_names)
        user_stat_list.append(user_gender_table)

        # Display earliest, most recent, and most common year of birth
        column_names = ['Birth Year of oldest rider',
                        'Birth Year of youngest rider',
                        'Most common Birth Year']
        rdf_rows = []
        oldest_year = int(df['Birth Year'].min())
        youngest_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        rdf_rows.append([oldest_year, youngest_year, most_common_year])

        user_age_table = create_dbc_table(rdf_rows, column_names)
        user_stat_list.append(user_age_table)

    # execution time
    time_taken = "This computation took {} seconds.".format(round((time.time() - start_time), 4))
    user_stat_list.append(time_taken)

    return user_stat_list
# #############################################################################


# RAW DATA
def display_raw_data(df):
    """
    Computes raw data 5 rows at a time
    Args:
        (pd.DataFrame) df - dataframe used for the computations
    Returns:
        (list) output_list - output list containing return values for
                            application layout components
    """
    num_rows_to_show = ROW_ADVANCE
    output_list = []
    output_list.append("Displaying rows {} through {} from data table".format(1, ROW_COUNTER))

    # Deselecting the last three columns as they're not part of the original data
    raw_df = DF.iloc[: ROW_COUNTER, :-3]
    last_page = ROW_COUNTER//ROW_ADVANCE - 1
    raw_table = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in raw_df.columns],
        data=raw_df.to_dict('records'),
        page_size=num_rows_to_show,
        page_current=last_page,
        style_table={
            'overflowY': 'scroll',
        },
        style_cell={'color': 'black'}
    )
    output_list.append(raw_table)

    # Print message if there are no more data to display
    if ROW_COUNTER == len(DF):
        warn_text = "There are no more data rows to show!!"
    else:
        warn_text = ""
    output_list.append(warn_text)
    return output_list
# #############################################################################
