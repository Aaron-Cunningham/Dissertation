from utils.utils_data import *
from utils.graph_configs import *
from dash import dcc, html, Output, Input
from utils.cache_config import cache
import dash_bootstrap_components as dbc
from functools import reduce
import plotly.express as px
from utils.colour_map import *
from typing import Tuple, List
import pandas as pd
import pydeck as pdk
import numpy as np
import math
import os
import json
import dash

LABEL = {
    "padding": "4px 10px",
    "margin-bottom": "5px",
    "text-decoration": "underline",
    "text-underline-offset": "4px",
    "font-weight": "bold",
}


def create_dropdown(
    dropdown_id="resource-dropdown",
    default_value=None,
    options=None,
    label_text="None",
    flex_direction="column",
    width="100%",
):
    """
    Creates a Dash dropdown component so a user can select a fossil fuel type

    args:
        dropfown_id str: This is the ID for the dropdown component. Default is resource-dropdown
        default_value str: This is the default value for the dropdrop component. Default is None
        options list: This is the list of options for the dropdown component. Default is None
        label_text str: This is the text that will be displayed above the dropdown component. Default is None

    returns:
        html.div: This div compoenent will return a html.label and a dropdown menu with fossil fuel compoenents

    notes:
        1) The dropdown options are fixed e.g ('Oil', 'Gas', 'Coal')
        2) The component compes pre styled

    """
    return html.Div(
        [
            html.Label(f"{label_text}", style={**LABEL}),
            dcc.Dropdown(
                id=dropdown_id,
                options=options,
                value=default_value,
                style={
                    "min-width": "0px",
                    "max-width": "250px",
                    "width": width,
                    "text-align": "center",
                    "border-radius": "10px",
                },
            ),
        ],
        style={
            "display": "flex",
            "flex-direction": flex_direction,
            "align-items": "center",
            "padding-bottom": "5px",
            "padding-top": "5px",
            "background-color": "#F0F0F0",
        },
    )


def create_radio(dropdown_id, default_value, options, label_text):
    """
    Creates a Dash dropdown component so a user can select a chart type

    args:
        dropdown_id (str): This is the ID for the dropdown component
        default_value (str): This is the default value for the dropdown component
    returns:
        A html.div element with the label and dropdown component
    """
    return html.Div(
        [
            html.Label(label_text, style={**LABEL}),
            dcc.RadioItems(
                id=dropdown_id,
                options=options,
                value=default_value,
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "justify-content": "center",
                    "gap": "20px",
                    "align-items": "center",
                },
            ),
        ],
        style={
            "display": "flex",
            "flex-direction": "row",
            "justify-content": "center",
            "align-items": "center",
            "margin-bottom": "5px",
            "margin-top": "5px",
        },
    )


