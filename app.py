# Whatsapp chat analyzer
# Debosmita Mukherjee

import streamlit as st
import preprocessor, helper, sentiment_analysis
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

# file uploading
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None :
    bytes_data = uploaded_file.getvalue()
    # the just uploaded file is in format of byte stream , we need to convert it in string in order to use it
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    # we are trying to do 2 types of analysis:
    #     group level : where analysis will be on perspective of all the users, overall group
    #     user level : for each member of group , we will show analysis of the group separately

    # extracting unique users
    user_list = df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis with respect to : ", user_list)

    if st.sidebar.button("Show Analysis"):
        # shoeing stats of all the chat
        st.title("Top Statistics")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)


        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # showing monthly timeline of messages
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # showing daily timeline of messages
        st.title("Daily Timeline")
        timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['just_date'], timeline['message'])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        # activity heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding busy member of the group(only group level analysis)
        # showing bar chart of only top 5 users
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, show_df = helper.fetch_most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2:
                st.dataframe(show_df)

        # wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common 20 words
        most_common_df = helper.most_common_words(selected_user, df)
        # plotting bar chart
        st.title("Bar Chart of Most Used Words")
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1]) # horizontal bar chart
        plt.xticks(rotation=90)
        st.pyplot(fig)


        # dff = sentiment_analysis.sentiment_analysis(selected_user, df)
        # st.dataframe(dff)
