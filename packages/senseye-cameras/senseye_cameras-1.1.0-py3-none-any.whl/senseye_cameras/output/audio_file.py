import logging

import soundfile as sf

from . file import File

log = logging.getLogger(__name__)


class AudioFile(File):
    '''
    Records audio to a file.

    Args:
        path (str): Output path of audio.
        config (dict): Configuration dictionary. Accepted keywords:
            channels (int): number of audio channels
            samplerate (int): audio sample rate
            subtype (str): audio type
    '''

    def __init__(self, **kwargs):
        defaults = {
            'channels': 1,
            'samplerate': 44100,
            'subtype': 'PCM_16',
        }
        File.__init__(self, defaults=defaults, **kwargs)

    def open(self):
        self.output = sf.SoundFile(
            self.tmp_path,
            mode='w',
            samplerate=self.config['samplerate'],
            channels=self.config['channels'],
            subtype=self.config['subtype']
        )
