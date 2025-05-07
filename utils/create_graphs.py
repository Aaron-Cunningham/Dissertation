import plotly.graph_objects as go
from utils.input_components import (
    Tuple,
    List,
    pd,
    continent_colours,
    reduce,
    np,
    load_country_shapes,
    px,
)


def create_map(
    data,
    color,
    custom_data,
    zoom,
    center,
    locations,
    colour_scale="Plasma_r",
    map_style="carto-positron",
    color_range=None,
):
    """
    Creates a choropleth map

    args:
        data pd.DataFrame: A dataframe with export data
        fossil_fuel str: The name of the selected fossil fuel
        title_text str: Text to be added to the map title
        color str: The name of the column with the values to map to colours
        color_scale str: A colour scheme the map will follow (default plasma)
        map_style str: Mapbox style
        color_range: the min and max on the colours
        visible_legend bool: Determines whether the legend shows or not
        title_position int: The position of the map title
        margin dict: The figures margins (pixels)

    returns:
        A generated choropleth map

    notes:
        1) Reuqires an internet connection to load the GeoJSON for country boundaries
    """
    # Code referenced from https://plotly.com/python/tile-county-choropleth/
    # loads the geojson for country boundaries
    country_shapes = load_country_shapes()
    # Code adapted from https://stackoverflow.com/questions/59057881/how-to-customize-hover-template-on-with-what-information-to-show
    map = px.choropleth_mapbox(
        data,
        locations=locations,
        color=color,
        color_continuous_scale=colour_scale,
        geojson=country_shapes,
        mapbox_style=map_style,
        zoom=zoom,
        center=center,
        range_color=color_range,
        custom_data=custom_data,
    )

    return map


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


def make_sankey(
    df: pd.DataFrame, node_groups: list = None, colors: dict = None
) -> dict:
    """Generate parameter dicts for go.Figure plotting function

    Notes:
        1) Code referenced from https://geoffruddock.com/notebooks/data-viz/sankey-diagrams/#further-reading
    """

    # Create list of unique labels across node columns (source, target)
    observed_labels_set = df["source"].pipe(set) | df["target"].pipe(set)
    expected_labels = reduce(lambda x, y: x + y, node_groups)
    expected_labels_set = set(expected_labels)
    assert observed_labels_set == expected_labels_set, (
        "Mismatch between node_groups and unique values in source/target columns\n"
        f"\tMissing from node_groups: {observed_labels_set-expected_labels_set}\n"
        f"\tMissing from df: {expected_labels_set-observed_labels_set}"
    )

    # Nodes
    nodes_dict = {"label": expected_labels}
    nodes_dict["x"], nodes_dict["y"] = calc_node_positions(expected_labels, node_groups)
    if colors:
        country_to_continent = (
            df.set_index("source")[
                "exporter continent"
            ]  # index by the source and select exporter continent
            .combine_first(
                df.set_index("target")["importer continent"]
            )  # merge with target
            .to_dict()  # convert to dict
        )
        nodes_dict["color"] = [
            colors.get(country_to_continent.get(x)) for x in expected_labels
        ]
    # Links
    sankey_data = df[["source", "target", "count"]]
    sources, targets, values = sankey_data.values.T.tolist()
    source_idx = list(map(expected_labels.index, sources))
    target_idx = list(map(expected_labels.index, targets))
    links_dict = {"source": source_idx, "target": target_idx, "value": values}

    # Tooltips
    nodes_dict["customdata"], nodes_dict["hovertemplate"] = calc_node_tooltips(
        df, node_groups
    )
    links_dict["customdata"], links_dict["hovertemplate"] = calc_link_tooltips(
        df, node_groups
    )

    return nodes_dict, links_dict


def create_sankey_diagram(top_flows_sankey, fossil_fuel, text, num_of_flows):
    """
    Creates a sankey diagram

    args:
        top_flows_sankey pd.DataFrame: a dataframe that includes source and target
        fossil_fuel str: The name of the selected fossil fuel
        text str: Additional text for the title
        num_of_flows int: The number of top trade flows being shown

    returns:
        A generated Sankey Diagram figure

    notes:
        1) The function relies on a helper function called 'make_sankey'
        2) Legend doesn't come with Sankey charts so I used an override method from https://stackoverflow.com/questions/58852056/how-to-show-a-legend-in-plotly-python-sankey
    """

    # creates node groups from exporters and importers (for tooltips)
    node_groups = [
        top_flows_sankey["source"].unique().tolist(),
        top_flows_sankey["target"].unique().tolist(),
    ]
    # generates nodes and links with tooltips
    nodes, links = make_sankey(
        top_flows_sankey, colors=continent_colours, node_groups=node_groups
    )
    # creates the sankey diagram
    trade_flow_sankey = go.Sankey(node=nodes, link=links, arrangement="snap")

    # Legend override code adapted from https://stackoverflow.com/questions/58852056/how-to-show-a-legend-in-plotly-python-sankey
    legend = []
    # Colours and Entries for the legend
    legend_entries = [
        ["#009E73", "Europe"],
        ["#0072B2", "North America"],
        ["#56B4E9", "South America"],
        ["#F0E341", "Asia"],
        ["#E69F00", "Africa"],
        ["#D45E00", "Oceania"],
    ]
    for entry in legend_entries:
        # appends a new entry to the list
        legend.append(
            go.Scatter(
                mode="markers",
                x=[None],
                y=[None],
                marker=dict(size=10, color=entry[0], symbol="square"),
                name=entry[1],
            )
        )
    # combines sankey diagram and legend marker traces
    traces = [trade_flow_sankey] + legend

    layout = go.Layout(
        showlegend=True,  # forces the legend to show
        plot_bgcolor="#F0F0F0",  # sets background of the plot
    )
    final_sankey = go.Figure(data=traces, layout=layout)
    final_sankey.update_xaxes(visible=False)  # hides grid on x axis
    final_sankey.update_yaxes(visible=False)  # hides grid on y axis
    final_sankey.update_layout(
        font_size=10,  # font size for legend
        height=380,  # width of sankey diagram
        width=710,  # height of sankey diagram
        margin={
            "r": 20,
            "l": 20,
        },
        paper_bgcolor="#F0F0F0",
        title={  # title config
            "text": f"Top {num_of_flows} {fossil_fuel} Trade Flows To Europe {text}",  # title text
            "x": 0.5,  # title position (centre)
            "font": {  # size, colour, and weight
                "size": 15,
                "weight": "bold",
                "color": "black",
            },
        },
    )

    return final_sankey
