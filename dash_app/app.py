import re
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# THEME auswählen
THEME = dbc.themes.LUX

#THEME = dbc.themes.FLATLY
#THEME = dbc.themes.ZEPHYR
#THEME = dbc.themes.MINTY
#THEME = dbc.themes.MORPH
#THEME = dbc.themes.COSMO
#THEME = dbc.themes.SLATE
#THEME = dbc.themes.QUARTZ
#THEME = dbc.themes.VAPOR

DARK_THEMES = {
    dbc.themes.SLATE,
    dbc.themes.SOLAR,
    dbc.themes.SUPERHERO,
    dbc.themes.QUARTZ,
    dbc.themes.VAPOR,
}

PLOTLY_TEMPLATE = "plotly_dark" if THEME in DARK_THEMES else "plotly_white"

df = pd.read_csv("data/dashboard_data.csv")
importance = pd.read_csv("data/feature_importance_rf.csv")

labels = {
    "age": "Age",
    "gender": "Gender",
    "married": "Married",
    "smoking": "Smoking",
    "bmiCategory": "BMI Category",
    "healthRisk": "Health Risk",
    "riskScore": "Health Risk Score",
    "stress": "Stress Level (1–10)",
    "sleepDuration": "Sleep Duration (hours)",
    "sleepQuality": "Sleep Quality (1–10)",
    "alcohol": "Alcohol (drinks/week)",
    "sugar": "Sugar Intake (g/day)",
    "activity": "Physical Activity (min/day)",
    "steps": "Daily Steps",
    "heartRate": "Heart Rate (bpm)",
    "shortSleep": "Short Sleep",
    "lifestyleRisk": "Lifestyle Risk",
    "stressSleepMismatch": "Stress Sleep Missmatch",
    "cluster_label": "Cluster Label",
    "importance": "Importance",
    "feature": "Feature",
    "feature_label": "Feature",
    "count": "Count",
    "share_pct": "Share (%)",
}

# Cluster label just in case
fallback_cluster_names = {
    0: "Cluster 0",
    1: "Cluster 1",
    2: "Cluster 2",
    3: "Cluster 3",
}

if "cluster_label" not in df.columns and "cluster" in df.columns:
    df["cluster_label"] = df["cluster"].map(fallback_cluster_names).fillna(df["cluster"].astype(str))

# ==================================================
# CLUSTER-REIHENFOLGE
# ==================================================
def cluster_sort_key(label):
    match = re.search(r"(\d+)", str(label))
    return int(match.group(1)) if match else 999

cluster_order = sorted(df["cluster_label"].dropna().astype(str).unique(), key=cluster_sort_key)

# ==================================================
# FARBPALETTE FUER CLUSTER
# ==================================================
colors = px.colors.qualitative.Set2
cluster_color_map = {
    label: colors[i % len(colors)]
    for i, label in enumerate(cluster_order)
}

common_plot_kwargs = {
    "category_orders": {"cluster_label": cluster_order},
    "color_discrete_map": cluster_color_map,
    "labels": labels,
}

# ==================================================
# FEATURE-NAMEN UEBER LABEL-DICTIONARY
# ==================================================
importance = importance.copy()
importance["feature_label"] = importance["feature"].map(labels).fillna(importance["feature"])

# ==================================================
# FILTEROPTIONEN
# ==================================================
categorical_options = {
    "gender": sorted(df["gender"].dropna().astype(str).unique()) if "gender" in df.columns else [],
    "smoking": sorted(df["smoking"].dropna().astype(str).unique()) if "smoking" in df.columns else [],
    "bmiCategory": sorted(df["bmiCategory"].dropna().astype(str).unique()) if "bmiCategory" in df.columns else [],
    "cluster_label": cluster_order,
}

age_min = int(df["age"].min()) if "age" in df.columns else 0
age_max = int(df["age"].max()) if "age" in df.columns else 100

# ==================================================
# HILFSFUNKTIONEN
# ==================================================
def filter_df(data, age_range, gender, smoking, bmi, cluster):
    dff = data.copy()

    if "age" in dff.columns and age_range:
        dff = dff[(dff["age"] >= age_range[0]) & (dff["age"] <= age_range[1])]

    if gender and "gender" in dff.columns:
        dff = dff[dff["gender"].isin(gender)]

    if smoking and "smoking" in dff.columns:
        dff = dff[dff["smoking"].isin(smoking)]

    if bmi and "bmiCategory" in dff.columns:
        dff = dff[dff["bmiCategory"].isin(bmi)]

    if cluster and "cluster_label" in dff.columns:
        dff = dff[dff["cluster_label"].isin(cluster)]

    return dff


def safe_mean(series):
    return round(series.mean(), 2) if len(series) > 0 else 0


