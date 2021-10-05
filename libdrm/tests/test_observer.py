import pathlib
from unittest.mock import MagicMock

import libdrm.observer

# this path is the under observation with regards to testing
observed_path = pathlib.Path(__file__).resolve().parent


def fake_pipeline(arg1, arg2):
    gen = iter(range(5))
    return fake_step(gen)


def fake_step(gen):
    for _ in gen:
        yield _


def test_subject_init_state():
    # subject concrete class implements state and observation logic
    subject = libdrm.observer.FileUploadSubject(observed_path=observed_path)
    assert subject._state is False


def test_attach_observer():
    # subject concrete class implements state and observation logic
    subject = libdrm.observer.FileUploadSubject(observed_path=observed_path)
    # observe the subject's state for updates
    observer = libdrm.observer.FileUploadObserver(fake_pipeline, [fake_step])
    assert subject._observers == []
    subject.attach(observer)
    assert observer in subject._observers


def test_detach_observer():
    # subject concrete class implements state and observation logic
    subject = libdrm.observer.FileUploadSubject(observed_path=observed_path)
    # observe the subject's state for updates
    observer = libdrm.observer.FileUploadObserver(fake_pipeline, [fake_step])
    subject.attach(observer)
    assert observer in subject._observers
    subject.detach(observer)
    assert observer not in subject._observers


def test_get_files_with_file_create(valid_zipfile):
    # subject concrete class implements state and observation logic
    subject = libdrm.observer.FileUploadSubject(observed_path=observed_path)
    assert len(subject.get_files()) == 1
    assert valid_zipfile in subject.get_files()


def test_observe_no_updates():
    """
    As the subject starts observing the path, the following steps occur:
        1. subject observe the path
        2. subject updates its state
        3. subject notifies the attached observers
        4. observer applies business logic via self.update()
    """
    # subject concrete class implements state and observation logic
    subject = libdrm.observer.FileUploadSubject(observed_path=observed_path)
    # observe the subject's state for updates
    observer = libdrm.observer.FileUploadObserver(fake_pipeline, [fake_step])
    subject.attach(observer)
    # mock the steps and check if they get called
    subject.get_files = MagicMock()
    # start observing
    subject.observe()
    # step 1 / subject observe the path
    assert subject.get_files.called
    # step 2 / subject updates its state
    assert subject._state is False


def test_observe_new_file(valid_zipfile):
    """
    As the subject starts observing the path, the following steps occur:
        1. subject observe the path
        2. subject updates its state
        3. subject notifies the attached observers
        4. observer applies business logic via self.update()
    """
    # subject concrete class implements state and observation logic
    subject = libdrm.observer.FileUploadSubject(observed_path=observed_path)
    # observe the subject's state for updates
    observer = libdrm.observer.FileUploadObserver(fake_pipeline, [fake_step])
    subject.attach(observer)
    # mock the steps and check if they get called
    subject.get_files = MagicMock()
    subject.notify = MagicMock()
    # start observing
    subject.observe()
    # step 1 / subject observe the path
    assert subject.get_files.called
    # step 2 / subject updates its state
    assert subject._state is True
    # step 3 / subject notifies the attached observers
    assert subject.notify.called
