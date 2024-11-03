"""Example package containing the implementation of a file transfer protocol using Ice."""

from pathlib import Path

try:
    import FileTransfer

except ImportError:
    import Ice
    Ice.loadSlice(str(Path(__file__).absolute().parent.joinpath('filetransfer.ice')))
    import FileTransfer
