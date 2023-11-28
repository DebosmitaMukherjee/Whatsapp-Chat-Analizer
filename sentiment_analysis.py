# from nltk.sentiment import SentimentIntensityAnalyzer

# sentimentAnalyzer = SentimentIntensityAnalyzer()

def sentiment_analysis(selected_user, df):
    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # df['positive'] = [sentimentAnalyzer.polarity_scores(i)['pos'] for i in df['message']] # storing positive sentiment scores
    # df['negative'] = [sentimentAnalyzer.polarity_scores(i)['neg'] for i in df['message']] # storing negative sentiment scores
    # df['neutral'] = [sentimentAnalyzer.polarity_scores(i)['neu'] for i in df['message']] # storing neutral sentiment scores

    return df

