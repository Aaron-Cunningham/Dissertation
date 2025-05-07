from utils.utils_data import load_fuel_cleaned, load_electricity_data, calculate_change
from tests.test_functions.data_types import data_types
import pandas as pd


def fuel_line_chart_processing(fuel_data, range_slider_fuel):
    """
    Processes the data for the fuel line chart
    args:
        range_slider_fuel list: the year range selected by the user
    returns:
        fuel_data_filtered: the data for the fuel line chart
        percentage_text: the percentage change between the two years
    """

    if range_slider_fuel[0] > range_slider_fuel[1]:
        raise ValueError("The start year must be less than the end year")

    if fuel_data.empty:
        raise ValueError("Input data is empty")

    try:
        data_types(fuel_data)  # checks the data types of the input data
        # groups by year and calculates the average of petrol and diesel
        fuel_data_average = (
            fuel_data.groupby(["Year", "Fuel"])["Price"].mean().reset_index()
        )

        # pivots petrol and diesel into their own columns
        fuel_data_average = fuel_data_average.pivot(
            index="Year", columns="Fuel", values="Price"
        ).reset_index()

        for column in ["Petrol", "Diesel"]:
            if column not in fuel_data.columns:
                fuel_data[column] = 0.0
        # converts petrol and diesel prices to per 1 litre
        fuel_data_average["Petrol"] = fuel_data_average["Petrol"] / 1000
        fuel_data_average["Diesel"] = fuel_data_average["Diesel"] / 1000

        fuel_data_filtered = fuel_data_average[
            (fuel_data_average["Year"] >= range_slider_fuel[0])
            & (fuel_data_average["Year"] <= range_slider_fuel[1])
        ]

        (fuel_data_filtered)
        percentage_text = calculate_change(
            fuel_data_filtered,
            range_slider_fuel[0],
            range_slider_fuel[1],
            "Petrol",
            "Diesel",
        )

        return fuel_data_filtered, percentage_text
    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )


def electricity_line_chart_processing(electricity_data, range_slider_electric):
    """
    Processes the data for the electricity line chart
    args:
        range_slider_electric list: the year range selected by the user
    returns:
        electricity_data: the data for the electricity line chart
        percentage_change: the percentage change between the two years
    """
    if range_slider_electric[0] > range_slider_electric[1]:
        raise ValueError("The start year must be less than the end year")

    if electricity_data.empty:
        raise ValueError("Input data is empty")

    try:
        data_types(electricity_data)  # checks the data types of the input data
        # groups by year and calculates the average of electricity price across europe
        electricity_data = (
            electricity_data.groupby("Year")["Price"].mean().reset_index()
        )

        # filters the data based on the user input
        electricity_data = electricity_data[
            (electricity_data["Year"] >= range_slider_electric[0])
            & (electricity_data["Year"] <= range_slider_electric[1])
        ]

        # calculate change overtime
        percentage_change = calculate_change(
            electricity_data,
            range_slider_electric[0],
            range_slider_electric[1],
            "Price",
        )
        (electricity_data)

        return electricity_data, percentage_change
    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )


def fuel_map_processing(fuel_data, years_map, fuel_dropdown):
    """
    Processes the data for the fuel map
    args:
        years_map list: the year selected by the user
        fuel_dropdown list: the fuel selected by the user
    returns:
        fuel_data: the data for the fuel map
    """
    if fuel_data.empty:
        raise ValueError("Input data is empty")
    try:
        data_types(fuel_data)  # checks the data types of the input data
        fuel_data = fuel_data[
            (fuel_data["Year"] == years_map) & (fuel_data["Fuel"] == fuel_dropdown)
        ]
        # converts petrol and diesel prices to per 1 litre
        fuel_data["Price"] = fuel_data["Price"] / 1000
        (fuel_data)
        return fuel_data
    except KeyError as e:
        raise ValueError(
            f"Input data must contain the following columns: {', '.join(e.args)}"
        )
