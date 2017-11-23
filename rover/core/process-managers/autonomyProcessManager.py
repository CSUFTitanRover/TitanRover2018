import logging
import time

def Main():
    t = time.strftime("%m%d%Y-%H%M%S")
    logging.basicConfig(filename='debug/autonomyDump_' + t + '.log',filemode = 'w', level=logging.DEBUG)
    logging.info('Started log at ' + t)

    t = time.strftime("%m%d%Y-%H%M%S")
    logging.info('Stopped log at ' + t)
     
if __name__ == '__main__':
    Main()