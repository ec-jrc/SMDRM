# -*- coding: utf-8 -*-

import pathlib

from libdrm import uploader


observed_path = "/tmp/files_to_upload"
zipfile_path = "/tmp/files_to_upload/test.zip"
config = uploader.get_config(env="test")


def make_test_zip_file(path):
    empty_zip_data = b"PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    with open(path, "wb") as zipfile:
        zipfile.write(empty_zip_data)


def test_subject_init_state():
    # subject concrete class implements state and observation logic
    subject = uploader.FileUpload(path=observed_path, config=config)
    assert subject._state is False


def test_attach_observer():
    # subject concrete class implements state and observation logic
    subject = uploader.FileUpload(path=observed_path, config=config)
    # observe the subject's state for updates
    observer = uploader.FileUploadObserver()
    assert subject._observers == []
    subject.attach(observer)
    assert observer in subject._observers


def test_detach_observer():
    # subject concrete class implements state and observation logic
    subject = uploader.FileUpload(path=observed_path, config=config)
    # observe the subject's state for updates
    observer = uploader.FileUploadObserver()
    subject.attach(observer)
    assert observer in subject._observers
    subject.detach(observer)
    assert observer not in subject._observers


def test_get_files_with_file_create():
    # subject concrete class implements state and observation logic
    subject = uploader.FileUpload(path=observed_path, config=config)
    # ensure it is clean
    subject._cleanup()
    assert subject.get_files() == []
    # create a file
    make_test_zip_file(zipfile_path)
    assert len(subject.get_files()) == 1
    assert pathlib.Path(zipfile_path) in subject.get_files()
    # clean after test
    subject._cleanup()


def test_observe_new_file():
    # subject concrete class implements state and observation logic
    subject = uploader.FileUpload(path=observed_path, config=config)
    make_test_zip_file(zipfile_path)
    subject.observe()
    assert subject._state is True
    # clean after test
    subject._cleanup()


def test_observe_unprocessed_file():
    # make path "dirty"
    make_test_zip_file(zipfile_path)
    # subject concrete class implements state and observation logic
    subject = uploader.FileUpload(path=observed_path, config=config)
    subject.observe()
    assert subject._state is True
    # clean after test
    subject._cleanup()
