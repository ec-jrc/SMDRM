# -*- coding: utf-8 -*-

import pytest
import sys
import pathlib

root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from src.config import TestConfig
from src.observer import FileUpload, FileUploadObserver


observed_path = root / "files_to_upload"
zipfile_path = observed_path / "test.zip"


def make_test_zip_file(path):
    empty_zip_data = b"PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    with open(path, "wb") as zipfile:
        zipfile.write(empty_zip_data)


def test_subject_init_state():
    # subject concrete class implements state and observation logic
    subject = FileUpload(path=observed_path, config=TestConfig)
    assert subject._state is False


def test_attach_observer():
    # subject concrete class implements state and observation logic
    subject = FileUpload(path=observed_path, config=TestConfig)
    # observe the subject's state for updates
    observer = FileUploadObserver()
    assert subject._observers == []
    subject.attach(observer)
    assert observer in subject._observers


def test_detach_observer():
    # subject concrete class implements state and observation logic
    subject = FileUpload(path=observed_path, config=TestConfig)
    # observe the subject's state for updates
    observer = FileUploadObserver()
    subject.attach(observer)
    assert observer in subject._observers
    subject.detach(observer)
    assert observer not in subject._observers


def test_get_files_with_file_create():
    # subject concrete class implements state and observation logic
    subject = FileUpload(path=observed_path, config=TestConfig)
    # ensure it is clean
    subject._cleanup()
    assert subject.get_files() == []
    # create a file
    make_test_zip_file(zipfile_path)
    assert len(subject.get_files()) == 1
    assert zipfile_path in subject.get_files()
    # clean after test
    subject._cleanup()


def test_observe_new_file():
    # subject concrete class implements state and observation logic
    subject = FileUpload(path=observed_path, config=TestConfig)
    make_test_zip_file(zipfile_path)
    subject.observe()
    assert subject._state is True
    # clean after test
    subject._cleanup()


def test_observe_unprocessed_file():
    # make path "dirty"
    make_test_zip_file(zipfile_path)
    # subject concrete class implements state and observation logic
    subject = FileUpload(path=observed_path, config=TestConfig)
    subject.observe()
    assert subject._state is True
    # clean after test
    subject._cleanup()
