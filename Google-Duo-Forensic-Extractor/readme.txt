# H1 Google Duo DB Parser

Operating System: Android (Tested), iOS (Untested)
Release/Version: 15 August 2016
Application: Google Duo

Python file to extract information from Google Duo databases and print the data in human readable csv files.

Usage: 
Extract /data/data/com.google.android.apps.tachyon from Cellebrite/XRY/Oxygen/Android backup to a location on your machine

Have Python 3.5 installed and go to cmd, find the location of the the script and type:
python duo_extract.py

Then follow the instructions and enter the full path to where you extracted the folder earlier.
Then enter where you want the reports to be saved, the same folder works fine for this.

Two converted CSV files will now have been created.


Background:
Data in Google Duo is stored in 3 databases
/data/data/com.google.android.apps.tachyon/databases/CallHistory.db - list of all calls made by the user (Format:SQLite)
/data/data/com.google.android.apps.tachyon/databases/PhoneNumberInfo.db - contact list including hidden and blocked contacts (Format:SQLite)
/data/data/com.google.android.apps.tachyon/shared_prefs/com.google.android.apps.tachyon_preferences.xml - the owners phone number (Format:XML)


Tested in Windows enviroments, requires all three files to work.
