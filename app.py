import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Netflix Intelligence Dashboard",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&f[]=clash-display@600,700&display=swap');

:root {
    --bg: #0a0c10;
    --bg-2: #11151b;
    --panel: #141922;
    --panel-2: #1a2030;
    --stroke: rgba(255,255,255,0.08);
    --text: #f5f7fb;
    --muted: #a8b0bf;
    --accent: #e50914;
    --accent-soft: rgba(229, 9, 20, 0.14);
    --cyan: #4f98a3;
    --shadow: 0 14px 40px rgba(0,0,0,0.45);
}

html, body, [class*="css"] {
    font-family: 'Satoshi', sans-serif;
    background: linear-gradient(180deg, #090b0f 0%, #11151b 100%);
    color: var(--text);
}

body {
    color: var(--text);
    background: linear-gradient(180deg, #090b0f 0%, #11151b 100%);
}

.stApp {
    background: linear-gradient(180deg, #090b0f 0%, #11151b 100%);
}

h1, h2, h3 {
    font-family: 'Clash Display', 'Satoshi', sans-serif;
    letter-spacing: -0.02em;
    color: var(--text);
}

.block-container {
    padding-top: 6rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

section[data-testid="stHeader"] {
    background: rgba(10,12,16,0.95);
    backdrop-filter: blur(10px);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1319 0%, #0c1016 100%);
    border-right: 1px solid var(--stroke);
}

section[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

div[data-testid="metric-container"] {
    background: linear-gradient(180deg, #161b24 0%, #121720 100%);
    border: 1px solid var(--stroke);
    border-radius: 20px;
    padding: 1rem 1.1rem;
    box-shadow: var(--shadow);
}

div[data-testid="metric-container"] label {
    color: var(--muted) !important;
    font-weight: 500;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--text);
    font-family: 'Clash Display', sans-serif;
    letter-spacing: -0.03em;
}

.hero {
    display: grid;
    grid-template-columns: 1.5fr .8fr;
    gap: 1rem;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}

.hero-card {
    background: linear-gradient(135deg, rgba(229,9,20,0.10), rgba(255,255,255,0.02));
    border: 1px solid var(--stroke);
    border-radius: 26px;
    padding: 1.6rem;
    min-height: 190px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow);
}

.hero-card::after {
    content: "";
    position: absolute;
    right: -30px;
    bottom: -30px;
    width: 140px;
    height: 140px;
    background: radial-gradient(circle, rgba(229,9,20,0.18), transparent 72%);
    filter: blur(10px);
}

.eyebrow {
    text-transform: uppercase;
    letter-spacing: .18em;
    font-size: .72rem;
    color: #c0c7d4;
    margin-bottom: .65rem;
}

.hero-title {
    font-size: clamp(2rem, 3vw, 3.4rem);
    line-height: 1;
    margin: 0;
    color: #ffffff;
}

.hero-copy {
    color: var(--muted);
    margin-top: .85rem;
    max-width: 62ch;
    font-size: 1rem;
}

.stat-mini {
    display: grid;
    gap: .8rem;
}

.stat-box {
    background: linear-gradient(180deg, #171c25 0%, #121720 100%);
    border: 1px solid var(--stroke);
    border-radius: 22px;
    padding: 1rem 1.1rem;
    box-shadow: var(--shadow);
}

.stat-box .label {
    color: var(--muted);
    font-size: .85rem;
}

.stat-box .value {
    font-family: 'Clash Display', sans-serif;
    font-size: 1.6rem;
    margin-top: .25rem;
    color: #ffffff;
}

.chart-card {
    background: #141922;
    border: 1px solid var(--stroke);
    border-radius: 22px;
    padding: .85rem .95rem .35rem .95rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}

.chart-title {
    font-family: 'Clash Display', sans-serif;
    font-size: 1rem;
    margin: .2rem 0 .55rem .2rem;
    color: #ffffff;
}

.stDataFrame, div[data-testid="stDataFrame"] {
    border: 1px solid var(--stroke);
    border-radius: 18px;
    overflow: hidden;
    background: #141922;
}

@media (max-width: 980px) {
    .hero {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .block-container {
        padding-top: 6.5rem;
    }
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("data/netflix_data.csv")

    df["director"] = df["director"].fillna("Unknown")
    df["cast"] = df["cast"].fillna("Unknown")
    df["country"] = df["country"].fillna("Unknown")
    df["listed_in"] = df["listed_in"].fillna("Unknown")
    df["rating"] = df["rating"].fillna("Unknown")

    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df = df.dropna(subset=["date_added"]).copy()

    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month_name().str.slice(stop=3)
    df["content_age"] = pd.Timestamp.now().year - df["release_year"]
    df["duration_num"] = df["duration"].astype(str).str.extract(r"(\\d+)").astype(float)
    df["duration_unit"] = df["duration"].astype(str).str.extract(r"([A-Za-z]+)")

    return df


def style_fig(fig):
    fig.update_layout(
        paper_bgcolor="#141922",
        plot_bgcolor="#141922",
        font=dict(color="#f5f7fb", family="Satoshi"),
        margin=dict(l=20, r=20, t=45, b=20),
        hoverlabel=dict(
            bgcolor="#0f141c",
            bordercolor="rgba(255,255,255,0.12)",
            font=dict(color="#f5f7fb")
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dce3ee")
        )
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        color="#dce3ee",
        title_font=dict(color="#dce3ee")
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        color="#dce3ee",
        title_font=dict(color="#dce3ee")
    )
    return fig


df = load_data()

st.sidebar.markdown("## Netflix Atlas")
st.sidebar.caption("Curated streaming intelligence")

type_filter = st.sidebar.multiselect(
    "Content Type",
    options=sorted(df["type"].dropna().unique()),
    default=sorted(df["type"].dropna().unique())
)

year_filter = st.sidebar.slider(
    "Year Added",
    min_value=int(df["year_added"].min()),
    max_value=int(df["year_added"].max()),
    value=(int(df["year_added"].min()), int(df["year_added"].max()))
)

rating_options = sorted(df["rating"].dropna().unique())
rating_filter = st.sidebar.multiselect(
    "Rating",
    options=rating_options,
    default=rating_options
)

country_options = sorted(
    df["country"].str.split(", ").explode().dropna().unique().tolist()
)
country_filter = st.sidebar.multiselect(
    "Country",
    options=country_options,
    default=[]
)

filtered_df = df[
    (df["type"].isin(type_filter)) &
    (df["year_added"].between(year_filter[0], year_filter[1])) &
    (df["rating"].isin(rating_filter))
].copy()

if country_filter:
    filtered_df = filtered_df[
        filtered_df["country"].apply(lambda x: any(c in str(x).split(", ") for c in country_filter))
    ]

movie_count = int((filtered_df["type"] == "Movie").sum())
tv_count = int((filtered_df["type"] == "TV Show").sum())
avg_release_year = round(filtered_df["release_year"].mean(), 1) if not filtered_df.empty else 0

avg_movie_duration_value = filtered_df.loc[filtered_df["type"] == "Movie", "duration_num"].mean()
avg_movie_duration = round(avg_movie_duration_value, 1) if pd.notna(avg_movie_duration_value) else 0

country_count = filtered_df["country"].str.split(", ").explode().nunique() if not filtered_df.empty else 0

st.markdown(f"""
<div class="hero">
  <div class="hero-card">
    <div class="eyebrow">Premium analytics view</div>
    <h1 class="hero-title">Netflix Intelligence Dashboard</h1>
    <p class="hero-copy">A cleaner executive-style workspace for tracking content mix, release cadence, genre density, geographic spread, and title-level detail across the filtered catalog.</p>
  </div>
  <div class="stat-mini">
    <div class="stat-box"><div class="label">Filter window</div><div class="value">{year_filter[0]}–{year_filter[1]}</div></div>
    <div class="stat-box"><div class="label">Average release year</div><div class="value">{avg_release_year}</div></div>
    <div class="stat-box"><div class="label">Avg. movie runtime</div><div class="value">{avg_movie_duration} min</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

metric_cols = st.columns(4)
metric_cols[0].metric("Total Titles", len(filtered_df))
metric_cols[1].metric("Movies", movie_count)
metric_cols[2].metric("TV Shows", tv_count)
metric_cols[3].metric("Countries in View", country_count)

if filtered_df.empty:
    st.warning("No results match the current filters.")
else:
    content_mix = filtered_df["type"].value_counts().reset_index()
    content_mix.columns = ["type", "count"]

    fig1 = px.bar(
        content_mix,
        x="type",
        y="count",
        color="type",
        color_discrete_map={"Movie": "#E50914", "TV Show": "#4F98A3"},
        title="Content Mix"
    )
    fig1.update_traces(marker_line_width=0)
    style_fig(fig1)

    year_counts = filtered_df["year_added"].value_counts().sort_index().reset_index()
    year_counts.columns = ["year_added", "count"]

    fig2 = px.line(
        year_counts,
        x="year_added",
        y="count",
        markers=True,
        title="Additions Over Time"
    )
    fig2.update_traces(line_color="#E50914", line_width=3, marker_size=8)
    style_fig(fig2)

    country_counts = (
        filtered_df.assign(country=filtered_df["country"].str.split(", "))
        .explode("country")["country"]
        .value_counts()
        .head(10)
        .sort_values(ascending=True)
        .reset_index()
    )
    country_counts.columns = ["country", "count"]

    fig3 = px.bar(
        country_counts,
        x="count",
        y="country",
        orientation="h",
        title="Top Production Countries"
    )
    fig3.update_traces(marker_color="#4F98A3", marker_line_width=0)
    style_fig(fig3)

    genre_counts = (
        filtered_df.assign(listed_in=filtered_df["listed_in"].str.split(", "))
        .explode("listed_in")["listed_in"]
        .value_counts()
        .head(10)
        .sort_values(ascending=True)
        .reset_index()
    )
    genre_counts.columns = ["genre", "count"]

    fig4 = px.bar(
        genre_counts,
        x="count",
        y="genre",
        orientation="h",
        title="Top Genres"
    )
    fig4.update_traces(marker_color="#ff7b72", marker_line_width=0)
    style_fig(fig4)

    movie_df = filtered_df[filtered_df["type"] == "Movie"].copy()
    fig5 = px.histogram(
        movie_df,
        x="duration_num",
        nbins=25,
        title="Movie Runtime Distribution",
        labels={"duration_num": "Runtime (minutes)"}
    )
    fig5.update_traces(marker_color="#b8c0cc", marker_line_width=0)
    style_fig(fig5)

    rating_counts = filtered_df["rating"].value_counts().head(8).reset_index()
    rating_counts.columns = ["rating", "count"]

    fig6 = px.pie(
        rating_counts,
        names="rating",
        values="count",
        hole=0.62,
        title="Audience Rating Split",
        color_discrete_sequence=[
            "#E50914", "#4F98A3", "#ff7b72", "#9aa5b5",
            "#6daa45", "#d19900", "#5591c7", "#a86fdf"
        ]
    )
    fig6.update_traces(textposition="inside", textinfo="percent+label")
    style_fig(fig6)
    fig6.update_yaxes(showgrid=False)

    row1 = st.columns(2)
    with row1[0]:
        st.markdown('<div class="chart-card"><div class="chart-title">Content Mix</div>', unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row1[1]:
        st.markdown('<div class="chart-card"><div class="chart-title">Additions Over Time</div>', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    row2 = st.columns(2)
    with row2[0]:
        st.markdown('<div class="chart-card"><div class="chart-title">Top Production Countries</div>', unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row2[1]:
        st.markdown('<div class="chart-card"><div class="chart-title">Top Genres</div>', unsafe_allow_html=True)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    row3 = st.columns((1.2, 0.8))
    with row3[0]:
        st.markdown('<div class="chart-card"><div class="chart-title">Movie Runtime Distribution</div>', unsafe_allow_html=True)
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row3[1]:
        st.markdown('<div class="chart-card"><div class="chart-title">Audience Rating Split</div>', unsafe_allow_html=True)
        st.plotly_chart(fig6, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### Catalog Preview")
    preview_cols = [
        "title", "type", "country", "release_year", "rating",
        "duration", "listed_in", "director", "date_added"
    ]
    st.dataframe(
        filtered_df[preview_cols].sort_values("date_added", ascending=False).head(50),
        use_container_width=True
    )