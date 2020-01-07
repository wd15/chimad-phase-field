"""Test main.py
"""

from starlette.testclient import TestClient
from toolz.curried import pipe
from main import APP, get_auth, upload_to_box
from unittest.mock import patch, Mock
from fastapi import UploadFile
from click.testing import CliRunner
import json
from boxsdk import JWTAuth


client = TestClient(APP)  # pylint: disable=invalid-name


is_ = lambda x: (lambda y: x is y)

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



@patch('main.JWTAuth', autospec=True)
@patch('main.Client', new=MockClient)
def test_upload_to_box(*args):
    # mock_folder = Mock(name="mock_folder")
    # mock_subfolder = Mock(name="mock_subfolder")
    # mock_stream = Mock(name="mock_stream")
    # mock_folder.create_subfolder.return_value = mock_subfolder
    # mock_subfolder.upload_stream.return_value = mock_stream
    # mock_stream.id.return_value = 0
    # mock_stream.get_download_url.return_value = 'https://test.com/file'
    # client.folder.return_value = mock_folder

    with CliRunner().isolated_filesystem():
        data = dict(
            enterpriseID='test',
            boxAppSettings=dict(
                clientID='test',
                clientSecret='test',
                appAuth=dict(
                    publicKeyID='test',
                    passphrase='test'
                )
            )
        )
        print(data)
        with open('config_file', 'w') as f:
            json.dump(data, f)
        out = upload_to_box(UploadFile('wow'), 'test')('config_file')

    import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    # test_auth()
    test_upload_to_box()
