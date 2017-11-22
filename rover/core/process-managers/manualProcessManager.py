import logging

def Main():
    t = time.strftime("%m%d%Y-%H%M%S")
    logging.basicConfig(filename='debug\\coreDump_' + t + '.log',level=logging.DEBUG)
    logging.info('Started log at ' + t)

    t = time.strftime("%m%d%Y-%H%M%S")
    logging.info('Stopped log at ' + t)
     
if __name__ == '__main__':
    Main()