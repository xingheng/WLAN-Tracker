import os
import logging
import logging.handlers

loggers = []


def get_logger(module_name, basepath = '.'):
    if not module_name:
        module_name = 'generic'

    if '.' in module_name:
        module_name = module_name.split('.')[0]

    if '/' in module_name:
        module_name = module_name.split('/')[-1]

    basepath = os.path.join(basepath, 'logs')

    if not os.path.exists(basepath):
        os.mkdir(basepath)

    logger = logging.getLogger(module_name)

    if logger in loggers:
        return logger

    logger.setLevel(logging.DEBUG)
    loggers.append(logger)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # console handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # file handler
    filehandler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(basepath, '%s.log' % module_name), when='D')
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    return logger
