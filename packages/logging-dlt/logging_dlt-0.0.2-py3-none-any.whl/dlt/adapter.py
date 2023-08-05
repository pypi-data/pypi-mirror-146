""" module:: dlt.adapter
    :synopsis: The adapter linking the dlt stream into the python logging mechanism.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: CC-BY-NC
"""

import logging

from dlt.protocol import DltLogLevel, DltRecordType
from dlt.serial_port import SerialStreamHandler

LOG_LEVEL_MAPPING = {DltLogLevel.FATAL: logging.FATAL,
                     DltLogLevel.ERROR: logging.ERROR,
                     DltLogLevel.WARN: logging.WARNING,
                     DltLogLevel.INFO: logging.INFO,
                     DltLogLevel.DEBUG: logging.DEBUG,
                     DltLogLevel.VERBOSE: logging.NOTSET}


class DltAdapter(SerialStreamHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, record):
        if record.get("record_type") == DltRecordType.LOG:
            name_contents = ["dlt", ]
            level = LOG_LEVEL_MAPPING.get(record.get("log_level"))
            if level is None:
                level = logging.INFO
            msg = record.get("payload_text")
            if msg is not None:
                keys_for_name = ["ecuid", "sessionid", "applicationid", "contextid"]
                # name_contents.append(value) for key, value in record.items())
                name_contents.extend(
                    [value for key, value in record.items() if (key in keys_for_name and value is not None)])
                name = ".".join(name_contents)
                keys_for_extra = ["timestamp", ]
                extra = {key: val for key, val in record.items() if key in keys_for_extra}
                logger = logging.getLogger(name=name)
                logger.log(level=level, msg=msg, extra=extra)
