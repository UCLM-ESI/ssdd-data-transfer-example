module FileTransfer {

    sequence<byte> Bytes;
    sequence<string> Strings;

    exception FailedToReadData { string reason; };
    exception FileNotFound { string filename; };

    interface DataTransfer {
        Bytes read(int size) throws FailedToReadData;
        void close();
    };

    interface Folder {
        idempotent Strings contents();
        DataTransfer* download(string filename) throws FileNotFound;
    };
};
