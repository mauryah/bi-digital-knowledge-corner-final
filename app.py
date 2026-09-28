import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

# ============================================================
# BI DIGITAL KNOWLEDGE CORNER - CLEAN VERSION
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
        "short": "Mengenal Rupiah sebagai alat pembayaran dan simbol kedaulatan negara.",
        "what": "Rupiah adalah alat pembayaran yang sah di wilayah Negara Kesatuan Republik Indonesia. Selain digunakan dalam transaksi sehari-hari, Rupiah juga menjadi simbol kedaulatan negara.",
        "why": "Memahami Rupiah membantu masyarakat mengenali fungsi uang dan memahami pentingnya menggunakan serta memperlakukan Rupiah dengan baik.",
        "source": "Informasi Rupiah dan Cinta, Bangga, Paham Rupiah tersedia melalui kanal resmi Bank Indonesia.",
    },
    "Sistem Pembayaran": {
        "icon": "💳",
        "image": "payment.svg",
        "short": "Mengenal perkembangan sistem pembayaran dan transaksi digital di Indonesia.",
        "what": "Sistem pembayaran mencakup berbagai mekanisme yang digunakan untuk memindahkan dana dalam kegiatan ekonomi, baik secara tunai maupun nontunai.",
        "why": "Memahami sistem pembayaran membantu masyarakat mengenali cara transaksi yang tersedia serta perkembangan pembayaran digital di Indonesia.",
        "source": "Informasi sistem pembayaran dan kebijakan terkait tersedia melalui kanal resmi Bank Indonesia.",
    },
    "Stabilitas Ekonomi": {
        "icon": "📈",
        "image": "economy.svg",
        "short": "Memahami inflasi, kebijakan moneter, dan upaya menjaga stabilitas ekonomi.",
        "what": "Stabilitas ekonomi berkaitan dengan kondisi perekonomian yang tetap terjaga, termasuk perkembangan harga, nilai Rupiah, dan kondisi ekonomi secara umum.",
        "why": "Pemahaman mengenai stabilitas ekonomi membantu masyarakat melihat hubungan antara perubahan harga, kebijakan moneter, dan aktivitas ekonomi sehari-hari.",
        "source": "Informasi ekonomi dan kebijakan moneter dapat dipelajari melalui publikasi resmi Bank Indonesia.",
    },
    "Ketahanan Pangan": {
        "icon": "🌾",
        "image": "food.svg",
        "short": "Mengenal keterkaitan pangan, harga, dan kestabilan ekonomi.",
        "what": "Ketahanan pangan berkaitan dengan ketersediaan, keterjangkauan, dan keberlanjutan pangan. Perkembangan harga pangan juga dapat memengaruhi kondisi inflasi.",
        "why": "Memahami ketahanan pangan membantu masyarakat melihat hubungan antara produksi, distribusi, harga pangan, dan stabilitas ekonomi.",
        "source": "Informasi mengenai inflasi pangan dan sinergi pengendalian inflasi tersedia melalui kanal resmi Bank Indonesia.",
    },
    "Data & Publikasi": {
        "icon": "📊",
        "image": "data.svg",
        "short": "Menemukan data, laporan, dan publikasi ekonomi dari Bank Indonesia.",
        "what": "Data dan publikasi menyediakan informasi ekonomi dan keuangan yang dapat digunakan untuk memahami perkembangan perekonomian Indonesia.",
        "why": "Data membantu masyarakat, mahasiswa, peneliti, dan pemangku kepentingan memperoleh informasi yang lebih terukur dan dapat ditelusuri.",
        "source": "Data dan publikasi resmi dapat diakses melalui situs Bank Indonesia dan koleksi Perpustakaan BI.",
    },
    "Kebanksentralan": {
        "icon": "🏦",
        "image": "centralbank.svg",
        "short": "Mengenal peran dan fungsi Bank Indonesia sebagai bank sentral.",
        "what": "Bank Indonesia merupakan bank sentral Republik Indonesia yang memiliki peran dalam menjaga stabilitas nilai Rupiah serta mendukung stabilitas sistem keuangan dan sistem pembayaran sesuai mandatnya.",
        "why": "Pemahaman kebanksentralan membantu masyarakat mengetahui mengapa kebijakan Bank Indonesia dapat berkaitan dengan kehidupan ekonomi sehari-hari.",
        "source": "Informasi mengenai tugas, kebijakan, dan fungsi Bank Indonesia tersedia pada situs resmi Bank Indonesia.",
    },
}


