"""SpaceX launch dashboard built with Dash, Pandas, and Plotly."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

APP_TITLE = "SpaceX Launch Success Dashboard"
APP_SUBTITLE = (
    "Explore SpaceX launch performance by site and payload mass to see how mission "
    "conditions relate to launch outcomes."
)
DATA_PATH = Path(__file__).resolve().parent / "data" / "spacex_launch_dash.csv"
DEFAULT_LAUNCH_SITE = "ALL"
PAYLOAD_SLIDER_BOUNDS = (0, 10000)
DEFAULT_PAYLOAD_RANGE = list(PAYLOAD_SLIDER_BOUNDS)
PAYLOAD_SLIDER_STEP = 500
OUTCOME_LABELS = {0: "Failure", 1: "Success"}
CHART_TITLES = {
    "pie": "Launch Outcomes by Site",
    "scatter": "Payload Mass vs. Launch Outcome",
}
AXIS_LABELS = {
    "Payload Mass (kg)": "Payload Mass (kg)",
    "Booster Version Category": "Booster Version Category",
    "Launch Outcome": "Launch Outcome",
}
REQUIRED_COLUMNS = {
    "Launch Site",
    "class",
    "Payload Mass (kg)",
    "Booster Version Category",
    "Flight Number",
}
GRAPH_HEIGHTS = {"pie": 420, "scatter": 500}

PAGE_STYLE = {
    "background": "linear-gradient(180deg, #f8fafc 0%, #eef4fb 100%)",
    "minHeight": "100vh",
    "padding": "40px 16px 56px",
    "fontFamily": '"Avenir Next", "Segoe UI", sans-serif',
}
CONTENT_STYLE = {
    "maxWidth": "1100px",
    "margin": "0 auto",
    "display": "flex",
    "flexDirection": "column",
    "gap": "24px",
}
CARD_STYLE = {
    "backgroundColor": "#ffffff",
    "borderRadius": "16px",
    "boxShadow": "0 12px 30px rgba(15, 23, 42, 0.08)",
    "padding": "24px 28px",
    "border": "1px solid #e2e8f0",
}
HEADER_STYLE = {
    "textAlign": "center",
    "margin": "0",
    "color": "#0f172a",
    "fontSize": "2.2rem",
}
SUBTITLE_STYLE = {
    "textAlign": "center",
    "margin": "12px auto 0",
    "maxWidth": "720px",
    "color": "#475569",
    "lineHeight": "1.7",
    "fontSize": "1rem",
}
FILTER_SECTION_STYLE = {
    "display": "flex",
    "flexDirection": "column",
    "gap": "20px",
}
FILTER_GROUP_STYLE = {
    "display": "flex",
    "flexDirection": "column",
    "gap": "10px",
}
CONTROL_LABEL_STYLE = {
    "display": "block",
    "fontSize": "0.95rem",
    "fontWeight": "600",
    "margin": "0",
    "color": "#1f2937",
}
GRAPH_STYLE = {
    "width": "100%",
}
SECTION_HEADING_STYLE = {
    "margin": "0 0 18px",
    "fontSize": "1.05rem",
    "fontWeight": "600",
    "color": "#0f172a",
}


def is_debug_mode() -> bool:
    """Read Dash debug behavior from the environment."""
    return os.getenv("DASH_DEBUG", "").strip().lower() in {"1", "true", "yes", "on"}


def load_spacex_data(csv_path: Path = DATA_PATH) -> pd.DataFrame:
    """Load and validate the SpaceX launch dataset."""
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {csv_path}. Run scripts/download_spacex_data.py "
            "or place spacex_launch_dash.csv in the data/ directory."
        )

    dataframe = pd.read_csv(csv_path)
    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Dataset is missing required columns: {missing}")

    dataframe = dataframe.drop(columns=["Unnamed: 0"], errors="ignore").copy()
    dataframe["Launch Outcome"] = dataframe["class"].map(OUTCOME_LABELS).fillna("Unknown")
    dataframe["Outcome"] = dataframe["Launch Outcome"]
    dataframe["Launch Site"] = dataframe["Launch Site"].astype(str)
    return dataframe


def build_site_options(dataframe: pd.DataFrame) -> List[Dict[str, str]]:
    site_values = sorted(dataframe["Launch Site"].dropna().unique())
    options = [{"label": "All Launch Sites", "value": DEFAULT_LAUNCH_SITE}]
    options.extend({"label": site, "value": site} for site in site_values)
    return options


def format_chart_title(base_title: str, selected_site: str) -> str:
    if selected_site == DEFAULT_LAUNCH_SITE:
        return base_title
    return f"{base_title} | {selected_site}"


def create_empty_figure(title: str, message: str, height: int) -> go.Figure:
    figure = go.Figure()
    figure.update_layout(
        title=title,
        template="plotly_white",
        height=height,
        annotations=[
            {
                "text": message,
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
                "font": {"size": 16, "color": "#475569"},
            }
        ],
        xaxis={"visible": False},
        yaxis={"visible": False},
        margin={"l": 30, "r": 30, "t": 90, "b": 40},
    )
    return figure


def build_error_layout(error_message: str) -> html.Div:
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(
                                APP_TITLE,
                                style=HEADER_STYLE,
                            ),
                            html.P(
                                "The dashboard could not load its dataset.",
                                style={
                                    "fontSize": "1.1rem",
                                    "margin": "12px 0 8px",
                                    "color": "#b91c1c",
                                },
                            ),
                            html.Pre(
                                error_message,
                                style={
                                    "whiteSpace": "pre-wrap",
                                    "backgroundColor": "#fff7ed",
                                    "border": "1px solid #fdba74",
                                    "borderRadius": "12px",
                                    "padding": "16px",
                                    "color": "#9a3412",
                                },
                            ),
                            html.P(
                                "Add data/spacex_launch_dash.csv or run "
                                "scripts/download_spacex_data.py, then restart the app.",
                                style={"marginTop": "12px", "color": "#334155"},
                            ),
                        ],
                        style=CARD_STYLE,
                    )
                ],
                style=CONTENT_STYLE,
            )
        ],
        style=PAGE_STYLE,
    )


def build_dashboard_layout(dataframe: pd.DataFrame) -> html.Div:
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(APP_TITLE, style=HEADER_STYLE),
                            html.P(APP_SUBTITLE, style=SUBTITLE_STYLE),
                        ],
                        style=CARD_STYLE,
                    ),
                    html.Div(
                        [
                            html.H2("Filters", style=SECTION_HEADING_STYLE),
                            html.Div(
                                [
                                    html.Label(
                                        "Select Launch Site",
                                        htmlFor="site-dropdown",
                                        style=CONTROL_LABEL_STYLE,
                                    ),
                                    dcc.Dropdown(
                                        id="site-dropdown",
                                        options=build_site_options(dataframe),
                                        value=DEFAULT_LAUNCH_SITE,
                                        placeholder="Select a launch site",
                                        searchable=True,
                                        clearable=False,
                                    ),
                                ],
                                style=FILTER_GROUP_STYLE,
                            ),
                            html.Div(
                                [
                                    html.Label(
                                        "Payload Mass Range (kg)",
                                        htmlFor="payload-slider",
                                        style=CONTROL_LABEL_STYLE,
                                    ),
                                    dcc.RangeSlider(
                                        id="payload-slider",
                                        min=PAYLOAD_SLIDER_BOUNDS[0],
                                        max=PAYLOAD_SLIDER_BOUNDS[1],
                                        step=PAYLOAD_SLIDER_STEP,
                                        value=DEFAULT_PAYLOAD_RANGE,
                                        marks={
                                            value: f"{value:,}"
                                            for value in range(
                                                PAYLOAD_SLIDER_BOUNDS[0],
                                                PAYLOAD_SLIDER_BOUNDS[1] + 1,
                                                2000,
                                            )
                                        },
                                        tooltip={
                                            "placement": "bottom",
                                            "always_visible": False,
                                        },
                                        allowCross=False,
                                    ),
                                ],
                                style=FILTER_GROUP_STYLE,
                            ),
                        ],
                        style={**CARD_STYLE, **FILTER_SECTION_STYLE},
                    ),
                    html.Div(
                        [
                            html.H2(CHART_TITLES["pie"], style=SECTION_HEADING_STYLE),
                            dcc.Graph(
                                id="success-pie-chart",
                                figure=create_empty_figure(
                                    CHART_TITLES["pie"],
                                    "Select a launch site to view launch outcomes.",
                                    GRAPH_HEIGHTS["pie"],
                                ),
                                config={"displayModeBar": False, "responsive": True},
                                style={**GRAPH_STYLE, "height": f"{GRAPH_HEIGHTS['pie']}px"},
                            ),
                        ],
                        style=CARD_STYLE,
                    ),
                    html.Div(
                        [
                            html.H2(
                                CHART_TITLES["scatter"], style=SECTION_HEADING_STYLE
                            ),
                            dcc.Graph(
                                id="success-payload-scatter-chart",
                                figure=create_empty_figure(
                                    CHART_TITLES["scatter"],
                                    "Adjust the payload range to inspect launch results.",
                                    GRAPH_HEIGHTS["scatter"],
                                ),
                                config={"displayModeBar": False, "responsive": True},
                                style={
                                    **GRAPH_STYLE,
                                    "height": f"{GRAPH_HEIGHTS['scatter']}px",
                                },
                            ),
                        ],
                        style=CARD_STYLE,
                    ),
                ],
                style=CONTENT_STYLE,
            )
        ],
        style=PAGE_STYLE,
    )


def style_figure(figure: go.Figure, height: int) -> go.Figure:
    figure.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin={"l": 40, "r": 40, "t": 90, "b": 50},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "x": 0,
            "title": {"text": ""},
            "font": {"size": 12},
        },
        font={"color": "#0f172a", "size": 13},
        hoverlabel={"bgcolor": "#ffffff", "font_size": 12, "font_family": "Avenir Next"},
        title={"x": 0.02, "xanchor": "left"},
    )
    figure.update_xaxes(showgrid=True, gridcolor="#e2e8f0", zeroline=False)
    figure.update_yaxes(showgrid=True, gridcolor="#e2e8f0", zeroline=False)
    return figure


app = Dash(__name__)
app.title = APP_TITLE
server = app.server

DATAFRAME: Optional[pd.DataFrame] = None
DATA_ERROR: Optional[str] = None

try:
    DATAFRAME = load_spacex_data()
except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
    DATA_ERROR = str(error)

app.layout = (
    build_dashboard_layout(DATAFRAME)
    if DATAFRAME is not None
    else build_error_layout(DATA_ERROR or "Unknown error")
)


if DATAFRAME is not None:

    @app.callback(
        Output("success-pie-chart", "figure"),
        Input("site-dropdown", "value"),
    )
    def update_success_pie_chart(selected_site: str) -> go.Figure:
        if selected_site == DEFAULT_LAUNCH_SITE:
            launch_summary = (
                DATAFRAME.groupby("Launch Site", as_index=False)["class"]
                .sum()
                .rename(columns={"class": "Successful Launches"})
            )
            figure = px.pie(
                launch_summary,
                values="Successful Launches",
                names="Launch Site",
                title=CHART_TITLES["pie"],
                hole=0.35,
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            return style_figure(figure, GRAPH_HEIGHTS["pie"])

        site_frame = DATAFRAME[DATAFRAME["Launch Site"] == selected_site]
        if site_frame.empty:
            return create_empty_figure(
                format_chart_title(CHART_TITLES["pie"], selected_site),
                "No launch records are available for the selected site.",
                GRAPH_HEIGHTS["pie"],
            )

        outcome_summary = (
            site_frame.groupby("Launch Outcome", as_index=False)
            .size()
            .rename(columns={"size": "Launch Count"})
        )
        figure = px.pie(
            outcome_summary,
            values="Launch Count",
            names="Launch Outcome",
            title=format_chart_title(CHART_TITLES["pie"], selected_site),
            hole=0.35,
            color="Launch Outcome",
            color_discrete_map={"Failure": "#e76f51", "Success": "#2a9d8f"},
        )
        return style_figure(figure, GRAPH_HEIGHTS["pie"])


    @app.callback(
        Output("success-payload-scatter-chart", "figure"),
        Input("site-dropdown", "value"),
        Input("payload-slider", "value"),
    )
    def update_payload_scatter_chart(
        selected_site: str,
        payload_range: List[int],
    ) -> go.Figure:
        filtered_frame = DATAFRAME[
            DATAFRAME["Payload Mass (kg)"].between(payload_range[0], payload_range[1])
        ]

        if selected_site != DEFAULT_LAUNCH_SITE:
            filtered_frame = filtered_frame[filtered_frame["Launch Site"] == selected_site]

        if filtered_frame.empty:
            return create_empty_figure(
                format_chart_title(CHART_TITLES["scatter"], selected_site),
                "No launches match the selected filters. Try widening the payload range.",
                GRAPH_HEIGHTS["scatter"],
            )

        figure = px.scatter(
            filtered_frame,
            x="Payload Mass (kg)",
            y="Launch Outcome",
            color="Booster Version Category",
            custom_data=[
                "Launch Site",
                "Payload Mass (kg)",
                "Booster Version Category",
                "Launch Outcome",
            ],
            category_orders={"Launch Outcome": ["Failure", "Success"]},
            labels=AXIS_LABELS,
            title=format_chart_title(CHART_TITLES["scatter"], selected_site),
            color_discrete_sequence=px.colors.qualitative.Safe,
        )
        figure.update_traces(
            marker={"size": 11, "opacity": 0.8, "line": {"width": 0}},
            hovertemplate=(
                "Launch Site=%{customdata[0]}<br>"
                "Payload Mass=%{customdata[1]:,.0f} kg<br>"
                "Booster Version Category=%{customdata[2]}<br>"
                "Launch Outcome=%{customdata[3]}<extra></extra>"
            ),
        )
        return style_figure(figure, GRAPH_HEIGHTS["scatter"])


if __name__ == "__main__":
    app.run(debug=is_debug_mode())
