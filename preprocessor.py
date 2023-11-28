import re
import pandas as pd


def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(AM|PM)\s-\s'
    # extracting the message
    messagesDummy = re.split(pattern, data)[1:]
    messages = []
    for i in messagesDummy:
        if i == 'AM':
            continue
        elif i == 'PM':
            continue
        else:
            messages.append(i)

    # extracting the dates
    datesAmPm = re.findall(pattern, data)
    for ele in data:
        if re.search(pattern, ele):
            datesAmPm.append(ele[0: 18])

    pattern2 = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}'
    dates = re.findall(pattern2, data)
    for i in range(min(len(dates), len(datesAmPm))):
        length = 4
        minute = dates[i][(len(dates[i]) - 2): len(dates[i])]
        if (dates[i][len(dates[i]) - 5] != ' '):
            hour = int(dates[i][(len(dates[i]) - 5): (len(dates[i]) - 3)])
            length = 5
        else:
            hour = int(dates[i][(len(dates[i]) - 4): (len(dates[i]) - 3)])
            length = 4

        if datesAmPm[i] == 'PM':
            if hour != 12:
                hour = hour + 12
                time_ = str(hour) + ":" + str(minute)
                dates[i] = dates[i][0: (len(dates[i]) - length)] + time_
        else:
            if hour == 12:
                dates[i] = dates[i][0: (len(dates[i]) - length)] + "0:" + dates[i][(len(dates[i]) - 2): (len(dates[i]))]

    # extracting all info in a dataframe
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    onlyMessage = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # message has user name
            users.append(entry[1])
            onlyMessage.append(entry[2])
        else:
            users.append('group_notification')
            onlyMessage.append(entry[0])

    df['user'] = users
    df['message'] = onlyMessage
    df.drop(columns=['user_message'], inplace=True)

    # year month day hour minute extracting separately
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['just_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    # for heatmap creation
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str(00))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    return df
