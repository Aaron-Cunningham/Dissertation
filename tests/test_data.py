import pytest
import pandas as pd


# Test Data
@pytest.fixture
def trade_data_sample():
    """
    Sample trade data
    """
    return pd.DataFrame(
        {
            "value (US$)": [1000, 2100, 1500, 1800, 2200, 2500, 2000, 2100, 1000, 900],
            "year": [2021, 2021, 2022, 2022, 2023, 2023, 2023, 2024, 2025, 2025],
            "importer": [
                "Germany",
                "Germany",
                "Germany",
                "Russia",
                "India",
                "France",
                "Germany",
                "Germany",
                "Norway",
                "Romania",
            ],
            "resource": [
                "Oil",
                "Oil",
                "Gas",
                "Oil",
                "Coal",
                "Gas",
                "Coal",
                "Coal",
                "Oil",
                "Oil",
            ],
            "importer continent": [
                "Europe",
                "Europe",
                "Europe",
                "Europe",
                "Asia",
                "Europe",
                "Europe",
                "Europe",
                "Europe",
                "Europe",
            ],
            "exporter": [
                "USA",
                "Canada",
                "Mexico",
                "Brazil",
                "Australia",
                "Norway",
                "South Africa",
                "Nigeria",
                "Germany",
                "France",
            ],
            "exporter continent": [
                "North America",
                "North America",
                "North America",
                "South America",
                "Australia",
                "Europe",
                "Africa",
                "Africa",
                "Europe",
                "Europe",
            ],
            "importerISO": [
                "DEU",
                "DEU",
                "DEU",
                "RUS",
                "IND",
                "FRA",
                "DEU",
                "DEU",
                "NOR",
                "ROU",
            ],
            "exporterISO": [
                "USA",
                "CAN",
                "MEX",
                "BRA",
                "AUS",
                "NOR",
                "ZAF",
                "NGA",
                "DEU",
                "FRA",
            ],
        }
    )


# Test Data for electricity
@pytest.fixture
def electricity_data_sample():
    """
    Sample electricity data
    """
    return pd.DataFrame(
        {
            "Price": [0.123, 0.857, 0.576, 0.824, 0.344, 0.859, 0.323, 0.665],
            "Year": [2021, 2021, 2022, 2022, 2023, 2023, 2022, 2022],
            "Country": [
                "Austria",
                "Belgium",
                "Bulgaria",
                "Cyprus",
                "Czechia",
                "Czechia",
                "Czechia",
                "Czechia",
            ],
            "countryISO": [
                "AUT",
                "BEL",
                "BGR",
                "CYP",
                "CZE",
                "CZE",
                "CZE",
                "CZE",
            ],
        }
    )


# Test Data for fuel
@pytest.fixture
def fuel_data_sample():
    """
    Sample fuel data
    """
    return pd.DataFrame(
        {
            "Price": [2100, 2100, 1800, 900, 2200, 1000, 2000, 2500, 900],
            "Year": [2021, 2022, 2022, 2022, 2023, 2023, 2021, 2023, 2021],
            "Country": [
                "Belgium",
                "Bulgaria",
                "Cyprus",
                "Czechia",
                "Czechia",
                "Czechia",
                "Czechia",
                "Austria",
                "Czechia",
            ],
            "Fuel": [
                "Petrol",
                "Diesel",
                "Petrol",
                "Diesel",
                "Diesel",
                "Diesel",
                "Diesel",
                "Petrol",
                "Diesel",
            ],
            "countryISO": [
                "BEL",
                "BGR",
                "CYP",
                "CZE",
                "CZE",
                "CZE",
                "CZE",
                "AUT",
                "CZE",
            ],
        }
    )
