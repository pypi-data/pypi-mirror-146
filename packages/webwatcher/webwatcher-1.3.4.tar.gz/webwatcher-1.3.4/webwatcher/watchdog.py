import os
from pathlib import Path
from time import sleep

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers.polling import PollingObserver

from .MediaFile import MediaFile
from .args import config, IS_DOCKER
from .logging import logger
from .utils import get_exclude_dirs


def on_created(event):
    logger.info(f"CREATED: {event.src_path}")
    size = -1
    while size != os.path.getsize(event.src_path):
        size = os.path.getsize(event.src_path)
        sleep(1)
    media = MediaFile(Path(event.src_path))
    media.process_file()


def get_observer():
    observer = Observer()
    if config.windows and IS_DOCKER:
        logger.info('WARNING: Using less performant observer because host is Windows.')
        observer = PollingObserver()
    return observer


def schedule_observer(observer):
    fs_handle = PatternMatchingEventHandler(
        patterns=['*'],
        ignore_patterns=get_exclude_dirs(),
        ignore_directories=False,
        case_sensitive=True
    )
    fs_handle.on_created = on_created

    for p in config.watch_dirs:
        path = Path(p)
        if path.exists():
            logger.info(f'Watching directory {path.resolve()}')
            observer.schedule(fs_handle, f'{path.resolve()}', recursive=True)
        else:
            logger.info(f'Skipping watch directory `{path.resolve()}` because it does not exist')
    return observer

