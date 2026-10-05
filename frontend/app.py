import sys
from pathlib import Path
from urllib.parse import urlparse

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import streamlit as st

from backend.repository import (
    clone_repository,
    cleanup_repository
)

from backend.code_processor import (
    build_repository_context
)

from backend.llm import (
    explain_repository
)

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RepoLens AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800'
    '&family=Space+Grotesk:wght@500;600;700&display=swap'
);

html,
body,
[class*="css"] {
    font-family: Inter, sans-serif;
}

.stApp {

    background:
        radial-gradient(
            circle at 8% 8%,
            rgba(139,92,246,.16),
            transparent 27%
        ),

        radial-gradient(
            circle at 92% 12%,
            rgba(6,182,212,.13),
            transparent 24%
        ),

        radial-gradient(
            circle at 50% 100%,
            rgba(99,102,241,.09),
            transparent 32%
        ),

        #070a12;
}


/* Header */

[data-testid="stHeader"] {
    background: transparent;
}


/* Sidebar */

[data-testid="stSidebar"] {

    background: rgba(7,10,18,.94);

    border-right:
        1px solid rgba(148,163,184,.14);
}


/* Main container */

.block-container {

    max-width: 1280px;

    padding-top: 2.2rem;

    padding-bottom: 4rem;
}


/* Hide Streamlit branding */

#MainMenu,
footer {

    visibility: hidden;
}


/* Hero */

.hero {

    padding: 34px 0 18px;
}


.eyebrow {

    display: inline-flex;

    padding: 7px 12px;

    border-radius: 999px;

    color: #c4b5fd;

    background:
        rgba(139,92,246,.10);

    border:
        1px solid rgba(139,92,246,.25);

    font-size: 12px;

    font-weight: 800;

    letter-spacing: .5px;
}


