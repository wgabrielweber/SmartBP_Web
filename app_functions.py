import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

def pending_categorization(measures, file_path):
    # Initialize a list to collect rows for the table
    table_data = []

    # Extract and organize measures
    for parameter, measurements in measures.items():
        for measure_id, measure_data in measurements.items():
            category = measure_data.get("category", "")  # Get category or empty string
            table_data.append({
                "Parameter": parameter,
                "Measure ID": measure_id,
                "Timestamp": measure_data.get("timestamp", ""),
                "Type": measure_data.get("measureType", ""),
                "Frequency": measure_data.get("measureFrequency", ""),
                "Category": category
            })
    
    # Convert to a DataFrame for display
    df = pd.DataFrame(table_data)

    # Filter rows where "Category" is missing or empty
    df_filtered = df[df["Category"].astype(str).str.strip() == ""]

    # Show the editable table
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1]) 
        with col1:
            save_button = st.button("Save Changes")
            if save_button:
                st.success("Changes saved successfully!")
            st.empty()
        with col2:
            edited_df = st.data_editor(df_filtered, use_container_width=True, hide_index=True)

    # Save changes button
    if save_button:
        # Update the JSON file with new categories
        for index, row in edited_df.iterrows():
            parameter = row["Parameter"]
            measure_id = row["Measure ID"]
            category = row["Category"]
            measures[parameter][measure_id]["category"] = category
        
        # Save the updated measures back to the JSON file
        with open(file_path, "w") as f:
            json.dump(measures, f, indent=4)

def categorization_stats(measures):
    """Display statistics for categorized measures."""
    # Initialize a dictionary to count measures per category
    category_counts = {}

    # Loop through all measures to count categories
    for parameter, measurements in measures.items():
        for measure_id, measure_data in measurements.items():
            category = measure_data.get("category", "").strip()
            if not category:
                category = "Uncategorized"
            category_counts[category] = category_counts.get(category, 0) + 1

    # Convert the category counts to a DataFrame for display
    stats_df = pd.DataFrame.from_dict(
        category_counts, orient="index", columns=["Count"]
    ).reset_index()
    stats_df.rename(columns={"index": "Category"}, inplace=True)

    # Sort the DataFrame by "Count" in descending order
    stats_df = stats_df.sort_values(by="Count", ascending=False).reset_index(drop=True)

    # Display the table
    st.write("### Categorization Statistics")
    st.table(stats_df)

    # Plot a bar chart for the category counts
    st.write("### Categorization Distribution")
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1]) 
        with col1:
            st.bar_chart(stats_df.set_index("Category"), horizontal=True)

        with col2:
            # Optional: Plot a pie chart for a visual representation
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(
                stats_df["Count"],
                labels=stats_df["Category"],
                autopct="%1.1f%%",
                startangle=140,
            )
            ax.set_title("Categorization Distribution (Pie Chart)")
            st.pyplot(fig)