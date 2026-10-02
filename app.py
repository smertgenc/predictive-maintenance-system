import altair as alt
import pandas as pd
import streamlit as st

from predictive_model import DEFAULT_DATA_PATH, predict_failure_risk


# =========================================================
# 1. SAYFA AYARLARI
# =========================================================

st.set_page_config(
    page_title="Predictive Maintenance System",
    page_icon="⚙️",
    layout="wide",
)

# 10.000 satırlık veriyle Altair çalışabilsin
alt.data_transformers.disable_max_rows()


# =========================================================
# 2. RENKLER
# =========================================================

BG = "#0b1020"
PANEL = "#0f172a"
PANEL_2 = "#111827"
PANEL_3 = "#1e293b"

TEXT = "#f8fafc"
MUTED = "#cbd5e1"

ACCENT = "#38bdf8"
ACCENT_DARK = "#0284c7"

SUCCESS = "#4ade80"
WARNING = "#fbbf24"
DANGER = "#f87171"

GRID = "#263449"
BORDER = "#334155"

FAILURE_DOMAIN = [
    "No Failure",
    "Failure",
]

FAILURE_RANGE = [
    ACCENT,
    DANGER,
]


# =========================================================
# 3. STREAMLIT KOYU TEMA CSS
# =========================================================

st.markdown(
    """
<style>

/* ======================================================
   GENEL SAYFA
   ====================================================== */

html,
body,
[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(
            135deg,
            #0b1020 0%,
            #111827 45%,
            #0f172a 100%
        );
    color: #f8fafc;
}

[data-testid="stHeader"] {
    background: rgba(11, 16, 32, 0.95);
}

[data-testid="stAppViewBlockContainer"] {
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ======================================================
   NORMAL METİNLER
   ====================================================== */

h1,
h2,
h3,
h4,
h5,
h6 {
    color: #f8fafc !important;
}

p {
    color: #e2e8f0;
}

label {
    color: #f8fafc !important;
}


/* ======================================================
   HERO / BAŞLIK
   ====================================================== */

.hero-container {
    background:
        linear-gradient(
            135deg,
            #0f172a,
            #111827 60%,
            #0b1120
        );

    border: 1px solid rgba(148, 163, 184, 0.22);

    box-shadow:
        0 12px 30px
        rgba(14, 165, 233, 0.10);

    padding: 22px 24px;

    border-radius: 16px;

    margin-bottom: 14px;

    width: 100%;

    text-align: center;
}

.hero-container h1 {
    margin: 0 !important;

    font-size: 3rem !important;

    font-weight: 750 !important;

    color: #f8fafc !important;

    letter-spacing: 0.01em;
}


/* ======================================================
   METRIC KARTLARI
   ====================================================== */

div[data-testid="stMetric"] {
    background:
        linear-gradient(
            135deg,
            rgba(15, 23, 42, 0.98),
            rgba(30, 41, 59, 0.95)
        );

    border: 1px solid rgba(148, 163, 184, 0.18);

    border-radius: 14px;

    padding: 16px;

    box-shadow:
        0 10px 30px
        rgba(14, 116, 144, 0.10);
}

div[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}

div[data-testid="stMetricValue"] {
    color: #f8fafc !important;
}


/* ======================================================
   INPUT LABEL
   ====================================================== */

[data-testid="stWidgetLabel"] p {
    color: #f8fafc !important;
    font-weight: 600;
}


/* ======================================================
   SELECTBOX + MULTISELECT
   ====================================================== */

div[data-baseweb="select"] > div {
    background-color: #172033 !important;

    border: 1px solid #475569 !important;

    color: #f8fafc !important;

    border-radius: 10px !important;

    min-height: 42px;
}


/* Select içerisinde yazılan metin */

div[data-baseweb="select"] input {
    color: #f8fafc !important;

    -webkit-text-fill-color: #f8fafc !important;

    background-color: transparent !important;
}

div[data-baseweb="select"] input::placeholder {
    color: #cbd5e1 !important;
    -webkit-text-fill-color: #cbd5e1 !important;
    opacity: 1;
}


/* Select ana yazısı */

div[data-baseweb="select"] [role="combobox"] {
    color: #f8fafc !important;
}


/* ======================================================
   MULTISELECT SEÇİLİ ETİKETLER
   ====================================================== */

[data-baseweb="tag"] {
    background-color: #0369a1 !important;

    border: 1px solid #38bdf8 !important;

    border-radius: 7px !important;

    color: #ffffff !important;
}

[data-baseweb="tag"] span {
    color: #ffffff !important;
}

[data-baseweb="tag"] svg {
    fill: #ffffff !important;
}


/* ======================================================
   DROPDOWN AÇILIR MENÜ
   EN ÖNEMLİ DÜZELTME
   ====================================================== */

div[data-baseweb="popover"] {
    background-color: #0f172a !important;

    border: 1px solid #334155 !important;

    border-radius: 10px !important;
}

div[data-baseweb="popover"] > div {
    background-color: #0f172a !important;
}


/* Dropdown liste */

[role="listbox"] {
    background-color: #0f172a !important;

    color: #f8fafc !important;

    border: 1px solid #334155 !important;

    border-radius: 10px !important;
}


/* Dropdown seçenekleri */

[role="option"] {
    background-color: #0f172a !important;

    color: #f8fafc !important;
}


/* Dropdown içindeki bütün yazılar */

[role="option"] * {
    color: #f8fafc !important;
}


/* Üzerine gelince */

[role="option"]:hover,
[role="option"][aria-selected="true"] {
    background-color: #1e293b !important;

    color: #ffffff !important;
}


/* Seçili seçenek */

[role="option"][aria-selected="true"][aria-disabled="false"] {
    background-color: #075985 !important;

    color: #ffffff !important;
}


/* ======================================================
   NUMBER INPUT
   ====================================================== */

[data-testid="stNumberInput"] input {
    background-color: #172033 !important;

    color: #f8fafc !important;

    -webkit-text-fill-color: #f8fafc !important;

    border-color: #475569 !important;
}


/* +/- düğmeleri */

[data-testid="stNumberInput"] button {
    background-color: #1e293b !important;

    color: #f8fafc !important;

    border-color: #475569 !important;
}

[data-testid="stNumberInput"] button:hover {
    background-color: #334155 !important;
}


/* ======================================================
   BUTTON
   ====================================================== */

.stButton > button {
    background:
        linear-gradient(
            135deg,
            #0284c7,
            #38bdf8
        ) !important;

    color: #02131d !important;

    border: 0 !important;

    border-radius: 10px !important;

    font-weight: 700 !important;

    min-height: 44px;
}

.stButton > button:hover {
    background:
        linear-gradient(
            135deg,
            #0ea5e9,
            #7dd3fc
        ) !important;
}


/* ======================================================
   TAB
   ====================================================== */

.stTabs [role="tablist"] {
    background-color: rgba(17, 24, 39, 0.85);

    border: 1px solid #334155;

    border-radius: 12px;

    padding: 4px;
}

.stTabs [role="tab"] {
    color: #cbd5e1 !important;

    border-radius: 9px;
}

.stTabs [role="tab"] p {
    color: #cbd5e1 !important;
}

.stTabs [role="tab"][aria-selected="true"] {
    background-color: rgba(14, 165, 233, 0.18);

    border:
        1px solid
        rgba(56, 189, 248, 0.50);
}

.stTabs [role="tab"][aria-selected="true"] p {
    color: #ffffff !important;
}


/* ======================================================
   EXPANDER
   ====================================================== */

[data-testid="stExpander"] {
    background-color: rgba(15, 23, 42, 0.85);

    border: 1px solid #334155 !important;

    border-radius: 12px !important;
}

[data-testid="stExpander"] summary {
    color: #f8fafc !important;
}


/* ======================================================
   ALERT
   ====================================================== */

[data-testid="stAlert"] {
    border-radius: 12px;
}


/* ======================================================
   DATAFRAME DIŞ ÇERÇEVE
   ====================================================== */

[data-testid="stDataFrame"] {
    border:
        1px solid
        rgba(148, 163, 184, 0.22);

    border-radius: 10px;

    overflow: hidden;
}


/* ======================================================
   SCROLLBAR
   ====================================================== */

::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #0f172a;
}

::-webkit-scrollbar-thumb {
    background: #475569;
    border-radius: 8px;
}

::-webkit-scrollbar-thumb:hover {
    background: #64748b;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# 4. ALTAIR KOYU TEMA
# =========================================================

def dark_chart(chart):

    return (
        chart

        .configure(
            background=PANEL
        )

        .configure_view(
            fill=PANEL,
            stroke=BORDER,
            strokeWidth=1
        )

        .configure_axis(
            labelColor=MUTED,
            titleColor=TEXT,

            gridColor=GRID,

            domainColor=BORDER,

            tickColor=BORDER,

            labelFontSize=12,

            titleFontSize=13,

            titlePadding=12
        )

        .configure_legend(
            labelColor=TEXT,

            titleColor=TEXT,

            labelFontSize=12,

            titleFontSize=12,

            padding=10,

            symbolOpacity=1
        )

        .configure_title(
            color=TEXT,

            fontSize=17,

            fontWeight="bold",

            anchor="start",

            offset=15
        )
    )


# =========================================================
# 5. VERİ SETİNİ YÜKLE
# =========================================================

@st.cache_data
def load_dataset():
    if not DEFAULT_DATA_PATH.is_file() or DEFAULT_DATA_PATH.stat().st_size == 0:
        raise FileNotFoundError(
            f"Dataset not found or empty: {DEFAULT_DATA_PATH}"
        )

    return pd.read_csv(DEFAULT_DATA_PATH)


df = load_dataset()


# =========================================================
# 6. YENİ DEĞİŞKENLER
# =========================================================

df["Failure Label"] = (
    df["Machine failure"]
    .map(
        {
            0: "No Failure",
            1: "Failure",
        }
    )
)


df["Temperature Difference [K]"] = (
    df["Process temperature [K]"]
    - df["Air temperature [K]"]
)


# =========================================================
# 7. KPI
# =========================================================

total_machines = len(df)


failure_count = int(
    df["Machine failure"]
    .sum()
)


normal_count = (
    total_machines
    - failure_count
)


failure_rate = (
    df["Machine failure"]
    .mean()
    * 100
)


# =========================================================
# 8. BAŞLIK
# =========================================================

st.markdown(
    '<div class="hero-container">'
    '<h1>⚙️ Predictive Maintenance System</h1>'
    '</div>',
    unsafe_allow_html=True,
)


st.caption(
    "Makine arıza tahmin ve bakım karar destek sistemi"
)


# =========================================================
# 9. KPI KARTLARI
# =========================================================

col1, col2, col3, col4 = (
    st.columns(4)
)


with col1:

    st.metric(
        "Toplam Makine",
        f"{total_machines:,}"
    )


with col2:

    st.metric(
        "Arıza Sayısı",
        f"{failure_count:,}"
    )


with col3:

    st.metric(
        "Normal Makine",
        f"{normal_count:,}"
    )


with col4:

    st.metric(
        "Arıza Oranı",
        f"{failure_rate:.2f}%"
    )


st.divider()


# =========================================================
# 10. MAKİNE ANALİZİ
# =========================================================

st.subheader(
    "🔍 Makine Analizi"
)


left, right = st.columns(
    [1, 1],
    gap="large"
)


# =========================================================
# 11. MAKİNE PARAMETRELERİ
# =========================================================

with left:

    st.markdown(
        "### ⚙️ Makine Parametreleri"
    )


    machine_type = st.selectbox(
        "Makine Tipi",
        options=[
            "L",
            "M",
            "H"
        ]
    )


    air_temperature = (
        st.number_input(
            "Hava Sıcaklığı [K]",
            min_value=280.0,
            max_value=330.0,
            value=300.0,
            step=0.1,
        )
    )


    process_temperature = (
        st.number_input(
            "Proses Sıcaklığı [K]",
            min_value=290.0,
            max_value=350.0,
            value=310.0,
            step=0.1,
        )
    )


    rotational_speed = (
        st.number_input(
            "Dönüş Hızı [rpm]",
            min_value=500,
            max_value=4000,
            value=1500,
            step=10,
        )
    )


    torque = (
        st.number_input(
            "Tork [Nm]",
            min_value=0.0,
            max_value=100.0,
            value=40.0,
            step=0.1,
        )
    )


    tool_wear = (
        st.number_input(
            "Takım Aşınması [min]",
            min_value=0,
            max_value=300,
            value=100,
            step=1,
        )
    )


    analyze_button = st.button(
        "🔎 Makineyi Analiz Et",
        width="stretch"
    )


# =========================================================
# 12. TAHMİN SONUCU
# =========================================================

with right:

    st.markdown(
        "### 🤖 Tahmin Sonucu"
    )


    if analyze_button:

        result = (
            predict_failure_risk(

                machine_type=
                machine_type,

                air_temperature=
                float(
                    air_temperature
                ),

                process_temperature=
                float(
                    process_temperature
                ),

                rotational_speed=
                float(
                    rotational_speed
                ),

                torque=
                float(
                    torque
                ),

                tool_wear=
                float(
                    tool_wear
                ),
            )
        )


        probability = float(
            result[
                "probability"
            ]
        )


        label = result[
            "label"
        ]


        result_col1, result_col2 = (
            st.columns(2)
        )


        with result_col1:

            st.metric(
                "Arıza Olasılığı",
                f"{probability * 100:.2f}%"
            )


        with result_col2:

            st.metric(
                "Risk Durumu",
                label
            )


        st.progress(
            min(
                max(
                    probability,
                    0.0
                ),
                1.0
            )
        )


        if label == "High Risk":

            st.error(
                """
                ⚠️ **Yüksek arıza riski tespit edildi.**

                Makinenin bakım planlamasının
                kontrol edilmesi önerilir.
                """
            )

        else:

            st.success(
                """
                ✅ **Düşük arıza riski tespit edildi.**

                Makine normal çalışma
                aralığında görünmektedir.
                """
            )


        st.markdown(
            "### 📋 Analiz Edilen Değerler"
        )


        input_data = pd.DataFrame(
            {
                "Parametre": [
                    "Makine Tipi",
                    "Hava Sıcaklığı",
                    "Proses Sıcaklığı",
                    "Dönüş Hızı",
                    "Tork",
                    "Takım Aşınması",
                ],

                "Değer": [
                    machine_type,

                    f"{air_temperature:.1f} K",

                    f"{process_temperature:.1f} K",

                    f"{rotational_speed} rpm",

                    f"{torque:.1f} Nm",

                    f"{tool_wear} min",
                ]
            }
        )


        st.dataframe(
            input_data,
            hide_index=True,
            width="stretch"
        )


    else:

        st.info(
            """
            Sol taraftaki parametreleri belirledikten sonra
            **Makineyi Analiz Et** butonuna basın.
            """
        )


st.divider()


# =========================================================
# 13. ANALİTİK DASHBOARD
# =========================================================

st.subheader(
    "📊 Analitik Dashboard"
)


tab1, tab2, tab3, tab4 = (
    st.tabs(
        [
            "📈 Genel Bakış",

            "⚙️ Çalışma Koşulları",

            "🔧 Aşınma & Sıcaklık",

            "🚨 Arıza Türleri",
        ]
    )
)


# =========================================================
# TAB 1
# GENEL BAKIŞ
# =========================================================

with tab1:

    overview_col1, overview_col2 = (
        st.columns(2)
    )


    # -----------------------------------------------------
    # ARIZA DAĞILIMI
    # -----------------------------------------------------

    failure_summary = (
        df[
            "Failure Label"
        ]

        .value_counts()

        .rename_axis(
            "Status"
        )

        .reset_index(
            name="Count"
        )
    )


    failure_chart = (
        alt.Chart(
            failure_summary
        )

        .mark_arc(
            innerRadius=80,
            outerRadius=145
        )

        .encode(

            theta=alt.Theta(
                "Count:Q"
            ),

            color=alt.Color(

                "Status:N",

                title="Durum",

                scale=alt.Scale(
                    domain=
                    FAILURE_DOMAIN,

                    range=
                    FAILURE_RANGE
                )
            ),

            tooltip=[

                alt.Tooltip(
                    "Status:N",
                    title="Durum"
                ),

                alt.Tooltip(
                    "Count:Q",
                    title="Makine Sayısı"
                ),
            ]
        )

        .properties(
            title=
            "Makine Arıza Dağılımı",

            height=350
        )
    )


    failure_chart = dark_chart(
        failure_chart
    )


    with overview_col1:

        st.altair_chart(
            failure_chart,

            width="stretch",

            theme=None
        )


    # -----------------------------------------------------
    # MAKİNE TİPİ / ARIZA ORANI
    # -----------------------------------------------------

    type_failure = (
        df.groupby(
            "Type",
            as_index=False
        )[
            "Machine failure"
        ]
        .mean()
    )


    type_failure[
        "Failure Rate"
    ] = (
        type_failure[
            "Machine failure"
        ]
        * 100
    )


    type_chart = (
        alt.Chart(
            type_failure
        )

        .mark_bar(
            color=ACCENT,

            cornerRadiusTopLeft=6,

            cornerRadiusTopRight=6
        )

        .encode(

            x=alt.X(
                "Type:N",
                title="Makine Tipi"
            ),

            y=alt.Y(
                "Failure Rate:Q",
                title="Arıza Oranı (%)"
            ),

            tooltip=[

                alt.Tooltip(
                    "Type:N",
                    title="Makine Tipi"
                ),

                alt.Tooltip(
                    "Failure Rate:Q",
                    title="Arıza Oranı (%)",
                    format=".2f"
                ),
            ]
        )

        .properties(
            title=
            "Makine Tipine Göre Arıza Oranı",

            height=350
        )
    )


    type_chart = dark_chart(
        type_chart
    )


    with overview_col2:

        st.altair_chart(
            type_chart,

            width="stretch",

            theme=None
        )


# =========================================================
# TAB 2
# ÇALIŞMA KOŞULLARI
# =========================================================

with tab2:

    st.markdown(
        "### ⚙️ Dönüş Hızı ve Tork Analizi"
    )


    filter1, filter2 = (
        st.columns(2)
    )


    with filter1:

        selected_machine_types = (
            st.multiselect(

                "Makine Tipi Filtresi",

                options=[
                    "L",
                    "M",
                    "H",
                ],

                default=[
                    "L",
                    "M",
                    "H",
                ],

                key=
                "condition_machine_types",
            )
        )


    with filter2:

        selected_failure_status = (
            st.multiselect(

                "Makine Durumu Filtresi",

                options=[
                    "No Failure",
                    "Failure",
                ],

                default=[
                    "No Failure",
                    "Failure",
                ],

                key=
                "condition_failure_status",
            )
        )


    condition_df = (
        df[
            df[
                "Type"
            ].isin(
                selected_machine_types
            )

            &

            df[
                "Failure Label"
            ].isin(
                selected_failure_status
            )
        ]
    )


    if condition_df.empty:

        st.warning(
            """
            Seçilen filtrelere uygun veri bulunamadı.
            En az bir Makine Tipi ve Makine Durumu seçin.
            """
        )


    else:

        condition_plot_df = (
            condition_df.sample(

                n=min(
                    len(
                        condition_df
                    ),
                    4500
                ),

                random_state=42
            )
        )


        # -------------------------------------------------
        # RPM - TORK SCATTER
        # -------------------------------------------------

        legend_selection = (
            alt.selection_point(

                fields=[
                    "Failure Label"
                ],

                bind="legend"
            )
        )


        scatter = (
            alt.Chart(
                condition_plot_df
            )

            .mark_circle(
                size=65,

                stroke="#0b1020",

                strokeWidth=0.4
            )

            .encode(

                x=alt.X(
                    "Rotational speed [rpm]:Q",

                    title=
                    "Dönüş Hızı (rpm)",

                    scale=alt.Scale(
                        zero=False
                    )
                ),

                y=alt.Y(
                    "Torque [Nm]:Q",

                    title=
                    "Tork (Nm)",

                    scale=alt.Scale(
                        zero=False
                    )
                ),

                color=alt.Color(

                    "Failure Label:N",

                    title=
                    "Makine Durumu",

                    scale=alt.Scale(

                        domain=
                        FAILURE_DOMAIN,

                        range=
                        FAILURE_RANGE
                    )
                ),

                opacity=alt.condition(

                    legend_selection,

                    alt.value(
                        0.82
                    ),

                    alt.value(
                        0.20
                    )
                ),

                tooltip=[

                    alt.Tooltip(
                        "Product ID:N",
                        title="Product ID"
                    ),

                    alt.Tooltip(
                        "Type:N",
                        title="Makine Tipi"
                    ),

                    alt.Tooltip(
                        "Rotational speed [rpm]:Q",
                        title="RPM"
                    ),

                    alt.Tooltip(
                        "Torque [Nm]:Q",
                        title="Tork"
                    ),

                    alt.Tooltip(
                        "Tool wear [min]:Q",
                        title="Takım Aşınması"
                    ),

                    alt.Tooltip(
                        "Failure Label:N",
                        title="Durum"
                    ),
                ]
            )

            .add_params(
                legend_selection
            )

            .properties(
                title=
                "Tork – Dönüş Hızı ve Arıza İlişkisi",

                height=520
            )

            .interactive()
        )


        scatter = dark_chart(
            scatter
        )


        st.altair_chart(
            scatter,

            width="stretch",

            theme=None
        )


        st.caption(
            """
            Noktaların üzerine gelerek makine bilgilerini
            görebilir ve grafik üzerinde zoom yapabilirsiniz.
            Sağdaki lejant üzerinden Failure / No Failure
            grupları da seçilebilir.
            """
        )


        # -------------------------------------------------
        # TORK DAĞILIMI
        # -------------------------------------------------

        st.markdown(
            "### 📦 Tork Dağılımı"
        )


        torque_box = (
            alt.Chart(
                condition_plot_df
            )

            .mark_boxplot(
                size=70,

                opacity=0.80
            )

            .encode(

                x=alt.X(
                    "Failure Label:N",

                    title=
                    "Makine Durumu"
                ),

                y=alt.Y(
                    "Torque [Nm]:Q",

                    title=
                    "Tork (Nm)",

                    scale=alt.Scale(
                        zero=False
                    )
                ),

                color=alt.Color(

                    "Failure Label:N",

                    title="Durum",

                    scale=alt.Scale(

                        domain=
                        FAILURE_DOMAIN,

                        range=
                        FAILURE_RANGE
                    )
                )
            )
        )


        torque_points = (
            alt.Chart(
                condition_plot_df
            )

            .mark_circle(
                size=22,

                opacity=0.35
            )

            .encode(

                x=alt.X(
                    "Failure Label:N"
                ),

                y=alt.Y(
                    "Torque [Nm]:Q"
                ),

                color=alt.Color(

                    "Failure Label:N",

                    legend=None,

                    scale=alt.Scale(

                        domain=
                        FAILURE_DOMAIN,

                        range=
                        FAILURE_RANGE
                    )
                ),

                tooltip=[

                    alt.Tooltip(
                        "Product ID:N",
                        title="Product ID"
                    ),

                    alt.Tooltip(
                        "Type:N",
                        title="Makine Tipi"
                    ),

                    alt.Tooltip(
                        "Torque [Nm]:Q",
                        title="Tork"
                    ),

                    alt.Tooltip(
                        "Rotational speed [rpm]:Q",
                        title="RPM"
                    ),

                    alt.Tooltip(
                        "Failure Label:N",
                        title="Durum"
                    ),
                ]
            )
        )


        torque_chart = (
            torque_box
            + torque_points
        ).properties(

            title=
            "Arıza Durumuna Göre Tork Dağılımı",

            height=430
        )


        torque_chart = (
            dark_chart(
                torque_chart
            )
        )


        st.altair_chart(
            torque_chart,

            width="stretch",

            theme=None
        )


        # -------------------------------------------------
        # VERİ TABLOSU
        # -------------------------------------------------

        with st.expander(
            "📋 Çalışma Koşulları Verilerini Görüntüle"
        ):

            condition_table = (
                condition_df[
                    [
                        "Product ID",
                        "Type",
                        "Rotational speed [rpm]",
                        "Torque [Nm]",
                        "Tool wear [min]",
                        "Air temperature [K]",
                        "Process temperature [K]",
                        "Failure Label",
                    ]
                ]
                .reset_index(
                    drop=True
                )
            )


            st.dataframe(
                condition_table,

                hide_index=True,

                width="stretch",

                height=350
            )


# =========================================================
# TAB 3
# AŞINMA VE SICAKLIK
# =========================================================

with tab3:

    st.markdown(
        "### 🔧 Aşınma ve Sıcaklık Analizi"
    )


    wear_filter1, wear_filter2 = (
        st.columns(2)
    )


    with wear_filter1:

        wear_machine_types = (
            st.multiselect(

                "Makine Tipi",

                options=[
                    "L",
                    "M",
                    "H",
                ],

                default=[
                    "L",
                    "M",
                    "H",
                ],

                key=
                "wear_machine_types"
            )
        )


    with wear_filter2:

        wear_failure_status = (
            st.multiselect(

                "Makine Durumu",

                options=[
                    "No Failure",
                    "Failure",
                ],

                default=[
                    "No Failure",
                    "Failure",
                ],

                key=
                "wear_failure_status"
            )
        )


    wear_df = (
        df[
            df[
                "Type"
            ].isin(
                wear_machine_types
            )

            &

            df[
                "Failure Label"
            ].isin(
                wear_failure_status
            )
        ]
    )


    if wear_df.empty:

        st.warning(
            """
            Seçilen filtrelere uygun veri bulunamadı.
            En az bir Makine Tipi ve Makine Durumu seçin.
            """
        )


    else:

        wear_plot_df = (
            wear_df.sample(

                n=min(
                    len(
                        wear_df
                    ),
                    4500
                ),

                random_state=42
            )
        )


        wear_col1, wear_col2 = (
            st.columns(2)
        )


        # -------------------------------------------------
        # TOOL WEAR
        # -------------------------------------------------

        tool_box = (
            alt.Chart(
                wear_plot_df
            )

            .mark_boxplot(
                size=65,

                opacity=0.80
            )

            .encode(

                x=alt.X(
                    "Failure Label:N",

                    title=
                    "Makine Durumu"
                ),

                y=alt.Y(
                    "Tool wear [min]:Q",

                    title=
                    "Takım Aşınması (min)",

                    scale=alt.Scale(
                        zero=False
                    )
                ),

                color=alt.Color(

                    "Failure Label:N",

                    title="Durum",

                    scale=alt.Scale(

                        domain=
                        FAILURE_DOMAIN,

                        range=
                        FAILURE_RANGE
                    )
                )
            )
        )


        tool_points = (
            alt.Chart(
                wear_plot_df
            )

            .mark_circle(
                size=20,

                opacity=0.35
            )

            .encode(

                x=
                "Failure Label:N",

                y=
                "Tool wear [min]:Q",

                color=alt.Color(

                    "Failure Label:N",

                    legend=None,

                    scale=alt.Scale(

                        domain=
                        FAILURE_DOMAIN,

                        range=
                        FAILURE_RANGE
                    )
                ),

                tooltip=[

                    alt.Tooltip(
                        "Product ID:N",
                        title="Product ID"
                    ),

                    alt.Tooltip(
                        "Type:N",
                        title="Makine Tipi"
                    ),

                    alt.Tooltip(
                        "Tool wear [min]:Q",
                        title="Takım Aşınması"
                    ),

                    alt.Tooltip(
                        "Torque [Nm]:Q",
                        title="Tork"
                    ),

                    alt.Tooltip(
                        "Failure Label:N",
                        title="Durum"
                    ),
                ]
            )
        )


        tool_wear_chart = (
            tool_box
            + tool_points
        ).properties(

            title=
            "Arıza Durumuna Göre Takım Aşınması",

            height=420
        )


        tool_wear_chart = (
            dark_chart(
                tool_wear_chart
            )
        )


        with wear_col1:

            st.altair_chart(
                tool_wear_chart,

                width="stretch",

                theme=None
            )


        # -------------------------------------------------
        # SICAKLIK FARKI
        # -------------------------------------------------

        temperature_box = (
            alt.Chart(
                wear_plot_df
            )

            .mark_boxplot(
                size=65,

                opacity=0.80
            )

            .encode(

                x=alt.X(
                    "Failure Label:N",

                    title=
                    "Makine Durumu"
                ),

                y=alt.Y(
                    "Temperature Difference [K]:Q",

                    title=
                    "Sıcaklık Farkı (K)",

                    scale=alt.Scale(
                        zero=False
                    )
                ),

                color=alt.Color(

                    "Failure Label:N",

                    title="Durum",

                    scale=alt.Scale(

                        domain=
                        FAILURE_DOMAIN,

                        range=
                        FAILURE_RANGE
                    )
                )
            )
        )


        temperature_points = (
            alt.Chart(
                wear_plot_df
            )

            .mark_circle(
                size=20,

                opacity=0.35
            )

            .encode(

                x=
                "Failure Label:N",

                y=
                "Temperature Difference [K]:Q",

                color=alt.Color(

                    "Failure Label:N",

                    legend=None,

                    scale=alt.Scale(

                        domain=
                        FAILURE_DOMAIN,

                        range=
                        FAILURE_RANGE
                    )
                ),

                tooltip=[

                    alt.Tooltip(
                        "Product ID:N",
                        title="Product ID"
                    ),

                    alt.Tooltip(
                        "Type:N",
                        title="Makine Tipi"
                    ),

                    alt.Tooltip(
                        "Air temperature [K]:Q",
                        title="Hava Sıcaklığı"
                    ),

                    alt.Tooltip(
                        "Process temperature [K]:Q",
                        title="Proses Sıcaklığı"
                    ),

                    alt.Tooltip(
                        "Temperature Difference [K]:Q",
                        title="Sıcaklık Farkı"
                    ),

                    alt.Tooltip(
                        "Failure Label:N",
                        title="Durum"
                    ),
                ]
            )
        )


        temperature_chart = (
            temperature_box
            + temperature_points
        ).properties(

            title=
            "Sıcaklık Farkı – Arıza İlişkisi",

            height=420
        )


        temperature_chart = (
            dark_chart(
                temperature_chart
            )
        )


        with wear_col2:

            st.altair_chart(
                temperature_chart,

                width="stretch",

                theme=None
            )


        # -------------------------------------------------
        # HAVA + PROSES SICAKLIĞI
        # -------------------------------------------------

        st.markdown(
            "### 🌡️ Hava ve Proses Sıcaklığı"
        )


        temp_selection = (
            alt.selection_point(

                fields=[
                    "Failure Label"
                ],

                bind="legend"
            )
        )


        temperature_scatter = (
            alt.Chart(
                wear_plot_df
            )

            .mark_circle(
                size=60,

                stroke="#0b1020",

                strokeWidth=0.4
            )

            .encode(

                x=alt.X(
                    "Air temperature [K]:Q",

                    title=
                    "Hava Sıcaklığı (K)",

                    scale=alt.Scale(
                        zero=False
                    )
                ),

                y=alt.Y(
                    "Process temperature [K]:Q",

                    title=
                    "Proses Sıcaklığı (K)",

                    scale=alt.Scale(
                        zero=False
                    )
                ),

                color=alt.Color(

                    "Failure Label:N",

                    title="Durum",

                    scale=alt.Scale(

                        domain=
                        FAILURE_DOMAIN,

                        range=
                        FAILURE_RANGE
                    )
                ),

                opacity=alt.condition(

                    temp_selection,

                    alt.value(
                        0.78
                    ),

                    alt.value(
                        0.20
                    )
                ),

                tooltip=[

                    alt.Tooltip(
                        "Product ID:N",
                        title="Product ID"
                    ),

                    alt.Tooltip(
                        "Type:N",
                        title="Makine Tipi"
                    ),

                    alt.Tooltip(
                        "Air temperature [K]:Q",
                        title="Hava Sıcaklığı"
                    ),

                    alt.Tooltip(
                        "Process temperature [K]:Q",
                        title="Proses Sıcaklığı"
                    ),

                    alt.Tooltip(
                        "Temperature Difference [K]:Q",
                        title="Sıcaklık Farkı"
                    ),

                    alt.Tooltip(
                        "Failure Label:N",
                        title="Durum"
                    ),
                ]
            )

            .add_params(
                temp_selection
            )

            .properties(

                title=
                "Hava ve Proses Sıcaklığı Arasındaki İlişki",

                height=500
            )

            .interactive()
        )


        temperature_scatter = (
            dark_chart(
                temperature_scatter
            )
        )


        st.altair_chart(
            temperature_scatter,

            width="stretch",

            theme=None
        )


        st.caption(
            """
            Grafik üzerinde zoom yapılabilir. Noktaların üzerine
            geldiğinizde sıcaklık, makine tipi ve arıza durumu
            bilgileri görüntülenir.
            """
        )


        # -------------------------------------------------
        # VERİ TABLOSU
        # -------------------------------------------------

        with st.expander(
            "📋 Aşınma ve Sıcaklık Verilerini Görüntüle"
        ):

            wear_table = (
                wear_df[
                    [
                        "Product ID",
                        "Type",
                        "Tool wear [min]",
                        "Air temperature [K]",
                        "Process temperature [K]",
                        "Temperature Difference [K]",
                        "Torque [Nm]",
                        "Rotational speed [rpm]",
                        "Failure Label",
                    ]
                ]
                .reset_index(
                    drop=True
                )
            )


            st.dataframe(
                wear_table,

                hide_index=True,

                width="stretch",

                height=350
            )


# =========================================================
# TAB 4
# ARIZA TÜRLERİ
# =========================================================

with tab4:

    st.markdown(
        """
        Bu bölüm veri setindeki geçmiş gerçek arıza
        türlerinin dağılımını göstermektedir.

        **Not:** Tahmin modelimiz şu anda arıza türünü
        değil, makinenin **arıza yapıp yapmayacağını**
        tahmin etmektedir.
        """
    )


    failure_types = (
        pd.DataFrame(
            {
                "Failure Type": [
                    "TWF",
                    "HDF",
                    "PWF",
                    "OSF",
                    "RNF",
                ],

                "Count": [

                    int(
                        df[
                            "TWF"
                        ].sum()
                    ),

                    int(
                        df[
                            "HDF"
                        ].sum()
                    ),

                    int(
                        df[
                            "PWF"
                        ].sum()
                    ),

                    int(
                        df[
                            "OSF"
                        ].sum()
                    ),

                    int(
                        df[
                            "RNF"
                        ].sum()
                    ),
                ]
            }
        )
    )


    failure_type_chart = (
        alt.Chart(
            failure_types
        )

        .mark_bar(
            color=DANGER,

            cornerRadiusTopLeft=6,

            cornerRadiusTopRight=6
        )

        .encode(

            x=alt.X(
                "Failure Type:N",

                title=
                "Arıza Türü",

                sort="-y"
            ),

            y=alt.Y(
                "Count:Q",

                title=
                "Arıza Sayısı"
            ),

            tooltip=[

                alt.Tooltip(
                    "Failure Type:N",
                    title="Arıza Türü"
                ),

                alt.Tooltip(
                    "Count:Q",
                    title="Arıza Sayısı"
                ),
            ]
        )

        .properties(

            title=
            "Arıza Türlerinin Dağılımı",

            height=450
        )
    )


    failure_type_chart = (
        dark_chart(
            failure_type_chart
        )
    )


    st.altair_chart(
        failure_type_chart,

        width="stretch",

        theme=None
    )


    st.markdown(
        "### 📋 Arıza Türü Verileri"
    )


    st.dataframe(

        failure_types
        .sort_values(
            "Count",
            ascending=False
        ),

        hide_index=True,

        width="stretch"
    )


# =========================================================
# 14. FOOTER
# =========================================================

st.divider()


st.caption(
    "Predictive Maintenance System | "
    "Machine Learning Based Failure Prediction"
)