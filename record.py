#!/usr/bin/env python
import argparse
from datetime import datetime
import os, sys, time, errno
import subprocess
import platform
import logging
import shutil
from systemd.journal import JournaldLogHandler

# 172.16.187.99

DEBUG = False
# TODO: uploader

IN_BUFFER = bytearray(33600)

# get an instance of the logger object this module will use
logger = logging.getLogger(__name__)

# instantiate the JournaldLogHandler to hook into systemd
journald_handler = JournaldLogHandler()

# set a formatter to include the level name
journald_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(message)s'
))

# add the journald handler to the current logger
logger.addHandler(journald_handler)

# optionally set the logging level
logger.setLevel(logging.DEBUG)

###          
# Funcion for value of sampling rate for arecord
#
def check_rates(value):
    ivalue = int(value)
    if ivalue < 2000 or ivalue > 192000:
         raise argparse.ArgumentTypeError("%s is invalid rate value." % value)
    return ivalue
###          
# Funcion for check values of durancion and periodic if mode SA (sampling) is activ
#
def check_period(dur, per):
    if dur > per:
         #raise argparse.ArgumentTypeError("%s is invalid. Period must be bigger then durantion." % per)
         sys.stderr.write("Period %s is invalid, must be bigger then durantion.\n" % per)
         sys.exit(1)
    return per
    
###          
# Funcion for parse records
# 
def parse_arguments():
  parser = argparse.ArgumentParser(description='Parse default arguments for script')
  parser.add_argument("Mode",type=str, nargs='?', default="SA", choices=['SA','ST'], 
                    help="Setting style of recording.")
  parser.add_argument("Format", type=str, nargs='?', default="S32_LE", 
                    choices=['S8', 'U8','S16_LE','S16_BE','U16_LE','U16_SE','S24_LE','S24_BE','U24_LE','U24_BE','S32_LE','S32_BE','U32_LE','U32_BE'], 
                    help="Set format of recording")
  parser.add_argument("Channel",type=int, nargs='?', default=2, choices=[1,2],
                    help="Set number of channels.")
  parser.add_argument("Rate", type=check_rates, nargs='?', default=44000, 
                    help="Set rate of recording (Hz).")
  parser.add_argument("Durantion", type=int, nargs='?', default=5, 
                    help="Set durantion of recording (s).")
  parser.add_argument("Period", type=int, nargs='?', default=15, 
                    help="Set period of recording (s).")
  args = parser.parse_args()
  
  if args.Mode == 'SA':
    check_period(args.Durantion, args.Period)
  
  if DEBUG:
    print args.Mode
    print args.Format
    print args.Channel
    print args.Rate
    print args.Durantion
    print args.Period
  return args
  
###          
# Funcion to make subdirectory to save records
# 
def make_subdir():
  filePath = os.path.dirname(os.path.abspath( __file__ )) + "/recording/"
  directory = os.path.dirname(filePath)
  try:
      os.makedirs(directory)
  except OSError as e:
      if e.errno != errno.EEXIST:
          raise
###          
# Func to stard arecord to make record save in wav with parameters
#  - Argumenty: sample/strema (sampling), number of channels (-c), format (-f), rate (-r), durantion (-d), period 
# arecord -f S32_LE -c 2 -r 96000 -d 5 test.wav
def record(dirToSave, nameDevice, args):
  timeNow = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
  timeD = args.Durantion 
  record = 'arecord' + ' -f ' + args.Format + ' -c ' + str(args.Channel) + ' -r ' + str(args.Rate) + ' -d ' + str(args.Durantion) + ' ' +  \
  dirToSave + '/' + timeNow + '-' + nameDevice + '.wav'
  #"recording/" + timeNow + '-' + nameDevice + '.wav'
  #record = 'rec -c 2 '+ "recording/" + timeNow + '-' + nameDevice + '.wav' + ' trim 0 ' + str(args.Durantion)
  #'--file-type raw '
  p = subprocess.Popen(record, shell=True, bufsize=len(IN_BUFFER))
  logger.info('Record wav file into: %s',  dirToSave)
  p.wait()
  
###          
# Function to delete old date from mount disk
# 
def deleteData(dirToSave):
  fileList = os.listdir(dirToSave)
  for fileName in fileList:
   os.remove(dirToSave+"/"+fileName)
      
###          
# Main function
# 
def main():
  # Directory to save date
  dirToSave='/mnt/xfsdata'
  # Delete old data
  #if os.path.exists("recording"):
  #  shutil.rmtree('recording')
  deleteData(dirToSave)  
  # Set logging
  logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
  # Get name of device to filename
  nameDevice = platform.node()
  # Parse arguments of device 
  args = parse_arguments()
  # Make dir to save records
  #make_subdir()
  # Main loop to recordig
  while True:
    record(dirToSave, nameDevice, args)
    if args.Mode == 'SA':
      timeToSleep = args.Period - args.Durantion
      time.sleep(timeToSleep)
      
# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
    










   


