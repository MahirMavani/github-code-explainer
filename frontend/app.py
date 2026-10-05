import os
from pathlib import Path
from urllib.parse import urlparse

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="RepoLens AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- UI ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] { font-family: Inter, sans-serif; }

.stApp {
    background:
        radial-gradient(circle at 8% 8%, rgba(139,92,246,.16), transparent 27%),
        radial-gradient(circle at 92% 12%, rgba(6,182,212,.13), transparent 24%),
        radial-gradient(circle at 50% 100%, rgba(99,102,241,.09), transparent 32%),
        #070a12;
}

[data-testid="stHeader"] { background: transparent; }

[data-testid="stSidebar"] {
    background: rgba(7,10,18,.94);
    border-right: 1px solid rgba(148,163,184,.14);
}

.block-container {
    max-width: 1280px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}

#MainMenu, footer { visibility: hidden; }

.hero { padding: 34px 0 18px; }

.eyebrow {
    display: inline-flex;
    padding: 7px 12px;
    border-radius: 999px;
    color: #c4b5fd;
    background: rgba(139,92,246,.10);
    border: 1px solid rgba(139,92,246,.25);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .5px;
}

.hero h1 {
    font-family: "Space Grotesk", sans-serif;
    font-size: clamp(44px, 6vw, 78px);
    line-height: .97;
    letter-spacing: -3px;
    margin: 18px 0;
    background: linear-gradient(90deg, #fff 5%, #ddd6fe 42%, #67e8f9 90%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 800px;
    color: #a8b3c7;
    font-size: 17px;
    line-height: 1.7;
}

.glow-line {
    height: 1px;
    margin: 28px 0;
    background: linear-gradient(90deg, transparent, #8b5cf6, #06b6d4, transparent);
}

.search-card {
    background: linear-gradient(145deg, rgba(18,25,42,.88), rgba(11,16,29,.76));
    border: 1px solid rgba(148,163,184,.16);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 25px 70px rgba(0,0,0,.24);
}

div[data-testid="stTextInput"] input {
    background: rgba(8,12,22,.88) !important;
    border: 1px solid rgba(148,163,184,.20) !important;
    border-radius: 13px !important;
    color: #f8fafc !important;
    height: 52px !important;
    font-size: 15px !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: rgba(139,92,246,.8) !important;
    box-shadow: 0 0 0 2px rgba(139,92,246,.12) !important;
}

.stButton > button {
    width: 100%;
    height: 52px;
    border: 0 !important;
    border-radius: 13px !important;
    background: linear-gradient(100deg, #7c3aed, #8b5cf6 48%, #06b6d4) !important;
    color: white !important;
    font-weight: 800 !important;
    box-shadow: 0 12px 30px rgba(124,58,237,.23);
}

.stButton > button:hover { transform: translateY(-2px); }

.metric-card {
    background: linear-gradient(145deg, rgba(18,25,42,.82), rgba(12,17,30,.72));
    border: 1px solid rgba(148,163,184,.16);
    border-radius: 18px;
    padding: 19px;
    min-height: 116px;
}

.metric-icon { font-size: 18px; margin-bottom: 9px; }

.metric-label {
    color: #8fa0b8;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .8px;
}

.metric-value {
    margin-top: 4px;
    font-family: "Space Grotesk";
    font-size: 25px;
    font-weight: 700;
    color: #fff;
}

.section-title {
    font-family: "Space Grotesk";
    font-size: 25px;
    font-weight: 700;
    margin: 30px 0 14px;
}

.section-subtitle {
    color: #8290a7;
    font-size: 13px;
    margin-top: -7px;
    margin-bottom: 18px;
}

.info-card {
    border: 1px solid rgba(148,163,184,.14);
    background: rgba(15,23,42,.52);
    border-radius: 18px;
    padding: 20px;
    height: 100%;
}

.info-card h4 {
    margin: 0 0 8px;
    color: #f8fafc;
    font-family: "Space Grotesk";
}

.info-card p {
    margin: 0;
    color: #8fa0b8;
    line-height: 1.65;
    font-size: 13px;
}

.repo-pill {
    display: inline-flex;
    padding: 8px 12px;
    border-radius: 999px;
    color: #c4b5fd;
    background: rgba(139,92,246,.09);
    border: 1px solid rgba(139,92,246,.22);
    font-size: 12px;
    font-weight: 700;
}

.arch {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    padding: 24px 12px;
}

.arch-node {
    padding: 13px 17px;
    border-radius: 14px;
    background: linear-gradient(145deg, rgba(30,41,59,.82), rgba(15,23,42,.72));
    border: 1px solid rgba(148,163,184,.16);
    text-align: center;
    min-width: 125px;
}

.arch-node strong {
    display: block;
    font-size: 13px;
    color: #f8fafc;
}

.arch-node span {
    display: block;
    font-size: 10px;
    color: #7f8da5;
    margin-top: 4px;
}

.arch-arrow {
    color: #8b5cf6;
    font-size: 22px;
    font-weight: 800;
}

.file-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 13px 15px;
    margin-bottom: 8px;
    border-radius: 13px;
    background: rgba(15,23,42,.60);
    border: 1px solid rgba(148,163,184,.10);
}

.file-name {
    color: #dbeafe;
    font-family: ui-monospace, monospace;
    font-size: 13px;
}

.file-ext {
    color: #7dd3fc;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
}

.footer {
    text-align: center;
    color: #56647a;
    font-size: 11px;
    padding-top: 30px;
}

.sidebar-logo {
    font-family: "Space Grotesk";
    font-size: 20px;
    font-weight: 800;
}

.sidebar-caption {
    color: #77869e;
    font-size: 12px;
    line-height: 1.5;
    margin-bottom: 22px;
}
</style>
""",
    unsafe_allow_html=True,
)


def repo_name(url: str) -> str:
    parts = [p for p in urlparse(url.strip()).path.strip("/").split("/") if p]
    return parts[1].replace(".git", "") if len(parts) >= 2 else "Repository"


def file_ext(name: str) -> str:
    suffix = Path(name).suffix.lower()
    return suffix[1:] if suffix else "file"


def valid_repo_url(url: str) -> bool:
    parsed = urlparse(url.strip())
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    return (
        parsed.netloc.lower() in {"github.com", "www.github.com"}
        and len(parts) >= 2
    )


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        '<div class="sidebar-logo">◈ RepoLens AI</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sidebar-caption">Understand unfamiliar GitHub repositories with a locally running LLM.</div>',
        unsafe_allow_html=True,
    )

    st.success("Local AI pipeline")

    st.markdown("---")
    st.markdown("### Workflow")
    for item in [
        "01  Paste URL",
        "02  Clone repository",
        "03  Extract code",
        "04  Ask Qwen",
        "05  Explain",
    ]:
        st.caption(item)

    st.markdown("---")
    st.markdown("### Stack")
    st.caption("Python • FastAPI • Streamlit")
    st.caption("GitPython • Ollama • Qwen 2.5 3B")

    st.markdown("---")
    st.caption("Runs locally. No cloud LLM API required.")


# ---------- Hero ----------
st.markdown(
    """
<div class="hero">
    <div class="eyebrow">✦ Local GenAI • Developer Tool</div>
    <h1>Understand any<br>repository faster.</h1>
    <p>
        RepoLens AI reads a public GitHub repository, identifies important source
        files, and uses a local LLM to turn unfamiliar code into a clear,
        beginner-friendly explanation.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)


# ---------- Search ----------
st.markdown('<div class="search-card">', unsafe_allow_html=True)

github_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/username/repository",
)

