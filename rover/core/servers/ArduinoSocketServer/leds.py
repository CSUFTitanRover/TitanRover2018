from smbus2 import SMBusWrapper
import time
ADDRESS = 0x04

def writeToBus(roverMode, frequency):
    if roverMode not in range(11) or frequency not in range(11):
        return False
    #if type(mode) != int or type(freq) != int:
    #return False
    try:
        with SMBusWrapper(1) as bus:
            bus.write_byte_data(ADDRESS, roverMode, frequency)
        return True
    except IOError:
        return False

def main():

    if __name__ == '__main__':
        main()


