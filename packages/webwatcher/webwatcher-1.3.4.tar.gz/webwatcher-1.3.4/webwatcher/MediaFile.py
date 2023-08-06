import os
import shutil
import signal
import subprocess
import sys
from pathlib import Path, WindowsPath
import ffmpeg

from webwatcher.args import config, IS_DOCKER
from webwatcher.logging import logger


class MediaFile:

    def __init__(self, path: Path, parent: Path = None):
        self.path = path
        self.parent = parent if parent else path
        self.is_media = False
        self.converted = False
        self.delete = config.delete_media
        self.keep = not self.delete
        self.dest = path
        self.failed = False

        # Set parent based on watch_dir
        for i, p in enumerate(self.path.parents):
            if p in config.watch_dirs:
                self.parent = p
                break

        # If only watch directory is /watch
        if len(config.watch_dirs) == 1 and config.watch_dirs[0] == '/watch':
            # Make source relative to watch directory
            self.source = config.source_dir / self.path.relative_to(self.parent.resolve())
        else:
            # Make source location relative to drive (to avoid duplicate paths)
            self.source = config.source_dir / self.path.relative_to(self.path.parents[-1].resolve())


        if self.path.suffix in config.audio_convert_formats:
            self.dest = self.dest.with_suffix('.webm')
            self.is_media = True
            self.is_audio = True
            self.keep = not config.keep_audio
        elif self.path.suffix in config.image_convert_formats:
            self.dest = self.dest.with_suffix('.webp')
            self.is_media = True
            self.is_image = True
            self.keep = not config.keep_images

        if not IS_DOCKER:
            self.source = config.source_dir / self.path.relative_to(self.path.anchor)

    def copy_to_source(self, override=False, move=False):
        """
        Copies the original file to the source folder, relative to the watch directory.
        :param override: boolean
        :param move: Move file instead of copying
        """
        if config.copy_source and not override:
            # Create source destination if not exists
            if not config.dry_run:
                self.source.parent.mkdir(exist_ok=True, parents=True)

            # Only copy if file doesn't exist already
            if not self.source.exists():
                logger.info(f'COPY:\t{self.source}')
                # Copy source to new folder
                if not config.dry_run:
                    if move:
                        shutil.move(self.path, self.source)
                    else:
                        shutil.copy(self.path, self.source)

    def convert(self):
        """
        Converts the input file based on its media type (audio or image)
        :return: success
        """
        # Exit if not media file
        if not self.is_media:
            return True

        if self.dest.suffix == '.webm':
            return self.convert_audio()
        elif self.dest.suffix == '.webp':
            return self.convert_image()

    def delete_file(self):
        # If the file was a supported extension
        logger.info(f'DELETE:\t{self.path.resolve()}')
        if not config.dry_run:
            self.path.unlink(missing_ok=True)

    def clean(self, copy=False):
        """
        Delete the source file it not in dry run mode
        """
        if self.is_media:
            if self.dest.exists() or config.force:
                if copy:
                    try:
                        self.copy_to_source(move=True)
                        self.delete_file()
                    except PermissionError:
                        logger.warn('Unable to copy source file.')

        elif config.all:
            if self.path.suffix not in ['.webm', '.webp']:
                if copy:
                    self.copy_to_source(move=True)
                self.delete_file()

    def convert_audio(self, overwrite=False):
        """
        Process the audio file with ffmpeg
        :param overwrite: bool
        :return: success<bool>
        """
        if not self.dest.exists() or overwrite:
            short_args = [
                'ffmpeg', '-y',
                '-i', f'"{self.path.relative_to(self.parent).resolve()}"',
                '-map', '0:a',
                '-c:a', 'libopus',
                '-quality', '100',
                f'"{self.dest.relative_to(self.parent).resolve()}"'
            ]
            logger.info(' '.join(['AUDIO: ', *short_args]))
            if not config.dry_run:
                try:
                    if config.audio_bitrate:
                        logger.info('Using custom audio bitrate')
                        (ffmpeg
                         .input(f'{self.path.resolve()}')
                         .output(f'{self.dest.resolve()}', map='0:a', format='webm', acodec='libopus', audio_bitrate=config.audio_bitrate)
                         .run(capture_stdout=True, capture_stderr=True)
                         )
                    else:
                        logger.info('NOT using custom audio bitrate')
                        (ffmpeg
                            .input(f'{self.path.resolve()}')
                            .output(f'{self.dest.resolve()}', map='0:a', format='webm',acodec='libopus', quality=100)
                            .run(capture_stdout=True, capture_stderr=True)
                        )
                    self.converted = True
                    return True
                except ffmpeg.Error as e:
                    logger.info(f'ffmpeg encountered an error converting audio file {self.path.resolve()}')
                    self.failed = True
                    return False
            return True

    def convert_image(self, overwrite=False):
        """
        Process the image file with ImageMagick
        :param overwrite: bool
        :return: success<bool>
        """
        code = 0
        # Only run conversion if destination file does not exist.
        if not self.dest.exists() or overwrite:
            args = [
                config.webp_command,
                f'{self.path.resolve()}',
                '-quality', config.webp_quality,
                f'{self.dest.resolve()}'
            ]
            short_args = [
                config.webp_command,
                f'"{self.path.relative_to(self.parent).resolve()}"',
                '-quality', config.webp_quality,
                f'"{self.dest.relative_to(self.parent).resolve()}"'
            ]
            logger.info(' '.join(['IMAGE: ', *short_args]))
            if not config.dry_run:
                p = subprocess.run(args)
                code = p.returncode
            if code == 0:
                self.converted = True
                return True
            else:
                self.failed = True
                return False

    def process_file(self):
        """
        Converts the file, followed by a copy and clean
        """
        self.convert()
        if not self.failed:
            self.clean(copy=True)

