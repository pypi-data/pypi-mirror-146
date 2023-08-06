# WebWatcher

WebWatcher is a small docker image meant to be a sidecar container to other applications.

WebWatcher will watch folders you specify for new audio or image files and convert them to the much smaller webm/webp formats.

Configurable to do things like keep source files, lossless compression, and quality control.

# Getting Started

## Running

### Python
```shell
python -m webwatcher --path <dir> [--path <other_dir>] [--source-dir <dir>] [...args] [command]
# If you want to copy source file to keep, you should specify a source-path
```

### Docker

```shell
docker run --name webwatcher --rm -D -v /path/to/media/dir:/watch/media -v /path/to/more/media/dir:/watch/extra -v /path/to/storage:/source webwatcher:latest
```

Simply, you run the container, mounting any number of directories under `/watch`, and, if you wish to keep the original files, a folder under `/source`.  Other options can be added either via environment variables using the `-e` flag, or by passing a custom `cmd` to the docker container.

### Docker Compose
```yaml
---
version: "2.1"
services:
  radarr:
    image: registry.gitlab.com/cclloyd1/webwatcher:latest
    container_name: webwatcher
    environment:
      - IS_WINDOWS=true # Only required if running on a Windows host
    volumes:
      - /path/to/media:/watch/media
      - /path/to/storage:/source
    restart: unless-stopped
```



## Subcommands 

| Command   | Description                                                                                                                                                               |
|:----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `clean`   | Moves old files to source if a converted file was found and deletes old files (respecting configuration options)                                                          |
| `watch`   | Default command that is run when no command is specified.  Watches the directories for new files and converts them if it matches a filetype, then cleans up the old file. |
| `convert` | Run a one-time pass of the `watch` command on the directories that will scan all existing files and process them.                                                         |



# Configuration Options

There are a few configuration options available when running the module.  Environment variables have higher priority than command line arguments.

Some CLI args are inverse of the environment variable, because the default behavior is True.

### Default File Types
- **Images:** .png, .jpg, .bmp, .jpeg
- **Audio:** .mp3, .aac, .flac, .wav, .wma, .aac, .m4a, .ogg

## All options

| CLI Argument            | Env Variable    | Description                                                                          | Default                  |
|:------------------------|:----------------|:-------------------------------------------------------------------------------------|:-------------------------|
| `--path <dir>`          | `WATCH_DIRS`    | Path(s) to watch for.  You can use `--path` multiple times.                          | `/watch`                 |
| `--source-dir <path>`   | `SOURCE_PATH`   | Where to store original files                                                        | `/source` or `C:\source` |
| `--dry-run`             | `DRY_RUN`       | Print output but perform no file/conversion operations                               | `False`                  |
| `--no-copy-source`      | `COPY_SOURCE`   | Moves source file to folder after converting                                         | `True`                   |
| `--no-watch-audio`      | `WATCH_AUDIO`   | Watch for new audio files                                                            | `True`                   |
| n/a                     | `DELETE_AUDIO`  | Delete audio files from watch dir once converted                                     | `True`                   |
| `--no-delete-audio`     | n/a             | Inverse of `DELETE_AUDIO`(after copying source)                                      | `False`                  |
| `--audio-format <str>`  | n/a             | Specify another extension to watch for as an audio file.  Can use multiple times.    | -                        |
| `--no-watch-images`     | `WATCH_IMAGES`  | Watch for new image files                                                            | `True`                   |
|                         | `DELETE_IMAGES` | Delete image files from watch dir once converted (after copying source)              | `True`                   |
| `--no-delete-image`     | n/a             | Inverse of `DELETE_IMAGES`                                                           | `False`                  |
| `--image-format <str>`  | n/a             | Specify another extension to watch for as an image file.  Can use multiple times.    | -                        |
| `--webp-command <path>` | `WEBP_COMMAND`  | Set the executable path of ImageMagick, when running as a module[^1]                 | `convert`                |
| `--webp-quality <int>`  | `WEBP_QUALITY`  | Quality when converting to webp.  0 - 100 (lossless).                                | `60`                     |
| `--webp-lossless`       | `WEBP_LOSSLESS` | Losslessly convert to webp (average 20% size reduction)                              | `False`                  |
| `--windows`             | `IS_WINDOWS`    | Use compatibility polling for watching filesystem changes[^2]                        | `False`                  |
| **Subcommands**         |                 | These commands only apply to subcommands, and are only available in the CLI (no env) |                          |
| `--force`               | n/a             | Deletes matching media files even if no matching webm/webp found.                    | `False`                  |
| `--all`                 | n/a             | Deletes ALL files that aren't webm/webp.                                             | `False`                  |

[^1]: On Windows, you would want to set this to `magick`
[^2]: If you are running from docker and mounting a Windows volume, you must specify this for the container to be able to see filesystem changes.


# Planned Changes
- Upload to PyPi
- More conversion options

