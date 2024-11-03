#!/usr/bin/env python3

"""Ice.Application for running the whole server."""


import sys
from typing import List
from pathlib import Path

import filetransfer.folder

import Ice


ADAPTER_NAME = 'filetransfer'
IDENTITY = 'FileTransfer'


class Server(Ice.Application):
    def run(self, args: List[str]) -> int:
        try:
            root = Path(args[1])
        except IndexError:
            root = Path().cwd()
        folder = filetransfer.folder.Folder(root)

        try:
            adapter = self.communicator().createObjectAdapter(ADAPTER_NAME)
        except Ice.InitializationException:
            adapter = self.communicator().createObjectAdapterWithEndpoints(ADAPTER_NAME, "tcp")

        proxy = adapter.add(folder, self.communicator().stringToIdentity(IDENTITY))
        print(f'Proxy: "{proxy}"', flush=True)
        adapter.activate()

        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()
        return 0


if __name__ == '__main__':
    server = Server()
    sys.exit(server.main(sys.argv))