# ============================================================
# HELPERS
# ============================================================

def asset_path(filename):
    """Mencari aset baik di folder assets maupun root repository."""
    p1 = ASSET_DIR / filename
    p2 = BASE_DIR / filename
    if p1.exists():
        return p1
    return p2


def svg_data_uri(filename):
    path = asset_path(filename)
    if not path.exists():
        return ""
    return "data:image/svg+xml;utf8," + quote(
        path.read_text(encoding="utf-8")
    )


def save_feedback(row):
    df_new = pd.DataFrame([row])
    if FEEDBACK_FILE.exists():
        df_old = pd.read_csv(FEEDBACK_FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_csv(FEEDBACK_FILE, index=False)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root{
    --bi-blue:#005596;
    --bi-dark:#073B68;
    --bi-light:#EAF4FB;
    --bi-red:#E31E24;
    --text:#1E293B;
    --muted:#64748B;
}

html, body, [class*="css"]{
    font-family:'Inter', sans-serif;
}

.stApp{
    background:#F5F9FC;
}

.main .block-container{
    max-width:1380px;
    padding:1.5rem 2.5rem 3rem;
}

/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#063D6B 0%,#075A8E 100%);
    border-right:0;
}

section[data-testid="stSidebar"] > div{
    padding:1.4rem 1rem;
}

.sidebar-brand{
    padding:.3rem .5rem 1.6rem;
    color:white;
}

.sidebar-logo{
    font-size:1rem;
    font-weight:800;
    letter-spacing:.02em;
    margin-bottom:.7rem;
}

.sidebar-title{
    font-size:1.45rem;
    line-height:1.1;
    font-weight:900;
}

.sidebar-sub{
    color:rgba(255,255,255,.72);
    font-size:.78rem;
    margin-top:.45rem;
    line-height:1.5;
}

.sidebar-label{
    color:rgba(255,255,255,.55);
    font-size:.68rem;
    font-weight:800;
    letter-spacing:.12em;
    margin:.8rem .5rem .45rem;
}

