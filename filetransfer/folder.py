"""Folder interface implementation."""

import os
from pathlib import Path
from typing import Optional, List

import Ice

import filetransfer
import filetransfer.datatransfer


class Folder(filetransfer.FileTransfer.Folder):
    def __init__(self, root: str) -> None:
        self._root_ = Path(root).absolute()

    @property
    def real_contents(self) -> List[str]:
        files = []
        for filename in os.listdir(self._root_):
            if self._root_.joinpath(filename).is_dir():
                continue
            files.append(filename)
        return files

    def contents(self, current: Optional[Ice.Current]) -> List[str]:
        return self.real_contents

    def download(self, filename: str, current: Optional[Ice.Current]):
        if filename not in self.real_contents:
            raise filetransfer.FileTransfer.FileNotFound(filename)
        data_transfer = filetransfer.datatransfer.DataTransfer(str(self._root_.joinpath(filename)))
        proxy = current.adapter.addWithUUID(data_transfer)
        return filetransfer.FileTransfer.DataTransferPrx.uncheckedCast(proxy)
