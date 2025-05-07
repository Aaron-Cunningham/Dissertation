from data_processing.exports_imports_processing import *
from utils.input_components import *
from utils.create_graphs import create_map


# registers the page so can be accessed referenced from https://dash.plotly.com/urls
dash.register_page(__name__, path="/exports", name="Exports")

# Loads the data
trade_data = load_trade_data()

# Dash app setup code adapted from
# 1) https://www.youtube.com/watch?v=d9SmpNfMg7U&ab_channel=CharmingData
# 2) https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
layout = html.Div(
    [
        dbc.Card(
            html.Div(
                [
                    create_dropdown(
                        dropdown_id="trade_type",
                        default_value="exporter",
                        options=[
                            {"label": "Exports", "value": "exporter"},
                            {"label": "Imports", "value": "importer"},
                        ],
                        label_text="Select Trade Direction",
                    ),
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
                    create_dropdown(
                        dropdown_id="measurement-dropdown",
                        default_value="value (US$)",
                        options=[
                            {"label": "Value (US$)", "value": "value (US$)"},
                            {"label": "Weight (Kg)", "value": "weight (kg)"},
                        ],
                        label_text="Select Measurement",
                    ),
                    create_slider_nums(
                        "number-of-countries",  # id
                        1,  # min
                        10,  # max
                        1,  # step
                        5,  # value
                        "Number of Exporters/Importers to view",  # title
                        max_width="350px",
                    ),
                ],
                style={
                    "display": "flex",
                    "align-items": "center",
                    "justify-content": "center",
                    "gap": "20px",
                    "background-color": "#F0F0F0",
                },
            ),
            style={"width": "100%", "max-width": "1050px", "margin": "10px auto"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [
                                create_slider(
                                    trade_data,
                                    "bar-year",
                                    "the Bar Chart",
                                    width="800px",
                                ),
                                # Graph for bar chart
                                dcc.Graph(id="bar-chart-graph", config=CONFIG_GRAPH),
                            ]
                        ),
                    ),
                    width="auto",
                ),
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [  # Year Range Slider for bar chart share
                                create_range_slider(
                                    trade_data,
                                    "range-slider-bar-share",
                                    "",
                                    "800px",
                                ),
                                # share bar chart
                                dcc.Graph(id="bar-chart-market", config=CONFIG_GRAPH),
                            ]
                        ),
                    ),
                    width="auto",
                ),
            ],
            justify="center",
            className=" g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [
                                # Graph for pre-war-map
                                # scrollZoom Config ref https://community.plotly.com/t/scatter-mapbox-not-allowing-zoom-with-either-scroll-wheel-or-buttons-in-vscode-notebook/88787
                                dcc.Graph(
                                    id="pre-war-map",
                                    config={
                                        "scrollZoom": True,
                                        "displaylogo": False,
                                    },
                                ),
                            ]
                        ),
                    ),
                    width="auto",
                ),
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [
                                # Graph for Since the War map
                                dcc.Graph(
                                    id="Since the War-map",
                                    config={
                                        "scrollZoom": True,
                                        "displaylogo": False,
                                    },
                                ),
                            ]
                        ),
                    ),
                    width="auto",
                ),
            ],
            justify="center",
            className="mt-1 g-3 mb-3",
        ),
    ]
)


