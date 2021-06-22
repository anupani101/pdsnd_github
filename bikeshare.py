# Udacity Programming for Data Science in Python
# Udacity US Bikeshare City Stats Project
# This is a Plotly Dash Web Application using Dash Bootstrap
# By: Anuradha Pani
# File: 'bikeshare.py' is the main app file
# #############################################################################


import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import logging
import bikeshare_helper as bk
from dash.dependencies import Input, Output, State


# Set logging level to suppress any unnecessary server logs
# #############################################################################
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# Create the App
# #############################################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Callback functions
# #############################################################################
@app.callback(
    Output('month-div', 'style'),
    Output('weekday-div', 'style'),
    [Input('filter-dropdown', 'value')])
def show_weekday_month_dropdown(filter_value):
    """
    Displays month and/or weekday dropdown options based on the main filter selection
    """

    if filter_value == 'month':
        return [{'display': 'block'}, {'display': 'none'}]
    elif filter_value == 'weekday':
        return [{'display': 'none'}, {'display': 'block'}]
    elif filter_value == 'both':
        return [{'display': 'block'}, {'display': 'block'}]
    else:
        return [{'display': 'none'}, {'display': 'none'}]




# Callback loads the global dataframe depending upon user filters
@app.callback(
    [
        Output('error-msg-placeholder', 'children'),
        Output('time-table-header', 'children'),
        Output('time-table', 'children'),
        Output('tab-time-exec', 'children'),
    ],
    [Input('submit-button', 'n_clicks')],
    [
        State('city-dropdown', 'value'),
        State('filter-dropdown', 'value'),
        State('month-dropdown', 'value'),
        State('weekday-dropdown', 'value'),
    ],
    prevent_initial_call=True
)
def load_filter_data(n_clicks, city, data_filter, month, weekday):
    """
    Loads the global dataframe and initializes global variables,
    depending upon user filter selections
    """

    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        # Reset month and weekday to 'none' if data_filter is 'none'
        if data_filter == 'none':
            month = 'none'
            weekday = 'none'
        try:
            # Load global data frame and city name
            bk.DF = bk.load_data(city, month, weekday)
            bk.CITY = city

            # Reset ROW_COUNTER to zero for raw data
            bk.ROW_COUNTER = 0

            # Get Time tab contents
            output_list = update_time_tab(bk.DF)

            # Insert empty error msg at the beginning of the list
            output_list.insert(0, dash.no_update)
        except Exception as e:
            print("Error occurred in load_filter_data(): {}".format(e))
            output_list = ["Data File is Empty!!! Please check your data!", dash.no_update, dash.no_update, dash.no_update]
        finally:
            return output_list



# Update Time Stats Tab
def update_time_tab(df):
    """
    Updates the output tab displaying Time Stats
    Args:
    (pd.DataFrame) df - the global dataframe which has been populated

    Returns:
    (list) output_list - this list contains all object for Dash Ouputs
    """

    try:
        output_list = bk.time_stats(df)
        return output_list
    except Exception as e:
        print("Some error occurred in update_time_tab(): {}".format(e))



# Callback updates the Station Stats tab
# Chained callback from Time Tab
@app.callback(
    [
        Output('station-table-header', 'children'),
        Output('station-table', 'children'),
        Output('tab-station-exec', 'children'),
    ],
    [Input('tab-time-exec', 'children')],
    prevent_initial_call=True
)
def update_station_tab(value):
    """ Updates the output tab displaying Station Stats  """
    if value is None:
        raise dash.exceptions.PreventUpdate
    else:
        try:
            output_list = bk.station_stats(bk.DF)
            return output_list
        except Exception as e:
            print("Some error occurred in update_station_tab(): {}".format(e))



# Callback updates the Trip Stats tab
# Chained callback from Station Tab
@app.callback(
    [
        Output('trip-table-header', 'children'),
        Output('trip-table', 'children'),
        Output('tab-trip-exec', 'children'),
    ],
    [Input('tab-station-exec', 'children')],
    prevent_initial_call=True
)
def update_trip_tab(value):
    """ Updates the output tab displaying Trip Stats """
    if value is None:
        raise dash.exceptions.PreventUpdate
    else:
        try:
            output_list = bk.trip_duration_stats(bk.DF)
            return output_list
        except Exception as e:
            print("Some error occurred in update_trip_tab(): {}".format(e))


# Callback updates the User Stats tab
# Chained callback from Trip Tab
@app.callback(
    [
        Output('user-type-table', 'children'),
        Output('user-type-pie-chart', 'figure'),
        Output('user-gender-table', 'children'),
        Output('user-age-table', 'children'),
        Output('tab-user-exec', 'children'),
    ],
    [Input('tab-trip-exec', 'children')],
    prevent_initial_call=True
)
def update_user_tab(value):
    """ Updates the output tab displaying User Stats """
    if value is None:
        raise dash.exceptions.PreventUpdate
    else:
        try:
            output_list = bk.user_stats(bk.DF)
            return output_list
        except Exception as e:
            print("Some error occurred in update_user_tab(): {}".format(e))





