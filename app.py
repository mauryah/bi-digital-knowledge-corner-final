import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import re
from urllib.parse import quote

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
USAGE_FILE = DATA_DIR / "usage.csv"

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
.stApp{background:#f5f9fd;}
.main .block-container{max-width:1380px;padding:1rem 2rem 2.5rem;}
section[data-testid="stSidebar"]{background:#fff;border-right:1px solid #e3ebf3;}
.brand{padding:.3rem .2rem 1rem;}
.brand-logo{font-weight:900;color:#07538A;font-size:1.1rem;letter-spacing:-.02em;}
.brand-title{font-size:1.35rem;font-weight:850;line-height:1.12;color:#073F70;margin-top:.35rem;}
.brand-sub{font-size:.78rem;color:#7B8794;margin-top:.35rem;line-height:1.4;}
.sidebar-quote{margin-top:1.1rem;background:#edf6ff;border-radius:16px;padding:1rem;color:#20557A;font-size:.78rem;line-height:1.55;}
.hero{position:relative;overflow:hidden;border-radius:28px;min-height:455px;background:linear-gradient(120deg,#063B67 0%,#075B8E 52%,#1593B7 100%);box-shadow:0 18px 45px rgba(9,74,112,.18);}
.hero-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.97;}
.hero-overlay{position:absolute;inset:0;background:linear-gradient(90deg,rgba(4,51,91,.96) 0%,rgba(5,73,111,.78) 45%,rgba(5,107,146,.12) 82%);}
.hero-content{position:relative;z-index:2;padding:3.1rem 3.2rem;max-width:730px;color:#fff;}
.eyebrow{font-size:.72rem;font-weight:850;letter-spacing:.18em;opacity:.84;margin-bottom:.8rem;}
.hero h1{font-size:clamp(2.4rem,4.6vw,4.35rem);line-height:1.02;letter-spacing:-.045em;margin:0;font-weight:900;}
.hero-tag{font-size:1.28rem;font-weight:800;margin:1rem 0 .5rem;}
.hero-copy{font-size:1rem;line-height:1.65;max-width:680px;color:rgba(255,255,255,.92);}
.search-box{margin-top:1.35rem;background:#fff;border-radius:16px;padding:.42rem;box-shadow:0 10px 30px rgba(0,0,0,.16);}
.search-row{display:flex;align-items:center;gap:.65rem;padding:0 .85rem;}
.search-icon{font-size:1.5rem;color:#0A68A2;}
.search-placeholder{color:#738292;font-size:.92rem;}
.search-hint{font-size:.7rem;color:#9AA6B1;margin-top:.1rem;}
.quick-strip{margin-top:-1.85rem;position:relative;z-index:5;background:rgba(255,255,255,.96);border:1px solid #dce7ef;border-radius:18px;box-shadow:0 12px 32px rgba(17,66,98,.12);padding:.65rem;}
.quick-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.4rem;}
.quick{display:flex;gap:.7rem;align-items:center;padding:.75rem .8rem;}
.quick-icon{font-size:1.55rem;}
.quick b{display:block;color:#123f60;font-size:.8rem;}
.quick span{display:block;color:#7C8995;font-size:.69rem;margin-top:.12rem;}
.section-title{font-size:1.65rem;font-weight:900;color:#073F70;margin:2rem 0 .2rem;}
.section-sub{color:#71808D;font-size:.9rem;margin-bottom:1rem;}
.topic-card{background:#fff;border:1px solid #e0e9f1;border-radius:20px;overflow:hidden;box-shadow:0 6px 20px rgba(18,67,98,.045);height:100%;}
.topic-img{width:100%;height:120px;object-fit:cover;display:block;}
.topic-body{padding:1rem 1rem 1.05rem;}
.topic-body h3{color:#073F70;font-size:1.05rem;margin:0 0 .35rem;font-weight:850;}
.topic-body p{color:#687785;font-size:.82rem;line-height:1.5;min-height:52px;margin:0 0 .8rem;}
.panel{background:#fff;border:1px solid #e0e9f1;border-radius:20px;padding:1.25rem 1.35rem;box-shadow:0 6px 20px rgba(18,67,98,.045);height:100%;}
.panel h3{color:#073F70;margin:.1rem 0 .5rem;font-size:1.1rem;}
.panel p{color:#687785;font-size:.84rem;line-height:1.6;}
.panel-blue{background:linear-gradient(135deg,#e9f5ff,#f8fbff);}
.panel-cyan{background:linear-gradient(135deg,#e8f8fa,#fbffff);}
.panel-purple{background:linear-gradient(135deg,#f1efff,#fcfbff);}
.small-art{width:70px;height:70px;float:right;margin-left:1rem;}
.footer{border-top:1px solid #dfe8ef;margin-top:2.4rem;padding-top:1.2rem;text-align:center;color:#7A8792;font-size:.76rem;line-height:1.6;}
div.stButton>button,div[data-testid="stLinkButton"]>a{border-radius:11px!important;font-weight:750!important;min-height:2.65rem!important;}
@media(max-width:850px){.main .block-container{padding:1rem .8rem 2rem}.hero{min-height:560px}.hero-content{padding:2.1rem 1.35rem}.hero-bg{object-position:65% center;opacity:.55}.hero-overlay{background:linear-gradient(90deg,rgba(4,51,91,.96),rgba(5,73,111,.65))}.quick-strip{margin-top:1rem}.quick-grid{grid-template-columns:repeat(2,1fr)}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA
# ============================================================
TOPICS = {
    "💰 Rupiah":{"title":"Rupiah","short":"Mengenal Rupiah sebagai alat pembayaran dan simbol kedaulatan negara.","img":"rupiah.svg","keywords":["rupiah","uang","cbp","cinta","bangga","paham"]},
    "💳 Sistem Pembayaran":{"title":"Sistem Pembayaran","short":"Mengenal QRIS, BI-FAST, dan perkembangan sistem pembayaran Indonesia.","img":"payment.svg","keywords":["qris","bi-fast","pembayaran","digital","transaksi"]},
    "📈 Stabilitas Ekonomi":{"title":"Stabilitas Ekonomi","short":"Memahami inflasi, kebijakan moneter, dan stabilitas ekonomi.","img":"economy.svg","keywords":["inflasi","moneter","stabilitas","ekonomi","harga"]},
    "🌾 Ketahanan Pangan":{"title":"Ketahanan Pangan","short":"Memahami hubungan pasokan pangan, harga pangan, dan stabilitas ekonomi.","img":"food.svg","keywords":["pangan","gnpip","harga pangan","pasokan","distribusi"]},
    "📊 Data & Publikasi":{"title":"Data & Publikasi","short":"Akses awal menuju statistik, laporan, kajian, dan publikasi BI.","img":"data.svg","keywords":["data","statistik","publikasi","laporan","kajian"]},
    "🏦 Kebanksentralan":{"title":"Kebanksentralan","short":"Mengenal peran, tugas, dan bidang utama Bank Indonesia.","img":"centralbank.svg","keywords":["kebanksentralan","bank indonesia","moneter","makroprudensial"]},
}

def save_row(path,row):
    new=pd.DataFrame([row])
    if path.exists():
        old=pd.read_csv(path)
        new=pd.concat([old,new],ignore_index=True)
    new.to_csv(path,index=False)

def load_csv(path):
    return pd.read_csv(path) if path.exists() else pd.DataFrame()

def log_usage(action,topic="",query=""):
    save_row(USAGE_FILE,{"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"action":action,"topic":topic,"query":query})

def key(text):
    return re.sub(r"[^a-zA-Z0-9]+","_",text).strip("_").lower()

def go(menu,topic=None):
    st.session_state.menu=menu
    if topic: st.session_state.topic=topic
    st.rerun()

# ============================================================
# NAVIGATION
# ============================================================
MENU=["🏠 Beranda","🔎 Cari Informasi","📚 Jelajah Topik","📖 Perpustakaan BI","📝 Feedback","📊 Dashboard Evaluasi","ℹ️ Tentang"]
if "menu" not in st.session_state: st.session_state.menu="🏠 Beranda"
if "topic" not in st.session_state: st.session_state.topic=list(TOPICS)[0]

st.sidebar.markdown("""
<div class="brand">
  <div class="brand-logo">◉ BANK INDONESIA</div>
  <div class="brand-title">BI Digital<br>Knowledge Corner</div>
  <div class="brand-sub">Prototype Digital Knowledge Corner</div>
</div>
""",unsafe_allow_html=True)

st.session_state.menu=st.sidebar.radio("Navigasi",MENU,index=MENU.index(st.session_state.menu))
st.sidebar.markdown("""
<div class="sidebar-quote">
<b>“</b><br>
Media pendukung untuk diseminasi informasi kebanksentralan.
</div>
""",unsafe_allow_html=True)

menu=st.session_state.menu

# ============================================================
# HOME
# ============================================================
if menu=="🏠 Beranda":
    hero_path=(ASSET_DIR/"hero_building.svg").as_posix()
    st.markdown(f"""
    <div class="hero">
      <img class="hero-bg" src="data:image/svg+xml;utf8,{quote(Path(hero_path).read_text(encoding='utf-8'))}">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="eyebrow">DIGITAL KNOWLEDGE CORNER</div>
        <h1>BI Digital<br>Knowledge Corner</h1>
        <div class="hero-tag">Temukan. Pahami. Jelajahi.</div>
        <div class="hero-copy">
          Satu pintu akses untuk mengenal Rupiah, sistem pembayaran,
          stabilitas ekonomi, ketahanan pangan, data dan publikasi,
          serta informasi kebanksentralan.
        </div>
        <div class="search-box">
          <div class="search-row">
            <div class="search-icon">⌕</div>
            <div>
              <div class="search-placeholder">Apa yang ingin kamu cari?</div>
              <div class="search-hint">Contoh: QRIS, inflasi, BI-FAST, Rupiah, kebanksentralan...</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """,unsafe_allow_html=True)

    q=st.text_input("Cari informasi",placeholder="Ketik kata kunci untuk mencari...",label_visibility="collapsed",key="home_q").strip().lower()
    if q:
        results=[]
        for name,d in TOPICS.items():
            if q in (" ".join([name,d["title"],d["short"]]+d["keywords"])).lower():
                results.append(name)
        log_usage("search",query=q)
        if results:
            st.success(f"Ditemukan {len(results)} topik yang relevan.")
            for t in results:
                st.write(f"• **{TOPICS[t]['title']}** — {TOPICS[t]['short']}")
        else:
            st.warning("Belum ditemukan. Coba kata kunci lain.")

    st.markdown("""
    <div class="quick-strip"><div class="quick-grid">
      <div class="quick"><div class="quick-icon">📖</div><div><b>Ringkasan Informasi</b><span>Singkat & terarah</span></div></div>
      <div class="quick"><div class="quick-icon">📄</div><div><b>Sumber Resmi</b><span>Dari Bank Indonesia</span></div></div>
      <div class="quick"><div class="quick-icon">📚</div><div><b>Akses Langsung iBI Library</b><span>Jelajahi koleksi digital</span></div></div>
      <div class="quick"><div class="quick-icon">💡</div><div><b>Mudah Dipahami</b><span>Bahasa sederhana</span></div></div>
    </div></div>
    """,unsafe_allow_html=True)

    st.markdown('<div class="section-title">Jelajahi berdasarkan topik</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Pilih topik yang ingin kamu pelajari dan temukan informasi pentingnya secara ringkas dan terarah.</div>',unsafe_allow_html=True)

    cols=st.columns(3)
    for i,(name,d) in enumerate(TOPICS.items()):
        with cols[i%3]:
            img=(ASSET_DIR/d["img"]).read_text(encoding="utf-8")
            st.markdown(f"""
            <div class="topic-card">
              <img class="topic-img" src="data:image/svg+xml;utf8,{quote(img)}">
              <div class="topic-body">
                <h3>{d["title"]}</h3>
                <p>{d["short"]}</p>
              </div>
            </div>
            """,unsafe_allow_html=True)
            if st.button("Jelajahi →",key="home_"+key(name),use_container_width=True):
                log_usage("open_topic",topic=name); go("📚 Jelajah Topik",name)

    st.markdown("")
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown("""<div class="panel panel-blue"><img class="small-art" src="data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 80 80'%3E%3Ccircle cx='40' cy='40' r='34' fill='%23DDEEFF'/%3E%3Cpath d='M40 20c-13 0-22 8-22 19 0 14 12 19 22 23 10-4 22-9 22-23 0-11-9-19-22-19z' fill='%230B6FB0'/%3E%3Cpath d='M31 39h18M31 47h18' stroke='white' stroke-width='4'/%3E%3C/svg%3E"><h3>💡 Tahukah Kamu?</h3><p>Rupiah bukan hanya alat pembayaran, tetapi juga merupakan simbol kedaulatan negara.</p></div>""",unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="panel panel-cyan"><h3>📚 Ayo Baca Lebih Lanjut</h3><p>Ingin mendalami topik tertentu? Lanjutkan eksplorasi koleksi digital melalui iBI Library.</p></div>""",unsafe_allow_html=True)
        st.link_button("Buka iBI Library →",LIBRARY_URL,use_container_width=True)
    with c3:
        st.markdown("""<div class="panel panel-purple"><h3>📱 Cara Menggunakan</h3><p><b>1.</b> Scan QR Code<br><b>2.</b> Pilih topik<br><b>3.</b> Baca ringkasan<br><b>4.</b> Kunjungi sumber resmi / iBI Library</p></div>""",unsafe_allow_html=True)

# ============================================================
# SEARCH
# ============================================================
elif menu=="🔎 Cari Informasi":
    st.markdown('<div class="section-title">🔎 Cari Informasi</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Temukan topik dengan cepat berdasarkan kata kunci.</div>',unsafe_allow_html=True)
    q=st.text_input("Kata kunci",placeholder="Contoh: QRIS, Rupiah, inflasi, BI-FAST...",label_visibility="collapsed").strip().lower()
    if q:
        results=[]
        for name,d in TOPICS.items():
            if q in (" ".join([name,d["title"],d["short"]]+d["keywords"])).lower(): results.append(name)
        log_usage("search",query=q)
        if results:
            for t in results:
                with st.container(border=True):
                    st.subheader(TOPICS[t]["title"]); st.write(TOPICS[t]["short"])
                    a,b=st.columns(2)
                    with a:
                        if st.button("📖 Lihat topik",key="s_"+key(t),use_container_width=True): go("📚 Jelajah Topik",t)
                    with b: st.link_button("🏦 Sumber resmi BI",BI_URL,use_container_width=True)
        else: st.warning("Belum ditemukan. Coba kata kunci lain.")

# ============================================================
# TOPIC
# ============================================================
elif menu=="📚 Jelajah Topik":
    st.markdown('<div class="section-title">📚 Jelajah Topik</div>',unsafe_allow_html=True)
    names=list(TOPICS)
    st.session_state.topic=st.selectbox("Pilih topik",names,index=names.index(st.session_state.topic))
    t=st.session_state.topic; d=TOPICS[t]
    log_usage("view_topic",topic=t)
    img=(ASSET_DIR/d["img"]).read_text(encoding="utf-8")
    st.markdown(f"""
    <div class="panel panel-blue">
      <img class="small-art" src="data:image/svg+xml;utf8,{quote(img)}">
      <h3>{d["title"]}</h3><p>{d["short"]}</p>
    </div>
    """,unsafe_allow_html=True)
    st.markdown("### 📌 Ringkasan")
    st.write(d["short"])
    st.markdown("### 💡 Mengapa topik ini penting?")
    st.write("Gunakan topik ini sebagai pengantar sebelum membaca sumber resmi dan koleksi yang lebih lengkap.")
    st.markdown("### 🔗 Lanjutkan Eksplorasi")
    a,b=st.columns(2)
    with a: st.link_button("🏦 Sumber Resmi Bank Indonesia",BI_URL,use_container_width=True)
    with b: st.link_button("📚 Buka iBI Library",LIBRARY_URL,use_container_width=True)

# ============================================================
# LIBRARY
# ============================================================
elif menu=="📖 Perpustakaan BI":
    st.markdown('<div class="section-title">📖 Perpustakaan Bank Indonesia</div>',unsafe_allow_html=True)
    st.markdown("""
    <div class="panel panel-cyan">
      <h3>📚 Ayo Baca Lebih Lanjut</h3>
      <p>Digital Knowledge Corner menjadi pintu masuk informasi. Untuk eksplorasi koleksi dan layanan perpustakaan digital, lanjutkan ke iBI Library.</p>
    </div>
    """,unsafe_allow_html=True)
    st.link_button("📚 Buka iBI Library",LIBRARY_URL,use_container_width=True)
    log_usage("open_ibi_library")
    st.markdown("### 🔄 Alur Akses")
    a,b,c=st.columns(3)
    for col,n,title,desc in [(a,"01","Temukan","Pilih topik yang ingin dipelajari."),(b,"02","Pahami","Baca ringkasan secara singkat."),(c,"03","Dalami","Lanjutkan ke iBI Library dan sumber resmi.")]:
        with col: st.markdown(f'<div class="panel"><b style="color:#0B6FB0">{n}</b><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)

# ============================================================
# FEEDBACK
# ============================================================
elif menu=="📝 Feedback":
    st.markdown('<div class="section-title">📝 Feedback Pengguna</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Pendapat pengguna digunakan sebagai bahan evaluasi prototype.</div>',unsafe_allow_html=True)
    with st.form("feedback"):
        role=st.selectbox("Kategori pengguna",["Mahasiswa","Pelajar","Pegawai","Umum","Lainnya"])
        topic=st.selectbox("Topik yang paling menarik",list(TOPICS))
        ease=st.slider("Website mudah digunakan",1,5,4)
        find=st.slider("Informasi mudah ditemukan",1,5,4)
        understand=st.slider("Informasi mudah dipahami",1,5,4)
        useful=st.slider("Website bermanfaat",1,5,4)
        appearance=st.slider("Tampilan mudah dipahami",1,5,4)
        recommend=st.slider("Saya bersedia merekomendasikan website ini",1,5,4)
        comment=st.text_area("Saran atau komentar")
        submit=st.form_submit_button("Kirim Feedback",use_container_width=True)
    if submit:
        save_row(FEEDBACK_FILE,{"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"kategori_pengguna":role,"topik_menarik":topic,"kemudahan":ease,"kemudahan_mencari":find,"kemudahan_memahami":understand,"manfaat":useful,"tampilan":appearance,"rekomendasi":recommend,"komentar":comment})
        st.success("Terima kasih. Feedback berhasil dicatat.")

# ============================================================
# DASHBOARD
# ============================================================
elif menu=="📊 Dashboard Evaluasi":
    st.markdown('<div class="section-title">📊 Dashboard Evaluasi</div>',unsafe_allow_html=True)
    fb=load_csv(FEEDBACK_FILE); us=load_csv(USAGE_FILE)
    if fb.empty:
        st.info("Belum ada data feedback. Lakukan uji coba terlebih dahulu.")
    else:
        cols=["kemudahan","kemudahan_mencari","kemudahan_memahami","manfaat","tampilan","rekomendasi"]
        avg=fb[cols].mean()
        a,b,c,d=st.columns(4)
        a.metric("Responden",len(fb)); b.metric("Kemudahan",f"{avg['kemudahan']:.2f}/5"); c.metric("Manfaat",f"{avg['manfaat']:.2f}/5"); d.metric("Rekomendasi",f"{avg['rekomendasi']:.2f}/5")
        st.bar_chart(avg.rename({"kemudahan":"Kemudahan","kemudahan_mencari":"Pencarian","kemudahan_memahami":"Pemahaman","manfaat":"Manfaat","tampilan":"Tampilan","rekomendasi":"Rekomendasi"}))
        a,b=st.columns(2)
        with a: st.bar_chart(fb["kategori_pengguna"].value_counts())
        with b: st.bar_chart(fb["topik_menarik"].value_counts())
        if not us.empty: st.bar_chart(us["action"].value_counts())
        comments=fb[fb["komentar"].fillna("").astype(str).str.strip()!=""]
        st.subheader("💬 Feedback Pengguna")
        if comments.empty: st.write("Belum ada komentar.")
        else:
            for _,r in comments.iterrows(): st.markdown(f"**{r['kategori_pengguna']}** — {r['komentar']}")
        st.download_button("⬇️ Download Data Feedback",fb.to_csv(index=False).encode("utf-8"),"feedback_digital_knowledge_corner.csv","text/csv",use_container_width=True)
        if not us.empty: st.download_button("⬇️ Download Data Aktivitas",us.to_csv(index=False).encode("utf-8"),"aktivitas_digital_knowledge_corner.csv","text/csv",use_container_width=True)

# ============================================================
# ABOUT
# ============================================================
elif menu=="ℹ️ Tentang":
    st.markdown('<div class="section-title">ℹ️ Tentang Digital Knowledge Corner</div>',unsafe_allow_html=True)
    st.markdown("""
    <div class="panel panel-blue">
      <h3>🎯 Tujuan</h3>
      <p>Membantu pengunjung menemukan informasi kebanksentralan secara lebih mudah, ringkas, dan terarah melalui satu pintu digital.</p>
      <h3>🔄 Konsep</h3>
      <p><b>Koleksi → Kurasi → Akses Digital → Pemahaman → Eksplorasi</b></p>
    </div>
    """,unsafe_allow_html=True)
    st.warning("Website ini merupakan prototype tugas akhir magang dan bukan aplikasi resmi Bank Indonesia. Konten dan tautan perlu diverifikasi oleh unit terkait sebelum digunakan sebagai layanan resmi.")
    a,b=st.columns(2)
    with a: st.link_button("🏦 Bank Indonesia",BI_URL,use_container_width=True)
    with b: st.link_button("📚 iBI Library",LIBRARY_URL,use_container_width=True)

st.markdown("""
<div class="footer">
<b>BI Digital Knowledge Corner</b><br>
Prototype Tugas Akhir Magang — Media Pendukung Diseminasi Informasi Kebanksentralan<br>
Prototype — bukan aplikasi resmi Bank Indonesia
</div>
""",unsafe_allow_html=True)
