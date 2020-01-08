"""Test main.py
"""

from starlette.testclient import TestClient
from toolz.curried import pipe, curry
from main import APP, get_auth, upload_to_box
from unittest.mock import patch, Mock
from fastapi import UploadFile
from click.testing import CliRunner
import json
from boxsdk import JWTAuth


client = TestClient(APP)  # pylint: disable=invalid-name


is_ = lambda x: (lambda y: x is y)
equals = lambda x: (lambda y: x == y)

@patch('main.JWTAuth')
def test_auth(jwtauth):
    jwtauth.return_value = JWTAuth
    assert pipe(
        get_auth(
            dict(clientID='test', clientSecret='test'),
            dict(enterpriseID='test'),
            dict(publicKeyID='test', passphrase='test')
        ),
        is_(JWTAuth)
    )

class MockStream(Mock):
    def get_download_url(self):
        return 'https://test.com'

    id = 0

class MockFolder(Mock):
    def create_subfolder(self, folder_name):
        return MockFolder()

    def upload_stream(self, *args):
        return MockStream()

class MockClient(Mock):
    def folder(self, folder_id):
        return MockFolder()


@curry
def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)
    return filename


def get_test_config():
    return pipe(
        dict(
            enterpriseID='test',
            boxAppSettings=dict(
                clientID='test',
                clientSecret='test',
                appAuth=dict(
                    publicKeyID='test',
                    passphrase='test'
                )
            )
        ),
        write_json('test_config.json'),
    )


@patch('main.JWTAuth', autospec=True)
@patch('main.Client', new=MockClient)
@patch('main.get_config_filename', new=get_test_config)
def test_upload_to_box(*args):
    with CliRunner().isolated_filesystem():
        assert pipe(
            get_test_config(),
            upload_to_box(UploadFile('wow'), 'test'),
            equals(dict(file_id=0, download_link='https://test.com'))
        )


@patch('main.JWTAuth', autospec=True)
@patch('main.Client', new=MockClient)
@patch('main.get_config_filename', new=get_test_config)
def test_upload(*args):
    with CliRunner().isolated_filesystem():



if __name__ == '__main__':
    # test_auth()
    test_upload_to_box()
