import streamlit as st
import sys
import os

def render_foundation_data_management():
    """Render the Foundation Data Management System"""
    try:
        # Add the new_foundation path to sys.path
        foundation_path = os.path.join(os.getcwd(), 'new_foundation')
        if foundation_path not in sys.path:
            sys.path.insert(0, foundation_path)
        
        # Also add the panels path for foundation system
        panels_path = os.path.join(foundation_path, 'panels')
        if panels_path not in sys.path:
            sys.path.insert(0, panels_path)
        
        # Save current working directory and change to foundation directory
        original_cwd = os.getcwd()
        original_path = sys.path.copy()
        
        try:
            os.chdir(foundation_path)
            
            # Instead of executing the entire main_app.py, let's import the panels directly
            # and recreate the interface manually to avoid st.set_page_config conflicts
            
            # Import the foundation panel functions directly (based on the structure shown)
            from hierarchy_panel_fixed import show_hierarchy_panel
            
            # Import enhanced validation panel with fallback
            try:
                from enhanced_validation_panel import show_validation_panel
                VALIDATION_ENHANCED = True
            except ImportError:
                try:
                    from validation_panel_fixed import show_validation_panel
                    VALIDATION_ENHANCED = False
                except ImportError:
                    def show_validation_panel(state):
                        st.title("Validation Panel")
                        st.error("Validation panel not implemented yet")
                        st.info("This panel is under development")
                    VALIDATION_ENHANCED = False
            
            # Import admin panel with fallbacks
            try:
                from config_manager import show_admin_panel
            except ImportError:
                def show_admin_panel():
                    st.error("Admin panel not found. Please ensure config_manager.py exists.")
                    st.info("Create config_manager.py or place it in the panels/ folder")
            
            # Import statistics panel with fallbacks
            try:
                from statistics_panel import show_statistics_panel
                STATISTICS_ENHANCED = True
            except ImportError:
                def show_statistics_panel(state):
                    st.title("Statistics Panel") 
                    st.error("Statistics panel not implemented yet")
                    st.info("This panel is under development")
                STATISTICS_ENHANCED = False
            
            # Import health monitor (dashboard) panel with fallbacks
            try:
                from dashboard_panel import show_health_monitor_panel
                HEALTH_MONITOR_ENHANCED = True
            except ImportError:
                def show_health_monitor_panel(state):
                    st.title("Health Monitor Panel")
                    st.error("Health Monitor panel not implemented yet") 
                    st.info("This panel is under development")
                HEALTH_MONITOR_ENHANCED = False
            
            # Initialize session state with default level names (from the main_app.py structure)
            def get_default_level_names():
                """Get improved default level names"""
                return {
                    1: "Level1_LegalEntity",
                    2: "Level2_BusinessUnit", 
                    3: "Level3_Division",
                    4: "Level4_SubDivision",
                    5: "Level5_Department",
                    6: "Level6_SubDepartment",
                    7: "Level7_Team",
                    8: "Level8_Unit",
                    9: "Level9_Unit", 
                    10: "Level10_Unit",
                    11: "Level11_Unit",
                    12: "Level12_Unit",
                    13: "Level13_Unit",
                    14: "Level14_Unit",
                    15: "Level15_Unit",
                    16: "Level16_Unit",
                    17: "Level17_Unit",
                    18: "Level18_Unit",
                    19: "Level19_Unit",
                    20: "Level20_Unit"
                }
            
            # Initialize session state with admin config and improved level names
            if 'state' not in st.session_state:
                st.session_state.state = {
                    'hrp1000': None,
                    'hrp1001': None,
                    'hierarchy': None,
                    'level_names': get_default_level_names(),
                    'transformations': [],
                    'validation_results': None,
                    'statistics': None,
                    'pending_transforms': [],
                    'admin_mode': False,
                    'generated_output_files': {},  # For enhanced statistics
                    'output_generation_metadata': {}  # Metadata for statistics
                }
            
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
                    .admin-section {
                        background-color: #f8f9fa;
                        padding: 1rem;
                        border-radius: 0.5rem;
                        border-left: 4px solid #ff4b4b;
                        margin-bottom: 1rem;
                    }
                    .enhanced-panel {
                        background-color: #e8f5e8;
                        border: 1px solid #90ee90;
                        padding: 1rem;
                        border-radius: 0.5rem;
                        border-left: 4px solid #22c55e;
                    }
                </style>
            """, unsafe_allow_html=True)
            
            # Create the foundation interface
            st.title("📊 Org Hierarchy Visual Explorer v2.4")
            
            # Sidebar navigation with admin toggle
            with st.sidebar:
                st.title("Navigation")
                
                # Show enhancement status for all panels
                if STATISTICS_ENHANCED:
                    st.markdown('<div style="background: linear-gradient(90deg, #3b82f6, #8b5cf6); color: white; padding: 10px; border-radius: 8px; text-align: center; margin: 10px 0; font-weight: bold;">Enhanced Statistics Active 🚀</div>', unsafe_allow_html=True)
                    st.caption("End-to-end pipeline analysis available")
                else:
                    st.warning("Basic Statistics Mode")
                    st.caption("Enhanced pipeline analysis not available")
                
                if VALIDATION_ENHANCED:
                    st.markdown('<div style="background: linear-gradient(90deg, #ef4444, #f59e0b); color: white; padding: 10px; border-radius: 8px; text-align: center; margin: 10px 0; font-weight: bold;">Enhanced Validation Active 🔍</div>', unsafe_allow_html=True)
                    st.caption("Complete pipeline validation available")
                else:
                    st.warning("Basic Validation Mode")
                    st.caption("Enhanced pipeline validation not available")
                
                if HEALTH_MONITOR_ENHANCED:
                    st.markdown('<div style="background: linear-gradient(90deg, #8b5cf6, #3b82f6); color: white; padding: 10px; border-radius: 8px; text-align: center; margin: 10px 0; font-weight: bold;">Enhanced Health Monitor Active 🏥</div>', unsafe_allow_html=True)
                    st.caption("System health monitoring available")
                else:
                    st.warning("Basic Health Monitor Mode")
                    st.caption("System health monitoring not available")
                
                # Admin mode toggle
                admin_enabled = st.checkbox("Admin Mode", help="Enable configuration options", key="foundation_admin_mode")
                
                if admin_enabled:
                    st.session_state.state['admin_mode'] = True
                    st.info("Admin mode activated")
                else:
                    st.session_state.state['admin_mode'] = False
                
                # Show current data status
                st.divider()
                st.subheader("Data Status")
                
                # Check data status
                hrp1000_loaded = 'source_hrp1000' in st.session_state.state and st.session_state.state['source_hrp1000'] is not None
                hrp1001_loaded = 'source_hrp1001' in st.session_state.state and st.session_state.state['source_hrp1001'] is not None
                hierarchy_processed = 'hierarchy_structure' in st.session_state.state and st.session_state.state['hierarchy_structure'] is not None
                output_generated = 'generated_output_files' in st.session_state.state and st.session_state.state['generated_output_files']
                
                if hrp1000_loaded:
                    st.success("HRP1000 Loaded")
                    st.caption(f"{len(st.session_state.state['source_hrp1000']):,} records")
                else:
                    st.error("HRP1000 Missing")
                
                if hrp1001_loaded:
                    st.success("HRP1001 Loaded") 
                    st.caption(f"{len(st.session_state.state['source_hrp1001']):,} records")
                else:
                    st.error("HRP1001 Missing")
                
                if hierarchy_processed:
                    st.success("Hierarchy Processed")
                    max_level = max([info.get('level', 1) for info in st.session_state.state['hierarchy_structure'].values()]) if st.session_state.state['hierarchy_structure'] else 0
                    st.caption(f"{max_level} levels")
                else:
                    st.warning("Hierarchy Pending")
                
                # Enhanced: Show output file status for statistics
                if output_generated:
                    level_files = st.session_state.state['generated_output_files'].get('level_files', {})
                    association_files = st.session_state.state['generated_output_files'].get('association_files', {})
                    st.success("Output Files Generated")
                    st.caption(f"{len(level_files)} level + {len(association_files)} association files")
                    if STATISTICS_ENHANCED:
                        st.info("🔍 Ready for pipeline analysis")
                    if VALIDATION_ENHANCED:
                        st.info("🔍 Ready for complete validation")
                    if HEALTH_MONITOR_ENHANCED:
                        st.info("🏥 Ready for health monitoring")
                else:
                    st.warning("Output Files Pending")
                    if STATISTICS_ENHANCED or VALIDATION_ENHANCED or HEALTH_MONITOR_ENHANCED:
                        st.caption("Generate files for full analysis")
                
                st.divider()
                
                # Main navigation
                if st.session_state.state['admin_mode']:
                    panel_options = ["Admin", "Hierarchy", "Validation", "Statistics", "Health Monitor"]
                else:
                    panel_options = ["Hierarchy", "Validation", "Statistics", "Health Monitor"]
                
                panel = st.radio(
                    "Go to",
                    panel_options,
                    label_visibility="collapsed",
                    key="foundation_panel_selection"
                )
            
            # Show welcome message for first-time users
            if not hrp1000_loaded and not hrp1001_loaded:
                st.markdown("""
                ### Welcome to the Organizational Hierarchy Visual Explorer!
                
                **Getting Started:**
                1. **Upload Data**: Go to the Hierarchy panel to upload your HRP1000 and HRP1001 files
                2. **Process**: Process your organizational structure 
                3. **Validate**: Check data quality in the Validation panel
                4. **Generate**: Create output files for your target system
                5. **Analyze**: Use Statistics panel for end-to-end pipeline analysis
                6. **Monitor**: Check system health in the Health Monitor
                """)
            
            # Panel routing with enhanced error handling
            try:
                if panel == "Admin" and st.session_state.state['admin_mode']:
                    st.markdown("<div class='admin-section'>", unsafe_allow_html=True)
                    st.header("Admin Configuration Center")
                    show_admin_panel()
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                elif panel == "Hierarchy":
                    show_hierarchy_panel(st.session_state.state)
                    
                elif panel == "Validation":
                    if VALIDATION_ENHANCED:
                        st.markdown("<div class='enhanced-panel'>", unsafe_allow_html=True)
                    
                    try:
                        show_validation_panel(st.session_state.state)
                    except Exception as e:
                        st.error(f"Error in Validation panel: {str(e)}")
                    
                    if VALIDATION_ENHANCED:
                        st.markdown("</div>", unsafe_allow_html=True)
                
                elif panel == "Statistics":
                    if STATISTICS_ENHANCED:
                        st.markdown("<div class='enhanced-panel'>", unsafe_allow_html=True)
                    
                    try:
                        show_statistics_panel(st.session_state.state)
                    except Exception as e:
                        st.error(f"Error in Statistics panel: {str(e)}")
                    
                    if STATISTICS_ENHANCED:
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                elif panel == "Health Monitor":
                    if HEALTH_MONITOR_ENHANCED:
                        st.markdown("<div class='enhanced-panel'>", unsafe_allow_html=True)
                    
                    try:
                        show_health_monitor_panel(st.session_state.state)
                    except Exception as e:
                        st.error(f"Error in Health Monitor panel: {str(e)}")
                    
                    if HEALTH_MONITOR_ENHANCED:
                        st.markdown("</div>", unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"Error loading {panel} panel: {str(e)}")
                st.info("Please check that all required panel files exist and are properly configured")
            
        finally:
            # Always restore original working directory and path
            os.chdir(original_cwd)
            sys.path = original_path
        
    except ImportError as e:
        st.error(f"❌ **Foundation System Import Error:** {str(e)}")
        st.info("**Troubleshooting:**")
        st.write("1. Ensure `new_foundation/main_app.py` exists")
        st.write("2. Check that all foundation panel files are in `new_foundation/panels/`")
        st.write("3. Verify the foundation system structure")
        st.write("4. Ensure required panel files exist:")
        
        required_panels = [
            "hierarchy_panel_fixed.py",
            "enhanced_validation_panel.py (or validation_panel_fixed.py)",
            "statistics_panel.py",
            "dashboard_panel.py", 
            "config_manager.py"
        ]
        
        foundation_path = os.path.join(os.getcwd(), 'new_foundation')
        panels_path = os.path.join(foundation_path, 'panels')
        
        for panel in required_panels:
            panel_path = os.path.join(panels_path, panel.split()[0])  # Remove the "(or ...)" part
            if os.path.exists(panel_path):
                st.success(f"✅ {panel}")
            else:
                st.error(f"❌ {panel}")
        
        with st.expander("🔍 Technical Details"):
            st.code(f"Import Error: {str(e)}")
            st.write(f"**Looking for foundation system at:** `{foundation_path}`")
            st.write(f"**Looking for panels at:** `{panels_path}`")
    
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
