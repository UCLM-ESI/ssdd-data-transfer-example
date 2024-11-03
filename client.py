#!/usr/bin/env python3

import sys
import random
import logging
from typing import List

import Ice

import filetransfer


CHUNK_SIZE = 1024


class Client(Ice.Application):
    def run(self, argv: List[str]) -> int:
        try:
            proxy = self.communicator().stringToProxy(argv[1])
        except IndexError:
            logging.error('A proxy is mandatory!')
            return -1

        folder_service = filetransfer.FileTransfer.FolderPrx.checkedCast(proxy)
        if not folder_service:
            logging.error('Given proxy is not a ::FileTransfer::Folder object')
            return -1

        available_files = folder_service.contents()
        if not available_files:
            logging.error('No available files on remote folder')
            return 1

        print('Available files:')
        print('\n'.join(available_files))
        target_file = random.choice(available_files)
        print(f'Downloading: {target_file}')

        transfer = folder_service.download(target_file)
        fd = open("tempfile", 'wb')
        downloading = True
        while downloading:
            data = transfer.read(CHUNK_SIZE)
            if len(data) < CHUNK_SIZE:
                downloading = False
            if data:
                fd.write(data)
        fd.close()
        transfer.close()

        return 0


if __name__ == '__main__':
    client = Client()
    sys.exit(client.main(sys.argv))
