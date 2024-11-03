"""DataTransfer interface implementation."""

import logging
from typing import Optional

import Ice

import filetransfer
import filetransfer.datatransfer


class DataTransfer(filetransfer.FileTransfer.DataTransfer):
    def __init__(self, local_filename: str) -> None:
        self._fd_ = open(local_filename, 'rb')

    def read(self, size: int, current: Optional[Ice.Current]):
        if not self._fd_:
            raise filetransfer.FileTransfer.FailedToReadData('Server file descriptor is already closed')
        try:
            return self._fd_.read(size)
        except Exception as error:
            raise filetransfer.FileTransfer.FailedToReadData(str(error)) from error

    def close(self, current: Optional[Ice.Current]) -> None:
        try:
            self._fd_.close()
        except Exception as error:
            logging.error('Failed to close file descriptor:', str(error))
        finally:
            current.adapter.remove(current.id)
