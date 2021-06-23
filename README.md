# US Bikeshare Project
#### By Anuradha Pani
The US Bikeshare Project was created as part of the curriculum for Udacity's [Programming for Data Science with Python](https://www.udacity.com/course/programming-for-data-science-nanodegree--nd104) Nanodegree Program.

## Description
This project explores the data related to bike share systems in three major cities in the USA, namely, Chicago, New York City and Washington DC. Python is used as the underlying programming language of choice. This project is an interactive web application using Python Dash component library and can be deployed on the local machine.

The statistics computed for this project are:

__1. Popular times of travel (i.e., occurs most often in the start time)__
* Most common month
* Most common day of week
* Most common hour of day

__2. Popular stations and trip__

* Most common start station
* Most common end station
* Most common trip from start to end (i.e., most frequent combination of start station and end station)

__3. Trip duration__

* Total travel time
* Average travel time

__4. User info__

* Counts of each user type
* Counts of each gender (only available for NYC and Chicago)
* Earliest, most recent, most common year of birth (only available for NYC and Chicago)

## Files used
* bikeshare.py - the main python file containing Dash application component layout and the accompanying callback functions
* bikeshare_helper.py - this file contains python functions to read the data files and compute the required statistics.
* assets/bikes.jpeg - the image file for the dash web application
* data/chicago.csv - data file for Chicago
* data/new_york_city.csv - data file for New York City
* data/washington.csv - data file for Washington DC

## Credits
The following is the list of websites referred to:
1. https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html
2. https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
3. https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#time-date-components
4. https://blog.softhints.com/pandas-how-to-filter-results-of-value_counts/
5. https://knowledge.udacity.com/questions/175167
6. https://pandas.pydata.org/docs/reference/api/pandas.to_timedelta.html
7. https://stackoverflow.com/questions/50558458/pandas-get-frequency-of-item-occurrences-in-a-column-as-percentage
8. https://www.codegrepper.com/code-examples/html/how+to+display+dataframe+in+flask
9. https://www.youtube.com/watch?v=mTsZL-VmRVE&t=1145s
10. https://community.plotly.com/t/initail-callback-of-div-element-not-triggred-why/46824
11. https://dash-bootstrap-components.opensource.faculty.ai/
12. https://dash.plotly.com/advanced-callbacks
