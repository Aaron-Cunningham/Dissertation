from utils.utils_data import load_trade_data, group_data, calculate_change
from tests.test_functions.data_types import data_types

trade_data = load_trade_data()


def pre_war_map_processing(trade_data, measurement, fossil_fuel, chart_select):
    """
    Processes the data for the pre-war map
    args:
        measurement str: the measurement selected by the user (weight kg or value US$)
        fossil_fuel str: the fossil fuel selected by the user (coal, oil, gas)
        chart_select str: the chart selected by the user (importer or exporter)
    returns:
        pre_war_filtered: the data for the pre-war map"""
    # excludes russia as an input (excluding Russia) as focus to mainland europe
    data_types(trade_data)

    if trade_data.empty:
        raise ValueError("Input data is empty")

    if fossil_fuel not in trade_data["resource"].values:
        raise ValueError("Fossil fuel not found in the data")

    if chart_select not in trade_data.columns:
        raise ValueError("Chart select not found in the data")

    if measurement not in trade_data.columns:
        raise ValueError("Measurement not found in the data")

    try:
        if chart_select == "importer":
            trade_data = trade_data[(trade_data["importer"] != "Russia")]

        # filters the data based on pre war years and europe as the importer
        pre_war_filtered = trade_data[
            (trade_data["year"] >= 2019)
            & (trade_data["year"] <= 2021)
            & (trade_data["importer continent"] == "Europe")
            & (trade_data["resource"] == fossil_fuel)
        ]
        # groups by resoruce, exporter and exporterISO (for the map) and sums up the value then returns the data
        return group_data(
            pre_war_filtered,
            [f"{chart_select}", "resource", f"{chart_select}ISO"],
            f"{measurement}",
        )
    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )


def post_war_map_processing(trade_data, measurement, fossil_fuel, chart_select):
    """
    Processes the data for the Since the War map
    args:
        measurement str: the measurement selected by the user (weight kg or value US$)
        fossil_fuel str: the fossil fuel selected by the user (coal, oil, gas)
        chart_select str: the chart selected by the user (importer or exporter)
    returns:
        pre_war_filtered: the data for the pre-war map"""

    data_types(trade_data)
    if trade_data.empty:
        raise ValueError("Input data is empty")

    if fossil_fuel not in trade_data["resource"].values:
        raise ValueError("Fossil fuel not found in the data")

    if chart_select not in trade_data.columns:
        raise ValueError("Chart select not found in the data")

    if measurement not in trade_data.columns:
        raise ValueError("Measurement not found in the data")

    try:
        # excludes russia as an input (excluding Russia) as focus to mainland europe
        if chart_select == "importer":
            trade_data = trade_data[(trade_data["importer"] != "Russia")]

        # filters the data based on pre war years and europe as the importer
        pre_war_filtered = trade_data[
            (trade_data["year"] >= 2022)
            & (trade_data["year"] <= 2024)
            & (trade_data["importer continent"] == "Europe")
            & (trade_data["resource"] == fossil_fuel)
        ]

        # groups by resoruce, exporter and importer/exporterISO (for the map) and sums up the value then returns the data
        return group_data(
            pre_war_filtered,
            [f"{chart_select}", "resource", f"{chart_select}ISO"],
            f"{measurement}",
        )
    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )


def market_share_bar_processing(
    trade_data,
    measurement_dropdown,
    fossil_fuel,
    bar_chart_years,
    num_countries,
    chart_select,
    continent,
):
    """

    Processes the data for the market share bar chart
    args:
        measurement_dropdown str: the measurement selected by the user (weight kg or value US$)
        fossil_fuel str: the fossil fuel selected by the user (coal, oil, gas)
        bar_chart_years list: the year range selected by the user
        num_countries int: the number of countries to display
        chart_select str: the chart selected by the user (importer or exporter)
    returns:
        data_filtered_bar: the data for the market share bar chart
    """

    data_types(trade_data)
    if trade_data.empty:
        raise ValueError("Input data is empty")
    if measurement_dropdown not in trade_data.columns:
        raise ValueError("Measurement not found in the data")

    if fossil_fuel not in trade_data["resource"].values:
        raise ValueError("Fossil fuel not found in the data")

    if bar_chart_years[0] > bar_chart_years[1]:
        raise ValueError("The start year must be less than the end year")

    if num_countries < 1:
        raise ValueError("The number of countries must be greater than 0")

    if chart_select not in trade_data.columns:
        raise ValueError("Chart select not found in the data")

    if continent not in trade_data.columns:
        raise ValueError("Continent not found in the data")

    try:
        # filters the data based on user input of resource, years, and importer continent
        data_filtered_bar = trade_data[
            (trade_data["resource"] == fossil_fuel)
            & (trade_data["year"] >= bar_chart_years[0])
            & (trade_data["year"] <= bar_chart_years[1])
            & (trade_data["importer continent"] == "Europe")
        ]

        # groups by exporter and sums the value
        data_filtered_bar = group_data(
            data_filtered_bar,
            [chart_select, "resource", continent],
            measurement_dropdown,
        )

        # adapted from https://www.datasciencemadesimple.com/rank-dataframe-python-pandas-min-max-dense-rank-group/
        # ranks exporters by value (US$ or weight (kg)) from hieghts to lowest ranks 1,2,3,4,5 etc
        data_filtered_bar["rank"] = data_filtered_bar[f"{measurement_dropdown}"].rank(
            method="dense", ascending=False
        )

        # replaces importers/exporters and importer/exporter continents ranked above 5 with 'Others'
        data_filtered_bar.loc[
            data_filtered_bar["rank"] > num_countries, [chart_select, continent]
        ] = "Others"

        # combines 'Others' so it is one entry
        data_filtered_bar = group_data(
            data_filtered_bar,
            [chart_select, "resource", continent],
            f"{measurement_dropdown}",
        )

        # calculates the total for percentage
        total_value = data_filtered_bar[f"{measurement_dropdown}"].sum()

        # calculates the market share for each exporter and adds to percent column
        data_filtered_bar["percent"] = (
            data_filtered_bar[measurement_dropdown] / total_value
        ) * 100

        # sorts and returns the bar charts in ascending order
        return data_filtered_bar.sort_values("percent", ascending=True)

    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )


def top_export_bar_processing(
    trade_data,
    measurement_dropdown,
    fossil_fuel,
    year,
    num_countries,
    chart_select,
    continent,
):
    """
    Processes the data for the top export bar chart
    args:
        measurement_dropdown str: the measurement selected by the user (weight kg or value US$)
        fossil_fuel str: the fossil fuel selected by the user (coal, oil, gas)
        year int: the year selected by the user
        num_countries int: the number of countries to display
        chart_select str: the chart selected by the user (importer or exporter)
    returns:
        fossil_by_country_year: the data for the top export bar chart
    """

    data_types(trade_data)
    if trade_data.empty:
        raise ValueError("Input data is empty")
    if measurement_dropdown not in trade_data.columns:
        raise ValueError("Measurement not found in the data")

    if fossil_fuel not in trade_data["resource"].values:
        raise ValueError("Fossil fuel not found in the data")

    if year not in trade_data["year"].values:
        raise ValueError("Year not found in the data")

    if num_countries < 1:
        raise ValueError("The number of countries must be greater than 0")

    if chart_select not in trade_data.columns:
        raise ValueError("Chart select not found in the data")

    if continent not in trade_data.columns:
        raise ValueError("Continent not found in the data")

    try:
        # filters the data based on user input
        input_filtered_bar = trade_data[
            (trade_data["resource"] == fossil_fuel)
            & (trade_data["year"] == year)
            & (trade_data["importer continent"] == "Europe")
        ]

        # groups by exporter, year, and resource and sums the value
        fossil_by_country_year = group_data(
            input_filtered_bar,
            [chart_select, "resource", "year", f"{continent}"],
            measurement_dropdown,
        )

        # ranks exporters by value (US$ or weight (kg)) from hieghts to lowest ranks 1,2,3,4,5 etc
        fossil_by_country_year["rank"] = fossil_by_country_year[
            f"{measurement_dropdown}"
        ].rank(method="dense", ascending=False)

        # replaces importers/exporters and importer/exporter continents ranked above 5 with 'Others'
        fossil_by_country_year.loc[
            fossil_by_country_year["rank"] > num_countries, [chart_select, continent]
        ] = "Others"

        # combines 'Others' so it is one entry
        fossil_by_country_year = group_data(
            fossil_by_country_year,
            [chart_select, "resource", "year", continent],
            f"{measurement_dropdown}",
        )

        # returns the data sorted in ascending order
        return fossil_by_country_year.sort_values(
            f"{measurement_dropdown}", ascending=True
        )
    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )


def line_chart_imports_processed(trade_data, measurement_dropdown, range_slider):
    """
    Processes the data for the line chart
    args:
        measurement_dropdown str: the measurement selected by the user (weight kg or value US$)
        range_slider list: the year range selected by the user
    returns:
        imput_filtered_line: the data for the line chart
    """
    data_types(trade_data)
    if measurement_dropdown not in trade_data.columns:
        raise ValueError("Measurement not found in the data")

    if range_slider[0] > range_slider[1]:
        raise ValueError("The start year must be less than the end year")
    try:
        # filters the data by the user input of country and year range before pivot
        line_chart_trends_filtered = trade_data[
            (trade_data["importer continent"] == "Europe")
            & (trade_data["year"] >= range_slider[0])
            & (trade_data["year"] <= range_slider[1])
        ]
        imput_filtered_line = (
            line_chart_trends_filtered.pivot_table(
                values=measurement_dropdown,
                index=["year"],
                columns="resource",
                aggfunc="sum",
            )
            .reset_index()
            .fillna(
                0
            )  # any resources with N/A value will be filled with 0 to keep line chart consistent
        )

        # calculates the percentage change between the two years for each resource
        percentage_text = calculate_change(
            imput_filtered_line,
            range_slider[0],
            range_slider[1],
            "Oil",
            "Coal",
            "Gas",
        )

        return imput_filtered_line, percentage_text
    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )
