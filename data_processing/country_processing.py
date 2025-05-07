from utils.utils_data import (
    group_data,
    calculate_change,
)
import pandas as pd
from tests.test_functions.data_types import data_types


def pre_war_bar_processed(trade_data, fossil_fuel, country_select, num_of_countries):
    """
    Processes the data for the pre-war bar chart
    args:
        fossil_fuel str: the fossil fuel selected by the user
        country_select str: the country selected by the user
        num_of_countries int: the number of countries to display
    returns:
        pre_war_filtered: the data for the pre-war bar chart"""
    data_types(trade_data)  # checks if the columns are the correct data type

    # checks if the number of countries is greater than 0
    if num_of_countries < 1:
        raise ValueError("Number of countries must be greater than 0")

    if country_select not in trade_data["importer"].values:
        raise ValueError("Country not found in the data")

    if fossil_fuel not in trade_data["resource"].values:
        raise ValueError("Fossil fuel not found in the data")

    try:
        # Filters by year to only show data from 2019 to 2021
        # PRE WAR BAR
        # filter the data by the user input of fossil fuel and country
        pre_war_filtered = trade_data[
            (trade_data["importer"] == country_select)
            & (trade_data["resource"] == fossil_fuel)
            & (trade_data["year"] >= 2019)
            & (trade_data["year"] <= 2021)
        ]
        # groups the post war filtered by exporter, importer and resource and sums the value
        pre_war_filtered = group_data(
            pre_war_filtered,
            ["exporter", "importer", "resource", "exporter continent"],
        )

        # returns the top n countries based on the value
        return pre_war_filtered.nlargest(num_of_countries, "value (US$)").sort_values(
            "value (US$)", ascending=True
        )
    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )


def post_war_bar_processed(trade_data, fossil_fuel, country_select, num_of_countries):
    """
    Processes the data for the Since the War bar chart
    args:
        fossil_fuel str: the fossil fuel selected by the user
        country_select str: the country selected by the user
        num_of_countries int: the number of countries to display
    returns:
        pre_war_filtered: the data for the pre-war bar chart
    """
    data_types(trade_data)  # checks if the columns are the correct data type

    # checks if the number of countries is greater than 0
    if num_of_countries < 1:
        raise ValueError("Number of countries must be greater than 0")

    if country_select not in trade_data["importer"].values:
        raise ValueError("Country not found in the data")

    if fossil_fuel not in trade_data["resource"].values:
        raise ValueError("Fossil fuel not found in the data")

    try:
        # Filters by year to only show pre and Since the War +- 2 years
        post_war_bar_filtered = trade_data[
            (trade_data["year"] >= 2022)
            & (trade_data["year"] <= 2024)
            & (trade_data["importer"] == country_select)
            & (trade_data["resource"] == fossil_fuel)
        ]

        # groups the post war filtered by exporter, importer and resource and sums the value
        post_war_bar_filtered = group_data(
            post_war_bar_filtered,
            ["exporter", "importer", "resource", "exporter continent"],
        )

        # returns the top n countries based on the value
        return post_war_bar_filtered.nlargest(
            num_of_countries, "value (US$)"
        ).sort_values("value (US$)", ascending=True)
    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )


def line_chart_fossil_trends_processed(trade_data, country_select, line_chart_years):
    """
    Processes the data for the line chart fossil trends
    args:
        country_select str: the country selected by the user
        line_chart_years list: the year range selected by the user
    returns:
        line_chart_trends_pivot: the data for the line chart fossil trends
    """

    if line_chart_years[0] >= line_chart_years[1]:
        raise ValueError("The first year must be less than the second year")
    if country_select not in trade_data["importer"].values:
        raise ValueError("Country not found in the data")

    # try catch for key error handling
    try:
        # checks if the columns are the correct data type
        data_types(trade_data)

        # filters the data by the user input of country and year range before pivot
        line_chart_trends_filtered = trade_data[
            (trade_data["importer"] == country_select)
            & (trade_data["year"] >= line_chart_years[0])
            & (trade_data["year"] <= line_chart_years[1])
        ]

        # converts the resource column into separate columns Coal, Gas and Oil
        # then sums the improt values for each resource per importer year
        line_chart_trends_pivot = (
            line_chart_trends_filtered.pivot_table(
                values="value (US$)",
                index=["year", "importer"],
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
            line_chart_trends_pivot,
            line_chart_years[0],
            line_chart_years[1],
            "Oil",
            "Coal",
            "Gas",
        )
        return line_chart_trends_pivot, percentage_text
    # raises a value error if the columns are not present in the data
    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )


