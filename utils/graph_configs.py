LEGEND = {
    "bordercolor": "black",
    "borderwidth": 1,
    "x": 1.14,
    "y": 1,
    "xanchor": "center",
}

CONFIG_GRAPH = {
    "displaylogo": False,
}


def configure_line_graph(
    graph,
    percentage_text,
    hover_temp,
    text_temp,
    legend_title,
    height=365,
    tickprefix="",
):
    """
    Configures the line graph layout and traces

    args:
        graph plotly.Figure: This is the graph that will be configured
        percentage_text str: Optional Percentage change text to be shown on the graph
        y_axis dict: This is the title of the Y-Axis
        hover_temp str: this is the hover template string for the tooltip
        text_temp str: This is the template of the text for displaying data labels on graph
        legend_title str: This is the title of the legend

    returns:
        plotly.Figure
        An updated graoh with a configured layout

    notes:
        1) Adds a verticle dashed line at x=2022 to mark the start of the Ukraine war
        2) Reuqires the LEGNED variable to be imported
    """
    text_temp if text_temp != None else None

    graph.update_layout(
        width=780,
        height=height,
        paper_bgcolor="#F0F0F0",
        title={
            "font": {
                "size": 15,  # title size of title
                "weight": "bold",  # bold title
                "color": "black",  # black title
            },
            "x": 0.5,  # center title
        },
        legend=LEGEND,  # legend of the line chart
        template="plotly_white",  # changes the background to white for line
        yaxis={
            "tickprefix": tickprefix,  # adds a prefix to the y axis
        },
        margin={"r": 150, "t": 50, "l": 50, "b": 10},
        annotations=[
            {
                "text": percentage_text,
                "x": 1.03,
                "y": 0.35,
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "xanchor": "left",
            }
        ],
        legend_title_text=legend_title,  # legend title
        font={
            "size": 12,  # font size of the legend
        },
    )

    # adds a vertical line to the line chart indicating start of ukraine war
    graph.add_vline(
        x=2022,
        line_width=1,
        line_dash="dash",
        line_color="purple",
        annotation_text="Start of the Ukraine War",
        annotation_position="top",
        annotation={
            "font": {"size": 13, "color": "purple"},
        },
    )

    # Adapted from https://plotly.com/python/hover-text-and-formatting/
    graph.update_traces(
        opacity=0.9,
        hovertemplate=hover_temp,
        textposition="top center",  # sets position of the text on graph
        texttemplate=text_temp,  # text on line chart is filtered to price and to 2 decimal places
    )

    graph.update_xaxes(showspikes=True)  # adds spikes to the x axis
    graph.update_yaxes(showspikes=True)  # adds spikes to the y axis
    graph.update_yaxes(
        ticks="outside", tickwidth=1, ticklen=10, col=1
    )  # adds ticks to the y axis
    return graph


def configure_bar_chart(
    graph, df, legend_title, hovertemplate, texttemplate, xtick=None, chart_select=None
):
    """
    Configures the bar chart layout and traces

    args:
        graph plotly.Figure: This is the graph that will be configured
        df pandas.DataFrame: This is the dataframe that will be used to configure the graph
        legend_title str: This is the title of the legend
        hovertemplate str: this is the hover template string for the tooltip
        texttemplate str: This is the template of the text for displaying data labels on graph
        xtick = None: This is the xtick configuration
        chart_select = None: This is the column to be used for ordering the chart if other countries present

    returns:
        plotly.Figure
        An updated graph with a configured layout

    notes:
        1) Requires the LEGEND variable to be imported
        2) If the 'Others' is present in the data, it will be moved to the bottom of the chart
        3) Code adapted has been referenced in the function
    """

    # ordering code adapted from https://plotly.com/python/bar-charts/?_gl=1*uthub4*_gcl_au*Mjk2MTg3OTM1LjE3NDA0MTk4MTI.*_ga*Mzg4MDYwMDUxLjE3NDA0MTk4MTM.*_ga_6G7EE0JNSC*MTc0MTYwMDY5NC40OC4xLjE3NDE2MDEwODEuNjAuMC4w#bar-chart-with-sorted-or-ordered-categories
    ordering = df[f"{chart_select}"].to_list()  # gets the list of countries
    if "Others" in ordering:  # checks others is in the current list
        ordering.remove("Others")  # if others in the list remove it
        ordering.insert(
            0, "Others"
        )  # add others to the start of the list so it appears at the bottom of the chart
        # ['Nigeria', 'Kazakhstan', 'USA', 'Norway', 'Russia', 'Others'] -> ['Others', 'Nigeria', 'Kazakhstan', 'USA', 'Norway', 'Russia']

    graph.update_traces(
        opacity=0.9,  # opacity of the bars
        texttemplate=texttemplate,
        # Adapted from https://plotly.com/python/hover-text-and-formatting/
        hovertemplate=hovertemplate,
    )

    graph.update_layout(
        width=780,  # width of the bar chart
        height=365,  # height of the bar chart
        legend=LEGEND,  # legend of the bar chart
        title={
            "font": {
                "size": 15,  # title size of title
                "weight": "bold",  # bold title
                "color": "black",  # black title
            },
            "x": 0.5,  # center title
        },
        paper_bgcolor="#F0F0F0",  # background colour of the bar chart
        template="plotly_white",
        legend_title_text=legend_title,
        yaxis={
            "categoryorder": "array",
            "categoryarray": ordering,
        },
        margin={"r": 50, "t": 50, "l": 0, "b": 50},
        xaxis=xtick,
    )
    # Code rerenced from https://plotly.com/python/axes/?_gl=1*17cm6l*_gcl_au*Mjk2MTg3OTM1LjE3NDA0MTk4MTI.*_ga*Mzg4MDYwMDUxLjE3NDA0MTk4MTM.*_ga_6G7EE0JNSC*MTc0MjYwMjczNS43Mi4xLjE3NDI2MDI5NTIuMjguMC4w#set-axis-title-position
    graph.update_yaxes(ticks="outside", tickwidth=1, ticklen=10, col=1)


def configure_map(
    map,
    hovertemplate,
    title_text,
    height=365,
    margin={"r": 0, "t": 45, "l": 0, "b": 0},
    visible_legend=True,
    title_position=0.5,
    coloraxis_colorbar_title="",
    prefix="",
    suffix="",
):
    """
    Configures the map layout and traces

    args:
        map plotly.Figure: This is the graph that will be configured
        hovertemplate str: this is the hover template string for the tooltip
        title_text str: This is the title of the map
        height int: This is the height of the map
        margin dict: This is the margin of the map
        visible_legend bool: This is the visibility of the legend
        title_position float: This is the position of the title
        coloraxis_colorbar_title (str): This is the title of the colorbar
        prefix str: This is the prefix of the colorbar
        suffix str: This is the suffix of the colorbar

    returns:
        plotly.Figure
        An updated map with a configured layout

    notes:
        1) Requires the LEGEND variable to be imported

    """
    map.update_traces(hovertemplate=hovertemplate)
    map.update_layout(title=f"{title_text}")
    map.update_layout(
        margin=margin,
        width=780,
        height=height,
        title_x=title_position,
        coloraxis_colorbar_title=coloraxis_colorbar_title,
        coloraxis_colorbar_tickprefix=prefix,
        coloraxis_colorbar_ticksuffix=suffix,
        title={
            "font": {
                "size": 15,  # title size of title
                "weight": "bold",  # bold title
                "color": "black",  # black title
            },
            "x": 0.5,  # center title
        },
        coloraxis_showscale=visible_legend,
        paper_bgcolor="#F0F0F0",
        mapbox_center={"lat": 55.706772, "lon": 12.207891},
    )
    return map


def no_data_message(graph):
    """
    Displays a message when no data is found

    args:
        graph plotly.Figure: This is the graph that will be configured

    returns:
        plotly.Figure
        An updated graph with a message when no data is found
    """

    graph.update_layout(
        xaxis={"visible": False},  # removes the x axis
        yaxis={"visible": False},  # removes the y axis
        title={"text": ""},  # removes the title
        annotations=[
            {
                "text": "No matching data found, sorry!",  # text to display if no data is found
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,  # x position of the text
                "y": 0.5,  # y position of the text
                "showarrow": False,
                "font": {"size": 28},
            }
        ],
        template="presentation",
    )
    return [graph]
