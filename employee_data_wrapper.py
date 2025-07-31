import streamlit as st
import sys
import os

def render_employee_data_management():
    """Render the Employee Data Management System"""
    try:
        # Add the new_employee path to sys.path
        employee_path = os.path.join(os.getcwd(), 'new_employee')
        if employee_path not in sys.path:
            sys.path.insert(0, employee_path)
        
        # Also add the panels path
        panels_path = os.path.join(employee_path, 'panels')
        if panels_path not in sys.path:
            sys.path.insert(0, panels_path)
        
        # Save current working directory and change to employee directory
        original_cwd = os.getcwd()
        original_path = sys.path.copy()
        
        try:
            os.chdir(employee_path)
            
            # Read the main_app.py file content
            main_app_path = os.path.join(employee_path, 'main_app.py')
            if not os.path.exists(main_app_path):
                st.error("❌ Employee main_app.py not found")
                return
            
            with open(main_app_path, 'r', encoding='utf-8') as f:
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
                '__file__': main_app_path,
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
        st.error(f"❌ **Employee System Error:** {str(e)}")
        st.info("**Troubleshooting:**")
        st.write("1. Ensure `new_employee/main_app.py` exists")
        st.write("2. Check that all employee panel files are in `new_employee/panels/`")
        st.write("3. Verify the employee system structure")
        
        with st.expander("🔍 Technical Details"):
            st.code(f"Error Type: {type(e).__name__}\nError Message: {str(e)}")
            st.write(f"**Looking for employee system at:** `{employee_path}`")

def get_employee_system_status():
    """Get the status of the Employee Data Management System"""
    try:
        employee_path = os.path.join(os.getcwd(), 'new_employee')
        
        # Check if employee system exists
        if not os.path.exists(employee_path):
            return {
                'available': False,
                'status': 'Employee directory not found',
                'details': f'Path: {employee_path}'
            }
        
        main_app_path = os.path.join(employee_path, 'main_app.py')
        if not os.path.exists(main_app_path):
            return {
                'available': False,
                'status': 'main_app.py not found',
                'details': 'Employee system incomplete'
            }
        
        # Check required panels
        panels_path = os.path.join(employee_path, 'panels')
        required_panels = [
            "employee_main_panel.py",
            "employee_statistics_panel.py", 
            "employee_validation_panel.py",
            "employee_dashboard_panel.py",
            "employee_admin_panel.py"
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
        
        # Check session state for data status
        employee_state = getattr(st.session_state, 'state', {})
        
        pa_files_status = {}
        pa_files = ['PA0001', 'PA0002', 'PA0006', 'PA0105']
        files_loaded = 0
        
        for pa_file in pa_files:
            key = f'source_{pa_file.lower()}'
            is_loaded = employee_state.get(key) is not None
            pa_files_status[pa_file] = is_loaded
            if is_loaded:
                files_loaded += 1
        
        output_generated = bool(employee_state.get('generated_employee_files', {}))
        
        status_details = {
            'pa_files_loaded': files_loaded,
            'total_pa_files': len(pa_files),
            'pa_files_status': pa_files_status,
            'output_generated': output_generated,
            'ready_to_process': files_loaded >= 2  # Need at least PA0001 & PA0002
        }
        
        if output_generated:
            status_msg = "✅ Employee system ready - Output files generated"
        elif files_loaded >= 2:
            status_msg = f"🔄 Employee system ready - {files_loaded}/4 PA files loaded"
        elif files_loaded >= 1:
            status_msg = f"📊 Employee system ready - {files_loaded}/4 PA files loaded"
        else:
            status_msg = "📁 Employee system ready - Load PA files"
        
        return {
            'available': True,
            'status': status_msg,
            'details': status_details,
            'enhanced_features': [
                'PA Files Processing (PA0001, PA0002, PA0006, PA0105)',
                'Employee Data Validation',
                'Statistics & Detective Analysis',
                'Dashboard & Monitoring',
                'Admin Configuration'
            ]
        }
        
    except Exception as e:
        return {
            'available': False,
            'status': f'Employee system check failed: {str(e)}',
            'details': {'error': str(e)}
        }
