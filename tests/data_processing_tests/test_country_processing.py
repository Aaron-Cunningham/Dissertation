import pytest
import data_processing.country_processing as func
import pandas as pd
from tests.test_data import *


def test_line_chart_processed_missing_columns(trade_data_sample):
    """
    Test if the function raises an error when the columns are missing
    """
    trade_data = trade_data_sample.drop(columns=["resource"])

    with pytest.raises(
        ValueError, match="Input data must contain the following columns: resource"
    ):
        func.line_chart_fossil_trends_processed(trade_data, "Germany", [2021, 2023])


@pytest.mark.filterwarnings(
    "ignore::FutureWarning"
)  # ignore FutureWarning which keeps popping up
def test_line_chart_processed_string_as_value(trade_data_sample):
    """
    Test if the function raises an error when the value is string"""
    trade_data = trade_data_sample.copy()
    trade_data.loc[0, "value (US$)"] = "string"

    with pytest.raises(
        ValueError, match=r"Invalid data type: value \(us\$\) must be numeric"
    ):
        func.line_chart_fossil_trends_processed(trade_data, "Germany", [2021, 2023])


@pytest.mark.filterwarnings(
    "ignore::FutureWarning"
)  # ignore FutureWarning which keeps popping up
def test_line_chart_processed_string_as_year(trade_data_sample):
    """
    Test if the function raises an error when the year is string"""
    trade_data = trade_data_sample.copy()
    trade_data.loc[0, "year"] = "string"

    with pytest.raises(ValueError, match="Invalid data type: year must be numeric"):
        func.line_chart_fossil_trends_processed(trade_data, "Germany", [2021, 2023])


def test_line_chart_processed_numeric_for_importer(trade_data_sample):
    """
    Test if the function raises an error when the importer is numeric"""
    trade_data = trade_data_sample.copy()
    trade_data.loc[0, "importer"] = 1

    with pytest.raises(ValueError, match="Invalid data type: importer must be String"):
        func.line_chart_fossil_trends_processed(trade_data, "Germany", [2021, 2023])


def test_line_chart_processed_sum(trade_data_sample):
    """
    Test if the function correctly sums the values of the resources
    """
    result, percentage_text = func.line_chart_fossil_trends_processed(
        trade_data_sample, "Germany", [2021, 2023]
    )

    assert result["Oil"].iloc[0] == 3100
    assert result["Gas"].iloc[1] == 1500
    assert result["Coal"].iloc[2] == 2000


def test_line_chart_processed_years(trade_data_sample):
    """
    Test if the function raises an error when the first year is greater than the second year
    """
    with pytest.raises(
        ValueError, match="The first year must be less than the second year"
    ):
        func.line_chart_fossil_trends_processed(
            trade_data_sample, "Germany", [2023, 2021]
        )


def test_line_chart_missing_country(trade_data_sample):
    """
    Test if the function raises an error when the country is not present in the data
    """
    trade_data = trade_data_sample.copy()
    (trade_data.columns)
    with pytest.raises(ValueError, match="Country not found in the data"):
        func.line_chart_fossil_trends_processed(
            trade_data, "Greece", [2021, 2022]
        )  # greece is not present in the data so it should raise an error


def test_pre_war_bar_num_of_countries(trade_data_sample):
    """
    Test if the function raises an error when the number of countries is less than 1
    """
    with pytest.raises(ValueError, match="Number of countries must be greater than 0"):
        func.pre_war_bar_processed(trade_data_sample, "Oil", "Germany", 0)


def test_post_war_bar_num_of_countries(trade_data_sample):
    """
    Test if the function raises an error when the number of countries is less than 1
    """
    with pytest.raises(ValueError, match="Number of countries must be greater than 0"):
        func.post_war_bar_processed(
            trade_data_sample, "Oil", "Germany", 0
        )  # number of countries is 0 so it should raise an error


def test_post_war_bar_missing_country(trade_data_sample):
    """
    Test if the function raises an error when the country is not present in the data
    """
    trade_data = trade_data_sample.copy()
    with pytest.raises(ValueError, match="Country not found in the data"):
        func.post_war_bar_processed(
            trade_data, "Coal", "Greece", 1
        )  # greece is not present in the data so it should raise an error


