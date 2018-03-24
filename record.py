import argparse
# Argumenty: sample/strema (sampling), number of channels (-c), format (-f), rate (-r), durantion
# arecord -f S32_LE -c 2 -r 96000 -d 5 test.wav

def check_rates(value):
    ivalue = int(value)
    if ivalue < 2000 or ivalue > 192000:
         raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


parser = argparse.ArgumentParser(description='Parse default arguments for script')
parser.add_argument("Sampling",type=str, nargs='?', default="SA", choices=['SA','ST'], 
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

#parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',const=sum, default=max, help='sum the integers (default: find the max)')

args = parser.parse_args()
print args.Sampling
print args.Format
print args.Channel
print args.Rate
print args.Durantion
