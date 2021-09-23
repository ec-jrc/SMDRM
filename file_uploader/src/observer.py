# -*- coding: utf-8 -*-

"""
Design Pattern to track a user-defined directory for updates i.e.,
upload of new files and notify the attached Observers.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import pathlib
import typing

from .extractor import extract
from .config import (
    Config,
    nicelogging,
)

from libdrm import (
    rabbitmq,
    datamodel,
)


logger = nicelogging(__name__)


class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass


class FileUpload(Subject):
    """
    The Subject owns some important state and notifies observers when the state
    changes.

    For the sake of simplicity, the Subject's state, essential to all
    subscribers, is stored in the `_state` variable.
    states:
        _state=False > no changes
        _state=True > changes observed

    List of subscribers i.e., `_observers`. In real life, the list of subscribers
    can be stored more comprehensively (categorized by event type, etc.).
    """

    _state: bool = False
    _observers: typing.List[Observer] = []

    def __init__(self, path: str, config: typing.Type[Config]):
        super(FileUpload, self).__init__()
        # path to observe
        self._path = pathlib.Path(path)
        self._path.mkdir(parents=True, exist_ok=True)
        # glob pattern for traversing the path
        self._config = config

    def attach(self, observer: Observer) -> None:
        logger.info("{} attached.".format(observer))
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        logger.info("Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    """
    The `ad hoc` business logic methods:
        - List directory content
        - observe path for updates
    """

    def _cleanup(self):
        """
        Helper function to clean up the observed path to start from scratch.
        """
        for file in self.get_files():
            file.unlink()
            logger.warning("{}: removed".format(file))

    def get_files(self):
        """
        Helper function to get the list of files given a directory and a file extension pattern.
        """
        return [f for f in self._path.glob(self._config.path_glob_pattern)]

    def observe(self) -> None:
        """
        Usually, the subscription logic is only a fraction of what a Subject can
        really do. Subjects commonly hold some important business logic, that
        triggers a notification method whenever something important is about to
        happen (or after it).

        Observe the path regularly for new files. Update state, and notify observers if new files are detected.
        """

        logger.info("observing {}".format(self._path))
        # get the current files count
        current_files = self.get_files()
        logger.info("{} files detected.".format(len(current_files)))
        # get the latest path content update
        for _file in current_files:
            if _file:
                self._state = True
                self.notify()


class FileUploadObserver(Observer):
    """
    FileUploadObserver (Concrete Observer) reacts to the updates
    issued by the Subject it had been attached to.
    """

    def update(self, subject: Subject) -> None:
        if subject._state:
            # extract files
            for file in subject.get_files():
                logger.debug("processing {}".format(file))
                for line in extract(file):
                    # build event data model
                    event = datamodel.DisasterEvent.from_dict(line)
                    # to rabbitMQ
                    rabbitmq.produce(event.to_bytes())
                # file is not delete at failures, and it
                # can be processed at the next initialization
                file.unlink()
                logger.warning("processed: file removed")