def test_pre_war_bar_missing_country(trade_data_sample):
    """
    Test if the function raises an error when the country is not present in the data
    """
    trade_data = trade_data_sample.copy()
    with pytest.raises(ValueError, match="Country not found in the data"):
        func.pre_war_bar_processed(
            trade_data, "Gas", "Greece", 1
        )  # greece is not present in the data so it should raise an error


def test_pre_war_bar_fossil_fuel(trade_data_sample):
    """
    Test if the function raises an error when the fossil fuel is not present
    """
    trade_data = trade_data_sample.copy()
    trade_data = trade_data[
        trade_data["resource"] != "Coal"
    ]  # remove oil from the data

    with pytest.raises(ValueError, match="Fossil fuel not found in the data"):
        func.post_war_bar_processed(
            trade_data, "Coal", "Russia", 4
        )  # oil is not present in the data so it should raise an error


def test_post_war_bar_fossil_fuel(trade_data_sample):
    """
    Test if the function raises an error when the fossil fuel is not present
    """
    trade_data = trade_data_sample.copy()
    trade_data = trade_data[
        trade_data["resource"] != "Coal"
    ]  # remove oil from the data

    with pytest.raises(ValueError, match="Fossil fuel not found in the data"):
        func.post_war_bar_processed(
            trade_data, "Coal", "Russia", 4
        )  # oil is not present in the data so it should raise an error


def test_pre_war_bar_processed_top_exporters(trade_data_sample):
    """
    Test if the function returns the correct data for the pre war bar chart
    """
    result = func.pre_war_bar_processed(trade_data_sample, "Oil", "Germany", 2)

    assert result["exporter"].iloc[0] == "USA"
    assert result["exporter"].iloc[1] == "Canada"


def test_post_war_bar_processed_top_exporters(trade_data_sample):
    """
    Test if the function returns the correct data for the pre war bar chart
    """
    result = func.post_war_bar_processed(trade_data_sample, "Coal", "Germany", 2)

    assert result["exporter"].iloc[0] == "South Africa"
    assert result["exporter"].iloc[1] == "Nigeria"


def test_fuel_line_chart_processed_missing_country(fuel_data_sample):
    """
    Test if the function raises an error when the country is not present in the data
    """
    with pytest.raises(ValueError, match="Country not found in the data"):
        func.fuel_line_chart_processed(fuel_data_sample, "Greece", [2021, 2022])


def test_fuel_line_chart_processed_larger_year(fuel_data_sample):
    """
    Test if the function raises an error when the country is not present in the data
    """
    with pytest.raises(
        ValueError, match="The first year must be less than the second year"
    ):
        func.fuel_line_chart_processed(fuel_data_sample, "Greece", [2023, 2022])


def test_fuel_line_processed_missing_columns(fuel_data_sample):
    """
    Test if the function raises an error when the columns are missing
    """
    trade_data = fuel_data_sample.drop(columns=["Fuel"])
    (trade_data.columns)
    with pytest.raises(
        ValueError, match="Input data must contain the following columns: Fuel"
    ):
        func.fuel_line_chart_processed(trade_data, "Czechia", [2021, 2023])


def test_fuel_line_processed_numeric_for_country(fuel_data_sample):
    """
    Test if the function raises an error when the Country is numeric"""

    trade_data = fuel_data_sample.copy()
    trade_data.loc[0, "Country"] = 1  # change the country to numeric value at index 0

    with pytest.raises(ValueError, match="Invalid data type: Country must be String"):
        func.fuel_line_chart_processed(trade_data, "Czechia", [2021, 2023])


@pytest.mark.filterwarnings(
    "ignore::FutureWarning"
)  # ignore FutureWarning which keeps popping up
def test_fuel_line_chart_processed_string_as_year(fuel_data_sample):
    """
    Test if the function raises an error when the Year is string"""
    trade_data = fuel_data_sample.copy()
    trade_data.loc[0, "Year"] = "string"  # change the year to string value at index 0

    with pytest.raises(ValueError, match="Invalid data type: Year must be numeric"):
        func.fuel_line_chart_processed(trade_data, "Czechia", [2021, 2023])


@pytest.mark.filterwarnings(
    "ignore::FutureWarning"
)  # ignore FutureWarning which keeps popping up
def test_fuel_line_chart_processed_string_as_price(fuel_data_sample):
    """
    Test if the function raises an error when the Price is string"""
    trade_data = fuel_data_sample.copy()
    trade_data.loc[0, "Price"] = "string"  # change the year to string value at index 0

    with pytest.raises(ValueError, match="Invalid data type: Price must be numeric"):
        func.fuel_line_chart_processed(trade_data, "Czechia", [2021, 2023])


