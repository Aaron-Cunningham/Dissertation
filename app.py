import dash
from dash import Dash, html, dcc
from dotenv import load_dotenv
import dash_bootstrap_components as dbc
from utils.cache_config import cache


load_dotenv()

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
cache.init_app(app.server)
server = app.server

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Nav(
            children=[
                html.Div(
                    className="nav-buttons",
                    children=[
                        dcc.Link(
                            "Trade Flows",
                            href="/",
                            className="nav-button",
                            id="nav-trade-flows",
                        ),
                        dcc.Link(
                            "Exports and Imports",
                            href="/exports",
                            className="nav-button",
                            id="nav-exports",
                        ),
                        dcc.Link(
                            "Energy Prices",
                            href="/energy-prices",
                            className="nav-button",
                            id="nav-prices",
                        ),
                        dcc.Link(
                            "European Country Data",
                            href="/country-data",
                            className="nav-button",
                            id="nav-country-data",
                        ),
                    ],
                ),
            ],
        ),
        dash.page_container,  # This component dynamically loads the pages
    ]
)

# Runs the app
if __name__ == "__main__":
    app.run_server(debug=True)
