import streamlit as st

def render_top_bar(pipeline_active: bool):
    """Renders the top branding and live connectivity pipeline header badge."""
    status_badge_text = "● Running execution" if pipeline_active else "● System idle"
    st.markdown(f"""
        <div class="top-header-bar">
            <div class="header-title-container">
                <div class="header-title-main">⚙️ Universal Spec-Driven Feature Engine</div>
                <div class="header-title-sub">AI-native engineering pipeline console</div>
            </div>
            <div class="header-status-badge">{status_badge_text}</div>
        </div>
    """, unsafe_allow_html=True)

def render_terminal_header():
    """Renders the aesthetic structural upper header bar for simulated raw console log windows."""
    st.markdown("""
        <div class="terminal-header">
            <div class="terminal-title">► Live Terminal Output</div>
            <div class="terminal-actions">
                <span style="color: #8b949e; font-size: 0.75rem; margin-right: 12px; font-family: monospace;">stdout • bash</span>
                <span class="terminal-dot" style="background-color: #ff5f56;"></span>
                <span class="terminal-dot" style="background-color: #ffbd2e;"></span>
                <span class="terminal-dot" style="background-color: #27c93f;"></span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def get_default_terminal_text() -> str:
    """Returns standard placeholder configuration context text strings for idle terminal outputs."""
    return (
        "PIPELINE CONSOLE — AI-NATIVE PIPELINE CONSOLE — AI-NATIVE PIPELINE CONSOLE\n"
        "Stages: [1/6] Ingestion & quality gate checks [2/6] AI architectural blueprint design "
        "[3/6] Codebase contract generation [4/6] Code synthesis [5/6] Sandbox injection [6/6] Automated quality verification\n\n"
        "Provide a workspace path and spec file to activate. Terminal output will stream here in real time.\n\n"
        "$_"
    )