# Callback to update all the graphs
@dash.callback(
    [
        Output("pre-war-map", "figure"),
        Output("Since the War-map", "figure"),
    ],
    [
        Input("resource-dropdown", "value"),
        Input("measurement-dropdown", "value"),
        Input("trade_type", "value"),
    ],
)
@cache.memoize()
def pre_post_maps(fossil_fuel, measurement_dropdown, chart_select):

    # checks if the measurement is value or weight
    value_usd = "$" if measurement_dropdown == "value (US$)" else ""
    # checks if the measurement is value or weight
    kg = "" if measurement_dropdown == "value (US$)" else "kg"
    # checks if the chart is for exports or imports and updates the title and hover accordingly
    exports = "Exporters" if chart_select == "exporter" else "Imports"
    exported = "Exported" if chart_select == "exporter" else "Imported"

    # zoom level for the map based on the chart select
    zoom = 0 if chart_select == "exporter" else 1.4
    # sets the center of the map based on the chart select
    center = (
        {"lat": 45.056061, "lon": 12.381614}
        if chart_select == "exporter"
        else {"lat": 55.706772, "lon": 12.207891}
    )
    # filters the data for the pre war map
    data_filtered_pre = pre_war_map_processing(
        trade_data, measurement_dropdown, fossil_fuel, chart_select
    )
    # filters the data for the post war map
    data_filtered_post = post_war_map_processing(
        trade_data, measurement_dropdown, fossil_fuel, chart_select
    )

    # finds minimum value for the shared colour range
    minimum_colour = min(
        data_filtered_pre[f"{measurement_dropdown}"].min(),
        data_filtered_post[f"{measurement_dropdown}"].min(),
    )
    # finds maximum value for the shared colour range
    maximum_colour = max(
        data_filtered_pre[f"{measurement_dropdown}"].max(),
        data_filtered_post[f"{measurement_dropdown}"].max(),
    )

    # Pre war map
    pre_war_map = create_map(
        data_filtered_pre,
        color=f"{measurement_dropdown}",  # color of the map
        color_range=[minimum_colour, maximum_colour],  # colour range of the map
        custom_data=[f"{chart_select}", f"{measurement_dropdown}"],
        locations=f"{chart_select}ISO",
        center=center,
        zoom=zoom,
    )
    # configures the map pre war
    pre_war_map = configure_map(
        pre_war_map,
        hovertemplate="<b>%{customdata[0]}</b>"
        + "<br>"
        + f"Total {exported}: {value_usd}"
        + "%{customdata[1]:,.0f}"
        + f" {kg}"
        + f"<br> Fossil Fuel: {fossil_fuel}",
        title_text=f"{exports} of {fossil_fuel} to Europe Pre-War (2019 - 2021)<br><sup> Measured in {measurement_dropdown.upper()}</sup>",
        coloraxis_colorbar_title=f"{value_usd}{kg}",
        visible_legend=False,
    )

    # Post war map
    post_war_map = create_map(
        data_filtered_post,
        color=f"{measurement_dropdown}",  # color of the map
        color_range=[minimum_colour, maximum_colour],  # colour range of the map
        custom_data=[f"{chart_select}", f"{measurement_dropdown}"],
        center=center,
        zoom=zoom,
        locations=f"{chart_select}ISO",
    )
    # configures the map post war
    post_war_map = configure_map(
        post_war_map,
        hovertemplate="<b>%{customdata[0]}</b>"
        + "<br>"
        + f"Total {exported}: {value_usd}"
        + "%{customdata[1]:,.0f}"
        + f" {kg}"
        + f"<br> Fossil Fuel: {fossil_fuel}",
        title_text=f"{exports} of {fossil_fuel} to Europe Since the War (2022 - 2024)<br><sup> Measured in {measurement_dropdown.upper()}</sup>",
        coloraxis_colorbar_title=f"{measurement_dropdown.upper()}",
        visible_legend=True,
        prefix=f"{value_usd}",
        suffix=f" {kg}",
    )

    return pre_war_map, post_war_map


# Callback to update all the graphs
@dash.callback(
    [
        Output("bar-chart-market", "figure"),
    ],
    [
        Input("resource-dropdown", "value"),
        Input("range-slider-bar-share", "value"),
        Input("measurement-dropdown", "value"),
        Input("number-of-countries", "value"),
        Input("trade_type", "value"),
    ],
)
@cache.memoize()
def bar_chart_market_share_and_line_chart(
    fossil_fuel, chart_years, measurement_dropdown, num_countries, chart_select
):
    # checks if the measurement is value or weight
    value_usd = "$" if measurement_dropdown == "value (US$)" else ""
    kg = "" if measurement_dropdown == "value (US$)" else "kg"
    # checks if the chart is for exports or imports and updates the title and hover accordingly
    exported = "Exported" if chart_select == "exporter" else "Imported"
    exports = "Exports to" if chart_select == "exporter" else "Imports in"

    if chart_select == "exporter":
        # checks if the chart is for exports or imports and updates the processing
        continent = (
            "exporter continent" if chart_select == "exporter" else "importer continent"
        )

        data_filtered_bar = market_share_bar_processing(
            trade_data,
            measurement_dropdown,
            fossil_fuel,
            chart_years,
            num_countries,
            chart_select,
            continent,
        )

        # creates bar chart
        market_share_bar = px.bar(
            data_filtered_bar,  # data
            y=f"{chart_select}",  # y axis
            x="percent",  # x axis
            color=f"{continent}",  # type to be coloured
            color_discrete_map=continent_colours,  # colour map for continents (colour blind friendly)
            custom_data=[
                "resource",
                f"{chart_select}",
                f"{measurement_dropdown}",
            ],  # custom data for hover
            labels={  # labels for the x and y axis
                f"percent": f"MARKET SHARE (%)",
                f"{chart_select}": "COUNTRY",
            },  # labels for the x and y axis
            template="presentation",  # template for the graph
            title=f"Market share of {fossil_fuel} {exports} Europe ({chart_years[0]}-{chart_years[1]})",
            subtitle=f"Share (%) Measured in ({value_usd}{kg})",
        )

        # configures the bar chart
        configure_bar_chart(
            market_share_bar,
            df=data_filtered_bar,
            legend_title="Continent",
            hovertemplate="<b>%{customdata[1]}</b><br><br>"
            + "Market Share %{x:.2f}%<br>"
            + f"Total {exported}: "
            + f"{value_usd}"
            + "%{customdata[2]:,.0f}"
            + f"{kg}<br>"
            + "Resource: %{customdata[0]}",
            texttemplate="%{x:,.2f}%",
            xtick={"ticksuffix": "%"},
            chart_select=chart_select,
        )

        return [market_share_bar]
    else:
        # checks if the chart is for exports or imports and updates the processing
        line_chart_trends_filtered, percentage_change = line_chart_imports_processed(
            trade_data, measurement_dropdown, chart_years
        )
        # checks if the measurement is value or weight  and then updates the value
        value = (
            "Value (US$)" if measurement_dropdown == "value (US$)" else "Weight (kg)"
        )
        # creates the line chart
        line_chart_imports = px.line(
            line_chart_trends_filtered,  # data
            x="year",
            y=["Oil", "Coal", "Gas"],
            labels={"value": value, "year": "Year"},
            markers=True,  # adds markers to the line chart (dots)
            title=f"Import Trends of Oil, Coal, and Gas in Europe",
            subtitle=f"‎ ",  # invisible character to keep the subtitle hidden when graph changes
            custom_data=[],  # custom data to be used in the hover template
            color_discrete_map=colour_map_resource,  # colour of the lines
        )
        # configures the linegraph
        configure_line_graph(
            line_chart_imports,  # line chart
            percentage_text=percentage_change,  # percentage change
            hover_temp="Year: %{x}<br>"
            + f"Total Imported: {value_usd}"
            + "%{y:,.0f}"
            + f" {kg}",
            text_temp=None,
            legend_title="Fossil Fuels",
            tickprefix="$",
        )
        return [line_chart_imports]


