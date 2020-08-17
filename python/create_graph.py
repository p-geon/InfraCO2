# 参考: https://gist.github.com/okhiroyuki/070111958a8e8acdb943

import serial
import time
import subprocess
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

bps = 9600
CO2_list = []
clock_list = []

def get_port_num():
    """
    # python側からは見れないっぽい？
    print_port = subprocess.run(["ls" "-l" "/dev/tty.*", "/dev/null"], capture_output=True)
    print(print_port)c
    proc = subprocess.run(['ls', '-l', '/dev/cu.*', '/dev/null'], capture_output=True)
    result = subprocess.run(['ls', '-l', '/dev/cu.usb*'], stdout=subprocess.PIPE)
    print(result.stdout)
    """
    port = '/dev/tty.usbmodem14101'
    #port = "/dev/cu.usbmodem14201"
    return port

def plot_history(CO2_list, clock_list):

    fig = plt.figure(figsize=(8,9), dpi=108)
    ax = fig.add_subplot(1,1,1)
    ax.grid(which="both")
    ax.legend()

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    ax.set_xlabel(today)
    ax.set_ylabel('CO2 density')

    ax.set_ylim([0.0, 2000.0])

    #start_datetime = datetime.datetime(2020, 8, 18, 0, 0,0)
    #end_datetime = datetime.datetime(2020, 8, 18, 1, 0, 0)

    #print(clock_list)

    ax.plot(clock_list, CO2_list, label='CO2 density')
    daysFmt = mdates.DateFormatter('%H:%M:%S')
    #ax.xaxis.set_major_formatter(daysFmt)
    ax.xaxis.set_major_locator(mdates.MinuteLocator(byminute=range(0, 60, 3), tz=None))
    ax.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=range(0, 60, 1), tz=None))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    fig.autofmt_xdate()

    plt.savefig("CO2_timeline.png")
    print("saved graph")

def main():
    with serial.Serial(get_port_num(), bps, timeout=0.1) as ser:
        for i in range(10):
            # 最初の方の値は異常値になりがちなので捨てる
            _ = ser.readline().decode('utf-8')
        while True:
            for i in range(30):
                time.sleep(0.001)
                val_arduino = ser.readline().decode('utf-8')
                if(isinstance(val_arduino, str) and len(val_arduino) > 0):
                    CO2_density = int(val_arduino.split("\n")[0][:-1])
                    CO2_list.append(CO2_density)
                    clock = datetime.datetime.now()
                    clock_list.append(clock)

                    print(clock, CO2_density)

            plot_history(CO2_list, clock_list)

if(__name__ == "__main__"):
    main()