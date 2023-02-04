import csv
import os

def time_sec(time):
    h, m, s = time.split(":")
    return int(h)*60*60 + int(m)*60 + int(s)

log = os.getcwd() + "\\log\\"
first = None
last = None

for f in os.listdir(log):
    x = os.path.join(log, f)
    if os.path.isfile(x) and x[-4:] == ".csv":
        print(x)
        with open(x) as csv_file:
            csv_read = csv.reader(csv_file, delimiter=",")
            line = 0
            for row in csv_read:
                if line == 0:
                    line += 1
                elif line == 1:
                    first = row
                    line += 1
                else:
                    last = row
                    line += 1
        x = x.split("\\")[-1][:-4]
        with open(log + x + ".txt", "w") as txt:
            if first == None or last == None or first == last:
                txt.write("Input too short! Try taking another reading.")
            else:
                ft = time_sec(first[0]) - 10
                lt = time_sec(last[0])
                elapsed = lt-ft
                txt.write(f"Time elapsed: {elapsed}s\n")
                tick_s = round(elapsed/int(last[1]), 4)
                tock = int(last[2])
                tock_s = tock*tick_s
                worry = tock*0.2
                txt.write(f"Estimated valid capture time: {tock_s}s\n\n")
                head_high, head_low, neck_fore, neck_back, back_fore, back_back = int(last[3]), int(last[4]), int(last[5]), int(last[6]), int(last[7]), int(last[8])
                txt.write("Time Spent with:\n")
                txt.write(f"Head tilted too high - {head_high*tick_s}s\n")
                txt.write(f"Head tilted too low - {head_low*tick_s}s\n")
                txt.write(f"Neck bent too forward - {neck_fore*tick_s}s\n")
                txt.write(f"Neck bent too backward - {neck_back*tick_s}s\n")
                txt.write(f"Back bent too forward - {back_fore*tick_s}s\n")
                txt.write(f"Back bent too backward - {back_back*tick_s}s\n\n")
                txt.write("Evaluation:\n")
                worried = False
                if head_high > worry or head_low > worry:
                    txt.write("Consider working on your head angle!\n")
                    worried = True
                if neck_fore > worry or neck_back > worry:
                    txt.write("Consider working on straightening your neck!\n")
                    worried = True
                if back_fore > worry or back_back > worry:
                    txt.write("Consider working on straightening your back!\n")
                    worried = True
                if worried == False:
                    txt.write("No areas of concern; keep up the good posture!\n")
                txt.write("\nPlease note this is not a certified medical tool and should only be used as a general guideline.")
                




