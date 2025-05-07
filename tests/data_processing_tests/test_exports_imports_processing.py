import pytest
import data_processing.exports_imports_processing as func
import pandas as pd
from tests.test_data import *


# Pre and post war map processing tests
def test_pre_war_map_processing_empty_df():
    """
    Test if the function raises an error when data frame is empty"""
    trade_data = pd.DataFrame()  # empty dataframe

    with pytest.raises(ValueError, match="Input data is empty"):
        func.pre_war_map_processing(trade_data, "weight (kg)", "coal", "importer")


def test_post_war_map_processing_empty_df():
    """
    Test if the function raises an error when data frame is empty"""
    trade_data = pd.DataFrame()  # empty dataframe

    with pytest.raises(ValueError, match="Input data is empty"):
        func.pre_war_map_processing(trade_data, "weight (kg)", "coal", "importer")


def test_pre_war_map_processing_no_fossil_fuel(trade_data_sample):
    """
    Test if the function raises an error when the fossil fuel is not found in the data
    """  # empty dataframe

    with pytest.raises(ValueError, match="Fossil fuel not found in the data"):
        func.pre_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Wrong Fossil",
            "importer",  # wrong fossil fuel
        )


def test_post_war_map_processing_no_fossil_fuel(trade_data_sample):
    """
    Test if the function raises an error when the fossil fuel is not found in the data
    """  # empty dataframe

    with pytest.raises(ValueError, match="Fossil fuel not found in the data"):
        func.post_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Wrong Fossil",
            "importer",  # wrong fossil fuel
        )


def test_pre_war_map_processing_no_chart_select(trade_data_sample):
    """
    Test if the function raises an error when the chart select is not found in the data
    """  # empty dataframe

    with pytest.raises(ValueError, match="Chart select not found in the data"):
        func.pre_war_map_processing(
            trade_data_sample,
            "weight (kg)",
            "Coal",
            "wrong chart",  # wrong chart select
        )


def test_post_war_map_processing_no_chart_select(trade_data_sample):
    """
    Test if the function raises an error when the chart select is not found in the data
    """  # empty dataframe

    with pytest.raises(ValueError, match="Chart select not found in the data"):
        func.post_war_map_processing(
            trade_data_sample,
            "weight (kg)",
            "Coal",
            1,  # wrong chart select
        )


def test_pre_war_map_processing_no_chart_select(trade_data_sample):
    """
    Test if the function raises an error when the measurement is not found in the data
    """  # empty dataframe

    with pytest.raises(ValueError, match="Measurement not found in the data"):
        func.pre_war_map_processing(
            trade_data_sample,
            "pounds",  # wrong measurement
            "Coal",
            "importer",
        )


def test_post_war_map_processing_no_chart_select(trade_data_sample):
    """
    Test if the function raises an error when the measurement is not found in the data
    """  # empty dataframe

    with pytest.raises(ValueError, match="Measurement not found in the data"):
        func.post_war_map_processing(
            trade_data_sample,
            "eggs",  # wrong measurement
            "Coal",
            "importer",
        )


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_pre_war_map_processing_string_as_value(trade_data_sample):
    """
    Test if the function raises an error when the value is string"""
    trade_data_sample.loc[0, "value (US$)"] = "string"  # change the value to string

    with pytest.raises(
        ValueError, match=r"Invalid data type: value \(us\$\) must be numeric"
    ):
        func.pre_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_post_war_map_processing_string_as_value(trade_data_sample):
    """
    Test if the function raises an error when the value is string"""
    trade_data_sample.loc[0, "value (US$)"] = "string"  # change the value to string

    with pytest.raises(
        ValueError, match=r"Invalid data type: value \(us\$\) must be numeric"
    ):
        func.post_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_pre_war_map_processing_string_as_year(trade_data_sample):
    """
    Test if the function raises an error when the value is string"""
    trade_data_sample.loc[0, "year"] = "string"  # change the value to string

    with pytest.raises(ValueError, match="Invalid data type: year must be numeric"):
        func.pre_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_post_war_map_processing_string_as_year(trade_data_sample):
    """
    Test if the function raises an error when the value is string"""
    trade_data_sample.loc[0, "year"] = "string"  # change the value to string

    with pytest.raises(ValueError, match="Invalid data type: year must be numeric"):
        func.post_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


