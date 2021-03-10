import serial
import glob


def get_serial_acm():
    res = glob.glob("/dev/ttyACM*")
    print("Found the following serial input bus : ", res)
    if len(res) != 0 and res is not None:
        return res[0]


acm = get_serial_acm()


def get_serial_input():
    ser = serial.Serial(acm, 9600)
    return ser.readline().decode('utf-8')
