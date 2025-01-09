import streamlit as st
import json
import pandas as pd
import altair as alt
def show_graph():
        
    # Load the JSON file with utf-8 encoding
    with open('./bb_analysis.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Prepare data for the charts
    post_names = [item.get("caption", "Unnamed") for item in data]
    comments_counts = [item["commentsCount"] for item in data]
    likes_count = [item["likesCount"] for item in data]
    views_count = []

    for item in data:
        if item["type"] == "Video":
            views_count.append(item["videoViewCount"])
        else:
            views_count.append(0)

    # Create DataFrames
    chart_data = pd.DataFrame({"Post Name": post_names, "Comments Count": comments_counts})
    likes_data = pd.DataFrame({"Post Name": post_names, "Likes Count": likes_count})
    views_data = pd.DataFrame({"Post Name": post_names, "Views Count": views_count})

    # Streamlit UI
    # st.title("Social Media Data")

    # Comments Count Chart
    st.subheader("Comments Count for Each Post")
    comments_chart = alt.Chart(chart_data).mark_bar(color="steelblue").encode(
        x=alt.X("Post Name", sort="-y", title="Post Name"),
        y=alt.Y("Comments Count", title="Comments Count"),
        tooltip=["Post Name", "Comments Count"]
    ).properties(
        width=800,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(fontSize=16)

    st.altair_chart(comments_chart, use_container_width=True)

    # Likes Count Chart
    st.subheader("Likes Count for Each Post")
    likes_chart = alt.Chart(likes_data).mark_bar(color="orange").encode(
        x=alt.X("Post Name", sort="-y", title="Post Name"),
        y=alt.Y("Likes Count", title="Likes Count"),
        tooltip=["Post Name", "Likes Count"]
    ).properties(
        width=800,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(fontSize=16)

    st.altair_chart(likes_chart, use_container_width=True)

    # Views Count Chart
    st.subheader("Views Count for Reels")
    views_chart = alt.Chart(views_data).mark_bar(color="green").encode(
        x=alt.X("Post Name", sort="-y", title="Post Name"),
        y=alt.Y("Views Count", title="Views Count"),
        tooltip=["Post Name", "Views Count"]
    ).properties(
        width=800,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(fontSize=16)

    st.altair_chart(views_chart, use_container_width=True)


if __name__ == "__main__":
    show_graph()