def test_pre_war_map_processing_number_as_importer(trade_data_sample):
    """
    Test if the function raises an error when the value is a number"""
    trade_data_sample.loc[0, "importer"] = 0  # change the value to number

    with pytest.raises(ValueError, match="Invalid data type: importer must be String"):
        func.pre_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


def test_post_war_map_processing_number_as_importer(trade_data_sample):
    """
    Test if the function raises an error when the value is number"""
    trade_data_sample.loc[0, "importer"] = 0  # change the value to number

    with pytest.raises(ValueError, match="Invalid data type: importer must be String"):
        func.post_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


def test_pre_war_map_processing_number_as_importer_continent(trade_data_sample):
    """
    Test if the function raises an error when the importer continent is a number"""
    trade_data_sample.loc[0, "importer continent"] = 0  # change the value to number

    with pytest.raises(
        ValueError, match="Invalid data type: importer continent must be String"
    ):
        func.pre_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


def test_post_war_map_processing_number_as_importer_continent(trade_data_sample):
    """
    Test if the function raises an error when the importer continent is number"""
    trade_data_sample.loc[0, "importer continent"] = 0  # change the value to number

    with pytest.raises(
        ValueError, match="Invalid data type: importer continent must be String"
    ):
        func.post_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


def test_pre_war_map_processing_number_as_resource(trade_data_sample):
    """
    Test if the function raises an error when the resource is a number"""
    trade_data_sample.loc[0, "resource"] = 0  # change the value to number

    with pytest.raises(ValueError, match="Invalid data type: resource must be String"):
        func.pre_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


def test_post_war_map_processing_number_as_resource(trade_data_sample):
    """
    Test if the function raises an error when the resource is number"""
    trade_data_sample.loc[0, "resource"] = 0  # change the value to number

    with pytest.raises(ValueError, match="Invalid data type: resource must be String"):
        func.post_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


def test_pre_war_map_processing_number_as_exporterISO(trade_data_sample):
    """
    Test if the function raises an error when the exporterISO is a number"""
    trade_data_sample.loc[0, "exporterISO"] = 0  # change the value to number

    with pytest.raises(
        ValueError, match="Invalid data type: exporterISO must be String"
    ):
        func.pre_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


def test_post_war_map_processing_number_as_exporterISO(trade_data_sample):
    """
    Test if the function raises an error when the exporterISO is number"""
    trade_data_sample.loc[0, "exporterISO"] = 0  # change the value to number

    with pytest.raises(
        ValueError, match="Invalid data type: exporterISO must be String"
    ):
        func.post_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


def test_pre_war_map_processing_number_as_importerISO(trade_data_sample):
    """
    Test if the function raises an error when the importerISO is a number"""
    trade_data_sample.loc[0, "importerISO"] = 0  # change the value to number

    with pytest.raises(
        ValueError, match="Invalid data type: importerISO must be String"
    ):
        func.pre_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


def test_post_war_map_processing_number_as_importerISO(trade_data_sample):
    """
    Test if the function raises an error when the importerISO is number"""
    trade_data_sample.loc[0, "importerISO"] = 0  # change the value to number

    with pytest.raises(
        ValueError, match="Invalid data type: importerISO must be String"
    ):
        func.post_war_map_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            "importer",
        )


def test_pre_war_map_processing_missing_column(trade_data_sample):
    """
    Test if the function reaises error when the year column is missing"""
    trade_data = trade_data_sample.drop(columns=["year"])  # remove the column exporter
    with pytest.raises(
        ValueError, match="Input data must contain the following columns: year"
    ):
        func.pre_war_map_processing(
            trade_data,
            "value (US$)",
            "Coal",
            "importer",
        )