def fuel_line_chart_processed(fuel_data, country, range_slider):
    """
    Processes the data for the fuel line chart
    args:
        country str: the country selected by the user
        range_slider list: the year range selected by the user
    returns:
        fuel_data: the data for the fuel line chart
        percentage_text: the percentage change between the two years
    """

    # Data processing for fuel data #
    if range_slider[0] >= range_slider[1]:
        raise ValueError("The first year must be less than the second year")
    # checks if the country is in the data
    if country not in fuel_data["Country"].values:
        raise ValueError("Country not found in the data")
    try:
        data_types(fuel_data)  # checks if the columns are the correct data type
        # filters the data by the user input of year range
        fuel_data = fuel_data[
            (fuel_data["Year"] >= range_slider[0])
            & (fuel_data["Year"] <= range_slider[1])
            & (fuel_data["Country"] == country)
        ]
        # groups the data by year, fuel and country and calculates the mean price
        fuel_data = (
            fuel_data.groupby(["Year", "Fuel", "Country"])["Price"].mean().reset_index()
        )

        # pivots petrol and diesel into their own columns
        fuel_data = (
            fuel_data.pivot(index="Year", columns="Fuel", values="Price")
            .reset_index()
            .fillna(
                0
            )  # any resources with N/A value will be filled with 0 to keep line chart consistent
        )

        # checks if petrol and diesel columns are present in the data if not sets them to 0
        for column in ["Petrol", "Diesel"]:
            if column not in fuel_data.columns:
                fuel_data[column] = 0.0
        # converts petrol and diesel prices to per 1 litre
        fuel_data["Petrol"] = fuel_data["Petrol"] / 1000
        fuel_data["Diesel"] = fuel_data["Diesel"] / 1000

        # calculate change overtime
        percentage_text = calculate_change(
            fuel_data,
            range_slider[0],
            range_slider[1],
            "Petrol",
            "Diesel",
        )

        return fuel_data, percentage_text
    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )


def electricity_line_chart_processed(electricity_data, country, range_slider):
    """
    Processes the data for the electricity line chart
    args:
        country str: the country selected by the user
        range_slider list: the year range selected by the user
    returns:
        electricity_data: the data for the electricity line chart
        percentage_change: the percentage change between the two years
    """
    # Data processing for electricity data #
    # checks if the country is in the data
    if country not in electricity_data["Country"].values:
        raise ValueError("Country not found in the data")
    # checks if the first year is less than the second year
    if range_slider[0] >= range_slider[1]:
        raise ValueError("The first year must be less than the second year")
    try:
        data_types(electricity_data)  # checks if the columns are the correct data type

        # filters the data by the user input of year range and country
        electricity_data = electricity_data[
            (electricity_data["Year"] >= range_slider[0])
            & (electricity_data["Year"] <= range_slider[1])
            & (electricity_data["Country"] == country)
        ]
        # groups the data by year and calculates the mean price
        electricity_data = (
            electricity_data.groupby("Year")["Price"].mean().reset_index()
        )

        # calculate change overtime
        percentage_change = calculate_change(
            electricity_data,
            range_slider[0],
            range_slider[1],
            "Price",
        )

        return electricity_data, percentage_change
    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )
