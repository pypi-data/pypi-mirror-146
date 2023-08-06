import glob
from pathlib import Path

from webwatcher.MediaFile import MediaFile
from webwatcher.args import config


def get_exclude_dirs():
    exclude = list()
    for path in config.exclude_dirs:
        if path.is_absolute():
            exclude.append(path)
        else:
            # Return list of dirs with watch_dir appended
            exclude.extend([watch / path for watch in config.watch_dirs])
    return exclude


def get_all_files():
    # Get all files from all watched dirs
    all_files = []
    for d in config.watch_dirs:
        watch_dir = Path(d)
        files = [Path(f) for f in glob.glob(f'{watch_dir.resolve()}/**/*', recursive=True) if Path(f).is_file()]
        for f in files:
            all_files.append((f, watch_dir))
    return all_files


def convert_existing_files(file_pairs):
    for path, parent in file_pairs:
        media = MediaFile(path, parent=parent)
        media.process_file()


def convert_existing_file(file_pair):
    path, parent = file_pair
    exclude = any(path.match(p) for p in ['test/*'])
    if not exclude:
        media = MediaFile(path, parent=parent)
        media.process_file()


def clean_existing_files(file_pairs):
    for path, parent in file_pairs:
        media = MediaFile(path, parent=parent)
        media.clean(copy=True)

