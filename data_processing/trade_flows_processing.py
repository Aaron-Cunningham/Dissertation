from utils.utils_data import group_data, load_trade_data, load_coordinates_data

trade_data = load_trade_data()
coordinates = load_coordinates_data()


def map_data_processing():
    """
    Processes the data for the map in trade flows
    returns:
        merge_coordinates_partner: the data for the map in trade flows
    """
    # MAP DATA FILTERING
    # filters to only show imports to europe
    trade_data_filtered = trade_data[(trade_data["importer continent"] == "Europe")]
    # filters the the data so it shows unique trade flows between countries based on resource, exporter, and importer the sums the total with value (US$)
    trade_data_modified = group_data(
        trade_data_filtered,
        ["exporter", "importer", "resource", "exporterISO", "importerISO", "year"],
    )

    # adding the long and lat for exporter countries by matching alpha-3 code to exporterISO
    merge_coordinates_reporter = trade_data_modified.merge(
        coordinates[["Alpha-3 code", "Latitude (average)", "Longitude (average)"]],
        left_on="exporterISO",
        right_on="Alpha-3 code",
        how="left",
    )

    # renaming the exporter long and lat cols so they aren't duped when adding importer long and lat
    merge_coordinates_reporter.rename(
        columns={
            "Latitude (average)": "exporter_lat",
            "Longitude (average)": "exporter_lon",
        },
        inplace=True,
    )

    # adding the long and lat for importer countries by matching alpha-3 code to importerISO
    merge_coordinates_partner = merge_coordinates_reporter.merge(
        coordinates[["Alpha-3 code", "Latitude (average)", "Longitude (average)"]],
        left_on="importerISO",
        right_on="Alpha-3 code",
        how="left",
    )
    # renaming the importer lat and long cols to keep the data consistent
    merge_coordinates_partner.rename(
        columns={
            "Latitude (average)": "importer_lat",
            "Longitude (average)": "importer_lon",
        },
        inplace=True,
    )

    # removing the duplicate ISO-3 codes and returning
    return merge_coordinates_partner.drop(["Alpha-3 code_x", "Alpha-3 code_y"], axis=1)


def sankey_data_processing(fossil_fuel, start_year, end_year, num_trade_flows):
    """
    Processes the data for the sankey diagram
    args:
        data: the data for the sankey diagram
        fossil_fuel str: the fossil fuel selected by the user (coal, oil, gas)
        num_trade_flows int: the number of trade flows to display
    returns:
        sankey_renamed: the data for the sankey diagram
    """
    # groups by exporter, importer, resource, year, and exporter/importer continent (for colours) and sums by value
    sankey_data_grouped = group_data(
        trade_data,
        [
            "exporter",
            "importer",
            "resource",
            "year",
            "exporter continent",
            "importer continent",
        ],
    )
    # filters the data by the user input of fossil fuel, year range and only importer continent of Europe
    sankey_filtered = sankey_data_grouped[
        (sankey_data_grouped["resource"] == fossil_fuel)
        & (sankey_data_grouped["year"] >= start_year)
        & (sankey_data_grouped["year"] <= end_year)
        & (sankey_data_grouped["importer continent"] == "Europe")
    ]

    # renames the columns for the diagram
    sankey_renamed = sankey_filtered[
        [
            "exporter",
            "importer",
            "value (US$)",
            "exporter continent",
            "importer continent",
        ]
    ].rename(
        columns={
            "exporter": "source",
            "importer": "target",
            "value (US$)": "count",
        }
    )

    # Get top flows
    return sankey_renamed.nlargest(num_trade_flows, "count")
