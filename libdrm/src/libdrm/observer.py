# -*- coding: utf-8 -*-

"""
Design Pattern to track a user-defined directory for updates i.e.,
upload of new files and notify the attached Observers.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import pathlib
import typing

from libdrm.nicelogging import setup_logger


console = setup_logger("smdrm.observer")


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


class FileUploadSubject(Subject):
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

    _seen: set = {}
    _state: bool = False
    _observers: typing.List[Observer] = []

    def __init__(self, observed_path: str):
        super(FileUploadSubject, self).__init__()
        # input path to observe
        self.observed_path = pathlib.Path(observed_path)
        self.observed_path.mkdir(parents=True, exist_ok=True)

    def attach(self, observer: Observer) -> None:
        console.info("{} attached.".format(observer))
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
        console.info("{} removed.".format(observer))

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        console.info("Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    """
    The `ad hoc` business logic methods:
        - List directory content
        - observe path for updates
    """

    def get_logs(self) -> typing.List[pathlib.Path]:
        """
        Helper function to get the list of zip files in the given input directory.
        Uses `UPLOAD_GLOB_PATTERN` glob pattern to search for the file extension in the input path.
        """

        return [_ for _ in self.observed_path.glob("*.log*")]

    def observe(self) -> None:
        """
        It observes the path every OBSERVE_INTERVAL_SEC for new files.
        If new files are detected, update the subject's state, and notify attached observers.
        Delete files when the FileUploadObserver.update() method is called to clean the input directory.
        The subject._state will be set to False once the observe() method is called again after sleeping.
        """

        logs = self.get_logs()
        for file in logs:
            if file in self._seen:
                continue
            self._seen.add(file)
            self._state = True
            self.notify()
            console.info("{}: new file -> state updated: {}".format(file, self._state))


class FileUploadObserver(Observer):
    """
    FileUploadObserver (Concrete Observer) reacts to the updates
    issued by the Subject it had been attached to.
    """

    def update(self, subject: Subject) -> None:
        if subject._state is False:
            console.debug("Subject state did not change... Nothing to do.")
            pass
        console.debug("observed logs: {}".format(subject._seen))
        for file in subject.get_logs():
            if file not in subject._seen:
                console.info(file)
                # TODO processing:
                #   - annotate
                #   - geocode (coming soon...)
                #   -
        else:
            subject._state = False
