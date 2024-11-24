import streamlit as st
import pandas as pd
import plotly.express as px

# Load the cleaned data (ensure 'cleaned_data.csv' exists in the working directory)
data = pd.read_csv('cleaned_data.csv')

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Conflict Insights: Advanced Data Visualization 🌍",
    layout="wide",
    page_icon="📊"
)

# Title for the dashboard
st.title("Conflict Insights: Injuries & Deaths Over Time 🌍📊")

# Short description with emojis
st.markdown("""
Welcome to an advanced **interactive dashboard** designed for exploring the impact of conflict. 
Dive into insightful visualizations showcasing **injuries and deaths** for Palestinians and Israelis.
The data has been meticulously cleaned, analyzed, and transformed for global exploration. 🚀✨
""")

# Sidebar for Filters
st.sidebar.header("Filters 🧭")
year_range = st.sidebar.slider("Select Year Range", 
                                min_value=int(data["Year"].min()), 
                                max_value=int(data["Year"].max()), 
                                value=(int(data["Year"].min()), int(data["Year"].max())))
months = st.sidebar.multiselect("Select Months", options=data["Month"].unique(), default=data["Month"].unique())

# Filter data based on user input
filtered_data = data[(data["Year"] >= year_range[0]) & (data["Year"] <= year_range[1])]
filtered_data = filtered_data[filtered_data["Month"].isin(months)]

# Display filtered data
st.subheader("Filtered Data Preview 📋")
st.dataframe(filtered_data)

# --- Interactive Time Series Plot with Log Scale ---
st.subheader("Injuries & Deaths Over the Years (Log Scale) 📉")

fig1 = px.line(filtered_data, 
               x='Year', 
               y=['Palestinians Injuries', 'Israelis Injuries', 'Palestinians Killed', 'Israelis Killed'],
               title="Injuries and Deaths Over the Years (Log Scale)",
               labels={'value': 'Count', 'variable': 'Category'},
               markers=True)
fig1.update_layout(
    yaxis_type="log",
    template='plotly_dark',
    hovermode='x unified',
    title_font=dict(size=22),
    xaxis_title="Year",
    yaxis_title="Log Count",
    legend_title="Category"
)
st.plotly_chart(fig1)

# --- Monthly Breakdown of Injuries & Deaths ---
st.subheader("Monthly Breakdown of Injuries & Deaths 📊")

fig2 = px.bar(filtered_data, 
              x='Month', 
              y=['Palestinians Injuries', 'Israelis Injuries', 'Palestinians Killed', 'Israelis Killed'],
              barmode='group',
              labels={'value': 'Count', 'variable': 'Category'},
              title="Monthly Breakdown of Injuries and Deaths")
fig2.update_layout(
    template='plotly_dark',
    hovermode='x unified',
    title_font=dict(size=22),
    xaxis_title="Month",
    yaxis_title="Count",
    legend_title="Category"
)
st.plotly_chart(fig2)

# --- Normalized Heatmap for Injuries ---
st.subheader("Heatmap: Normalized Injuries by Year & Month 🔥")

# Group data by Year and Month for heatmap
data_month_year = filtered_data.groupby(['Year', 'Month'])[['Palestinians Injuries', 'Israelis Injuries', 'Palestinians Killed', 'Israelis Killed']].sum().reset_index()

# Normalize data
normalized_data = data_month_year[['Palestinians Injuries', 'Israelis Injuries', 'Palestinians Killed', 'Israelis Killed']].div(data_month_year[['Palestinians Injuries', 'Israelis Injuries', 'Palestinians Killed', 'Israelis Killed']].max(), axis=1)

# Create Heatmap for Palestinians Injuries
fig3 = px.density_heatmap(data_month_year, 
                          x='Month', 
                          y='Year', 
                          z=normalized_data['Palestinians Injuries'],
                          color_continuous_scale='Viridis',
                          labels={'z': 'Normalized Count'},
                          title="Normalized Heatmap: Palestinians Injuries by Year & Month")
fig3.update_layout(template='plotly_dark', title_font=dict(size=22))
st.plotly_chart(fig3)

# --- Stacked Bar Chart with Log Scale ---
st.subheader("Stacked Bar Chart: Injuries & Deaths by Year (Log Scale) 📊")

fig4 = px.bar(filtered_data, 
              x='Year', 
              y=['Palestinians Injuries', 'Israelis Injuries', 'Palestinians Killed', 'Israelis Killed'],
              barmode='stack',
              labels={'value': 'Count', 'variable': 'Category'},
              title="Stacked Bar Chart: Injuries & Deaths by Year (Log Scale)")
fig4.update_layout(
    yaxis_type="log",
    template='plotly_dark',
    title_font=dict(size=22),
    xaxis_title="Year",
    yaxis_title="Log Count",
    legend_title="Category"
)
st.plotly_chart(fig4)

# --- Correlation Heatmap ---
st.subheader("Correlation Between Injuries & Deaths 🔗")

corr_matrix = filtered_data[['Palestinians Injuries', 'Israelis Injuries', 'Palestinians Killed', 'Israelis Killed']].corr()

fig5 = px.imshow(corr_matrix, 
                 text_auto=True, 
                 color_continuous_scale='Blues', 
                 title="Correlation Heatmap: Injuries & Deaths")
fig5.update_layout(template='plotly_dark', title_font=dict(size=22))
st.plotly_chart(fig5)

# --- Thank You Message ---
st.markdown("""
### Thank You for Exploring! 🙌
This dashboard provides a data-driven perspective on **conflict insights**, revealing patterns of injuries and deaths across time. 
Your exploration helps uncover meaningful trends and foster understanding. 💡✨

---

📘 **Explore More**:  
- Check out the full analysis in my Kaggle notebook:  
  [Tracking Tragedy: Advanced Data Insights](https://www.kaggle.com/code/muhammadsamarshehzad/tracking-tragedy-advance-data-insights-conflict)  
- Original dataset provided by **Zusmani**:  
  [Palestine Body Count Dataset](https://www.kaggle.com/datasets/zusmani/palestine-body-count)

---

Thank you for your time and interest in this important topic! 🙏  
Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/muhammadsamarshehzad/) and share your thoughts. ✨
""")



# Feedback Section
st.markdown("---")
st.markdown("## We'd Love Your Feedback! 💬")
st.markdown(
    """
    ✨ **Your voice matters!** ✨  
    Let us know what you think about this dashboard.  
    Your feedback helps us grow and create better insights! 💡  
    """
)

# Feedback form
with st.form(key="feedback_form"):
    name = st.text_input("Your Name", placeholder="Enter your name", key="name_input")
    feedback = st.text_area(
        "Your Feedback", placeholder="Enter your feedback here...", key="feedback_input"
    )
    submit_button = st.form_submit_button(label="Submit Feedback 📨")

    if submit_button:
        if name.strip() == "" or feedback.strip() == "":
            st.warning("⚠️ Please fill in both fields before submitting.")
        else:
            # Save feedback to a CSV file
            feedback_data = pd.DataFrame({"Name": [name], "Feedback": [feedback]})
            try:
                # Append feedback to an existing CSV file
                feedback_data.to_csv("./feedback.csv", mode="a", index=False, header=False)
            except FileNotFoundError:
                # If the file doesn't exist, create it with headers
                feedback_data.to_csv("feedback.csv", mode="w", index=False, header=True)
            st.success("🎉 Thank you for your feedback! 🙌")

