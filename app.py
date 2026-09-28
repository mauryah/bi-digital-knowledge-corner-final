import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

# ============================================================
# BI DIGITAL KNOWLEDGE CORNER
# Tampilan dibuat mengikuti referensi: simpel, rapi, visual,
# dengan sidebar biru dan kartu topik yang kuat.
# ============================================================

st.set_page_config(
    page_title="BI Digital Knowledge Corner",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent
ASSET_DIR = BASE_DIR / "assets" if (BASE_DIR / "assets").exists() else BASE_DIR
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

BI_URL = "https://www.bi.go.id/"
LIBRARY_URL = "https://web-ibilibrary.moco.co.id/"
FEEDBACK_FILE = DATA_DIR / "feedback.csv"


# ============================================================
# DATA TOPIK
# ============================================================

TOPICS = {
    "Rupiah": {
        "icon": "💰",
        "image": "rupiah.svg",
        "tag": "RUPIAH",
        "short": "Mengenal Rupiah sebagai alat pembayaran dan simbol kedaulatan negara.",
        "what": "Rupiah merupakan alat pembayaran yang sah di wilayah Negara Kesatuan Republik Indonesia sekaligus simbol kedaulatan negara.",
        "why": "Pemahaman tentang Rupiah membantu masyarakat mengenali fungsi uang serta pentingnya menggunakan dan memperlakukan Rupiah dengan baik.",
    },
    "Sistem Pembayaran": {
        "icon": "💳",
        "image": "payment.svg",
        "tag": "SISTEM PEMBAYARAN",
        "short": "Mengenal perkembangan sistem pembayaran tunai dan digital di Indonesia.",
        "what": "Sistem pembayaran mencakup berbagai mekanisme yang digunakan untuk memindahkan dana dalam kegiatan ekonomi, baik secara tunai maupun nontunai.",
        "why": "Pemahaman sistem pembayaran membantu masyarakat mengenali berbagai cara transaksi dan perkembangan pembayaran digital di Indonesia.",
    },
    "Stabilitas Ekonomi": {
        "icon": "📈",
        "image": "economy.svg",
        "tag": "STABILITAS EKONOMI",
        "short": "Memahami inflasi, kebijakan moneter, dan stabilitas perekonomian.",
        "what": "Stabilitas ekonomi berkaitan dengan kondisi perekonomian yang tetap terjaga, termasuk perkembangan harga, nilai Rupiah, dan kondisi ekonomi secara umum.",
        "why": "Topik ini membantu masyarakat memahami hubungan antara perubahan harga, kebijakan moneter, dan aktivitas ekonomi sehari-hari.",
    },
    "Ketahanan Pangan": {
        "icon": "🌾",
        "image": "food.svg",
        "tag": "KETAHANAN PANGAN",
        "short": "Memahami hubungan pangan, harga, inflasi, dan kesejahteraan masyarakat.",
        "what": "Ketahanan pangan berkaitan dengan ketersediaan, keterjangkauan, dan keberlanjutan pangan. Perkembangan harga pangan juga berkaitan dengan inflasi.",
        "why": "Memahami ketahanan pangan membantu melihat hubungan antara produksi, distribusi, harga pangan, dan stabilitas ekonomi.",
    },
    "Data & Publikasi": {
        "icon": "📊",
        "image": "data.svg",
        "tag": "DATA & PUBLIKASI",
        "short": "Menemukan data, laporan, dan publikasi ekonomi Bank Indonesia.",
        "what": "Data dan publikasi menyediakan informasi ekonomi dan keuangan yang dapat digunakan untuk memahami perkembangan perekonomian Indonesia.",
        "why": "Data membantu masyarakat, mahasiswa, peneliti, dan pemangku kepentingan memperoleh informasi yang lebih terukur dan dapat ditelusuri.",
    },
    "Kebanksentralan": {
        "icon": "🏦",
        "image": "centralbank.svg",
        "tag": "KEBANKSENTRALAN",
        "short": "Mengenal peran dan fungsi Bank Indonesia sebagai bank sentral.",
        "what": "Bank Indonesia merupakan bank sentral Republik Indonesia yang menjalankan mandat di bidang moneter, sistem pembayaran, dan stabilitas sistem keuangan sesuai ketentuan yang berlaku.",
        "why": "Pemahaman kebanksentralan membantu masyarakat mengetahui keterkaitan kebijakan Bank Indonesia dengan kehidupan ekonomi sehari-hari.",
    },
}


# ============================================================
# HELPERS
# ============================================================

def asset_path(filename):
    p1 = ASSET_DIR / filename
    p2 = BASE_DIR / filename
    if p1.exists():
        return p1
    return p2


def svg_data_uri(filename):
    path = asset_path(filename)
    if not path.exists():
        return ""
    return "data:image/svg+xml;utf8," + quote(path.read_text(encoding="utf-8"))


def save_feedback(row):
    new_df = pd.DataFrame([row])
    if FEEDBACK_FILE.exists():
        old_df = pd.read_csv(FEEDBACK_FILE)
        new_df = pd.concat([old_df, new_df], ignore_index=True)
    new_df.to_csv(FEEDBACK_FILE, index=False)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root{
    --blue:#005596;
    --blue-dark:#063D6B;
    --blue-soft:#EAF4FB;
    --blue-pale:#F4F9FD;
    --red:#E31E24;
    --text:#18324A;
    --muted:#718096;
}

html, body, [class*="css"]{
    font-family:'Inter', sans-serif;
}

.stApp{
    background:#F6F9FC;
}

.main .block-container{
    max-width:1400px;
    padding:1.35rem 2.4rem 3rem;
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#063D6B 0%,#075D91 65%,#0A6D9E 100%);
    border:0;
}

section[data-testid="stSidebar"] > div{
    padding:1.15rem .85rem;
}

.sidebar-brand{
    padding:.3rem .55rem 1.35rem;
    color:white;
}

.sidebar-mark{
    display:inline-flex;
    width:35px;
    height:35px;
    align-items:center;
    justify-content:center;
    border-radius:9px;
    background:white;
    color:var(--blue);
    font-weight:900;
    margin-bottom:.7rem;
}

.sidebar-bi{
    font-size:.78rem;
    font-weight:800;
    letter-spacing:.03em;
}

.sidebar-title{
    margin-top:.3rem;
    font-size:1.35rem;
    line-height:1.08;
    font-weight:900;
}

.sidebar-sub{
    margin-top:.42rem;
    color:rgba(255,255,255,.72);
    font-size:.72rem;
    line-height:1.45;
}

.sidebar-section{
    color:rgba(255,255,255,.48);
    font-size:.62rem;
    font-weight:800;
    letter-spacing:.12em;
    margin:.7rem .5rem .35rem;
}

section[data-testid="stSidebar"] div[role="radiogroup"]{
    gap:.18rem;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label{
    border-radius:9px;
    padding:.34rem .5rem;
    color:rgba(255,255,255,.86);
    transition:.15s;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
    background:rgba(255,255,255,.10);
}

section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"]{
    background:#FFFFFF;
    color:#07538A;
    box-shadow:0 5px 15px rgba(0,0,0,.08);
}

section[data-testid="stSidebar"] div[role="radiogroup"] label p{
    font-size:.82rem;
    font-weight:600;
}

.sidebar-bottom{
    margin-top:1.4rem;
    padding:.9rem;
    border-radius:13px;
    background:rgba(255,255,255,.10);
    border:1px solid rgba(255,255,255,.12);
    color:rgba(255,255,255,.78);
    font-size:.68rem;
    line-height:1.5;
}

/* ================= GENERAL ================= */

.page-title{
    color:var(--blue-dark);
    font-size:2rem;
    line-height:1.08;
    font-weight:900;
    margin:.2rem 0 .25rem;
}

.page-subtitle{
    color:var(--muted);
    font-size:.86rem;
    margin-bottom:1.1rem;
}

.section-title{
    color:var(--blue-dark);
    font-size:1.12rem;
    font-weight:800;
    margin:.2rem 0 .15rem;
}

.section-sub{
    color:var(--muted);
    font-size:.74rem;
    margin-bottom:.75rem;
}

/* ================= HERO ================= */

.hero{
    position:relative;
    overflow:hidden;
    min-height:365px;
    border-radius:20px;
    background:linear-gradient(115deg,#063B66,#0877AA);
    box-shadow:0 14px 35px rgba(7,70,110,.16);
    margin-bottom:1.25rem;
}

.hero-bg{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    object-fit:cover;
}

.hero-overlay{
    position:absolute;
    inset:0;
    background:linear-gradient(90deg,
        rgba(4,48,82,.98) 0%,
        rgba(5,66,105,.91) 43%,
        rgba(6,86,124,.30) 80%,
        rgba(6,86,124,.08) 100%);
}

.hero-content{
    position:relative;
    z-index:2;
    padding:2.8rem 3rem;
    max-width:720px;
    color:white;
}

.hero-kicker{
    font-size:.62rem;
    font-weight:800;
    letter-spacing:.16em;
    color:#B9E6FF;
    margin-bottom:.55rem;
}

.hero-title{
    font-size:2.65rem;
    line-height:.98;
    font-weight:900;
    margin:0;
    letter-spacing:-.04em;
}

.hero-title span{
    color:#D9F3FF;
}

.hero-text{
    margin-top:.8rem;
    max-width:600px;
    color:rgba(255,255,255,.83);
    font-size:.76rem;
    line-height:1.55;
}

.search-box{
    margin-top:1.15rem;
    display:flex;
    align-items:center;
    background:white;
    border-radius:11px;
    padding:.3rem .45rem .3rem .75rem;
    max-width:610px;
    box-shadow:0 10px 25px rgba(0,0,0,.13);
}

.search-icon{
    color:#537087;
    font-size:1rem;
    margin-right:.45rem;
}

.search-placeholder{
    color:#8A9AAA;
    font-size:.72rem;
    flex:1;
}

.search-pill{
    background:var(--blue);
    color:white;
    border-radius:8px;
    padding:.45rem .85rem;
    font-size:.68rem;
    font-weight:700;
}

.hero-mini-row{
    display:flex;
    gap:.55rem;
    margin-top:1rem;
    flex-wrap:wrap;
}

.hero-mini{
    background:rgba(255,255,255,.12);
    border:1px solid rgba(255,255,255,.14);
    border-radius:8px;
    padding:.42rem .58rem;
    color:white;
    font-size:.6rem;
}

/* ================= TOPIC CARDS ================= */

.topic-card{
    height:100%;
    min-height:210px;
    background:white;
    border:1px solid #E3EDF5;
    border-radius:14px;
    overflow:hidden;
    box-shadow:0 5px 18px rgba(25,66,94,.07);
    transition:.2s;
}

.topic-card:hover{
    transform:translateY(-3px);
    box-shadow:0 10px 24px rgba(25,66,94,.12);
}

.topic-image{
    height:92px;
    background:linear-gradient(135deg,#EAF5FC,#F7FBFE);
    display:flex;
    align-items:center;
    justify-content:center;
    overflow:hidden;
}

.topic-image img{
    width:100%;
    height:100%;
    object-fit:cover;
}

.topic-body{
    padding:.72rem .75rem .8rem;
}

.topic-tag{
    color:#8B9BAB;
    font-size:.5rem;
    font-weight:800;
    letter-spacing:.08em;
    margin-bottom:.22rem;
}

.topic-name{
    color:var(--blue-dark);
    font-size:.82rem;
    font-weight:800;
    margin-bottom:.28rem;
}

.topic-desc{
    color:#718096;
    font-size:.61rem;
    line-height:1.45;
    min-height:38px;
}

.topic-arrow{
    margin-top:.5rem;
    width:24px;
    height:24px;
    border-radius:50%;
    background:var(--blue);
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:.72rem;
}

/* ================= LOWER INFO CARDS ================= */

.info-card{
    background:white;
    border:1px solid #E3EDF5;
    border-radius:14px;
    padding:.9rem 1rem;
    min-height:125px;
    box-shadow:0 4px 15px rgba(25,66,94,.05);
}

.info-icon{
    font-size:1.35rem;
    margin-bottom:.3rem;
}

.info-title{
    color:var(--blue-dark);
    font-size:.75rem;
    font-weight:800;
}

.info-text{
    color:#748396;
    font-size:.61rem;
    line-height:1.5;
    margin-top:.28rem;
}

/* ================= DETAIL PAGE ================= */

.detail-hero{
    background:white;
    border:1px solid #DDEAF3;
    border-radius:18px;
    overflow:hidden;
    box-shadow:0 7px 22px rgba(25,66,94,.06);
}

.detail-image{
    height:270px;
    background:linear-gradient(135deg,#EAF5FC,#F7FBFE);
    display:flex;
    align-items:center;
    justify-content:center;
}

.detail-image img{
    width:100%;
    height:100%;
    object-fit:cover;
}

.detail-content{
    padding:1.5rem;
}

.detail-tag{
    color:#7D91A2;
    font-size:.58rem;
    font-weight:800;
    letter-spacing:.12em;
}

.detail-title{
    color:var(--blue-dark);
    font-size:1.75rem;
    font-weight:900;
    margin:.25rem 0 .45rem;
}

.detail-short{
    color:#61778A;
    font-size:.78rem;
    line-height:1.55;
}

.detail-box{
    background:white;
    border:1px solid #E0EAF2;
    border-radius:14px;
    padding:1rem 1.15rem;
    min-height:145px;
}

.detail-box h4{
    color:var(--blue-dark);
    font-size:.9rem;
    margin:0 0 .45rem;
}

.detail-box p{
    color:#61778A;
    font-size:.7rem;
    line-height:1.6;
    margin:0;
}

/* ================= BUTTONS ================= */

.stButton > button,
.stLinkButton > a{
    border-radius:9px !important;
    font-weight:700 !important;
    font-size:.72rem !important;
}

.stButton > button{
    border:1px solid #D7E5EF !important;
}

.stLinkButton > a{
    background:var(--blue) !important;
    color:white !important;
    border:0 !important;
}

/* ================= FOOTER ================= */

.footer{
    text-align:center;
    color:#91A0AE;
    font-size:.58rem;
    padding:1.4rem 0 .2rem;
}

/* ================= MOBILE ================= */

@media (max-width:900px){
    .main .block-container{
        padding:.9rem 1rem 2rem;
    }

    .hero{
        min-height:390px;
    }

    .hero-content{
        padding:2rem 1.35rem;
    }

    .hero-title{
        font-size:2rem;
    }

    .topic-card{
        min-height:195px;
    }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="sidebar-mark">BI</div>
    <div class="sidebar-bi">BANK INDONESIA</div>
    <div class="sidebar-title">BI Digital<br>Knowledge Corner</div>
    <div class="sidebar-sub">Media pendukung untuk mengenal informasi kebanksentralan secara ringkas dan terarah.</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section">MENU UTAMA</div>', unsafe_allow_html=True)

pages = [
    "🏠 Beranda",
    "🔎 Cari Informasi",
    "📚 Jelajah Topik",
    "📖 Perpustakaan BI",
    "📝 Feedback",
    "ℹ️ Tentang",
]

# Navigasi dibuat berbasis session state agar tombol di halaman
# (misalnya "Pelajari") benar-benar berpindah halaman.
if "page" not in st.session_state:
    st.session_state["page"] = "🏠 Beranda"

current_page = st.session_state["page"]
if current_page not in pages:
    current_page = pages[0]

page = st.sidebar.radio(
    "Navigasi",
    pages,
    index=pages.index(current_page),
    label_visibility="collapsed",
)
st.session_state["page"] = page

st.sidebar.markdown("""
<div class="sidebar-bottom">
    <b>Knowledge Corner</b><br>
    Temukan informasi kebanksentralan secara sederhana, visual, dan mudah dipahami.
</div>
""", unsafe_allow_html=True)


# ============================================================
# BERANDA
# ============================================================

if page == "🏠 Beranda":

    hero_img = svg_data_uri("hero_building.svg")

    st.markdown(f"""
    <div class="hero">
        <img class="hero-bg" src="{hero_img}">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div class="hero-kicker">DIGITAL KNOWLEDGE CORNER</div>
            <h1 class="hero-title">BI Digital<br><span>Knowledge Corner</span></h1>
            <div class="hero-text">
                Temukan informasi tentang Rupiah, sistem pembayaran,
                stabilitas ekonomi, ketahanan pangan, data dan publikasi,
                serta kebanksentralan.
            </div>
            <div class="search-box">
                <span class="search-icon">⌕</span>
                <span class="search-placeholder">Gunakan pencarian di bawah untuk menemukan topik...</span>
                <span class="search-pill">Cari</span>
            </div>
            <div class="hero-mini-row">
                <div class="hero-mini">📚 Ringkasan informasi</div>
                <div class="hero-mini">📄 Sumber resmi</div>
                <div class="hero-mini">📖 Akses iBI Library</div>
                <div class="hero-mini">💡 Mudah dipahami</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Pencarian yang benar-benar aktif
    with st.form("home_search_form"):
        s1, s2 = st.columns([5, 1])
        with s1:
            home_query = st.text_input(
                "Cari informasi",
                placeholder="Contoh: Rupiah, QRIS, inflasi, pangan, data...",
                label_visibility="collapsed",
            )
        with s2:
            search_submit = st.form_submit_button("🔎 Cari", use_container_width=True)

    if search_submit:
        if home_query.strip():
            st.session_state["search_query"] = home_query.strip()
            st.session_state["page"] = "🔎 Cari Informasi"
            st.rerun()
        else:
            st.info("Masukkan kata kunci terlebih dahulu.")

    st.markdown("""
    <div class="section-title">Jelajahi berdasarkan topik</div>
    <div class="section-sub">Pilih topik yang ingin kamu pelajari dan temukan informasi pentingnya secara ringkas.</div>
    """, unsafe_allow_html=True)

    cols = st.columns(6, gap="small")

    for col, (name, item) in zip(cols, TOPICS.items()):
        with col:
            img = svg_data_uri(item["image"])
            st.markdown(f"""
            <div class="topic-card">
                <div class="topic-image">
                    <img src="{img}">
                </div>
                <div class="topic-body">
                    <div class="topic-tag">{item["tag"]}</div>
                    <div class="topic-name">{item["icon"]} {name}</div>
                    <div class="topic-desc">{item["short"]}</div>
                    <div class="topic-arrow">›</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Pelajari", key=f"topic_{name}", use_container_width=True):
                st.session_state["selected_topic"] = name
                st.session_state["page"] = "📚 Jelajah Topik"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="small")

    with c1:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">💡</div>
            <div class="info-title">Tahukah Kamu?</div>
            <div class="info-text">Rupiah bukan hanya alat pembayaran, tetapi juga simbol kedaulatan negara.</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📖</div>
            <div class="info-title">Ayo Baca Lebih Lanjut</div>
            <div class="info-text">Butuh informasi yang lebih lengkap? Akses koleksi Perpustakaan Bank Indonesia.</div>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("Buka iBI Library →", LIBRARY_URL, use_container_width=True)

    with c3:
        st.markdown("""
        <div class="info-card">
            <div class="info-icon">📱</div>
            <div class="info-title">Cara Menggunakan</div>
            <div class="info-text">Pilih topik → baca ringkasan → lanjutkan ke sumber resmi untuk informasi lebih lengkap.</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# CARI INFORMASI
# ============================================================

elif page == "🔎 Cari Informasi":

    st.markdown('<div class="page-title">Cari Informasi</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Cari topik kebanksentralan berdasarkan kata kunci.</div>', unsafe_allow_html=True)

    query = st.text_input(
        "Kata kunci",
        value=st.session_state.get("search_query", ""),
        placeholder="Contoh: Rupiah, QRIS, inflasi, pangan, data...",
        label_visibility="collapsed",
    )
    st.session_state["search_query"] = query

    if query:
        results = []
        q = query.lower()

        for name, item in TOPICS.items():
            text = f"{name} {item['short']} {item['what']} {item['why']}".lower()
            if q in text:
                results.append((name, item))

        if results:
            for name, item in results:
                img = svg_data_uri(item["image"])
                st.markdown(f"""
                <div class="detail-hero" style="margin-bottom:8px;">
                    <div style="display:flex;gap:16px;align-items:center;padding:12px;">
                        <img src="{img}" style="width:115px;height:80px;object-fit:cover;border-radius:10px;">
                        <div style="flex:1;">
                            <div class="detail-tag">{item["tag"]}</div>
                            <div class="detail-title" style="font-size:1.15rem;">{item["icon"]} {name}</div>
                            <div class="detail-short">{item["short"]}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Pelajari {name} →", key=f"search_open_{name}", use_container_width=True):
                    st.session_state["selected_topic"] = name
                    st.session_state["page"] = "📚 Jelajah Topik"
                    st.rerun()
        else:
            st.info("Topik belum ditemukan. Coba gunakan kata kunci lain.")


# ============================================================
# JELAJAH TOPIK
# ============================================================

elif page == "📚 Jelajah Topik":

    st.markdown('<div class="page-title">Jelajah Topik</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Pahami inti informasi terlebih dahulu, kemudian lanjutkan ke sumber resmi.</div>', unsafe_allow_html=True)

    names = list(TOPICS.keys())
    default_name = st.session_state.get("selected_topic", names[0])
    if default_name not in names:
        default_name = names[0]

    selected = st.selectbox(
        "Pilih topik",
        names,
        index=names.index(default_name),
    )

    item = TOPICS[selected]
    img = svg_data_uri(item["image"])

    st.markdown(f"""
    <div class="detail-hero">
        <div class="detail-image">
            <img src="{img}">
        </div>
        <div class="detail-content">
            <div class="detail-tag">{item["tag"]}</div>
            <div class="detail-title">{item["icon"]} {selected}</div>
            <div class="detail-short">{item["short"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="small")

    with c1:
        st.markdown(f"""
        <div class="detail-box">
            <h4>📌 Apa itu {selected}?</h4>
            <p>{item["what"]}</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="detail-box">
            <h4>💡 Mengapa topik ini penting?</h4>
            <p>{}</p>
        </div>
        """.format(item["why"]), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sumber informasi resmi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Gunakan sumber resmi Bank Indonesia untuk informasi yang lebih lengkap dan terbaru.</div>', unsafe_allow_html=True)

    b1, b2 = st.columns(2)

    with b1:
        st.link_button("🌐 Situs Resmi Bank Indonesia →", BI_URL, use_container_width=True)

    with b2:
        st.link_button("📚 Buka iBI Library →", LIBRARY_URL, use_container_width=True)


# ============================================================
# PERPUSTAKAAN
# ============================================================

elif page == "📖 Perpustakaan BI":

    st.markdown('<div class="page-title">Perpustakaan Bank Indonesia</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Akses koleksi dan sumber informasi melalui iBI Library.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="detail-hero">
        <div class="detail-content" style="padding:1.7rem;">
            <div class="detail-tag">PERPUSTAKAAN BI</div>
            <div class="detail-title">📚 iBI Library</div>
            <div class="detail-short">
                Gunakan iBI Library untuk menelusuri koleksi dan sumber informasi
                Perpustakaan Bank Indonesia secara lebih lengkap.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("📚 Buka iBI Library →", LIBRARY_URL, use_container_width=True)


# ============================================================
# FEEDBACK
# ============================================================

elif page == "📝 Feedback":

    st.markdown('<div class="page-title">Feedback</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Bantu kami mengetahui pengalaman kamu menggunakan Digital Knowledge Corner.</div>', unsafe_allow_html=True)

    with st.form("feedback_form"):
        kemudahan = st.slider("Kemudahan menggunakan website", 1, 5, 4)
        mencari = st.slider("Kemudahan menemukan informasi", 1, 5, 4)
        memahami = st.slider("Kemudahan memahami informasi", 1, 5, 4)
        manfaat = st.slider("Manfaat informasi", 1, 5, 4)
        tampilan = st.slider("Tampilan website", 1, 5, 4)
        rekomendasi = st.slider("Kesediaan merekomendasikan", 1, 5, 4)
        komentar = st.text_area("Komentar atau saran", placeholder="Tuliskan masukan kamu...")

        submitted = st.form_submit_button("Kirim Feedback", use_container_width=True)

        if submitted:
            save_feedback({
                "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "kemudahan": kemudahan,
                "kemudahan_mencari": mencari,
                "kemudahan_memahami": memahami,
                "manfaat": manfaat,
                "tampilan": tampilan,
                "rekomendasi": rekomendasi,
                "komentar": komentar,
            })
            st.success("Terima kasih. Feedback kamu sudah tersimpan.")


# ============================================================
# TENTANG
# ============================================================

elif page == "ℹ️ Tentang":

    st.markdown('<div class="page-title">Tentang Digital Knowledge Corner</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="detail-box">
        <h4>🎯 Tujuan</h4>
        <p>
        Digital Knowledge Corner dikembangkan sebagai media pendukung diseminasi
        informasi kebanksentralan yang menyajikan informasi secara ringkas,
        visual, dan mudah diakses melalui perangkat digital.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="detail-box">
        <h4>📌 Cara menggunakan</h4>
        <p>
        Pilih topik yang ingin diketahui → baca penjelasan singkat →
        gunakan tautan sumber resmi untuk memperoleh informasi yang lebih lengkap.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="detail-box">
        <h4>ℹ️ Catatan</h4>
        <p>
        Website ini merupakan prototype media diseminasi. Untuk kebijakan,
        statistik, data, dan informasi terbaru, tetap gunakan sumber resmi Bank Indonesia.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    BI Digital Knowledge Corner • Prototype Media Diseminasi Informasi Kebanksentralan
</div>
""", unsafe_allow_html=True)
