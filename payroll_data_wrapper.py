import streamlit as st
import sys
import os

def render_payroll_data_management():
    """Render the Payroll Data Management System"""
    try:
        # Add paths
        payroll_path = os.path.join(os.getcwd(), 'new_payroll')
        panels_path = os.path.join(payroll_path, 'payroll_panels')
        
        if payroll_path not in sys.path:
            sys.path.insert(0, payroll_path)
        if panels_path not in sys.path:
            sys.path.insert(0, panels_path)
        
        # Change directory
        original_cwd = os.getcwd()
        original_path = sys.path.copy()
        
        try:
            os.chdir(payroll_path)
            
            # Simple imports
            from payroll_main_panel import show_payroll_panel
            
            # Initialize session state
            if 'payroll_state' not in st.session_state:
                st.session_state.payroll_state = {}
            
            st.title("Payroll Data Management")
            
            # Simple navigation
            with st.sidebar:
                st.header("Payroll Navigation")
                panel = st.radio("Select Panel", ["Payroll Processing"], key="payroll_nav")
            
            # Show panel
            if panel == "Payroll Processing":
                show_payroll_panel(st.session_state.payroll_state)
                
        finally:
            os.chdir(original_cwd)
            sys.path = original_path
            
    except Exception as e:
        st.error(f"Payroll System Error: {str(e)}")
        st.info("Please check that new_payroll directory exists with required files")

def get_payroll_system_status():
    """Get payroll system status"""
    try:
        payroll_path = os.path.join(os.getcwd(), 'new_payroll')
        if os.path.exists(payroll_path):
            return {
                'available': True,
                'status': 'Payroll system available',
                'details': {}
            }
        else:
            return {
                'available': False,
                'status': 'Payroll directory not found',
                'details': {}
            }
    except Exception as e:
        return {
            'available': False,
            'status': f'Status check failed: {str(e)}',
            'details': {}
        }
