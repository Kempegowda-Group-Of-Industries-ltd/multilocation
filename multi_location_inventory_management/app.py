import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Set page configuration
st.set_page_config(
    page_title="Multi-location Inventory Management",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📦 Multi-location Inventory Management")
st.write("Manage your inventory across multiple locations with ease. Upload your CSV file to explore your inventory data through visualizations and statistics.")

# Sidebar header
st.sidebar.header("File Upload Section")

# Create an 'uploads' directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# File upload logic
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Save the uploaded file to the 'uploads' directory
    save_path = os.path.join("uploads", uploaded_file.name)
    
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.sidebar.success(f"File successfully saved at: {save_path}")

    # Read the uploaded CSV file
    df = pd.read_csv(save_path)

    # Displaying the data
    st.subheader("Uploaded Data Preview")
    st.write("Here is a preview of the uploaded inventory data:")
    st.dataframe(df)

    # Displaying basic statistics
    st.subheader("Basic Data Statistics")
    st.write("Some basic statistics of your inventory data:")
    st.write(df.describe())

    # Sidebar options for analysis
    st.sidebar.subheader("Analysis Options")
    location = st.sidebar.selectbox("Select Location to Filter", df["Location"].unique())

    # Filter data by selected location
    st.subheader(f"Inventory Data for {location} Location")
    filtered_df = df[df["Location"] == location]
    st.dataframe(filtered_df)

    # Plotting section with interactive visualizations
    st.subheader(f"Visualizations for {location}")
    
    # Bar Chart for Inventory Count
    st.markdown("### Inventory Count by Item")
    bar_chart = px.bar(filtered_df, x="Item", y="Count", title='Inventory Count by Item',
                        labels={'Item': 'Item', 'Count': 'Count'},
                        template='plotly_dark')
    st.plotly_chart(bar_chart, use_container_width=True)

    # Pie Chart for Distribution of Inventory by Item Category
    st.markdown("### Inventory Distribution by Item Category")
    inventory_distribution = df.groupby("Category")["Count"].sum().reset_index()
    pie_chart = px.pie(inventory_distribution, names='Category', values='Count', 
                        title='Inventory Distribution by Item Category',
                        template='plotly_dark')
    st.plotly_chart(pie_chart, use_container_width=True)

    # Scatter plot for Inventory Value vs Count
    st.markdown("### Scatter Plot: Inventory Value vs Count")
    scatter_plot = px.scatter(filtered_df, x="Value", y="Count", 
                               color="Category", title="Inventory Value vs Count",
                               labels={'Value': 'Inventory Value', 'Count': 'Count'},
                               template='plotly_dark')
    st.plotly_chart(scatter_plot, use_container_width=True)

    # Filter out non-numeric columns for correlation
    numeric_df = df.select_dtypes(include=['float64', 'int64'])

    # Calculate correlation matrix
    correlation = numeric_df.corr()

    # Display correlation matrix
    st.subheader("Correlation Heatmap")
    st.write("Heatmap of the correlation between numeric variables:")

    # Plot heatmap using Plotly
    fig = ff.create_annotated_heatmap(
        z=correlation.values,
        x=list(correlation.columns),
        y=list(correlation.index),
        annotation_text=correlation.round(2).values,
        colorscale='Viridis',
    )
    st.plotly_chart(fig, use_container_width=True)

    # Additional insights
    st.subheader("Insights")
    st.write(f"**Total Count for {location}:** {filtered_df['Count'].sum()}")
    st.write(f"**Total Inventory Value for {location}:** ${filtered_df['Value'].sum():,.2f}")

else:
    st.sidebar.info("Please upload a CSV file to get started.")
    st.write("Awaiting file upload...")

# Footer
st.markdown("""<hr>
    <small>Developed by [Your Name]. Powered by Streamlit.</small>
    """, unsafe_allow_html=True)
