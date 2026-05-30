import streamlit as st

def inject_ide_styles():
    """Injects custom global CSS rules to create an edge-to-edge dark theme layout."""
    st.markdown("""
        <style>
            /* 1. Global Reset & Edge-to-Edge Layout */
            html, body, [data-testid="stAppViewContainer"], .main, .block-container {
                background-color: #0b0f17 !important;
                max-height: 100vh !important;
                height: 100vh !important;
                overflow: hidden !important;
                color: #c9d1d9 !important;
                padding: 0px !important;
                margin: 0px !important;
            }
            
            [data-testid="stAppViewContainer"] {
                max-width: 100vw !important;
            }
            
            [data-testid="stHeader"] {
                display: none !important;
            }

            /* 2. Top Header Navigation Bar */
            .top-header-bar {
                background-color: #0d1117;
                border-bottom: 1px solid #21262d;
                padding: 0px 24px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 100vw;
                height: 65px;
                box-sizing: border-box;
            }
            .header-title-container {
                display: flex;
                flex-direction: column;
                justify-content: center;
                height: 100%;
            }
            .header-title-main {
                font-size: 1.15rem !important;
                font-weight: 600;
                color: #f0f6fc;
            }
            .header-title-sub {
                font-size: 0.78rem;
                color: #8b949e;
                margin-top: 2px;
            }
            .header-status-badge {
                background-color: #161b22;
                color: #8b949e;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.75rem;
                border: 1px solid #30363d;
                font-family: monospace;
            }

            /* 3. Grid Structure Resets */
            [data-testid="stHorizontalBlock"] {
                gap: 0px !important;
                padding: 0px !important;
                margin: 0px !important;
                width: 100vw !important;
            }
            
            [data-testid="stColumn"] {
                height: calc(100vh - 65px) !important;
                display: flex !important;
                flex-direction: column !important;
                padding: 0px !important;
                margin: 0px !important;
            }
            
            [data-testid="stColumn"]:nth-of-type(1) {
                background-color: #0d1117 !important;
                border-right: 1px solid #21262d;
                padding: 30px 24px !important;
                box-sizing: border-box;
            }
            
            [data-testid="stColumn"]:nth-of-type(2) {
                background-color: #070a0f !important;
                padding: 0px !important;
                box-sizing: border-box;
            }

            /* 4. Typography Elements */
            .panel-section-title {
                font-size: 0.72rem !important;
                font-weight: 700 !important;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                color: #8b949e;
                margin-bottom: 20px !important;
            }
            
            .status-validation-label {
                font-size: 0.8rem;
                color: #2ea043;
                margin-top: 6px;
                margin-bottom: 20px;
                font-weight: 500;
            }

            /* 5. Code Terminal Feed Shell Window */
            .terminal-header {
                background-color: #0d1117;
                border-bottom: 1px solid #21262d;
                padding: 0px 24px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                height: 45px;
                width: 100%;
                box-sizing: border-box;
            }
            .terminal-title {
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                color: #8b949e;
            }
            .terminal-actions {
                display: flex;
                gap: 8px;
                align-items: center;
            }
            .terminal-dot {
                width: 11px;
                height: 11px;
                border-radius: 50%;
                display: inline-block;
            }

            /* 6. Native Streamlit Code Blocks Adjustments */
            [data-testid="stColumn"]:nth-of-type(2) [data-testid="stVerticalBlock"] {
                padding: 0px !important;
                gap: 0px !important;
            }
            
            [data-testid="stCodeBlock"], [data-testid="element-container"]:has(pre), .stCodeBlock {
                height: calc(100vh - 110px) !important;
                max-height: calc(100vh - 110px) !important;
                overflow: hidden !important;
                margin: 0px !important;
                padding: 0px !important;
            }

            [data-testid="stMarkdownContainer"] pre, [data-testid="stCodeBlock"] pre, pre {
                background-color: #070a0f !important;
                border: none !important;
                border-radius: 0px !important;
                padding: 24px !important;
                height: calc(100vh - 110px) !important;
                max-height: calc(100vh - 110px) !important;
                overflow-y: auto !important;
                overflow-x: auto !important;
                white-space: pre !important;
                font-family: 'Fira Code', 'Source Code Pro', Consolas, Monaco, monospace !important;
                font-size: 0.88rem !important;
                color: #e6edf3 !important;
                line-height: 1.6 !important;
            }
            
            /* 7. Action Button Design Modifiers */
            div.stButton > button {
                background-color: #238636 !important;
                color: #ffffff !important;
                border: 1px solid rgba(240,246,252,0.1) !important;
                border-radius: 6px !important;
                padding: 12px 20px !important;
                font-weight: 500 !important;
                font-size: 0.92rem !important;
                transition: background-color 0.2s;
                margin-top: 25px;
            }
            div.stButton > button:hover {
                background-color: #2ea043 !important;
                color: #ffffff !important;
            }
            div.stButton > button:disabled {
                background-color: #21262d !important;
                color: #484f58 !important;
                border: 1px solid #30363d !important;
                cursor: not-allowed !important;
            }
        </style>
    """, unsafe_allow_html=True)