# Callback to show the raw data table if user clicks the 'yes' button
@app.callback(
    Output('show-raw-data', 'style'),
    Input('yes-button', 'n_clicks'),
    Input('no-button', 'n_clicks'),
    Input('submit-button', 'n_clicks'),
    prevent_initial_callback=True
)
def show_raw_data_block(yes, no, submit):
    """ Makes the raw data table visible/unvisible  """
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    else:
        ctx_button = ctx.triggered[0]['prop_id'].split('.')[0]
        if ctx_button == 'no-button' or ctx_button == 'submit-button':
            return {'display':'none'}
        else:
            return {'display': 'block'}


# Callback updates the Raw Data tab
# Chained callback from User Tab
@app.callback(
    [
        Output('raw-data-caption', 'children'),
        Output('raw-data-table', 'children'),
        Output('no-more-text', 'children'),
    ],
    [Input('tab-user-exec', 'children'),
     Input('more-button', 'n_clicks')],
    prevent_initial_call=True
)
def display_raw_data_tab(value, n_clicks):
    """ Loads raw data 5 rows at a time into the dash datatable for display  """
    ctx = dash.callback_context
    ctx_button = ctx.triggered[0]['prop_id'].split('.')[0]
    if value is None:
        raise dash.exceptions.PreventUpdate
    else:
        if ctx_button == 'more-button':
            # Update the row_counter
            if bk.ROW_COUNTER + bk.ROW_ADVANCE > len(bk.DF):
                num_remaining_rows = len(bk.DF) - bk.ROW_COUNTER
                bk.ROW_COUNTER += num_remaining_rows # Only add the remaining rows
            else:
                bk.ROW_COUNTER += bk.ROW_ADVANCE
        else: # triggered by 'submit-button'
            # dataframe has less than 5 rows
            if len(bk.DF) < bk.ROW_ADVANCE:
                bk.ROW_COUNTER += len(bk.DF)
            else:
                bk.ROW_COUNTER += bk.ROW_ADVANCE
        try:
            output_list = bk.display_raw_data(bk.DF)
            return output_list
        except Exception as e:
            print("Some Error occurred in display_raw_data_tab(): {}".format(e))



# Layout Components
# Header Card
# #############################################################################
header_card = dbc.Card([
    dbc.CardBody([html.Div(
        html.H1("US Bikeshare Statistics", className='text-center'),
    )])
],
    color='dark',
    inverse=True,
    outline=False,
    style={'align': 'right'}
)

# Main Card
# #############################################################################
main_card = dbc.Card(
    [
        dbc.CardImg(src="/assets/bikes.jpeg", top=True,
                    title="Image from Divy Bikes", alt="divy bikes",
                    style={'height':'250px'}),
        dbc.CardBody(
            [
                # city label
                html.P("Select the city you want to see statistics for:"),

                # city dropdown
                dcc.Dropdown(
                    id='city-dropdown',
                    options=[
                        {'label': 'New York City', 'value': 'nyc'},
                        {'label': 'Chicago', 'value': 'chicago'},
                        {'label': 'Washington', 'value': 'washington'}
                    ],
                    value='chicago',
                    clearable=False,
                    style={'color': '#000000'}
                ),
                html.Br(),

                # data filter label
                html.P(),
                html.P("Select the filter you want to apply:"),

                # filter dropdown
                dcc.Dropdown(
                    id='filter-dropdown',
                    options=[
                        {'label': 'By Month', 'value': 'month'},
                        {'label': 'By Weekday', 'value': 'weekday'},
                        {'label': 'By Month and Weekday', 'value': 'both'},
                        {'label': 'None', 'value': 'none'}
                    ],
                    value='none',
                    clearable=False,
                    style={'color': '#000000'}
                ),
                html.Br(),

                # month filter dropdown (only visible if month/month-weekday filter is selected
                html.Div([
                    # month filter label
                    html.P(),
                    html.P("Select the month:"),

                    dcc.Dropdown(
                        id='month-dropdown',
                        options=[
                            {'label': 'January', 'value': 'january'},
                            {'label': 'February', 'value': 'february'},
                            {'label': 'March', 'value': 'march'},
                            {'label': 'April', 'value': 'april'},
                            {'label': 'May', 'value': 'may'},
                            {'label': 'June', 'value': 'june'}
                        ],
                        value='january',
                        clearable=False,
                        style={'color': '#000000'}
                    ),
                ],
                    id='month-div',
                    style={'display': 'none'}

                ),
                html.Br(),

                # weekday filter dropdown (only visible if weekday/month-weekday filter is selected
                html.Div([
                    # weekday filter label
                    html.P(),
                    html.P("Select the weekday:"),
                    dcc.Dropdown(
                        id='weekday-dropdown',
                        options=[
                            {'label': 'Monday', 'value': 'monday'},
                            {'label': 'Tuesday', 'value': 'tuesday'},
                            {'label': 'Wednesday', 'value': 'wednesday'},
                            {'label': 'Thursday', 'value': 'thursday'},
                            {'label': 'Friday', 'value': 'friday'},
                            {'label': 'Saturday', 'value': 'saturday'},
                            {'label': 'Sunday', 'value': 'sunday'}
                        ],
                        value='sunday',
                        clearable=False,
                        style={'color': '#000000'}
                    ),
                ],
                    id='weekday-div',
                    style={'display': 'none'}
                ),
                html.Br(),

                # Submit Button
                html.P(),
                html.Div([
                    dbc.Button("Submit",
                               id='submit-button',
                               style={'color': 'success'}),
                ]),
            ]
        )
    ],
    color='dark',
    inverse=True,
    outline=False,
)