def kpi_card(title, value):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="text-muted small"),
                html.H3(value, className="mb-0 mt-2 fw-semibold"),
            ]
        ),
        className="shadow-sm border-0 h-100 kpi-card",
        style={"borderRadius": "14px"},
    )


def style_figure(fig, height=None):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        margin=dict(l=40, r=20, t=55, b=40),
        legend_title_text="Cluster Label",
        hoverlabel=dict(font_size=13),
    )
    if height is not None:
        fig.update_layout(height=height)
    return fig


# ==================================================
# APP
# ==================================================
app = Dash(
    __name__,
    external_stylesheets=[THEME],
    suppress_callback_exceptions=True,
)

app.title = "Too Stressed to Sleep?"

app.layout = dbc.Container(
    fluid=True,
    className="py-4",
    children=[
        dbc.Row(
            className="mb-4",
            children=[
                dbc.Col(
                    [
                        html.H1(
                            "Too Stressed to Sleep?",
                            className="display-4 fw-bold mb-2 text-capitalize"
                        ),
                        html.P(
                            "A data-driven exploration of sleep quality and lifestyle factors.",
                            className="text-muted fs-4 mb-0",
                        ),
                        
                        html.Hr(
                            className="mt-3 mb-4",
                            style={
                                "borderTop": "1px solid #e5e5e5",
                                "opacity": "1"
                            }
                        ),
                    ]
                )
            ],
        ),

        dbc.Row(
            className="g-4",
            children=[
                # SIDEBAR
                dbc.Col(
                    md=3,
                    lg=3,
                    children=[
                        dbc.Card(
                            className="shadow-sm border-0 sticky-top",
                            style={"top": "20px", "borderRadius": "14px"},
                            children=[
                                dbc.CardBody(
                                    [
                                        html.H4("Filters", className="mb-3 fw-semibold"),

                                        html.Label("Age", className="fw-semibold"),
                                        html.Div(id="age-label", className="text-muted small mb-2"),
                                        dcc.RangeSlider(
                                            id="age-slider",
                                            min=age_min,
                                            max=age_max,
                                            value=[age_min, age_max],
                                            marks={age_min: str(age_min), age_max: str(age_max)},
                                            tooltip={"placement": "bottom", "always_visible": False},
                                        ),

                                        html.Br(),
                                        html.Label("Gender", className="fw-semibold"),
                                        dcc.Dropdown(
                                            id="gender-dropdown",
                                            options=[{"label": x, "value": x} for x in categorical_options["gender"]],
                                            multi=True,
                                            placeholder="All",
                                        ),

                                        html.Br(),
                                        html.Label("Smoking", className="fw-semibold"),
                                        dcc.Dropdown(
                                            id="smoking-dropdown",
                                            options=[{"label": x, "value": x} for x in categorical_options["smoking"]],
                                            multi=True,
                                            placeholder="All",
                                        ),

                                        html.Br(),
                                        html.Label("BMI Category", className="fw-semibold"),
                                        dcc.Dropdown(
                                            id="bmi-dropdown",
                                            options=[{"label": x, "value": x} for x in categorical_options["bmiCategory"]],
                                            multi=True,
                                            placeholder="All",
                                        ),

                                        html.Br(),
                                        html.Label("Cluster", className="fw-semibold"),
                                        dcc.Dropdown(
                                            id="cluster-dropdown",
                                            options=[{"label": x, "value": x} for x in categorical_options["cluster_label"]],
                                            multi=True,
                                            placeholder="All",
                                        ),
                                    ]
                                )
                            ],
                        )
                    ],
                ),

                # MAIN
                dbc.Col(
                    md=9,
                    lg=9,
                    children=[
                        dbc.Row(
                            id="kpi-row",
                            className="g-3 mb-4 mt-1",
                        ),

                        dbc.Tabs(
                            [
                                dbc.Tab(
                                    label="Explore",
                                    children=[
                                        dbc.Card(
                                            className="shadow-sm border-0 mt-3",
                                            style={"borderRadius": "14px"},
                                            children=[
                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(id="scatter-fig"),
                                                        dcc.Graph(id="box-fig"),
                                                    ]
                                                )
                                            ],
                                        )
                                    ],
                                ),

                                dbc.Tab(
                                    label="Clusters",
                                    children=[
                                        dbc.Card(
                                            className="shadow-sm border-0 mt-3",
                                            style={"borderRadius": "14px"},
                                            children=[
                                                dbc.CardBody(
                                                    [
                                                        html.Label("Cluster Metric", className="fw-semibold"),
                                                        dcc.RadioItems(
                                                            id="cluster-metric-radio",
                                                            options=[
                                                                {"label": " Sleep Quality", "value": "sleepQuality"},
                                                                {"label": " High Stress", "value": "stressHigh"},
                                                                {"label": " Risk Score", "value": "riskScore"},
                                                            ],
                                                            value="sleepQuality",
                                                            inline=True,
                                                            className="mb-3",
                                                        ),
                                                        dcc.Graph(id="cluster-bar"),
                                                        dcc.Graph(id="cluster-size"),
                                                    ]
                                                )
                                            ],
                                        )
                                    ],
                                ),

                                dbc.Tab(
                                    label="Sleep Quality",
                                    children=[
                                        dbc.Card(
                                            className="shadow-sm border-0 mt-3",
                                            style={"borderRadius": "14px"},
                                            children=[
                                                dbc.CardBody(
                                                    [
                                                        html.Div(id="topn-label", className="fw-semibold mb-2"),
                                                        dcc.Slider(
                                                            id="topn-slider",
                                                            min=1,
                                                            max=len(importance),
                                                            step=1,
                                                            value=min(10, len(importance)),
                                                            tooltip={"placement": "bottom", "always_visible": False},
                                                        ),
                                                        html.Div(
                                                            id="importance-cumsum",
                                                            className="text-muted mt-3 mb-3"
                                                        ),
                                                        dcc.Graph(id="importance-fig"),
                                                    ]
                                                )
                                            ],
                                        )
                                    ],
                                ),

                                dbc.Tab(
                                    label="3D View",
                                    children=[
                                        dbc.Card(
                                            className="shadow-sm border-0 mt-3",
                                            style={"borderRadius": "14px"},
                                            children=[
                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(id="scatter-3d", style={"height": "920px"}),
                                                    ]
                                                )
                                            ],
                                        )
                                    ],
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Kleine UI-Callbacks
@app.callback(
    Output("age-label", "children"),
    Input("age-slider", "value"),
)
def age_label(age):
    return f"Selected Age Range: {age[0]} – {age[1]}"


@app.callback(
    Output("topn-label", "children"),
    Input("topn-slider", "value"),
)
def topn_label(n):
    return f"Top {n} Features"


@app.callback(
    Output("importance-cumsum", "children"),
    Input("topn-slider", "value"),
)
def importance_sum(n):
    sorted_imp = importance.sort_values("importance", ascending=False)
    cumsum = sorted_imp.head(n)["importance"].sum() * 100
    return f"Cumulative Importance: {cumsum:.1f} %"


# Callback
# ==================================================
@app.callback(
    Output("kpi-row", "children"),
    Output("scatter-fig", "figure"),
    Output("box-fig", "figure"),
    Output("cluster-bar", "figure"),
    Output("cluster-size", "figure"),
    Output("importance-fig", "figure"),
    Output("scatter-3d", "figure"),
    Input("age-slider", "value"),
    Input("gender-dropdown", "value"),
    Input("smoking-dropdown", "value"),
    Input("bmi-dropdown", "value"),
    Input("cluster-dropdown", "value"),
    Input("cluster-metric-radio", "value"),
    Input("topn-slider", "value"),
)
def update(age, gender, smoking, bmi, cluster, metric, topn):
    dff = filter_df(df, age, gender, smoking, bmi, cluster)

    kpis = [
        dbc.Col(kpi_card("Observations", len(dff)), md=6, lg=3),
        dbc.Col(kpi_card("Avg Sleep Quality", f"{safe_mean(dff['sleepQuality']):.2f}" if "sleepQuality" in dff.columns else "n/a"), md=6, lg=3),
        dbc.Col(kpi_card("Avg Stress", f"{safe_mean(dff['stress']):.2f}" if "stress" in dff.columns else "n/a"), md=6, lg=3),
        dbc.Col(kpi_card("Avg Sleep Duration", f"{safe_mean(dff['sleepDuration']):.2f}" if "sleepDuration" in dff.columns else "n/a"), md=6, lg=3),
    ]

    if len(dff) > 0:
        scatter = px.scatter(
            dff,
            x="stress",
            y="sleepQuality",
            color="cluster_label",
            opacity=0.6,
            hover_data={
                "age": True,
                "sleepDuration": True,
                "heartRate": True,
                "riskScore": True,
                "cluster_label": False,
            },
            **common_plot_kwargs,
        )
        scatter.update_traces(
            marker=dict(size=8),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "Stress Level (1–10): %{x:.2f}<br>"
                "Sleep Quality (1–10): %{y:.2f}<br>"
                "Age: %{customdata[0]}<br>"
                "Sleep Duration (hours): %{customdata[1]:.2f}<br>"
                "Heart Rate (bpm): %{customdata[2]:.2f}<br>"
                "Health Risk Score: %{customdata[3]:.2f}<extra></extra>"
            ),
        )
    else:
        scatter = px.scatter(title="No data after filtering")

    scatter = style_figure(scatter, height=500)

    if len(dff) > 0 and "cluster_label" in dff.columns and "sleepDuration" in dff.columns:
        box = px.box(
            dff,
            x="cluster_label",
            y="sleepDuration",
            color="cluster_label",
            points="outliers",
            **common_plot_kwargs,
        )
        box.update_traces(
            hovertemplate=(
                "Cluster Label: %{x}<br>"
                "Sleep Duration (hours): %{y:.2f}<extra></extra>"
            )
        )
    else:
        box = px.box(title="No data after filtering")

    box = style_figure(box, height=430)

    if len(dff) > 0 and "cluster_label" in dff.columns and metric in dff.columns:
        cluster_metric = dff.groupby("cluster_label", as_index=False)[metric].mean()
        cluster_metric["cluster_label"] = pd.Categorical(
            cluster_metric["cluster_label"], categories=cluster_order, ordered=True
        )
        cluster_metric = cluster_metric.sort_values("cluster_label")

        cluster_bar = px.bar(
            cluster_metric,
            x="cluster_label",
            y=metric,
            color="cluster_label",
            opacity=0.75,
            custom_data=["cluster_label"],
            **common_plot_kwargs,
        )
        metric_label = labels.get(metric, metric)
        cluster_bar.update_traces(
            hovertemplate=(
                "Cluster Label: %{x}<br>"
                f"{metric_label}: " + "%{y:.2f}<extra></extra>"
            )
        )
    else:
        cluster_bar = px.bar(title="No data after filtering")

    cluster_bar.update_layout(
        bargap=0.55,
        bargroupgap=0.15,
    )
    cluster_bar = style_figure(cluster_bar, height=420)

    if len(dff) > 0 and "cluster_label" in dff.columns:
        cluster_size = dff["cluster_label"].value_counts().reindex(cluster_order, fill_value=0).reset_index()
        cluster_size.columns = ["cluster_label", "count"]
        cluster_size["share_pct"] = (cluster_size["count"] / len(dff) * 100).round(1)

        cluster_size_fig = px.bar(
            cluster_size,
            x="cluster_label",
            y="count",
            color="cluster_label",
            opacity=0.75,
            text="share_pct",
            custom_data=["count", "share_pct"],
            **common_plot_kwargs,
        )
        cluster_size_fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "Cluster Label: %{x}<br>"
                "Count: %{customdata[0]}<br>"
                "Share (%): %{customdata[1]:.1f}<extra></extra>"
            ),
        )
    else:
        cluster_size_fig = px.bar(title="No data after filtering")

    cluster_size_fig.update_layout(
        bargap=0.55,
        bargroupgap=0.15,
    )
    cluster_size_fig = style_figure(cluster_size_fig, height=420)

    imp = importance.sort_values("importance", ascending=False).head(topn).copy()
    imp = imp.sort_values("importance", ascending=True)

    imp_fig = px.bar(
        imp,
        x="importance",
        y="feature_label",
        orientation="h",
        labels={
            "importance": "Importance",
            "feature_label": "Feature",
        },
    )
    imp_fig.update_traces(
        hovertemplate=(
            "Feature: %{y}<br>"
            "Importance: %{x:.4f}<extra></extra>"
        )
    )
    imp_fig.update_layout(
        bargap=0.38,
    )
    imp_fig = style_figure(imp_fig, height=max(400, 42 * len(imp) + 150))

    if len(dff) > 0:
        fig3d = px.scatter_3d(
            dff,
            x="stress",
            y="sleepDuration",
            z="sleepQuality",
            color="cluster_label",
            opacity=0.6,
            hover_data={
                "age": True,
                "heartRate": True,
                "riskScore": True,
                "activity": True if "activity" in dff.columns else False,
                "cluster_label": False,
            },
            **common_plot_kwargs,
        )
        fig3d.update_traces(
            marker=dict(size=4),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "Stress Level (1–10): %{x:.2f}<br>"
                "Sleep Duration (hours): %{y:.2f}<br>"
                "Sleep Quality (1–10): %{z:.2f}<br>"
                "Age: %{customdata[0]}<br>"
                "Heart Rate (bpm): %{customdata[1]:.2f}<br>"
                "Health Risk Score: %{customdata[2]:.2f}<br>"
                "Physical Activity (min/day): %{customdata[3]:.2f}<extra></extra>"
            ),
        )
    else:
        fig3d = px.scatter_3d(title="No data after filtering")

    fig3d.update_layout(
        template=PLOTLY_TEMPLATE,
        legend_title_text="Cluster Label",
        margin=dict(l=10, r=10, t=40, b=10),
        scene=dict(
            xaxis_title=labels["stress"],
            yaxis_title=labels["sleepDuration"],
            zaxis_title=labels["sleepQuality"],
            camera=dict(eye=dict(x=1.7, y=1.7, z=1.2)),
        ),
    )

    return kpis, scatter, box, cluster_bar, cluster_size_fig, imp_fig, fig3d


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=8050)