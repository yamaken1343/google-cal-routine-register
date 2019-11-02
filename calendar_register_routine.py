from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import calendar

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def calender_register(service, year, month, day, name):
    event = {
        'summary': name,
        'start': {
            'date': '{}-{}-{}'.format(year, month, day)
        },
        'end': {
            'date': '{}-{}-{}'.format(year, month, day)
        }
    }

    event = service.events().insert(calendarId='',  # 登録するカレンダー
                                    body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def main(target_year, target_month, start_id):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


    cal = calendar.Calendar()
    target_month_days = list(cal.itermonthdays(target_year, target_month))

    # 祝日の取得
    syukuzitu = []  # 祝日の日付が入ったリスト
    dtfrom = datetime.date(year=target_year, month=target_month, day=1).isoformat() + "T00:00:00.000000Z"
    dtto = datetime.date(year=target_year, month=target_month, day=max(target_month_days)).isoformat() + "T00:00:00.000000Z"
    events_result = service.events().list(calendarId='ja.japanese#holiday@group.v.calendar.google.com', timeMin=dtfrom,
                                          timeMax=dtto, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        syukuzitu.append(int(start[-2:]))
    print(syukuzitu)

    mnb = ['A', 'B', 'C', 'D']
    youbi = ['月', '火', '水', '木', '金', '土', '日']

    itr = start_user

    for date in cal.itermonthdays2(target_year, target_month):  # 日付と曜日を取得
        if date[0] == 0:  # dateが0は不正
            continue
        if date[1] == 5:  # 土曜
            continue
        if date[1] == 6:  # 日曜
            print()
            continue
        if date[0] in syukuzitu:
            continue
        print(target_month, date[0], youbi[date[1]], mnb[itr % len(mnb)])

        calender_register(service, target_year, target_month, date[0], mnb[itr % len(mnb)])

        itr += 1

    print("!!!!MEMO IT: Next start ID " + str(itr % len(mnb)) + " !!!!")


if __name__ == '__main__':
    main(target_year=2019, target_month=6, start_id=11)
