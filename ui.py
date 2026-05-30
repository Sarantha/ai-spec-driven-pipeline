import os
import sys
from pathlib import Path

root_path = str(Path(__file__).resolve().parent)
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import streamlit as st
import contextlib
from dotenv import load_dotenv

from ui.styles import inject_ide_styles
from ui.utils import StreamToStreamlit
from ui.components import render_top_bar, render_terminal_header, get_default_terminal_text

from services.spec_loader import YamlFeatureSpecLoader
from services.planner import GeminiArchitectPlanner
from services.synthesizer import GeminiCodeSynthesizer
from services.validator import PytestSubprocessValidator

st.set_page_config(
    page_title="Universal Spec-Driven Feature Engine",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_ide_styles()

is_running = st.session_state.get("pipeline_active", False)
render_top_bar(pipeline_active=is_running)

col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown('<div class="panel-section-title">⚙️ Configuration Profile</div>', unsafe_allow_html=True)
    
    target_dir_input = st.text_input(
        "Target workspace directory",
        value="",
        placeholder="e.g., D:\\AI Automation\\unique-customer-detector",
        key="target_dir"
    )
    
    if target_dir_input.strip():
        if os.path.exists(target_dir_input):
            st.markdown('<div class="status-validation-label">● Directory found</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-validation-label" style="color: #da3637;">● Directory not found</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="height: 42px;"></div>', unsafe_allow_html=True)
        
    uploaded_file = st.file_uploader(
        "Feature specification (.yaml / .yml)",
        type=["yaml", "yml"],
        key="spec_file"
    )
    
    if uploaded_file is not None:
        st.markdown(f'<div class="status-validation-label"> {uploaded_file.name} — ready</div>', unsafe_allow_html=True)
    else:
         st.markdown('<div style="height: 42px;"></div>', unsafe_allow_html=True)

    is_valid_input = bool(target_dir_input.strip() and os.path.exists(target_dir_input)) and (uploaded_file is not None)
    
    execute_button = st.button(
        "► Run pipeline", 
        use_container_width=True,
        disabled=not is_valid_input
    )

with col_right:
    render_terminal_header()
    
    status_box = st.empty()
    log_terminal_placeholder = st.empty()
    log_terminal_placeholder.code(get_default_terminal_text())
    
    if execute_button:
        load_dotenv()
        st.session_state["pipeline_active"] = True
        normalized_target_dir = os.path.abspath(target_dir_input)
        temp_spec_filename = "temp_uploaded_spec.yaml"
        
        with open(temp_spec_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        with col_right:
            status_box = st.status("Initializing Refactored Engine Architecture...", expanded=False)
            
        streamlit_logger = StreamToStreamlit(log_terminal_placeholder)
        
        with contextlib.redirect_stdout(streamlit_logger):
            try:
                
                loader = YamlFeatureSpecLoader()
                planner = GeminiArchitectPlanner()
                synthesizer = GeminiCodeSynthesizer()
                validator = PytestSubprocessValidator()
                
                spec_model_obj = loader.load(temp_spec_filename)
                blueprint_plan = planner.design_plan(spec_model_obj, normalized_target_dir)
                
                contract_data = blueprint_plan.codebase_contract
                g_vars = contract_data.get("global_variables", []) if isinstance(contract_data, dict) else getattr(contract_data, "global_variables", [])
                classes = contract_data.get("classes", []) if isinstance(contract_data, dict) else getattr(contract_data, "classes", [])
                funcs = contract_data.get("functions", []) if isinstance(contract_data, dict) else getattr(contract_data, "functions", [])
                
                print("\n" + "="*60)
                print("DYNAMIC CODEBASE INTERFACE CONTRACT GENERATED")
                print("="*60)
                print(f"Plan Summary: {blueprint_plan.technical_summary}")
                print(f"Selected Targets: {blueprint_plan.impacted_files}")
                print(f"Architecture Contract Global Vars: {g_vars}")
                print(f"Architecture Contract Classes: {classes}")
                print(f"Architecture Contract Functions: {funcs}")
                print("="*60 + "\n")
                
                target_test_script_name = synthesizer.implement(blueprint_plan, spec_model_obj, normalized_target_dir)
                success = validator.verify(normalized_target_dir, target_test_script_name)
                
                if success:
                    status_box.success("PIPELINE COMPLETE: Features engineered and verified successfully!")
                    st.balloons()
                else:
                    status_box.error("QUALITY GATE FAILURE: Generated code failed functional testing benchmarks.")
                    
            except BaseException as pipeline_err:
                print(f"\nCritical runtime crash encountered: {pipeline_err}")
                status_box.error(f"Pipeline Aborted: {pipeline_err}")
                
            finally:
                st.session_state["pipeline_active"] = False
                if os.path.exists(temp_spec_filename):
                    os.remove(temp_spec_filename)