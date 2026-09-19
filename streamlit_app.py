import streamlit as st
import yfinance as yf

from app import run


st.set_page_config(
    page_title="Market Lens | AI Stock Desk",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
    :root { --ink:#17231f; --muted:#65736d; --mint:#b9e9d3; --mint-dark:#1d765a; --paper:#f4f7f2; --line:#dce6df; }
    .stApp { background:var(--paper); color:var(--ink); }
    [data-testid="stHeader"] { background:transparent; }
    [data-testid="stSidebar"] { background:#19352c; }
    [data-testid="stSidebar"] * { color:#eef8f1 !important; }
    .block-container { max-width:1240px; padding:3.5rem 3rem 4rem; }
    h1,h2,h3,p,div { font-family:'DM Sans',sans-serif; }
    h1 { font-size:clamp(2.5rem,5vw,4.8rem); line-height:.95; max-width:760px; }
    .eyebrow,.quote-label { font-family:'Space Mono',monospace; font-size:.72rem; letter-spacing:.08em; color:var(--mint-dark); font-weight:700; }
    .hero-copy { color:var(--muted); font-size:1.1rem; max-width:620px; margin:1.2rem 0 2rem; }
    .quote-card { background:#19352c; color:#f4fff8; border-radius:8px; padding:1.5rem 1.7rem; min-height:190px; box-shadow:0 16px 30px #19352c1c; }
    .quote-card .quote-label { color:var(--mint); }
    .quote-name { margin-top:1.2rem; font-size:1.05rem; }
    .quote-price { font-size:2.5rem; line-height:1.1; font-weight:700; margin:.3rem 0; }
    .quote-change { font-family:'Space Mono',monospace; font-size:.8rem; }
    .positive { color:#9bf1c7; } .negative { color:#ffad9e; }
    .result-panel { background:#fff; border:1px solid var(--line); border-radius:8px; padding:1.5rem 1.8rem; margin-top:1rem; }
    .stButton > button { background:#b9e9d3; color:#17352b; border:0; border-radius:5px; font-weight:700; min-height:3rem; }
    .stButton > button:hover { background:#91d9b8; color:#17352b; }
    [data-testid="stMetric"] { background:#fff; border:1px solid var(--line); padding:1rem; border-radius:6px; }
    [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] p { color:#52615a !important; }
    [data-testid="stMetricValue"] { color:#17231f !important; }
    [data-testid="stMetricDelta"] { color:#1d765a !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_quote(ticker: str):
    info = yf.Ticker(ticker).info
    price = info.get("regularMarketPrice")
    if price is None:
        return None
    return {
        "price": price,
        "change": info.get("regularMarketChange") or 0,
        "change_percent": info.get("regularMarketChangePercent") or 0,
        "currency": info.get("currency", "USD"),
        "name": info.get("longName") or info.get("shortName") or ticker,
    }


def render_quote(quote):
    change = quote["change"]
    change_percent = quote["change_percent"]
    direction = "positive" if change >= 0 else "negative"
    sign = "+" if change >= 0 else ""
    st.markdown(
        f"""
        <div class="quote-card">
            <div class="quote-label">LIVE MARKET SNAPSHOT</div>
            <div class="quote-name">{quote['name']}</div>
            <div class="quote-price">{quote['currency']} {quote['price']:,.2f}</div>
            <div class="quote-change {direction}">{sign}{change:,.2f} ({sign}{change_percent:.2f}%) today</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown('<div class="eyebrow">MARKET LENS / AI STOCK DESK</div>', unsafe_allow_html=True)
st.title("A clearer read on the market.")
st.markdown(
    '<p class="hero-copy">Bring a ticker. Get a live market snapshot, an analyst brief, and an AI trading perspective in one focused workspace.</p>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Market Lens")
    st.caption("CrewAI research desk")
    st.divider()
    ticker = st.text_input("Ticker symbol", value="TSLA", max_chars=10).strip().upper()
    analyze = st.button("Run stock analysis", use_container_width=True)
    st.divider()
    st.caption("Data comes from Yahoo Finance. AI output is informational and not financial advice.")

if not ticker:
    st.warning("Enter a ticker symbol to begin.")
    st.stop()

try:
    quote = get_quote(ticker)
except Exception as error:
    st.error(f"Could not retrieve market data for {ticker}: {error}")
    st.stop()

if quote is None:
    st.error(f"No live quote was found for {ticker}. Check the ticker and try again.")
    st.stop()

left, right = st.columns([1.35, 1], gap="large")
with left:
    st.markdown('<div class="eyebrow">TODAY\'S SIGNAL</div>', unsafe_allow_html=True)
    st.subheader(f"{ticker} at a glance")
    st.write("The latest quote is ready. Run the desk for a deeper read across fundamentals, catalysts, and risk.")
    metric_a, metric_b = st.columns(2)
    metric_a.metric("Last price", f"{quote['currency']} {quote['price']:,.2f}", f"{quote['change_percent']:+.2f}%")
    metric_b.metric("Daily move", f"{quote['change']:+,.2f}", "Live market data")
with right:
    render_quote(quote)

if analyze:
    with st.status(f"Researching {ticker}...", expanded=False) as status:
        try:
            result = run(ticker)
            status.update(label="Analysis complete", state="complete")
            st.session_state["analysis"] = str(result)
            st.session_state["analysis_ticker"] = ticker
        except Exception as error:
            status.update(label="Analysis failed", state="error")
            message = str(error)
            if "rate_limit" in message.lower() or "rate limit" in message.lower():
                st.error("Groq is temporarily rate-limiting this request. Wait a few seconds and run it again.")
            else:
                st.error(f"The research run failed: {message}")

if st.session_state.get("analysis") and st.session_state.get("analysis_ticker") == ticker:
    st.markdown('<div class="eyebrow">CREWAI RESEARCH OUTPUT</div>', unsafe_allow_html=True)
    st.subheader(f"Desk brief for {ticker}")
    st.markdown('<div class="result-panel">', unsafe_allow_html=True)
    st.markdown(st.session_state["analysis"])
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("### Ready when you are")
    st.info("Use the button in the sidebar to run the analyst and trader agents.")
