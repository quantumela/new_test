import streamlit as st
import sys
import os

def render_payroll_data_management():
    """Render the Payroll Data Management System"""
    try:
        # Add the new_payroll path to sys.path
        payroll_path = os.path.join(os.getcwd(), 'new_payroll')
        if payroll_path not in sys.path:
            sys.path.insert(0, payroll_path)
        
        # Also add the payroll_panels path (note different folder name)
        panels_path = os.path.join(payroll_path, 'payroll_panels')
        if panels_path not in sys.path:
            sys.path.insert(0, panels_path)
        
        # Save current working directory and change to payroll directory
        original_cwd = os.getcwd()
        original_path = sys.path.copy()
        
        try:
            os.chdir(payroll_path)
            
            # Read the app.py file content (note: payroll uses app.py, not main_app.py)
            app_py_path = os.path.join(payroll_path, 'app.py')
            if not os.path.exists(app_py_path):
                st.error("❌ Payroll app.py not found")
                return
            
            with open(app_py_path, 'r', encoding='utf-8') as f:
                app_content = f.read()
            
            # Remove or comment out st.set_page_config lines to avoid conflicts
            lines = app_content.split('\n')
            modified_lines = []
            
            for line in lines:
                if 'st.set_page_config' in line and not line.strip().startswith('#'):
                    # Comment out the st.set_page_config line
                    modified_lines.append('# ' + line + '  # Commented out by wrapper')
                else:
                    modified_lines.append(line)
            
            modified_content = '\n'.join(modified_lines)
            
            # Create a local namespace for execution
            local_namespace = {
                '__name__': '__main__',
                '__file__': app_py_path,
                'st': st,
                'sys': sys,
                'os': os,
                'pd': None  # Will be imported in the executed code if needed
            }
            
            # Execute the modified content
            exec(modified_content, local_namespace)
            
        finally:
            # Always restore original working directory and path
            os.chdir(original_cwd)
            sys.path = original_path
        
    except Exception as e:
        st.error(f"❌ **Payroll System Error:** {str(e)}")
        st.info("**Troubleshooting:**")
        st.write("1. Ensure `new_payroll/app.py` exists")
        st.write("2. Check that all payroll panel files are in `new_payroll/payroll_panels/`")
        st.write("3. Verify the payroll system structure")
        
        with st.expander("🔍 Technical Details"):
            st.code(f"Error Type: {type(e).__name__}\nError Message: {str(e)}")
            st.write(f"**Looking for payroll system at:** `{payroll_path}`")
            st.write("**Note:** Payroll system uses `app.py` instead of `main_app.py`")

def get_payroll_system_status():
    """Get the status of the Payroll Data Management System"""
    try:
        payroll_path = os.path.join(os.getcwd(), 'new_payroll')
        
        # Check if payroll system exists
        if not os.path.exists(payroll_path):
            return {
                'available': False,
                'status': 'Payroll directory not found',
                'details': f'Path: {payroll_path}'
            }
        
        # Note: Payroll uses app.py instead of main_app.py
        app_path = os.path.join(payroll_path, 'app.py')
        if not os.path.exists(app_path):
            return {
                'available': False,
                'status': 'app.py not found',
                'details': 'Payroll system incomplete'
            }
        
        # Check required panels (note: payroll_panels folder)
        panels_path = os.path.join(payroll_path, 'payroll_panels')
        required_panels = [
            "payroll_main_panel.py",
            "payroll_statistics_panel.py", 
            "payroll_validation_panel.py",
            "payroll_dashboard_panel.py",
            "payroll_admin_panel.py"
        ]
        
        missing_panels = []
        for panel in required_panels:
            if not os.path.exists(os.path.join(panels_path, panel)):
                missing_panels.append(panel)
        
        if missing_panels:
            return {
                'available': False,
                'status': f'Missing panels: {", ".join(missing_panels)}',
                'details': {'missing_panels': missing_panels}
            }
        
        # Check session state for data status (note: payroll uses payroll_state)
        payroll_state = getattr(st.session_state, 'payroll_state', {})
        
        pa_files_status = {}
        pa_files = ['PA0008', 'PA0014']  # Payroll uses different PA files
        files_loaded = 0
        
        for pa_file in pa_files:
            key = f'source_{pa_file.lower()}'
            is_loaded = payroll_state.get(key) is not None
            pa_files_status[pa_file] = is_loaded
            if is_loaded:
                files_loaded += 1
        
        output_generated = bool(payroll_state.get('generated_payroll_files', {}))
        
        status_details = {
            'pa_files_loaded': files_loaded,
            'total_pa_files': len(pa_files),
            'pa_files_status': pa_files_status,
            'output_generated': output_generated,
            'ready_to_process': files_loaded >= 2  # Need both PA0008 & PA0014
        }
        
        if output_generated:
            status_msg = "✅ Payroll system ready - Output files generated"
        elif files_loaded >= 2:
            status_msg = "🔄 Payroll system ready - All PA files loaded"
        elif files_loaded >= 1:
            status_msg = f"📊 Payroll system ready - {files_loaded}/2 PA files loaded"
        else:
            status_msg = "📁 Payroll system ready - Load PA files"
        
        return {
            'available': True,
            'status': status_msg,
            'details': status_details,
            'enhanced_features': [
                'PA Files Processing (PA0008 Basic Pay, PA0014 Recurring Payments)',
                'Wage Type Mapping & Validation',
                'Payroll Statistics & Analytics',
                'Dashboard & Monitoring', 
                'Admin Configuration'
            ]
        }
        
    except Exception as e:
        return {
            'available': False,
            'status': f'Payroll system check failed: {str(e)}',
            'details': {'error': str(e)}
        }
