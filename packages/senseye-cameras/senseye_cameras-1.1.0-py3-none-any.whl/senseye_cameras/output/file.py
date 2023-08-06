import ffmpeg
import logging
import tempfile
from pathlib import Path

from . output import Output

log = logging.getLogger(__name__)


class File(Output):
    '''
    Records byte streams to a file.
    '''

    def __init__(self, path=None, **kwargs):
        Output.__init__(self, **kwargs)
        self.set_path(path=path)
        self.set_tmp_path(path=self.path)
        self.open()

    def set_path(self, path=None):
        '''Setter for self.path.'''
        self.path = Path(path).absolute()
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)

    def set_tmp_path(self, path):
        '''Generates a tmpfile name in path's directory.'''
        path = Path(path)
        self.tmp_path = tempfile.NamedTemporaryFile(
            prefix=path.stem,
            dir=path.parent,
            suffix=path.suffix,
            delete=True
        ).name

        log.debug(f'{str(self)} tmp path set to {self.tmp_path}')

    def open(self):
        self.output = open(self.tmp_path, 'bw')

    def write(self, data=None):
        if data is not None and self.output:
            try:
                self.output.write(data)
            except: pass

    def close(self):
        if self.output:
            self.output.close()
            self.output = None

            try:
                # make the stream reusable by creating a new tmp path
                old_tmp_path = self.tmp_path
                self.set_tmp_path(self.path)
                if self.path.exists():
                    raise Exception(f'Rename from {old_tmp_path} to {self.path} failed, {self.path} already exists.')
                Path(old_tmp_path).replace(self.path)
            except Exception as e:
                log.error(f'Recording rename failed: {e}')
