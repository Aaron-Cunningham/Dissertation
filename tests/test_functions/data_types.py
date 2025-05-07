import pandas as pd
from utils.utils_data import load_trade_data

trade_data = load_trade_data()


def data_types(data):
    """
    Checks if the columns are the correct data type
    args:
        data: the data to check
    returns:
        None
    Raises:
        ValueError: if the data type is incorrect
    """
    if "value (US$)" in data.columns:
        if not pd.api.types.is_numeric_dtype(data["value (US$)"]):
            raise ValueError("Invalid data type: value (us$) must be numeric")

    if "year" in data.columns:
        if not pd.api.types.is_numeric_dtype(data["year"]):
            raise ValueError("Invalid data type: year must be numeric")

    if "importer" in data.columns:
        if not pd.api.types.is_string_dtype(data["importer"]):
            raise ValueError("Invalid data type: importer must be String")

    if "exporter" in data.columns:
        if not pd.api.types.is_string_dtype(data["exporter"]):
            raise ValueError("Invalid data type: exporter must be String")
    if "importer continent" in data.columns:
        if not pd.api.types.is_string_dtype(data["importer continent"]):
            raise ValueError("Invalid data type: importer continent must be String")

    if "flow" in data.columns:
        if not pd.api.types.is_string_dtype(data["exporter"]):
            raise ValueError("Invalid data type: flow must be String")

    if "resource" in data.columns:
        if not pd.api.types.is_string_dtype(data["resource"]):
            raise ValueError("Invalid data type: resource must be String")

    if "exporterISO" in data.columns:
        if not pd.api.types.is_string_dtype(data["exporterISO"]):
            raise ValueError("Invalid data type: exporterISO must be String")

    if "importerISO" in data.columns:
        if not pd.api.types.is_string_dtype(data["importerISO"]):
            raise ValueError("Invalid data type: importerISO must be String")

    if "weight (kg)" in data.columns:
        if not pd.api.types.is_numeric_dtype(data["weight (kg)"]):
            raise ValueError("Invalid data type: weight (kg) must be numeric")

    if "importerISO" in data.columns:
        if not pd.api.types.is_string_dtype(data["importerISO"]):
            raise ValueError("Invalid data type: importerISO must be String")

    if "Country" in data.columns:
        if not pd.api.types.is_string_dtype(data["Country"]):
            raise ValueError("Invalid data type: Country must be String")

    if "Year" in data.columns:
        if not pd.api.types.is_numeric_dtype(data["Year"]):
            raise ValueError("Invalid data type: Year must be numeric")

    if "Price" in data.columns:
        if not pd.api.types.is_numeric_dtype(data["Price"]):
            raise ValueError("Invalid data type: Price must be numeric")

    if "Fuel" in data.columns:
        if not pd.api.types.is_string_dtype(data["Fuel"]):
            raise ValueError("Invalid data type: Fuel must be numeric")
