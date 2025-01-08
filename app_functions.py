import streamlit as st
import json
from plots import plotRawSignals, plotCleanedSignals, plotSignalsPeaks, plotSQA, plot_ppg_process, plot_beats

def cssStyling():
    """Handles the CSS styling of the page."""
    st.markdown("""
        <style>
            /* General Container Styling */
            .stContainer {
                margin-bottom: 20px;
            }

            /* Styling for Select Boxes */
            .stSelectbox > div > div {
                width: 275px !important;  /* Fixed width for the select box */
            }

            /* Styling for Buttons */
            .stButton {
                width: 300px;  /* Fixed width for buttons */
                margin-top: 28px;
                margin-left: 0;  /* Align the button to the left */
                border-radius: 5px;
            }

            /* Styling for Images */
            .stImage img {
                display: block;
                margin-left: auto;
                margin-right: auto;
                max-width: 1000px !important;  /* Max width to ensure it doesn't get too large */
                width: 100%;  /* Ensures the image scales properly */
                border-radius: 5px;
            }

        </style>
    """, unsafe_allow_html=True)

def select_box_sensor_params():
    # Select sensor parameters
    sensor_parameters = [
        "Default",
        "800 Hz - 4 samples",
        "1000 Hz - 8 samples",
        "1600 Hz - 8 samples",
        "1600 Hz - 16 samples",
    ]
    selected_param = st.selectbox("Select Sensor Parameters", sensor_parameters)    
    return selected_param

def pills_measure_type():
    """Function to create and handle the select box that permits the measure selection."""
    measure_option = {
                0: "IR Only",
                1: "Red + IR",
            }
    select_measure_type = st.pills(
        "Measure Types for Visualization",
        options=measure_option.keys(),
        format_func=lambda option: measure_option[option],
        selection_mode="single",
    )

    if select_measure_type is None:
        select_measure_type = 0
    
    st.write(
        "Your selected option: "
        f"{measure_option[select_measure_type]}"
    )

    return select_measure_type

def pills_sensor_params(measures):
    param_option = {
        0: "800 Hz - 4 samples",  
        1: "1000 Hz - 8 samples", # Default option
        2: "1600 Hz - 8 samples",
        3: "1600 Hz - 16 samples",
    }

    selected_param = st.pills(
        "Select Sensor Parameters",
        options=param_option.keys(),
        format_func=lambda option: param_option[option],
        selection_mode="single",
    )

    if selected_param is None:
        selected_param = 1  # Default to "1000 Hz - 8 samples"

    st.write(
        "Your selected sensor parameters: "
        f"{param_option[selected_param]}"
    )
    
    # Get the key for the selected parameter (e.g., "1000 Hz - 8 samples")
    selected_param_key = param_option[selected_param]

    # Return the measures corresponding to the selected parameter key
    selected_param_measures = measures.get(selected_param_key, {})

    return selected_param_measures  # Return all measures for the selected key

def select_box_measure(measures, measureType):
    """Function to create and handle the select box that permits the measure selection, filtered by the measureType."""  
    filtered_measures = {}
    # Filter measures based on the measureType argument (0 or 1)
    for measure_key, measure in measures.items():
        if measureType == 0:
            # Measure type 0: Only include measures where RedSignal is an empty string
            if measure.get("RedSignal", "") == "":
                filtered_measures[measure_key] = measure
        elif measureType == 1:
            # Measure type 1: Only include measures where both IrSignal and RedSignal are not empty
            if measure.get("IrSignal", "") != "" and measure.get("RedSignal", "") != "":
                filtered_measures[measure_key] = measure    
    
    # Allow the user to select a specific measure if available
    if filtered_measures:
        measure_keys = list(filtered_measures.keys())
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
        return filtered_measures[selected_measure_key]  # Return the selected measure
    return None  # Return None if no valid measure is selected
  
def delete_measure_bt(sensor_params, selected_measure, measures, file_path):
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

def selectPlotType(selected_measure):
    """Function to create and handle the select box that permits the plot type selection."""
    # Add the select box for plot types, with a default "Select Plot Type" option
    plot_types = ['Select Plot Type', 'Raw Signals', 'Filtered Signals', "Filtered Signals and Peaks", "Signals Quality Assessment", "PPG Process", "Heart Beats"]
    selected_plot_type = st.selectbox("Select Plot Type", plot_types)

    # Initialize the buffer variable
    plot_buf = None

    # Check if a measure is selected and plot based on the selected type
    if selected_measure != "No measure available" and selected_plot_type != 'Select Plot Type':
        if selected_plot_type == "Raw Signals":
            plot_buf = plotRawSignals(selected_measure)
        elif selected_plot_type == "Filtered Signals":
            plot_buf = plotCleanedSignals(selected_measure)
        elif selected_plot_type == "Filtered Signals and Peaks":
            plot_buf = plotSignalsPeaks(selected_measure)
        elif selected_plot_type == "Signals Quality Assessment":
            plot_buf = plotSQA(selected_measure)
        elif selected_plot_type == "PPG Process":
            plot_buf = plot_ppg_process(selected_measure)
        elif selected_plot_type == "Heart Beats":
            plot_buf = plot_beats(selected_measure)
    return plot_buf