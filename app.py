import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fieldnote · Research Pipeline",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #eae6d8;
}

.stApp {
    background: #0b0b0b;
    /* Restrained two-tone glow — amber bleeding out of black corners, not a flat AI-generic blob */
    background-image:
        radial-gradient(ellipse 70% 45% at 15% -8%, rgba(255,179,0,0.10) 0%, transparent 58%),
        radial-gradient(ellipse 55% 38% at 85% 108%, rgba(255,153,0,0.07) 0%, transparent 55%);
}

/* ══════════════════ BACKGROUND SECTION START ══════════════════
   Faint film-grain texture layered over the whole app. Pure CSS
   (base64 SVG noise filter) — no external image request, no extra
   network call. Delete everything between the START/END markers
   below if you decide you don't want it; nothing else depends on it. */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: 0.035;
    z-index: 0;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}

/* ══════════════════ BACKGROUND SECTION END ══════════════════ */

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #ffb300;
    margin-bottom: 1rem;
    opacity: 0.85;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: #f4f0e4;
    margin: 0 0 1rem;
}
.hero h1 span {
    color: #ffb300;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #9c9686;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,179,0,0.35), transparent);
    margin: 2rem 0;
}

/* ── Input section rule ──
   A real element (not a cross-call div hack) so it can't render as a
   stray empty box the way the old .input-card wrapper did. */
.input-rule {
    width: 42px;
    height: 2px;
    background: #ffb300;
    margin: 0 0 1.4rem;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,179,0,0.28) !important;
    border-radius: 3px !important;
    color: #f4f0e4 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ffb300 !important;
    box-shadow: 0 0 0 3px rgba(255,179,0,0.10) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #c9a227 !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    background: #ffb300 !important;
    color: #0b0b0b !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase;
    border: none !important;
    border-radius: 3px !important;
    padding: 0.75rem 2.2rem !important;
    cursor: pointer !important;
    transition: background 0.15s, transform 0.15s !important;
    width: 100%;
}
.stButton > button:hover {
    background: #ffc933 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    background: #e6a100 !important;
}

/* ── Input column spacing (replaces the old broken card wrapper) ── */
div[data-testid="stTextInput"] { margin-bottom: 0.6rem; }
div[data-testid="stButton"] { margin-bottom: 2rem; }

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 4px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, background 0.3s;
}
.step-card.active {
    border-color: rgba(255,179,0,0.45);
    background: rgba(255,179,0,0.04);
}
.step-card.done {
    border-color: rgba(255,179,0,0.22);
    background: rgba(255,255,255,0.015);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: rgba(255,255,255,0.08);
    transition: background 0.3s;
}
.step-card.active::before { background: #ffb300; }
.step-card.done::before   { background: #c9a227; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.3rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: #ffb300;
    opacity: 0.75;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #f4f0e4;
}
.step-status {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
}
.status-waiting  { color: #4a4a4a; }
.status-running  { color: #ffb300; }
.status-done     { color: #c9a227; }

/* ── Result panels ── */
.result-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 4px;
    padding: 1.8rem 2rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
.result-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ffb300;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(255,179,0,0.18);
}
.result-content {
    font-size: 0.92rem;
    line-height: 1.8;
    color: #cdc8bf;
    white-space: pre-wrap;
    font-family: 'DM Sans', sans-serif;
}

/* ── Report & feedback panels ── */
.report-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,179,0,0.25);
    border-radius: 4px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.feedback-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 4px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
}
.panel-label.orange {
    color: #ffb300;
    border-bottom: 1px solid rgba(255,179,0,0.2);
}
.panel-label.green {
    color: #eae6d8;
    border-bottom: 1px solid rgba(255,255,255,0.15);
}

/* ── Progress text ── */
.stSpinner > div { color: #ffb300 !important; }

/* ── Expander ── */
details summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #9c9686 !important;
    letter-spacing: 0.1em !important;
    cursor: pointer;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #f4f0e4;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-heading::before {
    content: '';
    width: 8px;
    height: 8px;
    background: #ffb300;
}

/* ── Example chips ── */
.example-chip {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,179,0,0.15);
    border-radius: 3px;
    padding: 0.28rem 0.75rem;
    font-size: 0.75rem;
    color: #b8b2a4;
    font-family: 'DM Sans', sans-serif;
}

/* ── Toast-style notice ── */
.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #4a4a4a;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#6b6558;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent Research System</div>
    <h1>Field<span>note</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to turn a topic into a field-researched, polished report.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-rule"></div>', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2026",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("Run Research Pipeline", use_container_width=True)

    # Example chips
    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;align-items:center;margin-bottom:1.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#4a4a4a;letter-spacing:0.12em;">TRY →</span>
    """, unsafe_allow_html=True)
    examples = ["LLM agents in 2026", "Room-temperature superconductors", "Fusion energy progress"]
    for ex in examples:
        st.markdown(f'<span class="example-chip">{ex}</span>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        idx = steps.index(step)
        completed = list(r.keys())
        # figure out which steps are done
        if step in r:
            return "done"
        # which step is running now (first not in r)
        if st.session_state.running:
            for i, k in enumerate(steps):
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None   # keep inline for now

    # ── Step 2: Reader ──
    with st.spinner("Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])   # render markdown natively
        st.markdown("</div>", unsafe_allow_html=True)

        # Download
        st.download_button(
            label="Download Report (.md)",
            data=r["writer"],
            file_name=f"fieldnote_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    Fieldnote · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)