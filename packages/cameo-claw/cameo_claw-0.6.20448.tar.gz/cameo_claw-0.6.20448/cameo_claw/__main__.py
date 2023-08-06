import sys

help_message = '''
python3 -m pip install cameo_claw --upgrade
python3 -c "
from cameo_claw import it_filter
lst_url=[
'https://cameo-claw-data.vercel.app/device_21152332479_daily_2022-03-30.csv',
'https://cameo-claw-data.vercel.app/device_21152332479_daily_2022-03-31.csv']
int_total=len(lst_url)
target_directory = './data/topic_filter/'
lst_distinct_column = ['deviceId', 'localTime', 'sensorId']
lst_column_match=[
    ['sensorId','pm2_5'],
    ['sensorId','voc']
]
sort_column='localTime'
for int_progress, done_url in it_filter(lst_url, target_directory, lst_distinct_column, lst_column_match, sort_column):
    print(f'int_progress/int_total = {int_progress}/{int_total}')
    print(f'done url: {done_url}')
"
'''


def show_help():
    if len(sys.argv) == 1:
        print(help_message)


if __name__ == '__main__':
    show_help()
