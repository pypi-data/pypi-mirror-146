import signal
from pathlib import Path
from time import sleep

from .args import config
from .logging import logger
from .utils import clean_existing_files, \
    convert_existing_files, get_all_files, convert_existing_file, get_exclude_dirs
from .watchdog import schedule_observer, get_observer
from multiprocessing.dummy import Pool as ThreadPool

observer = get_observer()


def finish(signum, frame):
    logger.info('Exiting application...')
    try:
        observer.stop()
        observer.join()
    except:
        logger.info('Error stopping observer.')
    exit(0)


signal.signal(signal.SIGTERM, finish)
signal.signal(signal.SIGINT, finish)

if config.dry_run:
    logger.info('Dry run enabled.  Will not perform any file operations but will still logger.info output of what would be happening.')

if config.copy_source:
    if not config.source_dir.exists():
        test: Path = config.source_dir
        try:
            if not config.dry_run:
                config.source_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            logger.error('Unable to create source directory.  Will not transfer source files.')

for p in get_exclude_dirs():
    logger.info(f'Excluding directory: {p}')


# Only start watcher if no subcommand is specified or watch command is specified
if config.subcommand is None or config.subcommand == 'watch':
    logger.info('Starting watcher')
    observer = schedule_observer(observer)
    observer.start()

    # New thread pool to process multiple existing files simultaneously
    pool = ThreadPool(config.workers)

    # Run new thread pool from all existing files
    logger.info('Running conversion on existing files.')
    results = pool.map(convert_existing_file, get_all_files())
    logger.info('Finished processing existing files.')
    # Run indefinitely so watchdog can do its thing
    while True:
        sleep(1)

elif config.subcommand == 'clean':
    logger.info('Cleaning existing files')
    clean_existing_files(get_all_files())

elif config.subcommand == 'convert':
    logger.info('Converting existing files')
    convert_existing_files(get_all_files())