def create_range_slider(data, slider_id, text, width="450px"):
    """
    Creates a dash range slider component with a label for selecting the year range

    args:
        data pandas.Dataframe: A pandas dataframe which contains the year column to determine the min and max years on the slider
        slider_id str: The ID for the range slider component
        text str: Text to be added to the slider to decribe it e.g. (Pie Chart)

    notes:
        1) The sliders range is dynamically set based on the data provided from year column in the dataframe
        2) Year markings are provided from 2017 to 2024
        3) The slider supports persistent session storage (will remember users previous settings until reset)
        3) Code adapted from https://www.youtube.com/watch?v=d9SmpNfMg7U&ab_channel=CharmingData
    """

    return html.Div(
        [
            html.Label(f"Select Years {text}", style={**LABEL}),
            dcc.RangeSlider(
                min=data["year"].min(),
                max=math.ceil(data["year"].max()),
                step=1,
                value=[data["year"].min(), data["year"].max()],
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode="drag",
                id=slider_id,
                marks={
                    year: str(year)
                    for year in [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
                },
                persistence=True,
                persistence_type="session",
            ),
        ],
        style={
            "width": "100%",
            "max-width": width,
            "padding": "3px",
            "text-align": "center",
        },
    )


def create_slider(data, slider_id, text, width="400px"):
    """
    Creates a dash range slider component with a label for selecting the year range

    args:
        data pandas.Dataframe: A pandas dataframe which contains the year column to determine the min and max years on the slider
        slider_id str: The ID for the range slider component
        text str: Text to be added to the slider to decribe it e.g. (Pie Chart)


    notes:
        1) The sliders range is dynamically set based on the data provided from year column in the dataframe
        2) Year markings are provided from 2017 to 2024
        3) The slider supports persistent session storage (will remember users previous settings until reset)
        3) Code adapted from https://www.youtube.com/watch?v=d9SmpNfMg7U&ab_channel=CharmingData
    """

    return html.Div(
        [
            html.Label(f"Select Year for {text}", style={**LABEL}),
            dcc.Slider(
                min=data["year"].min(),
                max=math.ceil(data["year"].max()),
                step=1,
                value=2020,
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode="drag",
                id=slider_id,
                marks={
                    year: str(year)
                    for year in [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
                },
                persistence=True,
                persistence_type="session",
            ),
        ],
        style={
            "width": "100%",
            "max-width": width,
            "padding": "3px",
            "text-align": "center",
        },
    )


def create_slider_nums(slider_id, min, max, step, value, label_text, max_width="400px"):
    """
    Creates a flow slider component so the user can select the amount of flows the wish to see on the sankey chart and map
    args:
        slider_id int: This is the ID for the slider component

    returns:
        A HTML.div element with the label and slider component

    notes:
        1) The slider has a set range of 20 to 200
        2) Each step on the slider is +10 flows
        3) The starting value is 20
        4) Users previous flow config is stored in persistent storage
    """

    return html.Div(
        [
            html.Label(label_text, style={**LABEL}),
            dcc.Slider(
                min=min,
                max=max,
                step=step,
                value=value,
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode="drag",
                id=slider_id,
                persistence=True,
                persistence_type="session",
            ),
        ],
        style={
            "min-width": "200px",
            "max-width": max_width,
            "width": "100%",
            "text-align": "center",
        },
    )


def create_country_select(dropdown_id, default_value="Germany"):
    """
    Creates a Dash dropdown component so a user can select country

    args:
        data pandas.Dataframe: A pandas dataframe which contains the importer column to determine the importers
        dropdown_id int: The ID for the dropdown component
        default_value: This is the value which the dropdown defaults to
    returns:
        A HTML.div element with the label and dropdown component

    notes:
        1) Each country is unique and is stored in a set
        2) Only detemines importer countries (European Countries)
    """
    # gets unique improters from EU countries
    data = load_fuel_cleaned()
    countries = set(data["Country"])
    sorted_countries = sorted(countries)
    return html.Div(
        [
            html.Label(f"Select Country", style={**LABEL}),
            dcc.Dropdown(
                id=dropdown_id,
                options=[
                    {"label": country, "value": country} for country in sorted_countries
                ],
                value=default_value,
                style={
                    "min-width": "200px",
                    "max-width": "250px",
                    "width": "100%",
                    "text-align": "center",
                    "border-radius": "10px",
                },
            ),
        ],
        style={
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",
            "margin-bottom": "10px",
            "margin-top": "10px",
        },
    )


def calc_node_positions(
    nodes: list, node_groups: list, final_group_extra_gap: float = 0.05, y_sep=0.3
) -> Tuple[list, list]:
    """Calculate x and y coords for a list of nodes, given a grouping.

    X coords force plotly to place nodes that belong to the same conceptual "level" together.
    Y positions "encourage" (not force) nodes into a vertical order.

    Args:
        final_group_extra_gap:
            Amount of additional x-axis (0-1) to allocate to final grouping,
            to account for the fact that labels on this group appear on left,
            and may overlap with labels from the penultimate group.
        y_sep:
            Amount of "encouragement" for vertical ordering.
            Best results ~0.1, layout gets weird if higher.
            Gets divided by len(group) so that smaller values used in groups with many nodes.

    Notes:
        Code referenced from https://geoffruddock.com/notebooks/data-viz/sankey-diagrams/

    """

    final_group_extra_gap = 0.05
    normal_gap = (1 - final_group_extra_gap) / (len(node_groups) - 1)

    x_pos = [
        (
            round(group_idx * normal_gap, 2)
            if group_idx < len(node_groups) - 1
            else round(group_idx * normal_gap + final_group_extra_gap, 2)
        )
        for group_idx, group in enumerate(node_groups)
        for node_idx, node in enumerate(group)
    ]

    y_pos = [
        node
        for group_idx, group in enumerate(node_groups)
        for node in np.cumsum(
            np.full(shape=len(group), fill_value=(y_sep / len(group)))
        )
        .round(4)
        .tolist()
    ]

    return x_pos, y_pos


def calc_node_tooltips(
    df: pd.DataFrame, node_groups: list
) -> Tuple[List[Tuple[float]], str]:
    """Generate data/template for tooltips on a Plotly sankey diagram.

    Expects input df with three columns: (source, target, count)

    Final template:
    {{ label }}
     x% of Total (in)
     x% of Total (out)

     Notes:
         1) Code adapted from https://geoffruddock.com/notebooks/data-viz/sankey-diagrams/
    """

    # calculate total flows through each node
    sorted_nodes = reduce(lambda x, y: x + y, node_groups)
    node_totals = df.groupby("target")["count"].sum().reindex(sorted_nodes)
    source_totals = df.groupby("source")["count"].sum().reindex(sorted_nodes)
    # calculatse the total imported. for start nodes with no imports, fill with 0
    totals_imported = node_totals.fillna(0).tolist()
    # calculates the total exported. for end nodes with no exports, fill with 0
    totals_exported = source_totals.fillna(0).tolist()

    customdata = [(x, y) for x, y in zip(totals_imported, totals_exported)]

    hovertemplate = (
        "%{label}<br>"
        + "Total Value Imported: $%{customdata[0]:,.0f} <br>"
        + "Total Value Exported: $%{customdata[1]:,.0f} <br>"
    )

    return customdata, hovertemplate


def calc_link_tooltips(
    df: pd.DataFrame, node_groups: list
) -> Tuple[List[Tuple[float]], str]:
    """Generate data/template for tooltips on a Plotly sankey diagram.

    Expects input df with three columns: (source, target, count)

    Final template:
    {{ source }} → {{ target }}
     x% of {{ source }}
     x% of {{ target }}

    Notes:
        1) Code adapted from https://geoffruddock.com/notebooks/data-viz/sankey-diagrams/
    """

    pct_of_source = (
        df.set_index("source")
        .assign(denom=lambda x: x.groupby(level=0)["count"].sum()[x.index])
        .pipe(lambda x: x["count"] / x["denom"])
        .map("{:.0%}".format)
        .values.tolist()
    )

    pct_of_target = (
        df.set_index("target")
        .assign(denom=lambda x: x.groupby(level=0)["count"].sum()[x.index])
        .pipe(lambda x: x["count"] / x["denom"])
        .map("{:.0%}".format)
        .values.tolist()
    )

    total_sent = df["count"].values.tolist()

    customdata = [
        (x, y, z) for x, y, z in zip(pct_of_source, pct_of_target, total_sent)
    ]

    hovertemplate = (
        "%{source.label} → %{target.label}<br>"
        + " %{customdata[0]} of %{source.label}'s Exports<br>"
        + " %{customdata[1]} of %{target.label}'s Imports<br>"
        + " Total Value Exported: $%{customdata[2]:,.0f}"
    )

    return customdata, hovertemplate