section[data-testid="stSidebar"] div[role="radiogroup"]{
    gap:.28rem;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label{
    border-radius:11px;
    padding:.48rem .55rem;
    color:rgba(255,255,255,.82);
    transition:.2s;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
    background:rgba(255,255,255,.10);
    color:white;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"]{
    background:white;
    color:#07538A;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label p{
    font-size:.88rem;
}

.sidebar-note{
    margin-top:2rem;
    padding:1rem;
    border-radius:15px;
    background:rgba(255,255,255,.10);
    border:1px solid rgba(255,255,255,.12);
    color:rgba(255,255,255,.82);
    font-size:.75rem;
    line-height:1.55;
}

/* ---------------- HERO ---------------- */

.hero{
    position:relative;
    overflow:hidden;
    min-height:460px;
    border-radius:28px;
    background:linear-gradient(120deg,#043B67,#0875A8);
    box-shadow:0 18px 45px rgba(7,70,110,.18);
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
        rgba(3,42,73,.97) 0%,
        rgba(4,61,96,.87) 45%,
        rgba(4,82,119,.20) 82%);
}

.hero-content{
    position:relative;
    z-index:2;
    padding:3.4rem 3.5rem;
    max-width:730px;
    color:white;
}

.eyebrow{
    font-size:.72rem;
    font-weight:800;
    letter-spacing:.18em;
    opacity:.78;
    margin-bottom:.8rem;
}

.hero h1{
    font-size:clamp(2.5rem,4.7vw,4.35rem);
    line-height:1.02;
    letter-spacing:-.045em;
    margin:0;
    font-weight:900;
}

.hero-copy{
    font-size:1rem;
    line-height:1.65;
    color:rgba(255,255,255,.90);
    margin-top:1rem;
    max-width:620px;
}

.hero-badge{
    display:inline-block;
    margin-top:1.3rem;
    padding:.55rem .85rem;
    border-radius:999px;
    background:rgba(255,255,255,.12);
    border:1px solid rgba(255,255,255,.20);
    font-size:.75rem;
}

/* ---------------- SECTION ---------------- */

.section-title{
    font-size:2rem;
    font-weight:900;
    color:#123F67;
    letter-spacing:-.03em;
    margin:2.7rem 0 .3rem;
}

.section-sub{
    color:var(--muted);
    margin-bottom:1.3rem;
}

/* ---------------- TOPIC CARD ---------------- */

.topic-card{
    background:white;
    border:1px solid #DFEAF2;
    border-radius:22px;
    overflow:hidden;
    height:100%;
    box-shadow:0 8px 25px rgba(16,63,92,.07);
    transition:.2s;
}

.topic-card:hover{
    transform:translateY(-3px);
    box-shadow:0 15px 35px rgba(16,63,92,.12);
}

.topic-image{
    height:185px;
    background:#EAF4FB;
    overflow:hidden;
}

.topic-image img{
    width:100%;
    height:100%;
    object-fit:cover;
}

.topic-body{
    padding:1.15rem 1.2rem 1.3rem;
}

.topic-name{
    font-size:1.15rem;
    font-weight:850;
    color:#104D7D;
}

.topic-text{
    font-size:.83rem;
    line-height:1.6;
    color:#66788A;
    margin-top:.45rem;
}

/* ---------------- DETAIL ---------------- */

.detail-header{
    background:linear-gradient(135deg,#EAF5FC,#F8FBFE);
    border:1px solid #D7E6F0;
    border-radius:25px;
    padding:1.6rem;
    margin-bottom:1.4rem;
}

.detail-image{
    width:100%;
    height:290px;
    object-fit:cover;
    border-radius:19px;
    background:#EAF4FB;
}

.detail-kicker{
    color:#0A69A2;
    font-weight:800;
    font-size:.78rem;
    letter-spacing:.08em;
    text-transform:uppercase;
}

.detail-title{
    font-size:2.25rem;
    line-height:1.1;
    font-weight:900;
    color:#0B4775;
    margin:.35rem 0 .7rem;
}

.detail-short{
    color:#64788A;
    font-size:1rem;
    line-height:1.65;
}

.info-box{
    background:white;
    border:1px solid #DFEAF2;
    border-radius:19px;
    padding:1.35rem 1.45rem;
    height:100%;
    box-shadow:0 7px 20px rgba(16,63,92,.05);
}

.info-title{
    font-size:1.15rem;
    font-weight:850;
    color:#104D7D;
    margin-bottom:.5rem;
}

.info-text{
    color:#526477;
    line-height:1.7;
    font-size:.92rem;
}

/* ---------------- SMALL CARDS ---------------- */

.simple-card{
    background:white;
    border:1px solid #DFEAF2;
    border-radius:20px;
    padding:1.4rem;
    box-shadow:0 7px 20px rgba(16,63,92,.05);
}

.footer{
    margin-top:3rem;
    padding-top:1.2rem;
    border-top:1px solid #DDE7EF;
    color:#81909D;
    font-size:.75rem;
    text-align:center;
}

div.stButton > button{
    border-radius:10px;
    font-weight:700;
}

@media (max-width: 800px){
    .main .block-container{
        padding:1rem;
    }
    .hero{
        min-height:410px;
    }
    .hero-content{
        padding:2rem;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">◎ BANK INDONESIA</div>
            <div class="sidebar-title">Digital<br>Knowledge Corner</div>
            <div class="sidebar-sub">Media informasi kebanksentralan yang ringkas dan mudah dipahami.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-label">MENU UTAMA</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigasi",
        [
            "🏠 Beranda",
            "📚 Jelajah Topik",
            "📖 Perpustakaan BI",
            "📝 Feedback",
            "ℹ️ Tentang",
        ],
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="sidebar-note">
        <b>Knowledge Corner</b><br>
        Pintu masuk singkat untuk mengenal informasi kebanksentralan sebelum membaca sumber resmi yang lebih lengkap.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# BERANDA
# ============================================================

if page == "🏠 Beranda":

    hero_img = svg_data_uri("hero_building.svg")

    st.markdown(
        f"""
        <div class="hero">
            <img class="hero-bg" src="{hero_img}">
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="eyebrow">BANK INDONESIA • DIGITAL KNOWLEDGE CORNER</div>
                <h1>Kenali Bank Indonesia dengan lebih sederhana.</h1>
                <div class="hero-copy">
                    Temukan informasi singkat mengenai Rupiah, sistem pembayaran,
                    stabilitas ekonomi, ketahanan pangan, data, dan kebanksentralan.
                </div>
                <div class="hero-badge">Informasi ringkas • Sumber resmi • Mudah dijelajahi</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Jelajahi Informasi</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Pilih topik yang ingin kamu ketahui.</div>',
        unsafe_allow_html=True,
    )

    names = list(TOPICS.keys())

    for row_start in range(0, len(names), 3):
        cols = st.columns(3, gap="large")

        for col, name in zip(cols, names[row_start:row_start + 3]):
            topic = TOPICS[name]
            img = svg_data_uri(topic["image"])

            with col:
                st.markdown(
                    f"""
                    <div class="topic-card">
                        <div class="topic-image">
                            <img src="{img}">
                        </div>
                        <div class="topic-body">
                            <div class="topic-name">{topic["icon"]} {name}</div>
                            <div class="topic-text">{topic["short"]}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    f"Pelajari {name} →",
                    key=f"home_{name}",
                    use_container_width=True,
                ):
                    st.session_state["selected_topic"] = name
                    st.session_state["page_from_topic"] = True
                    st.rerun()

    st.markdown('<div class="section-title">Butuh informasi lebih lengkap?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown(
            """
            <div class="simple-card">
                <div class="info-title">📖 Perpustakaan Bank Indonesia</div>
                <div class="info-text">
                    Lanjutkan membaca melalui koleksi digital iBI Library dan sumber
                    informasi resmi Bank Indonesia.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.link_button("Buka iBI Library →", LIBRARY_URL, use_container_width=True)

# ============================================================
# JELAJAH TOPIK
# ============================================================

elif page == "📚 Jelajah Topik":

    st.markdown('<div class="section-title">Jelajah Topik</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Pilih satu topik untuk mendapatkan penjelasan singkat.</div>',
        unsafe_allow_html=True,
    )

    default_topic = st.session_state.get("selected_topic", "Rupiah")
    if default_topic not in TOPICS:
        default_topic = "Rupiah"

    selected = st.selectbox(
        "Pilih topik",
        list(TOPICS.keys()),
        index=list(TOPICS.keys()).index(default_topic),
        label_visibility="collapsed",
    )

    topic = TOPICS[selected]
    img = svg_data_uri(topic["image"])

    st.markdown(
        f"""
        <div class="detail-header">
            <div class="detail-kicker">TOPIK KEBANKSENTRALAN</div>
            <div class="detail-title">{topic["icon"]} {selected}</div>
            <div class="detail-short">{topic["short"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_img, col_text = st.columns([1.05, 1], gap="large")

    with col_img:
        st.markdown(
            f'<img class="detail-image" src="{img}">',
            unsafe_allow_html=True,
        )

    with col_text:
        st.markdown(
            f"""
            <div class="info-box">
                <div class="info-title">Apa itu {selected}?</div>
                <div class="info-text">{topic["what"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            f"""
            <div class="info-box">
                <div class="info-title">💡 Mengapa topik ini penting?</div>
                <div class="info-text">{topic["why"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="info-box">
                <div class="info-title">📚 Sumber informasi</div>
                <div class="info-text">{topic["source"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.link_button("🌐 Buka Situs Bank Indonesia", BI_URL, use_container_width=True)
    with c2:
        st.link_button("📖 Buka iBI Library", LIBRARY_URL, use_container_width=True)


# ============================================================
# PERPUSTAKAAN
# ============================================================

elif page == "📖 Perpustakaan BI":

    st.markdown('<div class="section-title">Perpustakaan Bank Indonesia</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Lanjutkan pencarian informasi melalui iBI Library.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="simple-card">
            <div class="info-title">📚 iBI Library</div>
            <div class="info-text">
                iBI Library merupakan layanan perpustakaan digital Bank Indonesia
                yang dapat digunakan untuk melanjutkan eksplorasi koleksi dan
                informasi secara lebih lengkap.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("Buka iBI Library →", LIBRARY_URL, use_container_width=True)


# ============================================================
# FEEDBACK
# ============================================================

elif page == "📝 Feedback":

    st.markdown('<div class="section-title">Feedback Pengunjung</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Masukan singkat untuk membantu pengembangan Digital Knowledge Corner.</div>',
        unsafe_allow_html=True,
    )

    with st.form("feedback_form"):
        col1, col2 = st.columns(2)

        with col1:
            kemudahan = st.slider("Kemudahan menggunakan website", 1, 5, 4)
            mencari = st.slider("Kemudahan menemukan informasi", 1, 5, 4)
            memahami = st.slider("Kemudahan memahami isi", 1, 5, 4)

        with col2:
            manfaat = st.slider("Manfaat informasi", 1, 5, 4)
            tampilan = st.slider("Tampilan website", 1, 5, 4)
            rekomendasi = st.slider("Kesediaan merekomendasikan", 1, 5, 4)

        komentar = st.text_area("Komentar atau saran", placeholder="Tulis masukan kamu di sini...")
        submitted = st.form_submit_button("Kirim Feedback", use_container_width=True)

        if submitted:
            save_feedback(
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "kemudahan": kemudahan,
                    "kemudahan_mencari": mencari,
                    "kemudahan_memahami": memahami,
                    "manfaat": manfaat,
                    "tampilan": tampilan,
                    "rekomendasi": rekomendasi,
                    "komentar": komentar,
                }
            )
            st.success("Terima kasih. Feedback berhasil dicatat.")


# ============================================================
# TENTANG
# ============================================================

elif page == "ℹ️ Tentang":

    st.markdown('<div class="section-title">Tentang Digital Knowledge Corner</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="simple-card">
            <div class="info-title">Apa tujuan website ini?</div>
            <div class="info-text">
                Digital Knowledge Corner dirancang sebagai media pendukung diseminasi
                informasi kebanksentralan di Perpustakaan Bank Indonesia.
                Website ini menyajikan pengantar informasi secara ringkas agar
                pengunjung dapat memahami topik terlebih dahulu sebelum melanjutkan
                ke sumber resmi dan koleksi yang lebih lengkap.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="simple-card">
            <div class="info-title">Catatan</div>
            <div class="info-text">
                Website ini merupakan prototype pengembangan untuk kebutuhan
                diseminasi informasi. Informasi yang bersifat kebijakan,
                statistik, atau data terbaru tetap perlu merujuk pada publikasi
                resmi Bank Indonesia.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="footer">
        BI Digital Knowledge Corner • Prototype Media Diseminasi Informasi Kebanksentralan
    </div>
    """,
    unsafe_allow_html=True,
)
