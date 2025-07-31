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
            
            # Instead of executing the entire app.py, let's import the panels directly
            # and recreate the interface manually to avoid st.set_page_config conflicts
            
            # Import the payroll panel functions directly
            from payroll_main_panel import show_payroll_panel
            from payroll_statistics_panel import show_payroll_statistics_panel  
            from payroll_validation_panel import show_payroll_validation_panel
            from payroll_dashboard_panel import show_payroll_dashboard_panel
            from payroll_admin_panel import show_payroll_admin_panel
            
            # Initialize session state for payroll system (note: payroll uses payroll_state)
            if 'payroll_state' not in st.session_state:
                st.session_state.payroll_state = {}
            
            payroll_state = st.session_state.payroll_state
            
            # Recreate the payroll interface (based on the app.py structure)
            
            # Custom CSS for better display
            st.markdown("""
                <style>
                    .stDataFrame {
                        width: 100% !important;
                    }
                    .stDataFrame div[data-testid="stHorizontalBlock"] {
                        overflow-x: auto;
                    }
                    .stDataFrame table {
                        width: 100%;
                        font-size: 14px;
                    }
                    .stDataFrame th {
                        font-weight: bold !important;
                        background-color: #f0f2f6 !important;
                    }
                    .stDataFrame td {
                        white-space: nowrap;
                        max-width: 300px;
                        overflow: hidden;
                        text-overflow: ellipsis;
                    }
                </style>
            """, unsafe_allow_html=True)
            
            # Sidebar navigation
            st.sidebar.title("💰 Payroll Data Management")
            st.sidebar.markdown("---")
            
            panel = st.sidebar.radio(
                "**Choose Panel:**",
                [
                    "🏠 Payroll Processing",
                    "📊 Statistics & Analytics", 
                    "✅ Data Validation",
                    "📈 Dashboard",
                    "⚙️ Admin Configuration"
                ],
                key="payroll_panel_selection"
            )
            
            # Add quick stats in sidebar
            st.sidebar.markdown("---")
            st.sidebar.markdown("**📋 Quick Status:**")
            
            # Check data status
            pa_files_loaded = sum(1 for file_key in ['PA0008', 'PA0014'] 
                                 if payroll_state.get(f'source_{file_key.lower()}') is not None)
            output_generated = 'generated_payroll_files' in payroll_state and payroll_state['generated_payroll_files']
            
            st.sidebar.write(f"📂 PA Files: {pa_files_loaded}/2 loaded")
            st.sidebar.write(f"📤 Output: {'✅ Generated' if output_generated else '❌ Not yet'}")
            
            if pa_files_loaded >= 2:
                st.sidebar.success("✅ Ready to process")
            else:
                st.sidebar.error("❌ Need PA0008 & PA0014")
            
            st.sidebar.markdown("---")
            st.sidebar.markdown("**💡 Quick Tips:**")
            st.sidebar.info("1. Upload PA0008 & PA0014 files\n2. Process payroll data\n3. Validate results\n4. Analyze wage types")
            
            # Show selected panel with performance optimization
            try:
                if panel == "🏠 Payroll Processing":
                    show_payroll_panel(payroll_state)
                elif panel == "📊 Statistics & Analytics":
                    # Add warning for large datasets
                    pa0008_data = payroll_state.get('source_pa0008')
                    if pa0008_data is not None and len(pa0008_data) > 10000:
                        st.warning("⚠️ Large dataset detected. Statistics panel may take a moment to load...")
                    
                    with st.spinner("Loading payroll statistics..."):
                        show_payroll_statistics_panel(payroll_state)
                elif panel == "✅ Data Validation":
                    with st.spinner("Running validation checks..."):
                        show_payroll_validation_panel(payroll_state)
                elif panel == "📈 Dashboard":
                    show_payroll_dashboard_panel(payroll_state)
                elif panel == "⚙️ Admin Configuration":
                    show_payroll_admin_panel()
            
            except Exception as e:
                st.error(f"❌ **Panel Error:** {str(e)}")
                st.info("**What to do:** Try refreshing the page or switching to a different panel")
                
                # Show error details in expander
                with st.expander("🔍 Technical Details", expanded=False):
                    st.code(str(e))
                    if st.button("🔄 Reset Session", key="reset_payroll_session"):
                        for key in list(st.session_state.keys()):
                            if key.startswith('payroll'):
                                del st.session_state[key]
                        st.rerun()
            
            # Footer
            st.sidebar.markdown("---")
            st.sidebar.caption("💰 Payroll Data Management System v1.0")
            
        finally:
            # Always restore original working directory and path
            os.chdir(original_cwd)
            sys.path = original_path
        
    except ImportError as e:
        st.error(f"❌ **Payroll System Import Error:** {str(e)}")
        st.info("**Troubleshooting:**")
        st.write("1. Ensure `new_payroll/app.py` exists")
        st.write("2. Check that all payroll panel files are in `new_payroll/payroll_panels/`")
        st.write("3. Verify the payroll system structure")
        st.write("4. Ensure required panel files exist:")
        
        required_panels = [
            "payroll_main_panel.py",
            "payroll_statistics_panel.py", 
            "payroll_validation_panel.py",
            "payroll_dashboard_panel.py",
            "payroll_admin_panel.py"
        ]
        
        payroll_path = os.path.join(os.getcwd(), 'new_payroll')
        panels_path = os.path.join(payroll_path, 'payroll_panels')
        
        for panel in required_panels:
            panel_path = os.path.join(panels_path, panel)
            if os.path.exists(panel_path):
                st.success(f"✅ {panel}")
            else:
                st.error(f"❌ {panel}")
        
        with st.expander("🔍 Technical Details"):
            st.code(f"Import Error: {str(e)}")
            st.write(f"**Looking for payroll system at:** `{payroll_path}`")
            st.write(f"**Looking for panels at:** `{panels_path}`")
            st.write("**Note:** Payroll system uses `app.py` instead of `main_app.py`")
    
    except Exception as e:
        st.error(f"❌ **Payroll System Error:** {str(e)}")
        st.info("Please check the payroll system configuration and try again.")
        
        with st.expander("🔍 Technical Details"):
            st.code(f"Error Type: {type(e).__name__}\nError Message: {str(e)}")

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
