import logging

# Filter to pad levelname with spaces on right without padding inside brackets
def fmt_filter(record):
    record.levelname = '[%s]' % record.levelname
    record.funcName = '[%s]' % record.funcName
    return True


logging.basicConfig(
    format='WebWatcher | %(asctime)s | %(levelname)-10s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger('webwatcher')
logger.addFilter(fmt_filter)
