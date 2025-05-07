from utils.input_components import *
from data_processing.country_processing import *

# registers the page so can be accessed referenced from https://dash.plotly.com/urls
dash.register_page(__name__, path="/country-data", name="Country Data")

trade_data = load_trade_data()
# Dash app setup code adapted from
# 1) https://www.youtube.com/watch?v=d9SmpNfMg7U&ab_channel=CharmingData
# 2) https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
layout = html.Div(
    [
        dbc.Card(
            html.Div(
                [  # Country Select Dropdown
                    create_country_select("country-select"),
                    # Fossil Fuel Dropdown
                    create_dropdown(
                        dropdown_id="resource-dropdown",
                        default_value="Oil",
                        options=[
                            {"label": "Oil", "value": "Oil"},
                            {"label": "Coal", "value": "Coal"},
                            {"label": "Gas", "value": "Gas"},
                        ],
                        label_text="Select Fossil Fuel",
                    ),
                    create_slider_nums(
                        "number-of-countries",  # id
                        1,  # min
                        10,  # max
                        1,  # step
                        5,  # value
                        "Select the number of Exporters to view",  # label title
                        max_width="350px",
                    ),
                ],
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "align-items": "center",
                    "justify-content": "center",
                    "gap": "20px",
                    "background-color": "#F0F0F0",
                },
            ),
            style={"width": "100%", "max-width": "820px", "margin": "10px auto"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [
                                # Graph for pre-war-map
                                dcc.Graph(
                                    id="countries-top-importers-pre",
                                    config=CONFIG_GRAPH,
                                )
                            ]
                        ),
                    ),
                    width="auto",
                ),
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [
                                # Graph for Since the War-map
                                dcc.Graph(
                                    id="countries-top-importers-post",
                                    config=CONFIG_GRAPH,
                                )
                            ]
                        ),
                    ),
                    width="auto",
                ),
            ],
            justify="center",
            className="g-3",
        ),
        dbc.Card(
            html.Div(
                [
                    # Range Slider for line charts
                    create_range_slider(
                        trade_data,
                        "range-slider-trends",
                        "for The Trends Line Charts",
                        "600px",
                    ),
                    create_dropdown(
                        "chart-select",
                        "electricity",
                        [
                            {"label": "Fuel ", "value": "fuel"},
                            {
                                "label": "Electricity",
                                "value": "electricity",
                            },
                        ],
                        "Select Chart Type:",
                    ),
                ],
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "align-items": "center",
                    "justify-content": "center",
                    "gap": "20px",
                    "background-color": "#F0F0F0",
                },
            ),
            style={
                "width": "100%",
                "max-width": "800px",
                "margin": "10px auto",
                "background-color": "#F0F0F0",
            },
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [  # Line chart for fossil fuel trends
                                dcc.Graph(
                                    id="line-chart-fossil-trends",
                                    config=CONFIG_GRAPH,
                                ),
                            ]
                        ),
                    ),
                    width="auto",
                ),
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [  # Line chart for energy trends
                                dcc.Graph(
                                    id="line-chart-energy-trends",
                                    config=CONFIG_GRAPH,
                                ),
                            ]
                        ),
                        style={
                            "background-color": "#F0F0F0",
                        },
                    ),
                    width="auto",
                ),
            ],
            justify="center",
        ),
    ],
)


# Callback to update the graph
@dash.callback(
    [
        Output("countries-top-importers-pre", "figure"),
    ],
    [
        Input("country-select", "value"),
        Input("resource-dropdown", "value"),
        Input("number-of-countries", "value"),
    ],
)
@cache.memoize()
def pre_war_bar(country_select, fossil_fuel, num_of_countries):

    # retrieve the processed data
    pre_war_filtered = pre_war_bar_processed(
        trade_data, fossil_fuel, country_select, num_of_countries
    )

    # create the bar chart
    pre_war = px.bar(
        pre_war_filtered,
        x="value (US$)",
        y="exporter",
        color="exporter continent",  # color of the bars by continent
        color_discrete_map=continent_colours,
        title=f"Top {num_of_countries} Exporters to {country_select} for {fossil_fuel} Pre-War (2019 - 2021)",  # title of the bar chart
        labels={
            "exporter": "Country",
            "value (US$)": "Value (US$)",
        },  # labels for the x and y axis
        text="value (US$)",  # text to be displayed on the bars
        custom_data=["resource"],  # custom data to be used in the hover template
        template="presentation",  # template of the chart
    )
    # if no data is present displays message
    if pre_war_filtered.empty:
        return no_data_message(pre_war)

    # bar chart configuration
    configure_bar_chart(
        pre_war,
        df=pre_war_filtered,
        legend_title="Exporter Continent",
        hovertemplate="<b>%{y}</b><br>"  # values that show when hovering over bars
        + "<br>"
        + "Value: %{x}<br>"
        + "Resource: %{customdata[0]}",
        texttemplate="$%{text:,.0f}",
        xtick={"tickprefix": "$"},  # adds $ to the x axis
        chart_select="exporter",  # this is for the ordering of the and what to order by exporter
    )
    return [pre_war]


