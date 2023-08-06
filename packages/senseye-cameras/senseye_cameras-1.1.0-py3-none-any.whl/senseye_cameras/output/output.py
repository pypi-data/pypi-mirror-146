import atexit
import logging

log = logging.getLogger(__name__)


class Output:
    '''General interface for output streams.'''

    def __init__(self, config=None, defaults=None, input_config=None, **kwargs):
        config = config or {}
        defaults = defaults or {}
        input_config = input_config or {}
        self.output = None
        self.config = {**defaults, **input_config, **config}
        # ffmpeg expects gray, not mono8 pixel format.
        if self.config.get('pixel_format') == 'mono8':
            self.config['pixel_format'] = 'gray'

        atexit.register(self.close)

    def open(self):
        log.debug(f'open() not implemented for {str(self)}.')

    def write(self, data=None):
        log.debug(f'write() not implemented for {str(self)}.')

    def close(self):
        log.debug(f'close() not implemented for {str(self)}.')

    def __str__(self):
        return f'{self.__class__.__name__}'
