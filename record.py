import argparse
from datetime import datetime
import os, sys, time, errno
import subprocess
import platform
import logging
import shutil

DEBUG = False
# TODO: logging do journalctl, uploader

IN_BUFFER = bytearray(33600)
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
def record(nameDevice, args):
  timeNow = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
  #record = 'arecord' + ' -f ' + args.Format + ' -c ' + str(args.Channel) + ' -r ' + str(args.Rate) + ' -d ' + str(args.Durantion) + ' ' +  \
  #"recording/" + timeNow + '-' + nameDevice + '.wav'
  record = 'rec -c 2 '+ "recording/" + timeNow + '-' + nameDevice + '.wav' + ' trim 0 ' + str(args.Durantion)
  p = subprocess.Popen(record, shell=True, bufsize=len(IN_BUFFER))
  p.wait()
  #p.terminate()

###          
# Main function
# 
def main():
  # Delete old data
  if os.path.exists("recording"):
    shutil.rmtree('recording')
  # Set logging
  logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
  # Get name of device to filename
  nameDevice = platform.node()
  # Parse arguments of device 
  args = parse_arguments()
  # Make dir to save records
  make_subdir()
  
  #logging.debug("Pizza created")
  # Main loop to recordig
  while True:
    record(nameDevice, args)
    if args.Mode == 'SA':
      timeToSleep = args.Period - args.Durantion
      time.sleep(timeToSleep)
    else:
      time.sleep(0.1)  
      
    
# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()