def test_fuel_line_chart_processed_numeric_as_Fuel(fuel_data_sample):
    """
    Test if the function raises an error when the Price is string"""
    trade_data = fuel_data_sample.copy()
    trade_data.loc[0, "Fuel"] = 0  # change the year to string value at index 0

    with pytest.raises(ValueError, match="Invalid data type: Fuel must be numeric"):
        func.fuel_line_chart_processed(trade_data, "Czechia", [2021, 2023])


def test_fuel_line_chart_processed_sum(fuel_data_sample):
    """
    Test if the function correctly sums the values of the resources
    """
    result, percentage_text = func.fuel_line_chart_processed(
        fuel_data_sample, "Czechia", [2021, 2023]
    )

    (result)
    assert result["Diesel"].iloc[0] == 1.45  # mean of 900 and 2000 / 1000
    assert result["Diesel"].iloc[1] == 0.90  # only one value for 2023 900
    assert result["Diesel"].iloc[2] == 1.60  # mean of 2200 and 1000 / 1000
    assert (
        result["Petrol"].iloc[0] == 0
    )  # as there is no petrol in the data for czecia 2021 - 2023


def test_electricity_line_chart_missing_columns(electricity_data_sample):
    """
    Test if the function raises an error when the columns are missing
    """
    electricity_data = electricity_data_sample.drop(columns=["Price"])
    (electricity_data.columns)
    with pytest.raises(
        ValueError,
        match="Input data must contain the following columns: Column not found: Price",
    ):
        func.electricity_line_chart_processed(electricity_data, "Czechia", [2021, 2023])


def test_electricity_line_chart_processed_numeric_as_Country(electricity_data_sample):
    """
    Test if the function raises an error when the Country is numeric"""

    trade_data = electricity_data_sample.copy()
    trade_data.loc[0, "Country"] = 0  # change the country to numeric value at index 0

    with pytest.raises(ValueError, match="Invalid data type: Country must be String"):
        func.electricity_line_chart_processed(trade_data, "Czechia", [2021, 2023])


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_electricity_line_chart_processed_string_as_year(electricity_data_sample):
    """
    Test if the function raises an error when the Year is string"""
    trade_data = electricity_data_sample.copy()
    trade_data.loc[0, "Year"] = "string"  # change the year to string value at index 0

    with pytest.raises(ValueError, match="Invalid data type: Year must be numeric"):
        func.electricity_line_chart_processed(trade_data, "Czechia", [2021, 2023])


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_electricity_line_chart_processed_string_as_price(electricity_data_sample):
    """
    Test if the function raises an error when the Price is string"""
    trade_data = electricity_data_sample.copy()
    trade_data.loc[0, "Price"] = "string"  # change the year to string value at index 0

    with pytest.raises(ValueError, match="Invalid data type: Price must be numeric"):
        func.electricity_line_chart_processed(trade_data, "Czechia", [2021, 2023])


def test_electricity_line_chart_processed_mean(electricity_data_sample):
    """
    Test if the function correctly calculates the mean of the prices
    """
    result, percentage_text = func.electricity_line_chart_processed(
        electricity_data_sample, "Czechia", [2021, 2023]
    )

    assert result["Price"].iloc[0] == 0.494  # mean of 0.123 and 0.85

    assert round(result["Price"].iloc[1], 2) == 0.60  # mean of 0.323 and 0.665


def test_electricity_line_chart_processed_missing_country(electricity_data_sample):
    """
    Test if the function raises an error when the country is not present in the data
    """
    with pytest.raises(ValueError, match="Country not found in the data"):
        func.electricity_line_chart_processed(
            electricity_data_sample,
            "Greece",
            [
                2021,
                2022,
            ],  # greece is not present in the data so it should raise an error
        )


def test_electricity_line_chart_processed_larger_year(electricity_data_sample):
    """
    Test if the function raises an error when the country is not present in the data
    """
    with pytest.raises(
        ValueError, match="The first year must be less than the second year"
    ):
        func.fuel_line_chart_processed(
            electricity_data_sample, "Greece", [2023, 2022]
        )  # first year is greater than the second year so it should raise an error
