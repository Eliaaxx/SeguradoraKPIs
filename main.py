import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path




# Configuração da página
st.set_page_config(
    page_title="Insurance Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Centralização do titulo
st.markdown("""
    <h1 style='text-align: center;'>Insurance Analytics</h1>
    """, unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>1981 - 2018</h3>", unsafe_allow_html=True)

# Estilização Base (Dark Mode e Cyano)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    div[data-testid="stMetricValue"] {
        color: #00f2ea;
    }
    .stPlotlyChart {
        border-radius: 10px;
    }
    /* Sidebar: força cor primária teal/cyan */
    section[data-testid="stSidebar"] {
        --primary-color: #00f2ea !important;
    }

    /* Slider da sidebar (trilho e alças) */
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #00f2ea !important;
        border-color: #00f2ea !important;
    }
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div > div:first-child {
        background-color: rgba(0, 242, 234, 0.25) !important; /* trilho inativo */
    }
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div > div:nth-child(2) {
        background-color: #00f2ea !important; /* trilho ativo */
    }
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] p {
        color: #00f2ea !important; /* datas exibidas acima do slider */
    }
    /* Oculta datas fixas nas extremidades (mínimo e máximo) */
    section[data-testid="stSidebar"] div[data-testid="stSliderTickBarMin"],
    section[data-testid="stSidebar"] div[data-testid="stSliderTickBarMax"] {
        display: none !important;
    }

    /* Demais filtros da sidebar */
    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
        background-color: rgba(0, 242, 234, 0.2) !important;
        border: 1px solid #00f2ea !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div {
        border-color: #00f2ea !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Tenta primeiro o arquivo principal; se não existir, usa o alternativo
    base_path = Path(r"C:\Users\guest\Desktop\InsuranceDash")
    csv_path = base_path / "insurance.csv"
    if not csv_path.exists():
        csv_path = base_path / "isurance.csv"

    
    df = pd.read_csv(csv_path, sep=None, engine="python")
    
    # Conversão de datas
     
    df['Date_start_contract'] = pd.to_datetime(df['Date_start_contract'], errors='coerce', dayfirst=True)
    df['Date_birth'] = pd.to_datetime(df['Date_birth'], errors='coerce', dayfirst=True)
    df['Date_last_renewal'] = pd.to_datetime(df['Date_last_renewal'], errors='coerce', dayfirst=True)
    df['Date_next_renewal'] = pd.to_datetime(df['Date_next_renewal'], errors='coerce', dayfirst=True)

    current_year = datetime.now().year
    df["idade"] = current_year - df["Date_birth"].dt.year
    
    return df

df = load_data()

# --- SIDEBAR (Filtros) ---
st.sidebar.header("Filtros")
area_filter = st.sidebar.multiselect(
    "Selecione a Área:",
    options=df["Area"].unique(),
    default=df["Area"].unique()
)

risk_filter = st.sidebar.multiselect(
    "Tipo de Risco:",
    options=sorted(df["Type_risk"].unique()),
    default=df["Type_risk"].unique()
)

#=====================================================================================
# Filtro da Side Bar - Data slide
date_base = df["Date_start_contract"].dropna()
if not date_base.empty:
    min_date = date_base.min().date()
    max_date = date_base.max().date()
    selected_period = st.sidebar.date_input(
        "Selecione o período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
else:
    selected_period = ()
if isinstance(selected_period, tuple) and len(selected_period) == 2:
    start_date, end_date = selected_period
else:
    start_date = end_date = None
mask = df["Area"].isin(area_filter) & df["Type_risk"].isin(risk_filter)
if start_date is not None and end_date is not None:
    mask = mask & df["Date_start_contract"].dt.date.between(start_date, end_date)
df_selection = df.loc[mask]
#=====================================================================================



# --- MAIN PAGE ---
st.markdown("##")

#DEF PARA UNIDADE DE MEDIDA $
def format_compacto(valor: float) -> str:
    abs_valor = abs(valor)

    if abs_valor >= 1_000_000_000:
        numero = valor / 1_000_000_000
        sufixo = "B"   # bilhões
    elif abs_valor >= 1_000_000:
        numero = valor / 1_000_000
        sufixo = "M"   # milhões
    elif abs_valor >= 1_000:
        numero = valor / 1_000
        sufixo = "K"   # mil
    else:
        numero = valor
        sufixo = ""

    # 2 casas + troca ponto por vírgula
    return f"{numero:,.2f}{sufixo}".replace(",", "X").replace(".", ",").replace("X", ".")

# Métricas Principais (Top Cards)
ticket_medio = df_selection["Premium"].mean()
total_claims = df_selection["Cost_claims_year"].sum()
avg_age = df_selection["idade"].mean()
n_polices = df_selection.shape[0]

# Ano mais lucrativo (maior soma de Premium no Ano)
premium_por_ano = (
    df_selection.dropna(subset=["Date_start_contract"])
    .assign(ano=df_selection["Date_start_contract"].dt.year)
    .groupby("ano", as_index=True)["Premium"]
    .sum()
)
if not premium_por_ano.empty:
    ano_mais_lucrativo = int(premium_por_ano.idxmax())
    premium_ano_mais_lucrativo = premium_por_ano.max()
else:
    ano_mais_lucrativo = "-"
    premium_ano_mais_lucrativo = 0.0

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Ticket Médio (Premium)", f"$ {ticket_medio:,.2f}")
with col2:
    st.metric("Custo Total de Sinistros", f"$ {format_compacto(total_claims)}")
with col3:
    st.metric("Idade Média Segurados", f"{avg_age:.1f} anos")
with col4:
    st.metric("Total de Apólices", f"{n_polices:,}")
with col5:
    st.metric("Ano Mais Lucrativo", f"{ano_mais_lucrativo}", f"$ {format_compacto(premium_ano_mais_lucrativo)}")

st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1]) # [largura_esq, largura_grafico, largura_dir]