# Callback to update the graph
@dash.callback(
    [
        Output("countries-top-importers-post", "figure"),
    ],
    [
        Input("country-select", "value"),
        Input("resource-dropdown", "value"),
        Input("number-of-countries", "value"),
    ],
)
@cache.memoize()
def post_war_bar(country_select, fossil_fuel, num_of_countries):

    # retrieve the processed data
    post_war_filtered = post_war_bar_processed(
        trade_data, fossil_fuel, country_select, num_of_countries
    )
    # POST WAR BAR #
    post_war_bar = px.bar(
        post_war_filtered,
        x="value (US$)",
        y="exporter",
        color="exporter continent",  # color of the bars by continent
        title=f"Top {num_of_countries} Exporters to {country_select} for {fossil_fuel} Since the War (2022 - 2024)",  # title of the bar chart
        labels={
            "exporter": "Country",
            "value (US$)": "Value (US$)",
        },  # labels for the x and y axis
        text="value (US$)",  # text to be displayed on the bars
        custom_data=["resource"],  # custom data to be used in the hover template
        color_discrete_map=continent_colours,
        template="presentation",  # template of the chart
    )
    # if no data is present displays message
    if post_war_filtered.empty:
        return no_data_message(post_war_bar)

    # bar chart configuration
    configure_bar_chart(
        post_war_bar,
        df=post_war_filtered,
        legend_title="Exporter Continent",
        hovertemplate="<b>%{y}</b><br>"
        + "<br>"
        + "Value: %{x}<br>"
        + "Resource: %{customdata[0]}",
        texttemplate="$%{text:,.0f}",
        xtick={"tickprefix": "$"},  # adds $ to the x axis
        chart_select="exporter",
    )

    return [post_war_bar]


# Callback to update the graph
@dash.callback(
    [
        Output("line-chart-fossil-trends", "figure"),
    ],
    [
        Input("country-select", "value"),
        Input("range-slider-trends", "value"),
    ],
)
@cache.memoize()
def line_chart_trends(country_select, line_chart_years):

    # retrieve the processed data
    line_chart_trends_filtered, percentage_text = line_chart_fossil_trends_processed(
        trade_data, country_select, line_chart_years
    )

    # creates the line chart
    line_chart_trends = px.line(
        line_chart_trends_filtered,
        x="year",
        y=["Oil", "Coal", "Gas"],
        labels={"value": "Value (US$)", "year": "Year"},
        markers=True,  # adds markers to the line chart (dots)
        title=f"{country_select}'s Fossil Fuel Import Trends: Oil, Natural Gas, and Coal ({line_chart_years[0]} - {line_chart_years[1]})",
        custom_data=[
            "importer",
            "value",
        ],  # custom data to be used in the hover template
        color_discrete_map=colour_map_resource,  # color of the lines
    )
    # if no data is present displays message
    if line_chart_trends_filtered.empty:
        return no_data_message(line_chart_trends)
    # configures the linegraph
    configure_line_graph(
        line_chart_trends,
        percentage_text=percentage_text,
        hover_temp="<b>%{customdata[0]}</b><br>Value US$: %{y}<br>Year: %{x}<br>Fossil Fuel: %{data.name}<br>",
        text_temp=None,
        legend_title="Fossil Fuels",
        tickprefix="€",
    )

    return [line_chart_trends]


# Callback to update the graph
@dash.callback(
    [
        Output("line-chart-energy-trends", "figure"),
    ],
    [
        Input("country-select", "value"),
        Input("range-slider-trends", "value"),
        Input("chart-select", "value"),
    ],
)
@cache.memoize()
def line_chart_energy_fuel(country_select, range_slider, chart_select):
    fuel_data_loading = load_fuel_cleaned()
    electricity_data_loading = load_electricity_data()
    # check if the chart select is fuel
    if chart_select == "fuel":
        # retrieves the filtered data and the percentage change
        fuel_data, percentage_text = fuel_line_chart_processed(
            fuel_data_loading, country_select, range_slider
        )

        # calculate change overtime
        fuel_line = px.line(
            fuel_data,
            x="Year",
            y=["Petrol", "Diesel"],
            markers=True,
            title=f"Average Yearly Fuel Prices for the {country_select} (Excl. Taxes & Duties, {range_slider[0]} - {range_slider[1]})",
            labels={"value": "Fuel Price (Euros per Litre)"},
        )
        # if no data is present displays message
        if fuel_data.empty:
            return no_data_message(fuel_line)
        # configures the linegraph
        configure_line_graph(
            graph=fuel_line,
            percentage_text=percentage_text,
            hover_temp="Year: %{x}<br>" + "Price (Per 1 litre): €%{y:,.2f}<br>",
            text_temp="",
            legend_title="Type of Fuel",
            tickprefix="€",
        )

        return [fuel_line]
    # else the chart select is electricity
    else:
        # retrieves the filtered data and the percentage change
        electricity_data, percentage_text = electricity_line_chart_processed(
            electricity_data_loading, country_select, range_slider
        )

        electricity_line = px.line(
            electricity_data,
            x="Year",
            y="Price",
            text="Price",
            markers=True,
            title=f"Average Yearly Electricity Prices for {country_select} (Excl. Taxes & Levies, {range_slider[0]} - {range_slider[1]})",
        )
        # if no data is present displays message
        if electricity_data.empty:
            return no_data_message(electricity_line)
        # configures the linegraph
        configure_line_graph(
            electricity_line,
            percentage_text,
            "Year: %{x}<br>" + "Price (Per kWh): €%{y:,.2f}<br>",
            "€%{text:,.2f}",
            legend_title=None,
            tickprefix="€",
        )

        return [electricity_line]
