import streamlit as st
from pytrends.request import TrendReq
import pandas as pd


# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="TRENVYRA",
    page_icon="logo.png",
    layout="wide"
)


# ---------------------------------------
# CSS
# ---------------------------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f2a44,#1f4e79,#3270ab,#5aa0d6);
color:white;
}

.block-container{
padding-top:2rem;
}

.card{
background: rgba(255,255,255,0.08);
padding:20px;
border-radius:12px;
border:1px solid rgba(255,255,255,0.15);
text-align:center;
font-weight:600;
}

/* ปุ่มทั้งหมด */
div.stButton > button{
height:45px;
border-radius:25px;
padding:8px 18px;
font-weight:600;
font-size:16px;
background:#0f172a;
color:white;
border:1px solid rgba(255,255,255,0.2);
}

/* search input */
div[data-baseweb="input"]{
height:45px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------
# HEADER
# ---------------------------------------

logo = "../logo.png"

col_logo, col_title = st.columns([1,6])

with col_logo:
    st.image(logo, width=120)

with col_title:
    st.title("TRENVYRA")
    st.caption("AI Trend & Market Intelligence Platform")

st.divider()


# ---------------------------------------
# FEATURES
# ---------------------------------------

st.subheader("Platform Features")

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown('<div class="card">📈 Trend Analysis</div>', unsafe_allow_html=True)

with f2:
    st.markdown('<div class="card">🔥 Viral Detection</div>', unsafe_allow_html=True)

with f3:
    st.markdown('<div class="card">🧠 Market Insight</div>', unsafe_allow_html=True)

with f4:
    st.markdown('<div class="card">💡 Content Ideas</div>', unsafe_allow_html=True)

st.divider()


# ---------------------------------------
# GOOGLE TRENDS CONNECT
# ---------------------------------------

pytrends = TrendReq(
    hl='th-TH',
    tz=360
)


# ---------------------------------------
# SEARCH
# ---------------------------------------

st.subheader("🔎 Search Market Trend")

col1, col2 = st.columns([8,1])

with col1:
    keyword_input = st.text_input(
        "ค้นหาสินค้า ธุรกิจ หรือเทรนด์ที่ต้องการวิเคราะห์",
        placeholder="เช่น สกินแคร์, หุ้น, รถยนต์ไฟฟ้า",
        label_visibility="collapsed"
    )

with col2:
    search_click = st.button("🔍", use_container_width=True)

keyword = None
if search_click and keyword_input:
    keyword = keyword_input


# ---------------------------------------
# EXAMPLE KEYWORDS
# ---------------------------------------

st.write("💡 Example keywords")

example_keywords = [
    "สกินแคร์",
    "อาหารเสริม",
    "หุ้น",
    "crypto",
    "ฟุตบอล",
    "ท่องเที่ยว"
]

row = st.columns([1,2,2,2,2,2,2,1])

for i, k in enumerate(example_keywords):

    with row[i+1]:

        if st.button(k, key=f"example_{i}", use_container_width=True):
            keyword = k


# ---------------------------------------
# POPULAR TRENDS
# ---------------------------------------

st.subheader("🔥 Popular Business Trends")

popular_keywords = [
    "แฟรนไชส์",
    "ร้านอาหาร",
    "สกินแคร์",
    "คลินิกความงาม",
    "หุ้น",
    "การลงทุน",
    "รถยนต์ไฟฟ้า",
    "สุขภาพ"
]

row1 = st.columns([1,2,2,2,2,1])

for i in range(4):

    with row1[i+1]:

        if st.button(popular_keywords[i], key=f"popular_{i}", use_container_width=True):
            keyword = popular_keywords[i]


row2 = st.columns([1,2,2,2,2,1])

for i in range(4,8):

    with row2[i-3]:

        if st.button(popular_keywords[i], key=f"popular_{i}", use_container_width=True):
            keyword = popular_keywords[i]


# ---------------------------------------
# GOOGLE TRENDS DATA
# ---------------------------------------

if keyword:

    try:

        pytrends.build_payload(
            [keyword],
            timeframe='today 3-m',
            geo='TH'
        )

        interest = pytrends.interest_over_time()

        related = pytrends.related_queries()

        rising = None
        top = None

        if keyword in related:

            rising = related[keyword].get("rising")
            top = related[keyword].get("top")

    except Exception:

        st.error("ไม่สามารถดึงข้อมูล Google Trends ได้ กรุณาลองใหม่")
        st.stop()


    # ---------------------------------------
    # METRICS
    # ---------------------------------------

    if interest is not None and not interest.empty:

        latest = int(interest[keyword].iloc[-1])
        avg = int(interest[keyword].mean())
        peak = int(interest[keyword].max())

        trend_score = int((latest*0.4)+(avg*0.3)+(peak*0.3))

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("📈 Current Demand", latest)
        m2.metric("📊 Average Demand", avg)
        m3.metric("🚀 Peak Interest", peak)
        m4.metric("⭐ Trend Score", trend_score)


    st.divider()


    # ---------------------------------------
    # GRAPH
    # ---------------------------------------

    st.subheader("📈 Interest Over Time")

    if interest is not None and not interest.empty:
        st.line_chart(interest[keyword])


    st.divider()


    # ---------------------------------------
    # RISING + TOP
    # ---------------------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("🔥 Rising Trends")

        if rising is not None and not rising.empty:

            rising_display = rising.head(10)

            rising_display.index = rising_display.index + 1

            st.dataframe(rising_display)

            st.bar_chart(
                rising_display.set_index("query")["value"]
            )

        else:

            st.info("ไม่มี Rising Trends")


    with right:

        st.subheader("📊 Top Searches")

        if top is not None and not top.empty:

            top_display = top.head(10)

            top_display.index = top_display.index + 1

            st.dataframe(top_display)

            st.bar_chart(
                top_display.set_index("query")["value"]
            )

        else:

            st.info("ไม่มี Top Trends")


    st.divider()


    # ---------------------------------------
    # CONTENT IDEAS
    # ---------------------------------------

    st.subheader("💡 Marketing Content Ideas")

    ideas = [

        f"5 เรื่องที่ต้องรู้เกี่ยวกับ {keyword}",
        f"{keyword} ดีจริงไหม?",
        f"รีวิว {keyword} ที่กำลังเป็นกระแส",
        f"{keyword} สำหรับมือใหม่",
        f"เทรนด์ใหม่ของ {keyword}"

    ]

    for idea in ideas:
        st.write("•", idea)