with col1:
    st.markdown("### Tipos de risco")
    st.write("`1` → Moto")
    st.write("`2` → Vans")
    st.write("`3` → Carro")
    st.write("`4` → Carro Agricola")

with col2:
    st.write(' ')
    # Exemplo: st.line_chart(data)

with col3:
    st.markdown("### Tipos de Área")
    st.write(" - `0` → Rural")
    st.write(" - `1` → Urbano")

st.markdown("---")



# --- GRÁFICOS ---

left_column, right_column = st.columns(2)

# Gráfico 1: Ticket Médio por Tipo de Risco 
with left_column:
    st.subheader("Ticket Médio p/Tipo de Risco")
    avg_premium_risk = (
        df_selection.groupby(by=["Type_risk"]).mean(numeric_only=True)[["Premium"]].sort_values(by="Premium")
    )
    fig_premium = px.bar(
        avg_premium_risk,
        x=avg_premium_risk.index,
        y="Premium",
        orientation="v",
        color_discrete_sequence=["#00f2ea"] * len(avg_premium_risk),
        template="plotly_dark"
    )
    fig_premium.update_layout(plot_bgcolor="rgba(0,0,0,0)", yaxis=(dict(showgrid=False)))
    st.plotly_chart(fig_premium, use_container_width=True)

# Gráfico 2: Distribuição de Sinistros por Área
with right_column:
    st.subheader("Distribuição de Custos p/Área")
    fig_claims = px.pie(
        df_selection,
        values='Cost_claims_year',
        names='Area',
        hole=.4,
        color_discrete_sequence=["#00f2ea"],
        template="plotly_dark"
    )
    st.plotly_chart(fig_claims, use_container_width=True)

st.markdown("---")

# Gráfico 3: Idade Média por Tipo de Risco
st.subheader("Perfil de Idade p/Segmento de Risco")
age_risk = df_selection.groupby("Type_risk")["idade"].mean().reset_index()
fig_age = px.line(
    age_risk,
    x="Type_risk",
    y="idade",
    markers=True,
    template="plotly_dark",
    color_discrete_sequence=["#00f2ea"]
)


fig_age.update_layout(yaxis_title="Idade Média")
st.plotly_chart(fig_age, use_container_width=True)

# Gráfico 4: Ponto de Equilíbrio da Carteira (Sinistralidade)
st.markdown("---")
st.subheader("Ponto de Equilíbrio da Carteira (Sinistralidade Móvel)")

Sinestralidade_Média = 48.6

sin_df = (
    df_selection.dropna(subset=["Date_start_contract"])
    .copy()
    .set_index("Date_start_contract")
    .resample("MS")[["Premium", "Cost_claims_year"]]
    .sum()
    .reset_index()
)

if not sin_df.empty:
    # Sinistralidade mensal = sinistro / prêmio
    sin_df["sinistralidade_mensal"] = (
        (sin_df["Cost_claims_year"] / sin_df["Premium"].replace(0, pd.NA)) * 100
    ).fillna(0)

    # Sinistralidade móvel 12 meses para leitura de tendência de longo prazo
    sin_df["sinistralidade_movel_12m"] = (
        sin_df["sinistralidade_mensal"].rolling(window=12, min_periods=3).mean()
    )

    # Tendência: compara início vs fim da série móvel 12M
    serie_movel = sin_df["sinistralidade_movel_12m"].dropna()
    if len(serie_movel) >= 2:
        variacao = serie_movel.iloc[-1] - serie_movel.iloc[0]
        if variacao > 1:
            tendencia_txt = "Tendência: aumentando (sinal de alerta para revisar tarifa)."
        elif variacao < -1:
            tendencia_txt = "Tendência: diminuindo (melhora da carteira ao longo do tempo)."
        else:
            tendencia_txt = "Tendência: estável (variação pequena no período)."
    else:
        tendencia_txt = "Tendência: dados insuficientes para inferência robusta."

    fig_sin = go.Figure()
    fig_sin.add_trace(
        go.Scatter(
            x=sin_df["Date_start_contract"],
            y=sin_df["sinistralidade_mensal"],
            mode="lines",
            name="Sinistralidade Mensal (%)",
            line=dict(color="rgba(0,242,234,0.35)", width=1.5),
        )
    )
    fig_sin.add_trace(
        go.Scatter(
            x=sin_df["Date_start_contract"],
            y=sin_df["sinistralidade_movel_12m"],
            mode="lines",
            name="Sinistralidade Móvel 12M (%)",
            line=dict(color="#00f2ea", width=3),
        )
    )
    fig_sin.add_hline(
        y=Sinestralidade_Média,
        line_dash="dash",
        line_color="#ffae42",
        annotation_text=f"Sinestralidade Média {Sinestralidade_Média:.1f}%",
        annotation_position="top left",
    )
    fig_sin.update_layout(
        template="plotly_dark",
        xaxis_title="Mês",
        yaxis_title="Sinistralidade (%)",
        yaxis=dict(ticksuffix="%"),
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Séries",
    )
    st.plotly_chart(fig_sin, use_container_width=True)
    st.caption(tendencia_txt)
else:
    st.info("Sem dados suficientes no período selecionado para calcular a sinistralidade mensal.")

