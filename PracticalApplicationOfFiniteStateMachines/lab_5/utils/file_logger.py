"""Simple file logger for key-value pair arrays"""


class FileLogger:
    def __init__(self, filename):
        self._file = open(filename, "a+")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        if self._file is not None:
            self._file.close()

    def log(self, states):
        lines = [f"{key}: {value}\n" for key, value in states]
        lines.append("\n")
        if self._file is not None:
            self._file.writelines(lines)
