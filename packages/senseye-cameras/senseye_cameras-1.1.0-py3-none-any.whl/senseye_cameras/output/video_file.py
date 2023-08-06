import ffmpeg
import logging
from pathlib import Path

from . file import File

log = logging.getLogger(__name__)


class VideoFile(File):
    '''
    Records video to a file.

    Automatically detects the correct codec to use based on the path suffix.
    Supports suffixes: '.avi', '.mp4', '.mkv', '.yuv', '.raw'

    Args:
        path (str): Output path of video.
        config (dict): Configuration dictionary. Accepted keywords:
            fps (int)
            pixel_format (str): pixel format of the incoming raw video
            codec (str)
            format (str): defaults to 'rawvideo'
            res (tuple)
    '''

    def __init__(self, **kwargs):
        defaults = {
            'fps': 30,
            'format': 'rawvideo',
            'pixel_format': 'rgb24',
            'output_pixel_format': 'rgb24',
            'file_codec': {},
            'res': (1280, 720)
        }
        self.process = None
        File.__init__(self, defaults=defaults, **kwargs)

    def open(self):
        if Path(self.path).suffix == '.raw':
            File.open(self)
        else:
            self.generate_file_codec()
            self.initialize_ffmpeg()

    def generate_file_codec(self):
        '''Determines a good codec to use based on path.suffix.'''
        codec_lookup = {
            '.avi': {'vcodec': 'huffyuv'},
            '.mp4': {'vcodec': 'libx264', 'crf': 17, 'preset': 'ultrafast'},
            '.mkv': {'vcodec': 'h264', 'crf': 23, 'preset': 'ultrafast'},
            '.yuv': {'vcodec': 'rawvideo'}
        }

        suffix = Path(self.path).suffix
        self.config['file_codec'] = codec_lookup.get(suffix, None)
        if self.config['file_codec'] is None:
            raise Exception(f'File extension {suffix} not supported.')

    def initialize_ffmpeg(self):
        '''Initializes ffmpeg.'''
        # only include pixel_format and size if we're encoding raw video.
        raw_args = dict(
            pix_fmt=self.config.get('pixel_format'),
            s=f'{self.config.get("res")[0]}x{self.config.get("res")[1]}'
        ) if self.config['format'] == 'rawvideo' else {}

        self.process = (
            ffmpeg
            .input(
                'pipe:',
                format=self.config.get('format'),
                framerate=self.config.get('fps'),
                **raw_args
            )
            .output(
                self.tmp_path,
                **self.config.get('file_codec'),
            )
            # hide logging
            .global_args('-loglevel', 'error', '-hide_banner')
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )
        log.info(f'Running command: {" ".join(self.process.args)}')
        self.output = self.process.stdin

    def close(self):
        if self.process and self.process.poll() == None:
            try:
                self.process.communicate(timeout=5)
            except Exception as e:
                log.warning(f'Failed to end process cleanly with error {e}. Killing...')
                self.process.kill()
                outs, errs = self.process.communicate()
                log.error(f'Process kill results: {errs}')

        File.close(self)
