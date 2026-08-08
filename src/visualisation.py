# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import csv
from typing import Any, Dict, List

def import_csv(file_path: str) -> List[Dict[str, Any]]:
    """Read a CSV file into a list of dictionaries."""
    with open(file_path, mode="r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))

data = import_csv("data/output.csv")

app = Dash()

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame(data)
df["sales"] = df["sales"].rolling(window=50, min_periods=1).mean()
fig = px.line(df, x="date", y="sales", color="region")
fig.update_layout(hovermode="x unified")
fig.update_traces(opacity=0.5, line=dict(width=1.5))

app.layout = html.Div(children=[
    html.H1(children='Were sales higher before or after the Pink Morsel price increase on the 15th of January, 2021?'),


    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)