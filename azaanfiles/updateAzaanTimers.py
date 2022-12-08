#!/usr/bin/env python

import datetime
import time
import sys
import QuranPath

sys.path.insert(0, '/home/pi/adhan/crontab')

from praytimes import PrayTimes
PT = PrayTimes()


from crontab import CronTab
system_cron = CronTab(user='pi')

# QPath = QuranPath.FilePath(3) # using class object list
#QPath = QuranPath.getFilePathByID("10") # using database connection
QPath = QuranPath.nextFilePath() # using database connection
# print (QPath)

now = datetime.datetime.now()
strPlayFajrAzaanMP3Command = 'omxplayer -o local  /home/pi/adhan/azaanfiles/fajer.mp3 > /dev/null 2>&1'
strPlayQuranMP3Command = 'omxplayer -o local  /home/pi/adhan/quran/"' + QPath + '" > /dev/null 2>&1'
strPlayAzaansunriseMP3Command = 'omxplayer -o local  /home/pi/adhan/quran/fatiha.mp3 > /dev/null 2>&1'
strPlayAzaanzoharMP3Command = 'omxplayer -o local  /home/pi/adhan/azaanfiles/zohar.mp3 > /dev/null 2>&1'
strPlayAzaanAsrMP3Command = 'omxplayer -o local  /home/pi/adhan/azaanfiles/asser.mp3 > /dev/null 2>&1'
strPlayAzaanmagribMP3Command = 'omxplayer -o local  /home/pi/adhan/azaanfiles/magrib.mp3 > /dev/null 2>&1'
strPlayAzaanishaMP3Command = 'omxplayer -o local  /home/pi/adhan/azaanfiles/isha.mp3 > /dev/null 2>&1'
strUpdateCommand = 'python /home/pi/adhan/updateAzaanTimers.py >> /home/pi/adhan/adhan.log 2>&1'
strClearLogsCommand = 'truncate -s 0 /home/pi/adhan/adhan.log 2>&1'
strJobComment = 'rpiAdhanClockJob'

#Set latitude and longitude here
#--------------------
lat = 39.1630837
long = -76.9080178

#Set calculation method, utcOffset and dst here
#By default system timezone will be used
#--------------------
PT.setMethod('ISNA')
PT.settings.update(asr = 'Hanafi')
utcOffset = -(time.timezone/3600)
isDst = time.localtime().tm_isdst


#HELPER FUNCTIONS
#---------------------------------
#---------------------------------
#Function to add azaan time to cron
def addAzaanTime (strPrayerName, strPrayerTime, objCronTab, strCommand):
  job = objCronTab.new(command=strCommand,comment=strPrayerName)
  timeArr = strPrayerTime.split(':')
  hour = timeArr[0]
  min = timeArr[1]
  job.minute.on(int(min))
  job.hour.on(int(hour))
  job.set_comment(strJobComment)
  print(job)
  return

def addUpdateCronJob (objCronTab, strCommand):
  job = objCronTab.new(command=strCommand)
  job.minute.on(15)
  job.hour.on(3)
  job.set_comment(strJobComment)
  print(job)
  return

def addClearLogsCronJob (objCronTab, strCommand):
  job = objCronTab.new(command=strCommand)
  job.month.on(12)
  job.dom.on(31)
  job.minute.on(0)
  job.hour.on(0)
  job.set_comment(strJobComment)
  print (job)
  return
#---------------------------------
#---------------------------------
#HELPER FUNCTIONS END

# Remove existing jobs created by this script
system_cron.remove_all(comment=strJobComment)

# Calculate prayer times
times = PT.getTimes((now.year,now.month,now.day), (lat, long), utcOffset, isDst)
print ('FAJR ' + ": " + times['fajr'])
print ('QURAN' + ": " + times['quran'])
print ('Sunrise ' + ": " + times['sunrise'])
print ('Dhuhr ' + ": " + times['dhuhr'])
print ('Asr ' + ": " + times['asr'])
print ('Maghrib ' + ": " + times['maghrib'])
print ('Isha ' + ": " + times['isha'])

#print times['fajr']
#print times['sunrise']
#print times['dhuhr']
#print times['asr']
#print times['maghrib']
#print times['isha']

# Add times to crontab
addAzaanTime('fajr',times['fajr'],system_cron,strPlayFajrAzaanMP3Command)
addAzaanTime('quran',times['quran'],system_cron,strPlayQuranMP3Command)
addAzaanTime('sunrise',times['sunrise'],system_cron,strPlayAzaansunriseMP3Command)
addAzaanTime('dhuhr',times['dhuhr'],system_cron,strPlayAzaanzoharMP3Command)
addAzaanTime('asr',times['asr'],system_cron,strPlayAzaanAsrMP3Command)
addAzaanTime('maghrib',times['maghrib'],system_cron,strPlayAzaanmagribMP3Command)
addAzaanTime('isha',times['isha'],system_cron,strPlayAzaanishaMP3Command)

# Run this script again overnight
addUpdateCronJob(system_cron, strUpdateCommand)

# Clear the logs every month
addClearLogsCronJob(system_cron,strClearLogsCommand)

system_cron.write_to_user(user='pi')
print('Script execution finished at: ' + str(now))