.hero h1 {

    font-family:
        "Space Grotesk",
        sans-serif;

    font-size:
        clamp(44px, 6vw, 78px);

    line-height: .97;

    letter-spacing: -3px;

    margin: 18px 0;

    background:
        linear-gradient(
            90deg,
            #fff 5%,
            #ddd6fe 42%,
            #67e8f9 90%
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}


.hero p {

    max-width: 800px;

    color: #a8b3c7;

    font-size: 17px;

    line-height: 1.7;
}


/* Gradient divider */

.glow-line {

    height: 1px;

    margin: 28px 0;

    background:
        linear-gradient(
            90deg,
            transparent,
            #8b5cf6,
            #06b6d4,
            transparent
        );
}


/* Search */

.search-card {

    background:
        linear-gradient(
            145deg,
            rgba(18,25,42,.88),
            rgba(11,16,29,.76)
        );

    border:
        1px solid rgba(148,163,184,.16);

    border-radius: 22px;

    padding: 22px;

    box-shadow:
        0 25px 70px rgba(0,0,0,.24);
}


/* Input */

div[data-testid="stTextInput"] input {

    background:
        rgba(8,12,22,.88) !important;

    border:
        1px solid rgba(148,163,184,.20)
        !important;

    border-radius:
        13px !important;

    color:
        #f8fafc !important;

    height:
        52px !important;

    font-size:
        15px !important;
}


div[data-testid="stTextInput"] input:focus {

    border-color:
        rgba(139,92,246,.8) !important;

    box-shadow:
        0 0 0 2px
        rgba(139,92,246,.12)
        !important;
}


/* Buttons */

.stButton > button {

    width: 100%;

    height: 52px;

    border: 0 !important;

    border-radius:
        13px !important;

    background:
        linear-gradient(
            100deg,
            #7c3aed,
            #8b5cf6 48%,
            #06b6d4
        ) !important;

    color:
        white !important;

    font-weight:
        800 !important;

    box-shadow:
        0 12px 30px
        rgba(124,58,237,.23);
}


.stButton > button:hover {

    transform:
        translateY(-2px);
}


/* Metrics */

.metric-card {

    background:
        linear-gradient(
            145deg,
            rgba(18,25,42,.82),
            rgba(12,17,30,.72)
        );

    border:
        1px solid rgba(148,163,184,.16);

    border-radius:
        18px;

    padding:
        19px;

    min-height:
        116px;
}


.metric-icon {

    font-size:
        18px;

    margin-bottom:
        9px;
}


.metric-label {

    color:
        #8fa0b8;

    font-size:
        12px;

    font-weight:
        700;

    text-transform:
        uppercase;

    letter-spacing:
        .8px;
}


.metric-value {

    margin-top:
        4px;

    font-family:
        "Space Grotesk";

    font-size:
        25px;

    font-weight:
        700;

    color:
        #fff;
}


/* Sections */

.section-title {

    font-family:
        "Space Grotesk";

    font-size:
        25px;

    font-weight:
        700;

    margin:
        30px 0 14px;
}


.section-subtitle {

    color:
        #8290a7;

    font-size:
        13px;

    margin-top:
        -7px;

    margin-bottom:
        18px;
}


/* Cards */

.info-card {

    border:
        1px solid rgba(148,163,184,.14);

    background:
        rgba(15,23,42,.52);

    border-radius:
        18px;

    padding:
        20px;

    height:
        100%;
}


.info-card h4 {

    margin:
        0 0 8px;

    color:
        #f8fafc;

    font-family:
        "Space Grotesk";
}


.info-card p {

    margin:
        0;

    color:
        #8fa0b8;

    line-height:
        1.65;

    font-size:
        13px;
}


/* Repository pill */

.repo-pill {

    display:
        inline-flex;

    padding:
        8px 12px;

    border-radius:
        999px;

    color:
        #c4b5fd;

    background:
        rgba(139,92,246,.09);

    border:
        1px solid rgba(139,92,246,.22);

    font-size:
        12px;

    font-weight:
        700;
}


/* Architecture */

.arch {

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    gap:
        10px;

    flex-wrap:
        wrap;

    padding:
        24px 12px;
}


.arch-node {

    padding:
        13px 17px;

    border-radius:
        14px;

    background:
        linear-gradient(
            145deg,
            rgba(30,41,59,.82),
            rgba(15,23,42,.72)
        );

    border:
        1px solid rgba(148,163,184,.16);

    text-align:
        center;

    min-width:
        125px;
}


.arch-node strong {

    display:
        block;

    font-size:
        13px;

    color:
        #f8fafc;
}


.arch-node span {

    display:
        block;

    font-size:
        10px;

    color:
        #7f8da5;

    margin-top:
        4px;
}


.arch-arrow {

    color:
        #8b5cf6;

    font-size:
        22px;

    font-weight:
        800;
}


/* File list */

.file-item {

    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;

    padding:
        13px 15px;

    margin-bottom:
        8px;

    border-radius:
        13px;

    background:
        rgba(15,23,42,.60);

    border:
        1px solid rgba(148,163,184,.10);
}


.file-name {

    color:
        #dbeafe;

    font-family:
        ui-monospace,
        monospace;

    font-size:
        13px;
}


.file-ext {

    color:
        #7dd3fc;

    font-size:
        11px;

    font-weight:
        700;

    text-transform:
        uppercase;
}


/* Sidebar */

.sidebar-logo {

    font-family:
        "Space Grotesk";

    font-size:
        20px;

    font-weight:
        800;
}


.sidebar-caption {

    color:
        #77869e;

    font-size:
        12px;

    line-height:
        1.5;

    margin-bottom:
        22px;
}


/* Footer */

.footer {

    text-align:
        center;

    color:
        #56647a;

    font-size:
        11px;

    padding-top:
        30px;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def repo_name(url: str) -> str:

    parts = [
        p
        for p in urlparse(
            url.strip()
        ).path.strip("/").split("/")
        if p
    ]

    if len(parts) >= 2:

        return parts[1].replace(
            ".git",
            ""
        )

    return "Repository"


def file_ext(name: str) -> str:

    suffix = Path(name).suffix.lower()

    return (
        suffix[1:]
        if suffix
        else "file"
    )


def valid_repo_url(url: str) -> bool:

    parsed = urlparse(
        url.strip()
    )

    parts = [
        p
        for p in parsed.path.strip("/").split("/")
        if p
    ]

    return (
        parsed.netloc.lower()
        in {
            "github.com",
            "www.github.com"
        }
        and len(parts) >= 2
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">'
        '◈ RepoLens AI'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-caption">'
        'Understand unfamiliar GitHub repositories '
        'with an AI-powered Qwen language model.'
        '</div>',
        unsafe_allow_html=True
    )

    st.success(
        "Qwen AI pipeline"
    )

    st.markdown("---")

    st.markdown(
        "### Workflow"
    )

    workflow_items = [
        "01  Paste URL",
        "02  Clone repository",
        "03  Extract code",
        "04  Ask Qwen",
        "05  Explain"
    ]

    for item in workflow_items:

        st.caption(item)

    st.markdown("---")

    st.markdown(
        "### Stack"
    )

    st.caption(
        "Python • Streamlit • GitPython"
    )

    st.caption(
        "Qwen 2.5 0.5B • Ollama • Transformers"
    )

    st.markdown("---")

    st.caption(
        "Same Qwen model locally and in the "
        "deployed application."
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">

    <div class="eyebrow">
        ✦ GenAI • Developer Tool
    </div>

    <h1>
        Understand any<br>
        repository faster.
    </h1>

    <p>
        RepoLens AI reads a public GitHub repository,
        identifies important source files, and uses
        Qwen to turn unfamiliar code into a clear,
        beginner-friendly explanation.
    </p>

</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    '<div class="glow-line"></div>',
    unsafe_allow_html=True
)


# ============================================================
# SEARCH CARD
# ============================================================

st.markdown(
    '<div class="search-card">',
    unsafe_allow_html=True
)


github_url = st.text_input(
    "GitHub Repository URL",

    placeholder=(
        "https://github.com/username/repository"
    )
)


st.caption(
    "Tip: use the repository URL, not a "
    "/blob/main/file.py URL."
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "✦  Analyze Repository",
    type="primary"
):

    if not github_url.strip():

        st.error(
            "Please enter a GitHub repository URL."
        )

    elif not valid_repo_url(
        github_url
    ):

        st.error(
            "Please enter a valid public "
            "GitHub repository URL."
        )

    else:

        repo_path = None

        try:

            with st.status(
                "Analyzing repository...",
                expanded=True
            ) as status:

                # ----------------------------------------
                # STEP 1
                # ----------------------------------------

                st.write(
                    "🔗 Validating GitHub repository..."
                )

                # ----------------------------------------
                # STEP 2
                # ----------------------------------------

                st.write(
                    "📥 Cloning repository..."
                )

                repo_path = clone_repository(
                    github_url.strip()
                )

                # ----------------------------------------
                # STEP 3
                # ----------------------------------------

                st.write(
                    "🔎 Finding relevant source files..."
                )

                context, files = (
                    build_repository_context(
                        repo_path
                    )
                )

                if not context.strip():

                    raise RuntimeError(
                        "No supported source-code files "
                        "were found in the repository."
                    )

                st.write(
                    f"📄 Selected {len(files)} "
                    "relevant files."
                )

                # ----------------------------------------
                # STEP 4
                # ----------------------------------------

                st.write(
                    "🤖 Generating explanation with Qwen..."
                )

                explanation = explain_repository(
                    context
                )

                # ----------------------------------------
                # STORE RESULT
                # ----------------------------------------

                st.session_state["analysis"] = {

                    "github_url":
                        github_url.strip(),

                    "files_analyzed":
                        files,

                    "explanation":
                        explanation
                }

                st.session_state[
                    "analyzed_url"
                ] = github_url.strip()

                # ----------------------------------------
                # COMPLETE
                # ----------------------------------------

                status.update(

                    label=(
                        "Analysis completed successfully!"
                    ),

                    state="complete",

                    expanded=False
                )

            st.rerun()

        except Exception as exc:

            st.error(
                f"Analysis failed: {exc}"
            )

        finally:

            if repo_path:

                cleanup_repository(
                    repo_path
                )


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.get(
    "analysis"
)


if result:

    analyzed_url = (
        st.session_state.get(
            "analyzed_url",
            result.get(
                "github_url",
                ""
            )
        )
    )

    files = result.get(
        "files_analyzed",
        []
    )

    explanation = result.get(
        "explanation",
        ""
    )


    # ========================================================
    # REPOSITORY INTELLIGENCE
    # ========================================================

    languages = sorted(
        {
            file_ext(f)

            for f in files

            if file_ext(f)
            not in {
                "file",
                "md",
                "txt"
            }
        }
    )


    st.markdown(
        '<div class="section-title">'
        'Repository Intelligence'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-subtitle">'
        'Qwen AI analysis completed successfully.'
        '</div>',
        unsafe_allow_html=True
    )


    metric_cols = st.columns(4)


    metrics = [

        (
            "◉",
            "Repository",
            repo_name(
                analyzed_url
            )
        ),

        (
            "⌘",
            "Files analyzed",
            str(len(files))
        ),

        (
            "◇",
            "File types",
            str(len(languages))
        ),

        (
            "✦",
            "AI engine",
            "Qwen 0.5B"
        )
    ]


    for col, (
        icon,
        label,
        value
    ) in zip(
        metric_cols,
        metrics
    ):

        with col:

            st.markdown(
                f"""
<div class="metric-card">

    <div class="metric-icon">
        {icon}
    </div>

    <div class="metric-label">
        {label}
    </div>

    <div class="metric-value">
        {value}
    </div>

</div>
""",
                unsafe_allow_html=True
            )


    # ========================================================
    # REPOSITORY URL
    # ========================================================

    st.markdown(
        f"""
<div style="margin-top:18px;">

    <span class="repo-pill">
        ● Analysis completed
    </span>

    <span style="
        color:#64748b;
        font-size:12px;
        margin-left:8px;
    ">
        {analyzed_url}
    </span>

</div>
""",
        unsafe_allow_html=True
    )


    # ========================================================
    # ARCHITECTURE
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Analysis Pipeline'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-subtitle">'
        'How your repository moves through the GenAI system.'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
<div class="info-card">

    <div class="arch">

        <div class="arch-node">
            <strong>GitHub</strong>
            <span>Repository</span>
        </div>

        <div class="arch-arrow">
            →
        </div>

        <div class="arch-node">
            <strong>GitPython</strong>
            <span>Clone & scan</span>
        </div>

        <div class="arch-arrow">
            →
        </div>

        <div class="arch-node">
            <strong>Code Processor</strong>
            <span>Relevant files</span>
        </div>

        <div class="arch-arrow">
            →
        </div>

        <div class="arch-node">
            <strong>Qwen 0.5B</strong>
            <span>AI Model</span>
        </div>

        <div class="arch-arrow">
            →
        </div>

        <div class="arch-node">
            <strong>Explanation</strong>
            <span>Streamlit UI</span>
        </div>

    </div>

</div>
""",
        unsafe_allow_html=True
    )


    # ========================================================
    # TABS
    # ========================================================

    tab_ai, tab_files, tab_system = st.tabs(
        [
            "✦ AI Explanation",
            "⌘ Files Analyzed",
            "◎ System"
        ]
    )


    # ========================================================
    # AI EXPLANATION
    # ========================================================

    with tab_ai:

        st.markdown(
            '<div class="section-title">'
            'AI-Generated Explanation'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            explanation
        )


    # ========================================================
    # FILES
    # ========================================================

    with tab_files:

        st.markdown(
            '<div class="section-title">'
            'Repository File Map'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Files selected by the repository processor "
            "and provided to Qwen."
        )


        if files:

            left, right = st.columns(2)


            for index, name in enumerate(files):

                target = (
                    left
                    if index % 2 == 0
                    else right
                )


                with target:

                    st.markdown(
                        f"""
<div class="file-item">

    <span class="file-name">
        ⌁ {name}
    </span>

    <span class="file-ext">
        {file_ext(name)}
    </span>

</div>
""",
                        unsafe_allow_html=True
                    )

        else:

            st.info(
                "No file list was returned."
            )


    # ========================================================
    # SYSTEM
    # ========================================================

    with tab_system:

        a, b, c = st.columns(3)


        cards = [

            (
                "Qwen 2.5 0.5B",

                "The same Qwen model is used "
                "for repository explanation "
                "in both environments."
            ),

            (
                "Repository processing",

                "GitPython clones the repository "
                "and the code processor selects "
                "relevant files."
            ),

            (
                "Dual inference",

                "Local execution uses Ollama, "
                "while Streamlit Cloud uses "
                "Hugging Face Transformers."
            )
        ]


        for col, (
            title,
            body
        ) in zip(
            (a, b, c),
            cards
        ):

            with col:

                st.markdown(
                    f"""
<div class="info-card">

    <h4>
        {title}
    </h4>

    <p>
        {body}
    </p>

</div>
""",
                    unsafe_allow_html=True
                )


# ============================================================
# EMPTY STATE
# ============================================================

else:

    st.markdown(
        '<div class="section-title">'
        'Built for understanding code'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-subtitle">'
        'From a GitHub URL to a simple explanation '
        'in one workflow.'
        '</div>',
        unsafe_allow_html=True
    )


    c1, c2, c3 = st.columns(3)


    cards = [

        (
            "⌘ Repository Intelligence",

            "Clone a public repository and "
            "identify useful source files "
            "automatically."
        ),

        (
            "✦ Qwen AI Analysis",

            "Use Qwen 2.5 0.5B to turn "
            "repository code into a "
            "beginner-friendly explanation."
        ),

        (
            "↗ Dual Deployment",

            "Run the same application locally "
            "or deploy it through Streamlit Cloud."
        )
    ]


    for col, (
        title,
        body
    ) in zip(
        (c1, c2, c3),
        cards
    ):

        with col:

            st.markdown(
                f"""
<div class="info-card">

    <h4>
        {title}
    </h4>

    <p>
        {body}
    </p>

</div>
""",
                unsafe_allow_html=True
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
    RepoLens AI · Qwen 2.5 0.5B · Streamlit ·
    GitPython · Ollama · Transformers
</div>
""",
    unsafe_allow_html=True
)