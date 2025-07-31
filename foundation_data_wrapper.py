import streamlit as st
import sys
import os

def render_foundation_data_management():
    """Render the complete Foundation Data Management System"""
    try:
        # Add the new_foundation path to sys.path if not already there
        foundation_path = os.path.join(os.getcwd(), 'new_foundation')
        if foundation_path not in sys.path:
            sys.path.insert(0, foundation_path)
        
        # Import and run the foundation main app
        from main_app import *  # This will execute the foundation main app
        
    except ImportError as e:
        st.error(f"❌ **Foundation System Import Error:** {str(e)}")
        st.info("**Troubleshooting:**")
        st.write("1. Ensure `new_foundation/main_app.py` exists")
        st.write("2. Check that all foundation panel files are in `new_foundation/panels/`")
        st.write("3. Verify the foundation system structure")
        
        with st.expander("🔍 Technical Details"):
            st.code(f"Import Error: {str(e)}")
            st.write(f"**Looking for foundation system at:** `{foundation_path}`")
            
            # Check if directory exists
            if os.path.exists(foundation_path):
                st.success("✅ Foundation directory exists")
                main_app_path = os.path.join(foundation_path, 'main_app.py')
                if os.path.exists(main_app_path):
                    st.success("✅ main_app.py found")
                else:
                    st.error("❌ main_app.py not found")
            else:
                st.error("❌ Foundation directory not found")
    
    except Exception as e:
        st.error(f"❌ **Foundation System Error:** {str(e)}")
        st.info("Please check the foundation system configuration and try again.")
        
        with st.expander("🔍 Technical Details"):
            st.code(f"Error Type: {type(e).__name__}\nError Message: {str(e)}")

def get_foundation_system_status():
    """Get the status of the Foundation Data Management System"""
    try:
        foundation_path = os.path.join(os.getcwd(), 'new_foundation')
        
        # Check if foundation system exists
        if not os.path.exists(foundation_path):
            return {
                'available': False,
                'status': 'Foundation directory not found',
                'details': f'Path: {foundation_path}'
            }
        
        main_app_path = os.path.join(foundation_path, 'main_app.py')
        if not os.path.exists(main_app_path):
            return {
                'available': False,
                'status': 'main_app.py not found',
                'details': 'Foundation system incomplete'
            }
        
        # Check session state for data status
        foundation_state = getattr(st.session_state, 'state', {})
        
        hrp1000_loaded = foundation_state.get('source_hrp1000') is not None
        hrp1001_loaded = foundation_state.get('source_hrp1001') is not None
        hierarchy_processed = foundation_state.get('hierarchy_structure') is not None
        output_generated = bool(foundation_state.get('generated_output_files', {}))
        
        status_details = {
            'hrp1000_loaded': hrp1000_loaded,
            'hrp1001_loaded': hrp1001_loaded,
            'hierarchy_processed': hierarchy_processed,
            'output_generated': output_generated,
            'files_ready': hrp1000_loaded and hrp1001_loaded
        }
        
        if output_generated:
            status_msg = "✅ Foundation system ready - Output files generated"
        elif hierarchy_processed:
            status_msg = "🔄 Foundation system ready - Generate output files"
        elif hrp1000_loaded and hrp1001_loaded:
            status_msg = "📊 Foundation system ready - Process hierarchy"
        else:
            status_msg = "📁 Foundation system ready - Load data files"
        
        return {
            'available': True,
            'status': status_msg,
            'details': status_details,
            'enhanced_features': [
                'Hierarchy Processing (HRP1000 & HRP1001)',
                'Advanced Validation Engine', 
                'Statistics & Analytics',
                'Health Monitor Dashboard',
                'Admin Configuration'
            ]
        }
        
    except Exception as e:
        return {
            'available': False,
            'status': f'Foundation system check failed: {str(e)}',
            'details': {'error': str(e)}
        }
