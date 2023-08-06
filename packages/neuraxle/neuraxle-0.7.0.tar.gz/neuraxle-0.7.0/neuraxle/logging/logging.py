"""
Neuraxle's Logging module
====================================
This module contains the Logging class, which is used to log information about the execution of a pipeline.
It is used by the classes inheriting from BaseStep to log information.
It is also modified by the AutoML class and its Trainer and various Trial repositories-related classes
to log info in various folders.

..
    Copyright 2019, Neuraxio Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
import logging
import sys
from io import StringIO
from typing import IO, Dict, List, Optional

LOGGER_FORMAT = "[%(asctime)s][%(levelname)-8s][%(name)-8s][%(module)-1s.py:%(lineno)-1d]: %(message)s"
LOGGING_DATETIME_STR_FORMAT = '%Y-%m-%d_%H:%M:%S.%f'
FORMATTER = logging.Formatter(fmt=LOGGER_FORMAT, datefmt=LOGGING_DATETIME_STR_FORMAT)
if sys.version_info.major <= 3 and sys.version_info.minor <= 7:
    logging.basicConfig(format=LOGGER_FORMAT, datefmt=LOGGING_DATETIME_STR_FORMAT, level=logging.INFO)
else:
    logging.basicConfig(format=LOGGER_FORMAT, datefmt=LOGGING_DATETIME_STR_FORMAT, level=logging.INFO, force=True)


NEURAXLE_LOGGER_NAME = "neuraxle"

LOGGER_STRING_IO: Dict[str, StringIO] = {}
LOGGER_FILE_HANDLERS: Dict[str, logging.FileHandler] = {}


class _FilterSTDErr(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.WARN


class NeuraxleLogger(logging.Logger):

    @staticmethod
    def from_identifier(identifier: str) -> 'NeuraxleLogger':
        """
        Returns a logger from an identifier.
        :param identifier: The identifier of the logger
        :return: The logger
        """
        logger: NeuraxleLogger = logging.getLogger(identifier)

        logger.with_string_io(identifier)
        return logger

    def with_string_io(self, identifier: str) -> 'NeuraxleLogger':
        """
        Returns a logger from an identifier.
        :param identifier: The identifier of the logger
        :return: The logger
        """
        if identifier not in LOGGER_STRING_IO:
            string_io = StringIO()
            LOGGER_STRING_IO[identifier] = string_io
            self._add_stream_handler("string_io_handler", string_io)
        return self

    def with_file_handler(self, file_path: str) -> 'NeuraxleLogger':
        """
        Returns a logger from an identifier.
        :param identifier: The identifier of the logger
        :return: The logger
        """
        self.without_file_handler()

        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel('DEBUG')
        self._add_partial_handler(f"file_handler:{file_path}", file_handler, level=logging.DEBUG)

        LOGGER_FILE_HANDLERS[self.name] = file_handler
        return self

    def without_file_handler(self) -> 'NeuraxleLogger':
        """
        Returns a logger from an identifier.
        :param identifier: The identifier of the logger
        :return: The logger
        """
        if self.name in LOGGER_FILE_HANDLERS:
            LOGGER_FILE_HANDLERS[self.name].close()
            self.removeHandler(LOGGER_FILE_HANDLERS[self.name])
            del LOGGER_FILE_HANDLERS[self.name]
        return self

    def read_log_file(self) -> List[str]:
        if self.name not in LOGGER_FILE_HANDLERS:
            raise ValueError(
                f"No file handler for logger named `{self.name}`. Perhaps you forgot to call "
                f"`self.with_file_handler`, or removed the file handler?")
        with open(LOGGER_FILE_HANDLERS[self.name].baseFilename, 'r') as f:
            return f.readlines()

    def with_std_handlers(self) -> 'NeuraxleLogger':
        self._add_stream_handler("errr_handler", sys.stderr, logging.WARN)
        self._add_stream_handler("info_handler", sys.stdout, logging.DEBUG, _FilterSTDErr())
        return self

    def get_scoped_string_history(self) -> str:
        return LOGGER_STRING_IO[self.name].getvalue()

    def get_root_string_history(self) -> str:
        return LOGGER_STRING_IO[NEURAXLE_LOGGER_NAME].getvalue()

    def print_root_string_history(self) -> None:
        print(f"{NEURAXLE_LOGGER_NAME} -> str:\n\n"
              f"{LOGGER_STRING_IO[NEURAXLE_LOGGER_NAME].getvalue()}")

    def _add_stream_handler(
        self,
        handler_name: str,
        stream: IO,
        level: Optional[int] = None,
        _filter: Optional[logging.Filter] = None
    ) -> 'NeuraxleLogger':
        handler = logging.StreamHandler(stream=stream)
        return self._add_partial_handler(handler_name, handler, level, _filter)

    def _add_partial_handler(
        self,
        handler_name: str,
        handler: logging.Handler,
        level: Optional[int] = None,
        _filter: Optional[logging.Filter] = None
    ) -> 'NeuraxleLogger':
        handler.setFormatter(FORMATTER)
        handler.set_name(f"{self.name}.{handler_name}")
        if level is not None:
            handler.setLevel(level)
        if _filter is not None:
            handler.addFilter(_filter)
        self.addHandler(handler)
        return self


logging.setLoggerClass(NeuraxleLogger)

NEURAXLE_ROOT_LOGGER: NeuraxleLogger = NeuraxleLogger.from_identifier(NEURAXLE_LOGGER_NAME)
NEURAXLE_ROOT_LOGGER.setLevel(logging.DEBUG)
NEURAXLE_ROOT_LOGGER.with_std_handlers()