# Tab Time Stats
# #############################################################################
tab_time_content = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='error-msg-placeholder'), # used only id data files are empty
            html.P(id='time-table-header'),
            html.Div(id='time-table'),
            html.P(id='tab-time-exec'),
        ]
    ),
    color='dark',
    inverse=True,
    outline=False,
)

# Tab Station Stats
# #############################################################################
tab_station_content = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='station-table-header'),
            html.Div(id='station-table'),
            html.P(id='tab-station-exec'),
        ]
    ),
    color='dark',
    inverse=True,
    outline=False,
)

# Tab Trip Stats
# #############################################################################
tab_trip_content = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='trip-table-header'),
            html.Div(id='trip-table'),
            html.P(id='tab-trip-exec'),
        ]
    ),
    color='dark',
    inverse=True,
    outline=False,
)
# Tab User Stats
# #############################################################################
tab_user_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div([
                html.H6("Statistics for User Type: "),
                html.Div(id='user-type-table'),
                html.Div(html.Div(
                    dcc.Graph(id='user-type-pie-chart', ),
                ),
                style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content': 'center'})
            ]),
            html.Br(),

            html.Div([
                html.H6("Statistics for User Gender: "),
                html.Div(id='user-gender-table'),
            ]),
            html.Br(),

            html.Div([
                html.H6("Statistics for User Age Group: "),
                html.Div(id='user-age-table'),
            ]),
            html.Br(),

            html.Div(
                html.P(id='tab-user-exec')
            )
        ]
    ),
    color='dark',
    inverse=True,
    outline=False,
)

# Tab Raw Data
# #############################################################################
tab_raw_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                    dbc.Row([
                        dbc.Col(html.P("Do you want to see raw data?")),

                        # Yes Button
                        dbc.Col([
                            dbc.Button("Yes", id='yes-button', style={'color': 'success', 'margin': '10px'}),
                            dbc.Button("No", id='no-button', style={'color': 'success','margin': '10px'}),
                        ])
                    ])
            ),
            html.Div(
                [
                    html.H6(id='raw-data-caption'),
                    html.Div(id='raw-data-table'),
                    html.P(),

                    # Show more data button
                    html.Div([
                        dbc.Button("Show next 5 rows",
                                   id='more-button',
                                   style={'color': 'success'}),
                        html.P(id='no-more-text',
                               style={'color': 'red'})
                    ]),
                ],
                style={'display': 'none'},
                id='show-raw-data',
            ),
        ]
    ),
    color='dark',
    inverse=True,
    outline=False,
)

# Tabbed Output Card
# #############################################################################
tab_card = dbc.Card(
    dbc.Tabs(
        [
            dbc.Tab(tab_time_content, label="Time Stats", tab_id='time-tab', label_style={'color': '#00AEF9'}),
            dbc.Tab(tab_station_content, label="Station Stats", tab_id='station-tab', label_style={'color': '#00AEF9'}),
            dbc.Tab(tab_trip_content, label="Trip Stats", tab_id='trip-tab', label_style={'color': '#00AEF9'}),
            dbc.Tab(tab_user_content, label="User Stats", tab_id='user-tab', label_style={'color': '#00AEF9'}),
            dbc.Tab(tab_raw_content, label="Raw Data", tab_id='raw-tab', label_style={'color': '#00AEF9'}),
        ],
        id='tabs',
        active_tab="time-tab",
    ),
    color='dark',
    inverse=True,
    outline=False,
)

# App Layout
# #############################################################################
app.layout = html.Div([
    # Header
    dbc.Row([
        dbc.Col(header_card),
    ],
        justify='center'
    ),

    # Spacing underneath header
    dbc.Row([dbc.Col(html.P())], justify='center'),

    # Filter and Tab Ouput Cards
    dbc.Row([
        dbc.Col(main_card, width=4),
        dbc.Col(tab_card, width=8)
    ],
        justify='right',
        style={'margin-left': '0.5rem',
               'margin-right': '0.5rem'}
    ),
])

# Main Function
# #############################################################################
if __name__ == '__main__':
    app.run_server()