# Callback to update all the graphs
@dash.callback(
    [
        Output("bar-chart-graph", "figure"),
    ],
    [
        Input("resource-dropdown", "value"),
        Input("bar-year", "value"),
        Input("measurement-dropdown", "value"),
        Input("number-of-countries", "value"),
        Input("trade_type", "value"),
    ],
)
@cache.memoize()
def bar_chart_top_imports(
    fossil_fuel, year, measurement_dropdown, num_countries, chart_select
):
    # checks if the measurement is value or weight
    value_usd = "$" if measurement_dropdown == "value (US$)" else ""
    kg = "" if measurement_dropdown == "value (US$)" else "kg"
    # checks if the chart is for exports or imports and updates the processing
    continent = (
        "exporter continent" if chart_select == "exporter" else "importer continent"
    )
    # retrieves the data for the bar chart
    bar_filtered = top_export_bar_processing(
        trade_data,
        measurement_dropdown,
        fossil_fuel,
        year,
        num_countries,
        chart_select,
        continent,
    )
    # checks if the chart is for exports or imports and updates the title and hover accordingly
    exporters = "Exporters to" if chart_select == "exporter" else "Importers in"
    exported = "Exported" if chart_select == "exporter" else "Imported"

    # Bar Chart
    bar_chart = px.bar(
        bar_filtered,
        x=f"{measurement_dropdown}",  # x axis is the year
        y=f"{chart_select}",  # y axis is the value
        title=f"Top {num_countries} {fossil_fuel} {exporters} Europe in {year}",  # title of the line chart
        subtitle=f"Measured in ({value_usd}{kg})",
        color=f"{continent}",
        color_discrete_map=continent_colours,
        custom_data=[
            f"{chart_select}",
            "resource",
            "year",
            f"{measurement_dropdown}",
        ],  # custom data to be used in the hover template
        template="presentation",
        text=f"{measurement_dropdown}",  # display the figures
        labels={
            f"{measurement_dropdown}": f"{measurement_dropdown.upper()}",
            f"{chart_select}": "COUNTRY",
        },  # labels for the x and y axis
    )

    # configures the bar chart
    configure_bar_chart(
        bar_chart,
        df=bar_filtered,
        legend_title="Continent",
        hovertemplate="<b>%{customdata[0]}</b><br>"
        + "<br>"
        + f"Total {exported}: "
        + "%{x}"
        + f"{kg}"
        + "<br>Year: %{customdata[2]}<br>"
        + "Resource: %{customdata[1]}",
        texttemplate=f"{value_usd}" + "%{text:,.0f}" + f"{kg}",
        xtick={"tickprefix": f"{value_usd}", "ticksuffix": f" {kg}"},
        chart_select=chart_select,
    )
    return [bar_chart]
