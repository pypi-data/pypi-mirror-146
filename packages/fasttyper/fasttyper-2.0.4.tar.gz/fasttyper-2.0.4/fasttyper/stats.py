from .listener import Action
from datetime import datetime
import os
import csv
import pathlib


class Stats:
    def __init__(self):
        self.correct_chars = 0
        self.incorrect_chars = 0

        self.start_dtime = None
        self.stop_dtime = None

        self.buffer = None
        self.finished = False

    def set_buffer(self, buffer):
        self.buffer = buffer

    def running(self):
        return self.stop_dtime is None

    def signal_running(self):
        if self.start_dtime is None:
            self.start_dtime = datetime.now()

    def signal_valid(self):
        self.signal_running()
        self.correct_chars += 1

    def signal_invalid(self):
        self.signal_running()
        self.incorrect_chars += 1

    def signal_stop(self, finished=False):
        self.stop_dtime = datetime.now()
        self.finished = finished

    @property
    def correct_words(self):
        return self.buffer.correct_words

    @property
    def incorrect_words(self):
        return self.buffer.incorrect_words

    @property
    def total_seconds(self):
        stop_dtime = self.stop_dtime or datetime.now()
        start_dtime = self.start_dtime or datetime.now()
        return (stop_dtime - start_dtime).total_seconds() or 1

    @property
    def total_minutes(self):
        return self.total_seconds / 60

    @property
    def total_words(self):
        return self.incorrect_words + self.correct_words

    @property
    def total_chars(self):
        return self.incorrect_chars + self.correct_chars

    @property
    def wpm(self):
        return self.cpm / 5

    @property
    def cpm(self):
        return self.correct_chars / self.total_minutes

    @property
    def raw_wpm(self):
        return self.raw_cpm / 5

    @property
    def raw_cpm(self):
        return self.total_chars / self.total_minutes

    @property
    def accuracy(self):
        if self.total_chars:
            return self.correct_chars / self.total_chars * 100
        return 100

    def summarize(self, template):
        print(template.format(stats=self))

    def produce_record(self):
        return {
            "start_dtime": self.start_dtime.isoformat(),
            "stop_dtime": self.stop_dtime.isoformat(),
            "total_seconds": self.total_seconds,
            "total_minutes": self.total_minutes,
            "total_chars": self.total_chars,
            "correct_chars": self.correct_chars,
            "incorrect_chars": self.incorrect_chars,
            "total_words": self.total_words,
            "correct_words": self.correct_words,
            "incorrect_words": self.incorrect_words,
            "wpm": self.wpm,
            "cpm": self.cpm,
            "raw_wpm": self.raw_wpm,
            "raw_cpm": self.raw_cpm,
            "accuracy": self.accuracy,
        }

    def export_to_datafile(self, datafile):
        if datafile is None:
            return

        datafile = os.path.expanduser(datafile)
        data_dir, filename = os.path.split(datafile)

        pathlib.Path(data_dir).mkdir(exist_ok=True, parents=True)
        exists = os.path.isfile(datafile)

        record = self.produce_record()

        if not exists:
            with open(datafile, "w") as f:
                writter = csv.DictWriter(f, fieldnames=record.keys())
                writter.writeheader()
                writter.writerow(record)
        else:
            with open(datafile, "a") as f:
                writter = csv.DictWriter(f, fieldnames=record.keys())
                writter.writerow(record)

        print(f"\nwrote stats to {datafile}")
