import sqlite3
import datetime
import os
import csv

from collections import OrderedDict
from xml.dom import minidom


def main():
    # SQL Queries
    CALL_LOGS = "SELECT other_user_id, other_user_name, timestamp, is_outgoing_call, user_action, duration, is_video_call, called_back FROM call_history"
    CONTACT_LIST = "SELECT record_id, blocked, hidden FROM PhoneNumberInfo"

    file_path = input(
        'Enter the root Google Duo path you have exported/extracted (/data/data/com.google.android.apps.tachyon): ')
    report_path = input('Enter the path you wish the CSV report to be created: ')

    try:
        items = sql_finder(file_path)
        file_dict = {}
        for item in items:
            if 'com.google.android.apps.tachyon_preferences.xml' in item:
                file_dict['Preferences'] = item
            elif 'PhoneNumberInfo.db' in item:
                file_dict['Contacts'] = item
            elif 'CallHistory.db' in item:
                file_dict['Calls'] = item

        users_phone_number = process_user_details(file_dict['Preferences'])
        contact_list = process_contact_list(process_sql(file_dict['Contacts'], CONTACT_LIST))
        call_history = process_call_history(process_sql(file_dict['Calls'], CALL_LOGS), users_phone_number)

        csv_printer(report_path, contact_list, call_history)

    except Exception as error:
        print('Error Occurred! Log: {}'.format(error))


def process_sql(db, query):
    conn = sqlite3.connect(db)
    cursor = conn.execute(query)
    return cursor


def process_contact_list(data):
    contact_list = []
    for row in data:
        d = OrderedDict()
        d['Number'] = row[0]
        d['Blocked'] = bool_changer(row[1])
        d['Hidden'] = bool_changer(row[2])

        contact_list.append(d)
    return contact_list


def process_call_history(data, users_phone_number):
    call_history = []
    for row in data:
        d = OrderedDict()
        d['Users Phone Number'] = users_phone_number
        d['Target Phone Number'] = row[0]
        d['Target Name'] = row[1]
        d['Timestamp'] = datetime.datetime.fromtimestamp(row[2] / 1000).strftime('%Y-%m-%d %H:%M:%S')

        if row[3] == 1:
            d['Outgoing/Incoming'] = 'Outgoing'
        else:
            d['Outgoing/Incoming'] = 'Incoming'

        if row[4] == 1 or row[4] == 2:
            d['User Action'] = 'Accepted'
        else:
            d['User Action'] = 'Missed'

        d['Duration (Seconds)'] = row[5]
        d['Video Call'] = bool_changer(row[6])
        d['Called Back'] = bool_changer(row[7])
        call_history.append(d)

    return call_history


def bool_changer(value):
    if value == 1:
        return 'Yes'
    else:
        return 'No'


def csv_printer(report_path, contact_list, call_list):
    if contact_list:
        with open(os.path.join(report_path, 'PhoneNumberInfo.csv'), 'w', newline='') as f:
            csv_writer(f, contact_list)
            print('Report created : {}'.format(f.name))

    if call_list:
        with open(os.path.join(report_path, 'CallHistory.csv'), 'w', newline='') as g:
            csv_writer(g, call_list)
            print('Report created : {}'.format(g.name))


def csv_writer(report, db):
    dict_writer = csv.DictWriter(report, db[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(db)


def sql_finder(file_path):
    for item in os.listdir(file_path):
        full_item = os.path.join(file_path, item)
        if os.path.isfile(full_item):
            if full_item == os.path.join(file_path, 'PhoneNumberInfo.db') \
                    or full_item == os.path.join(file_path, 'CallHistory.db') \
                    or full_item == os.path.join(file_path, 'com.google.android.apps.tachyon_preferences.xml'):
                print('File Found: {}'.format(full_item))
                yield full_item
        elif os.path.isdir(full_item):
            yield from sql_finder(full_item)


def process_user_details(xml_file):
    xml_doc = minidom.parse(xml_file)
    item_list = xml_doc.getElementsByTagName('string')
    for s in item_list:
        if s.attributes['name'].value == 'user_id':
            return s.firstChild.nodeValue


if __name__ == '__main__':
    main()
