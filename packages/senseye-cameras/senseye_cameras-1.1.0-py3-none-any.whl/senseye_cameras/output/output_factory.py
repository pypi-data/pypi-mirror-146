import logging

from . audio_file import AudioFile
from . h264_pipe import H264Pipe
from . video_file import VideoFile

log = logging.getLogger(__name__)


def create_output(type='file', *args, **kwargs):
    '''
    Factory method for creating a video or audio output interface.
    Supports types: 'h264_pipe', 'file'/'raw'/'ffmpeg'/'video_file', 'audio_file'
    '''
    if type == 'h264_pipe':
        return H264Pipe(*args, **kwargs)
    if type == 'file' or type == 'raw' or type == 'ffmpeg' or type == 'video_file':
        return VideoFile(*args, **kwargs)
    if type == 'audio_file':
        return AudioFile(*args, **kwargs)

    log.warning(f'Output type: {type} not supported.')
