import pandas as pd
import json


def group_data(trade_data, group_cols, value_col="value (US$)"):
    """
    Groupes data by specified columns and then sums the value column

    args:
        trade_data (pandas.Dataframe): This is the input dataframe containing the trade data
        group_cols (list): This is a list of column names e.g. (['year', 'exporter'])
        value_col (str): The column name which will be used to sum e.g. ('value (US$)')

    returns:
        pandas.DataFrame: This will be a dataframe with the grouped data, summed values

    notes:
        1) reqrires pandas to be imported in the file where this function is used
    """
    return trade_data.groupby(group_cols)[value_col].sum().reset_index()


def load_trade_data():
    """
    Loads the updated trade data

    returns:
        pandas.DataFrmae: The dataframe containing the trade data

    notes:
        1) Data adapted from https://comtradeplus.un.org/TradeFlow?Frequency=A&Flows=X&CommodityCodes=TOTAL&Partners=0&Reporters=842&period=all&AggregateBy=none&BreakdownMode=plus
    """
    return pd.read_csv("data/Trade Data Updated.csv")


def load_coordinates_data():
    """
    Loads the updated trade data

    returns:
        pandas.DataFrmae: The dataframe containing the coordinates, country, and ISO data

    notes:
        1) Data refernced from https://gist.github.com/metal3d/5b925077e66194551df949de64e910f6
    """
    return pd.read_csv("data/country-coord.csv")


def load_electricity_data():
    """
    Loads the electricity prices data

    returns:
        pandas.DataFrmae: The dataframe containing 10 sheets, and columns with time and area e.g. (EU, Germany, Spain, Etc)

    notes:
        1) Data adapted from https://ec.europa.eu/eurostat/databrowser/view/nrg_pc_204/default/table?lang=en
    """
    return pd.read_csv("data/Electricity Prices Cleaned.csv")


def load_fuel_cleaned():
    """
    notes:
        1) Data adapted from https://energy.ec.europa.eu/data-and-analysis/weekly-oil-bulletin_en#price-developments

    returns:
        pandas.DataFrmae: The dataframe containing the fuel data
    """
    return pd.read_csv("data/Fuel Prices Cleaned.csv")


def load_country_shapes():
    """
    Loads the country shapes data

    returns:
        json file containing the country shapes data

    notes:
        Referenced from: https://github.com/johan/world.geo.json/blob/master/countries.geo.json
    """
    try:
        with open("data/countries.geo.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        ("Error: The CSV file could not be found.")
        return None
    except json.JSONDecodeError:
        ("Error: The JSON file could not be decoded.")
        return None
    except Exception as e:
        (f"Error: {e}")
        return None
    except UnicodeDecodeError:
        ("Error: The file could not be decoded.")
        return None


def calculate_change(data, start_year, end_year, *columns):
    """
    Calculates the percentage change between two inputted years for the speicic columns in the dataset

    agrs:
        data: This is a pandas dataframe
        start_year: starting year for the calculation
        end_year: ending year for the calculation
        *columns: number of column names to calculate the percentage change for

    returns:
        1) Formatted HTML string with the percentage change results

    Formula:
        Percentage Increase/Decrease = ((New Number - Original Number)/Original Number) * 100

    notes:
        1) Percentage change formula referenced from https://www.investopedia.com/terms/p/percentage-change.asp
        2) Returns the result with a positive sign if positive, the negative sign is defaulted
    """
    result = (
        f"<b>Percentage Change </b><br>"
        + f"<b>From {start_year} To {end_year}: </b><br> <br>"
    )

    for col in columns:
        try:
            start_value = data[col].iloc[0]  # accesses the first value from start year
            end_value = data[col].iloc[-1]  # accesses the last value from end year
            if start_value == 0:
                result += f"<b>{col}: Non Applicable"
            else:
                percentage_change = (
                    (end_value - start_value) / start_value
                ) * 100  # calculates the change
                sign = (
                    "+" if percentage_change >= 0 else ""
                )  # determines if it needs to use a positive sign
                result += f"<b>{col}: {sign}{percentage_change:.2f}%</b> <br> <br>"  # appends the results
        except ZeroDivisionError:
            result += f"<b>{col}: Non Applicable"
    return result