def test_post_war_map_processing_missing_column(trade_data_sample):
    """
    Test if the function raises error when the year column is missing"""
    trade_data = trade_data_sample.drop(columns=["year"])  # remove the column exporter

    with pytest.raises(
        ValueError, match="Input data must contain the following columns: year"
    ):
        func.post_war_map_processing(
            trade_data,
            "value (US$)",
            "Coal",
            "importer",
        )


# market share processing tests
def test_market_share_processing_empty_df():
    """
    Test if the function raises an error when data frame is empty"""
    trade_data = pd.DataFrame()  # empty dataframe

    with pytest.raises(ValueError, match="Input data is empty"):
        func.market_share_bar_processing(
            trade_data,
            "weight (kg)",
            "coal",
            [2021, 2022],
            5,
            "importer",
            "importer continent",
        )


# market share processing tests
def test_market_share_processing_no_measurement(trade_data_sample):
    """
    Test if the function raises an error when no measurement is found in the data"""

    with pytest.raises(ValueError, match="Measurement not found in the data"):
        func.market_share_bar_processing(
            trade_data_sample,
            "wrong measurement",  # wrong measurement
            "coal",
            [2021, 2022],
            5,
            "importer",
            "importer continent",
        )


def test_market_share_processing_no_fossil(trade_data_sample):
    """
    Test if the function raises an error when no fossil fuel is found in the data"""

    with pytest.raises(ValueError, match="Fossil fuel not found in the data"):
        func.market_share_bar_processing(
            trade_data_sample,
            "value (US$)",
            "banana",  # wrong fossil fuel
            [2021, 2022],
            5,
            "importer",
            "importer continent",
        )


def test_market_share_processing_incorrect_years(trade_data_sample):
    """
    Test if the function raises an error when incorrect years is found in the data"""

    with pytest.raises(
        ValueError, match="The start year must be less than the end year"
    ):
        func.market_share_bar_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            [2022, 2021],  # wrong years order
            5,
            "importer",
            "importer continent",
        )


def test_market_share_processing_zero_num_countries(trade_data_sample):
    """
    Test if the function raises an error when incorrect num of countries is found in the data
    """

    with pytest.raises(
        ValueError, match="The number of countries must be greater than 0"
    ):
        func.market_share_bar_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            [2022, 2023],
            0,  # wrong number of countries < 1
            "importer",
            "importer continent",
        )


def test_market_share_processing_chaart_select_not_found(trade_data_sample):
    """
    Test if the function raises an error when no chart select is found in the data
    """

    with pytest.raises(ValueError, match="Chart select not found in the data"):
        func.market_share_bar_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            [2022, 2023],
            1,
            "not an importer",  # wrong chart select
            "importer continent",
        )


def test_market_share_processing_chaart_wrong_continent(trade_data_sample):
    """
    Test if the function raises an error when wrong continent is found in the data
    """

    with pytest.raises(ValueError, match="Continent not found in the data"):
        func.market_share_bar_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            [2022, 2023],
            1,
            "importer",
            "wrong importer continent",  # wrong continent
        )


def test_market_share_processing_sum_and_ranking(trade_data_sample):
    """
    Test if the function correctly calculates the total sum and percentage the values of the resources
    """
    result = func.market_share_bar_processing(
        trade_data_sample,
        "value (US$)",
        "Gas",
        [2021, 2024],
        5,
        "importer",
        "importer continent",
    )

    total_value = result["value (US$)"].sum()
    assert total_value == 4000  # total sum 1500 + 2500 = 4000
    assert (
        result.loc[0, "percent"] == 62.5 and result.loc[0, "importer"] == "France"
    )  # frances share (2500 / 4000) * 100 = 0.625 * 100 = 62.5%
    assert (
        result.loc[1, "percent"] == 37.5 and result.loc[1, "importer"] == "Germany"
    )  # Germanys share (1500 / 4000) * 100 = 0.375 * 100 = 37.5%


