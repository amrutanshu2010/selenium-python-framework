import logging
import inspect

def customLogger(logLevel= logging.DEBUG):
    # get the name of class or method where this function is called
    loggerName = inspect.stack()[1][3]
    logger = logging.getLogger(loggerName)
    # set the level for logger
    logger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler("C:\\Users\\amrut\\PycharmProjects\\pythonProject\\letskodeit\\automation.log", mode='a')
    fileHandler.setLevel(logLevel)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    return logger