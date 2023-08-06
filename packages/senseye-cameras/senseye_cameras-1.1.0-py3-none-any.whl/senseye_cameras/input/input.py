import logging
import atexit

log = logging.getLogger(__name__)


class Input:
    '''General interface for cameras or other input streams.'''

    def __init__(self, id=0, config=None, defaults=None):
        config = config or {}
        defaults = defaults or {}
        self.id = id
        self.input = None
        self.config = {**defaults, **config}
        atexit.register(self.close)

    def open(self):
        '''Initializes the input.'''
        log.debug(f'open() not implemented for {str(self)}. There was most likely an error initializing this object.')

    def read(self):
        log.debug(f'read() not implemented for {str(self)}.')
        return None, None

    def close(self):
        '''Properly disposes of the input object.'''
        log.debug(f'close() not implemented for {str(self)}.')

    def __str__(self):
        return f'{self.__class__.__name__}:{self.id}'