def test_market_share_processing_missing_column(trade_data_sample):
    """
    Test if the function raises error when the year column is missing"""
    trade_data = trade_data_sample.drop(columns=["year"])  # remove the column exporter

    with pytest.raises(
        ValueError, match="Input data must contain the following columns: year"
    ):
        func.market_share_bar_processing(
            trade_data,
            "value (US$)",
            "Gas",
            [2021, 2024],
            5,
            "importer",
            "importer continent",
        )


# top export bar processing tests


def test_top_export_processing_no_measurement(trade_data_sample):
    """
    Test if the function raises an error when no measurement is found in the data"""

    with pytest.raises(ValueError, match="Measurement not found in the data"):
        func.top_export_bar_processing(
            trade_data_sample,
            "wrong measurement",  # wrong measurement
            "coal",
            2022,
            5,
            "importer",
            "importer continent",
        )


def test_top_export_processing_no_fossil(trade_data_sample):
    """
    Test if the function raises an error when no fossil fuel is found in the data"""

    with pytest.raises(ValueError, match="Fossil fuel not found in the data"):
        func.top_export_bar_processing(
            trade_data_sample,
            "value (US$)",
            "banana",  # wrong fossil fuel
            2022,
            5,
            "importer",
            "importer continent",
        )


def test_top_export_processing_zero_num_countries(trade_data_sample):
    """
    Test if the function raises an error when incorrect num of countries is found in the data
    """

    with pytest.raises(
        ValueError, match="The number of countries must be greater than 0"
    ):
        func.top_export_bar_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            2022,
            0,  # wrong number of countries < 1
            "importer",
            "importer continent",
        )


def test_top_export_processing_select_not_found(trade_data_sample):
    """
    Test if the function raises an error when no chart select is found in the data
    """

    with pytest.raises(ValueError, match="Chart select not found in the data"):
        func.top_export_bar_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            2022,
            1,
            "not an importer",  # wrong chart select
            "importer continent",
        )


def test_top_export_processing_wrong_continent(trade_data_sample):
    """
    Test if the function raises an error when wrong continent is found in the data
    """

    with pytest.raises(ValueError, match="Continent not found in the data"):
        func.top_export_bar_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            2022,
            1,
            "importer",
            "wrong importer continent",  # wrong continent
        )


def test_top_export_processing_no_year(trade_data_sample):
    """
    Test if the function raises an error when no year is found in the data
    """

    with pytest.raises(ValueError, match="Year not found in the data"):
        func.top_export_bar_processing(
            trade_data_sample,
            "value (US$)",
            "Coal",
            0,  # wrong year
            1,
            "importer",
            "importer continent",
        )


def test_top_export_processing_ranking(trade_data_sample):
    """
    Test if the function correctly calculates the total sum and percentage the values of the resources
    """
    result = func.top_export_bar_processing(
        trade_data_sample,
        "value (US$)",
        "Oil",
        2025,
        5,
        "importer",
        "importer continent",
    )

    assert result.loc[0, "importer"] == "Norway"  # Norway is the top exporter
    assert result.loc[1, "importer"] == "Romania"  # Romania is the second top exporter


# line chart processing tests
def test_line_chart_imports_processed_no_measurement(trade_data_sample):
    """
    Test if the function raises an error when no measurement is found in the data"""

    with pytest.raises(ValueError, match="Measurement not found in the data"):
        func.line_chart_imports_processed(
            trade_data_sample,
            "no measurement",  # wrong measurement
            [2021, 2022],
        )


def test_line_chart_imports_processed_incorrect_years(trade_data_sample):
    """
    Test if the function raises an error when incorrect years is found in the data"""

    with pytest.raises(
        ValueError, match="The start year must be less than the end year"
    ):
        func.line_chart_imports_processed(
            trade_data_sample,
            "value (US$)",
            [2023, 2022],  # wrong years order
        )
