# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd


def import_csv(file_path: str):
    """Read a CSV file into a list of dictionaries."""
    with open(file_path, mode="r", newline="", encoding="utf-8") as csv_file:
        return list(pd.read_csv(csv_file).to_dict(orient="records"))


data = import_csv("data/output.csv")

app = Dash()

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame(data)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df = df.dropna(subset=["date", "sales"]).sort_values(["region", "date"]).reset_index(drop=True)

df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
df = (
    df.groupby(["region", "month"], as_index=False)["sales"]
    .sum()
)

# Remove the specific incomplete months from the monthly series.
df = df[~df["month"].isin(pd.to_datetime(["2018-02-01", "2022-02-01"]))].copy()

regions = ["north", "east", "south", "west", "all"]


def build_figure(selected_region: str):
    filtered_df = df if selected_region == "all" else df[df["region"] == selected_region]
    fig = px.line(filtered_df, x="month", y="sales", color="region")
    fig.update_layout(hovermode="x unified")
    fig.update_traces(opacity=0.5, line=dict(width=1.5))
    return fig


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children='Were sales higher before or after the Pink Morsel price increase on the 15th of January, 2021?',
                    style={"marginBottom": "10px", "color": "#2c3e50"},
                ),
                html.P(
                    children="Select a region to focus the chart on a specific area.",
                    style={"marginBottom": "20px", "color": "#5f6b7a"},
                ),
                dcc.RadioItems(
                    id='region-selector',
                    options=[{"label": region.title(), "value": region} for region in regions],
                    value="all",
                    inline=True,
                    style={
                        "marginBottom": "20px",
                        "fontWeight": "500",
                        "color": "#2c3e50",
                    },
                ),
            ],
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "padding": "24px",
                "backgroundColor": "#f8fafc",
                "borderRadius": "12px",
                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
            },
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id='example-graph',
                    figure=build_figure("all"),
                    config={"displayModeBar": False},
                )
            ],
            style={"marginTop": "20px"},
        ),
    ],
    style={"padding": "20px", "backgroundColor": "#eef2f7", "minHeight": "100vh"},
)

@callback(
    Output('example-graph', 'figure'),
    Input('region-selector', 'value'))

def update_graph(selected_region: str):
    return build_figure(selected_region)

if __name__ == '__main__':
    app.run(debug=True)