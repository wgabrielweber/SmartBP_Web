import streamlit as st
from plots import plotRawData, plotRawAndFilteredData, plotFilteredData, plotFFT

def select_measure_box(measures):
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
    # Add the select box for plot types, with a default "Select Plot Type" option
    plot_types = ['Select Plot Type', 'Raw Data', 'Filtered Data', 'Raw and Filtered Data', 'FFT']
    selected_plot_type = st.selectbox("Select Plot Type", plot_types)

    # Initialize the buffer variable
    plot_buf = None

    # Check if a measure is selected and plot based on the selected type
    if selected_measure != "No measure available" and selected_plot_type != 'Select Plot Type':
        if selected_plot_type == "Raw Data":
            plot_buf = plotRawData(selected_measure)
        elif selected_plot_type == "Filtered Data":
            plot_buf = plotFilteredData(selected_measure)
        elif selected_plot_type == "Raw and Filtered Data":
            plot_buf = plotRawAndFilteredData(selected_measure)
        elif selected_plot_type == "FFT":
            plot_buf = plotFFT(selected_measure)

    return plot_buf