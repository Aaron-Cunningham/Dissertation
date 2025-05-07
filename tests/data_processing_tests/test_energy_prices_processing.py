import pytest
import data_processing.energy_prices_processing as func
import pandas as pd
from tests.test_data import *


def test_fuel_line_chart_processing_missing_columns(fuel_data_sample):
    """
    Test for missing columns in the fuel data
    """
    fuel_data_sample = fuel_data_sample.drop(columns=["Fuel"])  # Drop the Fuel column
    with pytest.raises(
        ValueError,
        match="Input data must contain the following columns: Fuel",  # should raise an error as no fuel column
    ):
        func.fuel_line_chart_processing(fuel_data_sample, [2021, 2023])


def test_electricity_line_chart_processing_missing_columns(electricity_data_sample):
    """Test for missing columns in the electricity data"""
    electricity_data_sample = electricity_data_sample.drop(
        columns=["Price"]
    )  # Drop the Price column
    with pytest.raises(
        ValueError,
        match="Input data must contain the following columns: Column not found: Price",  # should raise an error as no price column
    ):
        func.electricity_line_chart_processing(electricity_data_sample, [2021, 2023])


def test_fuel_map_processing_missing_columns(fuel_data_sample):
    """
    Test for missing columns in the fuel data
    """
    fuel_data_sample = fuel_data_sample.drop(columns=["Price"])  # Drop the Price column
    with pytest.raises(
        ValueError,
        match="Input data must contain the following columns: Price",  # should raise an error as no price column
    ):
        func.fuel_map_processing(fuel_data_sample, 2021, "Diesel")


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_fuel_map_processing_string_as_price(fuel_data_sample):
    """
    Test if the function raises an error when the value is string"""
    trade_data = fuel_data_sample.copy()
    trade_data.loc[0, "Price"] = "string"

    with pytest.raises(ValueError, match="Invalid data type: Price must be numeric"):
        func.fuel_map_processing(trade_data, 2021, "Diesel")


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_fuel_line_chart_processing_string_as_price(fuel_data_sample):
    """
    Test if the function raises an error when the value is string"""
    trade_data = fuel_data_sample.copy()
    trade_data.loc[0, "Price"] = "string"

    with pytest.raises(ValueError, match="Invalid data type: Price must be numeric"):
        func.fuel_line_chart_processing(trade_data, [2021, 2023])


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_electricity_line_chart_processing_string_as_price(electricity_data_sample):
    """
    Test if the function raises an error when the value is string"""
    trade_data = electricity_data_sample.copy()
    trade_data.loc[0, "Price"] = "string"

    with pytest.raises(ValueError, match="Invalid data type: Price must be numeric"):
        func.electricity_line_chart_processing(trade_data, [2021, 2023])


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_fuel_map_processing_string_as_year(fuel_data_sample):
    """
    Test if the function raises an error when the value is string"""
    trade_data = fuel_data_sample.copy()
    trade_data.loc[0, "Year"] = "string"

    with pytest.raises(ValueError, match="Invalid data type: Year must be numeric"):
        func.fuel_map_processing(trade_data, 2021, "Diesel")


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_fuel_line_chart_processing_string_as_year(fuel_data_sample):
    """
    Test if the function raises an error when the value is string"""
    trade_data = fuel_data_sample.copy()
    trade_data.loc[0, "Year"] = "string"

    with pytest.raises(ValueError, match="Invalid data type: Year must be numeric"):
        func.fuel_line_chart_processing(trade_data, [2021, 2023])


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_electricity_line_chart_processing_string_as_Year(electricity_data_sample):
    """
    Test if the function raises an error when the value is string"""
    trade_data = electricity_data_sample.copy()
    trade_data.loc[0, "Year"] = "string"

    with pytest.raises(ValueError, match="Invalid data type: Year must be numeric"):
        func.electricity_line_chart_processing(trade_data, [2021, 2023])


def test_fuel_map_processing_empty_df():
    """
    Test if the function raises an error when data frame is empty"""
    trade_data = pd.DataFrame()  # empty dataframe

    with pytest.raises(ValueError, match="Input data is empty"):
        func.fuel_map_processing(trade_data, 2021, "Diesel")


def test_fuel_line_chart_processing_empty_df():
    """
    Test if the function raises an error when data frame is empty"""
    trade_data = pd.DataFrame()  # empty dataframe

    with pytest.raises(ValueError, match="Input data is empty"):
        func.fuel_line_chart_processing(trade_data, [2021, 2022])


def test_electricity_line_chart_processing_empty_df():
    """
    Test if the function raises an error when data frame is empty"""
    trade_data = pd.DataFrame()  # empty dataframe

    with pytest.raises(ValueError, match="Input data is empty"):
        func.electricity_line_chart_processing(trade_data, [2021, 2022])


def test_fuel_line_chart_processing_invalid_year_range(fuel_data_sample):
    """
    Test for invalid year range in the fuel data
    """
    with pytest.raises(
        ValueError,
        match="The start year must be less than the end year",  # should raise an error as the start year is greater than the end year
    ):
        func.fuel_line_chart_processing(fuel_data_sample, [2023, 2021])


def test_electricity_line_chart_processing_invalid_year_range(electricity_data_sample):
    """
    Test for invalid year range in the electricity data
    """
    with pytest.raises(
        ValueError,
        match="The start year must be less than the end year",  # should raise an error as the start year is greater than the end year
    ):
        func.electricity_line_chart_processing(electricity_data_sample, [2023, 2021])


def test_electricity_line_chart_processing_results(electricity_data_sample):
    """
    Test if the function returns the correct data for the pre war bar chart
    """
    result, percentage_text = func.electricity_line_chart_processing(
        electricity_data_sample, [2021, 2023]
    )

    assert round(result["Price"].iloc[0], 4) == 0.4900  # mean of 0.123 and 0.857
    assert (
        round(result["Price"].iloc[1], 4) == 0.5970
    )  # mean of 0.576, 0.824, 0.323, and 0.665
    assert round(result["Price"].iloc[2], 4) == 0.6015  # mean of 0.344 and 0.859


def test_fuel_line_chart_processing_results(fuel_data_sample):
    """
    Test if the function returns the correct data for the pre war bar chart
    """
    result, percentage_text = func.fuel_line_chart_processing(
        fuel_data_sample, [2021, 2023]
    )
    (result)

    assert result["Diesel"].iloc[0] == 1.45  # mean of 2000 and 900
    assert result["Petrol"].iloc[0] == 2.1  # only 1 value in 2021 petrol == 2100
    assert result["Diesel"].iloc[1] == 1.5  # mean of 2100 and 900
    assert result["Petrol"].iloc[1] == 1.8  # mean of 1800 and 1800
    assert result["Diesel"].iloc[2] == 1.6  # mean of 2200 and 1000
    assert result["Petrol"].iloc[2] == 2.5  # mean of 2500 and 2500