st.caption("Tip: use the repository URL, not a /blob/main/file.py URL.")

if st.button("✦  Analyze Repository", type="primary"):
    if not github_url.strip():
        st.error("Please enter a GitHub repository URL.")

    elif not valid_repo_url(github_url):
        st.error("Please enter a valid public GitHub repository URL.")

    else:
        with st.spinner("Cloning • extracting • analyzing with local Qwen..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/explain",
                    json={"github_url": github_url.strip()},
                    timeout=660,
                )

                if response.ok:
                    st.session_state["analysis"] = response.json()
                    st.session_state["analyzed_url"] = github_url.strip()
                    st.rerun()

                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text

                    st.error(f"Backend error: {detail}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "FastAPI is not running. Start it with: "
                    "uvicorn backend.main:app --reload"
                )

            except requests.exceptions.Timeout:
                st.error("The analysis timed out. Try a smaller repository.")

            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")

st.markdown("</div>", unsafe_allow_html=True)


# ---------- Results ----------
result = st.session_state.get("analysis")

if result:
    analyzed_url = st.session_state.get(
        "analyzed_url",
        result.get("github_url", ""),
    )

    files = result.get("files_analyzed", [])
    explanation = result.get("explanation", "")

    languages = sorted(
        {
            file_ext(f)
            for f in files
            if file_ext(f) not in {"file", "md", "txt"}
        }
    )

    st.markdown(
        '<div class="section-title">Repository Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Local AI analysis completed successfully.</div>',
        unsafe_allow_html=True,
    )

    metric_cols = st.columns(4)

    metrics = [
        ("◉", "Repository", repo_name(analyzed_url)),
        ("⌘", "Files analyzed", str(len(files))),
        ("◇", "File types", str(len(languages))),
        ("✦", "AI engine", "Qwen"),
    ]

    for col, (icon, label, value) in zip(metric_cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        f"""
        <div style="margin-top:18px;">
            <span class="repo-pill">● Analyzed locally</span>
            <span style="color:#64748b;font-size:12px;">{analyzed_url}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="section-title">Analysis Pipeline</div>
<div class="section-subtitle">
    How your repository moves through the GenAI system.
</div>
<div class="info-card">
<div class="arch">
    <div class="arch-node"><strong>GitHub</strong><span>Repository</span></div>
    <div class="arch-arrow">→</div>
    <div class="arch-node"><strong>GitPython</strong><span>Clone & scan</span></div>
    <div class="arch-arrow">→</div>
    <div class="arch-node"><strong>Code Processor</strong><span>Relevant files</span></div>
    <div class="arch-arrow">→</div>
    <div class="arch-node"><strong>Qwen 2.5</strong><span>Local LLM</span></div>
    <div class="arch-arrow">→</div>
    <div class="arch-node"><strong>Explanation</strong><span>Streamlit UI</span></div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    tab_ai, tab_files, tab_system = st.tabs(
        ["✦ AI Explanation", "⌘ Files Analyzed", "◎ System"]
    )

    with tab_ai:
        st.markdown(
            '<div class="section-title">AI-Generated Explanation</div>',
            unsafe_allow_html=True,
        )
        st.markdown(explanation)

    with tab_files:
        st.markdown(
            '<div class="section-title">Repository File Map</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "Files selected by the repository processor and provided to the local LLM."
        )

        if files:
            left, right = st.columns(2)

            for index, name in enumerate(files):
                target = left if index % 2 == 0 else right

                with target:
                    st.markdown(
                        f"""
                        <div class="file-item">
                            <span class="file-name">⌁ {name}</span>
                            <span class="file-ext">{file_ext(name)}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            st.info("No file list was returned by the backend.")

    with tab_system:
        a, b, c = st.columns(3)

        cards = [
            (
                "Local inference",
                "Qwen runs through Ollama on your own machine.",
            ),
            (
                "Repository processing",
                "Generated folders and tests are filtered before analysis.",
            ),
            (
                "Backend architecture",
                "FastAPI connects the UI, repository processor, and local LLM.",
            ),
        ]

        for col, (title, body) in zip((a, b, c), cards):
            with col:
                st.markdown(
                    f"""
                    <div class="info-card">
                        <h4>{title}</h4>
                        <p>{body}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

else:
    st.markdown(
        '<div class="section-title">Built for understanding code</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">From a GitHub URL to a simple explanation in one workflow.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    cards = [
        (
            "⌘ Repository Intelligence",
            "Clone a public repository and identify useful source files automatically.",
        ),
        (
            "✦ Local AI Analysis",
            "Use Qwen through Ollama to turn code into a beginner-friendly explanation.",
        ),
        (
            "↗ Developer Workflow",
            "Understand architecture, technologies, important files, and application flow faster.",
        ),
    ]

    for col, (title, body) in zip((c1, c2, c3), cards):
        with col:
            st.markdown(
                f"""
                <div class="info-card">
                    <h4>{title}</h4>
                    <p>{body}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


st.markdown(
    '<div class="footer">RepoLens AI · Local GenAI · FastAPI · Streamlit · GitPython · Ollama · Qwen</div>',
    unsafe_allow_html=True,
)
