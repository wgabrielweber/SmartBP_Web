import streamlit as st
import json
from plots import plotRawData, plotRawAndFilteredDataCheby, plotFilteredDataCheby, plotFilteredDataMAF, plotRawAndFilteredDataMAF , plotFilteredDataComparison,plotFFT

def cssStyling():
    """Handles the CSS styling of the page."""
    st.markdown("""
        <style>
            /* Set a fixed width for the select boxes */
            .stSelectbox > div > div {
                width: 350px !important;  /* Fixed width for the select box */
            }

            /* Ensure the first column has the desired width */
            .stContainer > div:first-child {
                width: 350px !important;  /* Set the width for the first column */
            }

            /* Ensure the second column fills the remaining space */
            .stContainer > div:nth-child(2) {
                width: calc(100% - 350px) !important;  /* Adjust width for second column */
            }

            /* Vertical alignment for the columns */
            .stColumn {
                display: flex;
                align-items: flex-end;  /* Align content to the bottom */
            }

            /* Set fixed size for buttons, if needed */
            .stButton {
                width: 300px; /* Optional: set a fixed width for buttons */
                margin-left: 0; /* Align the button to the left */
            }
                
        .stImage img {
            display: block;
            margin-left: 50px;
            margin-right: 450px;
            max-width: 1020px !important;  /* Max width to ensure it doesn't get too large */
            width: 100%;  /* Ensures the image scales properly */
        }
        </style>
    """, unsafe_allow_html=True)

def select_measure_box(measures):
    """Function to create and handle the select box that permits the measure selection."""
    # Allow the user to select a specific measure if available
    if measures:
        measure_keys = list(measures.keys())
        is_disabled = False  # Enable select box if measures are available
    else:
        measure_keys = ["No measure available"]  # Default option if no measures exist
        is_disabled = True  # Disable select box if no measures exist

    selected_measure_key = st.selectbox(
        "Select Measure", 
        measure_keys, 
        key="measure_select", 
        disabled=is_disabled  # Disable interaction if no measures
    )

    # Handle the selection if a valid measure is chosen
    if not is_disabled and selected_measure_key != "No measure available":
        return measures[selected_measure_key]  # Return the selected measure
    return None  # Return None if no valid measure is selected
  
def selectPlotType(selected_measure):
    """Function to create and handle the select box that permits the plot type selection."""
    # Add the select box for plot types, with a default "Select Plot Type" option
    plot_types = ['Select Plot Type', 'Raw Signals', 'Filtered Signals [Cheby II]', 'Filtered Signals [MAF]', 'Raw and Filtered Signals [Cheby II]', 'Raw and Filtered Signals [MAF]', 'Filtered Signals Comparison', 'FFT']
    selected_plot_type = st.selectbox("Select Plot Type", plot_types)

    # Initialize the buffer variable
    plot_buf = None

    # Check if a measure is selected and plot based on the selected type
    if selected_measure != "No measure available" and selected_plot_type != 'Select Plot Type':
        if selected_plot_type == "Raw Signals":
            plot_buf = plotRawData(selected_measure)
        elif selected_plot_type == "Filtered Signals [Cheby II]":
            plot_buf = plotFilteredDataCheby(selected_measure)
        elif selected_plot_type == "Raw and Filtered Signals [Cheby II]":
            plot_buf = plotRawAndFilteredDataCheby(selected_measure)
        elif selected_plot_type == "Filtered Signals [MAF]":
            plot_buf = plotFilteredDataMAF(selected_measure)
        elif selected_plot_type == "Raw and Filtered Signals [MAF]":
            plot_buf = plotRawAndFilteredDataMAF(selected_measure)
        elif selected_plot_type == "Filtered Signals Comparison":
            plot_buf = plotFilteredDataComparison(selected_measure)

        elif selected_plot_type == "FFT":
            plot_buf = plotFFT(selected_measure)

    return plot_buf

def delete_measure_bt(selected_measure, measures, file_path):
    """Function to create and handle the button that permits the deletion of a measure."""
    # Add a button to remove the selected measure
    if st.button("Delete Selected Measure"):
        if selected_measure:
            # Remove the selected measure from the dictionary
            updated_measures = {key: value for key, value in measures.items() if value != selected_measure}
            
            # Renumber the keys to maintain sequential naming
            updated_measures = {
                f"measure_{i + 1}": value for i, (key, value) in enumerate(updated_measures.items())
            }
            
            # Save the updated measures back to the file
            with open(file_path, "w") as file:
                json.dump(updated_measures, file, indent=4)

            st.success("Selected measure deleted successfully!")

            # Clear the selected measure from session state to avoid issues
            if "selected_measure" in st.session_state:
                del st.session_state["selected_measure"]

            # Re-trigger the app logic by setting a flag
            st.session_state["measure_deleted"] = True

            st.rerun()
        else:
            st.warning("No measure selected to delete.")