import streamlit as st
from visualize import render_header, render_annotation, render_generate_data, render_eda, render_view_all_data

# Define page titles
ANNOTATION_PAGE = "Annotation"
GENERATE_DATA_PAGE = "Generate Data"
EDA_PAGE = "EDA"
VIEW_ALL_DATA_PAGE = "View All Data"

# Define sidebar options
SIDEBAR_OPTIONS = [ANNOTATION_PAGE, GENERATE_DATA_PAGE, EDA_PAGE, VIEW_ALL_DATA_PAGE]

# Main function to run the Streamlit app
def main():
    # Render the header
    render_header()

    # Add a sidebar for page navigation
    page_selection = st.sidebar.selectbox("Select Page", SIDEBAR_OPTIONS)

    # Render the selected page
    if page_selection == ANNOTATION_PAGE:
        render_annotation()
    elif page_selection == GENERATE_DATA_PAGE:
        render_generate_data()
    elif page_selection == EDA_PAGE:
        render_eda()
    elif page_selection == VIEW_ALL_DATA_PAGE:
        render_view_all_data()

# Run the app
if __name__ == "__main__":
    main()
