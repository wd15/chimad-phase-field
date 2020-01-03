# curl http://localhost:8000/files/ -X POST -H "Content-Type: application/json" -d @./test.data
#
# Also try:
#
#   curl -X "POST" -F "fileb=@./shell.nix" http://localhost:8000/files/?uuid=$(uuidgen)
#
# Todo:
#
#  - enable file upload and write to box with unique ID
#  - functionalize code
#  - lint
#  - set up test cases
#  - test on heroku


from boxsdk import OAuth2, Client
from fastapi import FastAPI
from fastapi import FastAPI
import requests
from toolz.curried import curry, get, compose, get_in, juxt, identity
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from pydantic import BaseModel, UrlStr
from fastapi import FastAPI, File, Form, UploadFile, Query
from boxsdk import JWTAuth
import json
from uuid import UUID
import uuid
# from fn import sequence, perform_readjson, DataEffect, get_data
# from effect import TypeDispatcher, sync_perform



CONFIG_FILE = '1014649_e91k0tua_config.json'


def sequence(*args):
    """Compose functions in order

    Args:
      args: the functions to compose

    Returns:
      composed functions

    >>> assert sequence(lambda x: x + 1, lambda x: x * 2)(3) == 8
    """
    return compose(*args[::-1])


def get_auth(settings, data, appAuth):
    return JWTAuth(
        client_id=settings['clientID'],
        client_secret=settings['clientSecret'],
        enterprise_id=data['enterpriseID'],
        jwt_key_id=appAuth['publicKeyID'],
        rsa_private_key_file_sys_path='./cert.pem',
        rsa_private_key_passphrase=appAuth['passphrase']
    )


def get_json(filename):
    with open(filename) as file_stream:
        return json.load(file_stream)


@curry
def upload_to_box(upload_file, folder_name, config_file):
    return sequence(
        get_json,
        juxt(get('boxAppSettings'), identity, get_in(['boxAppSettings', 'appAuth'])),
        lambda x: get_auth(*x),
        Client,
        lambda x: x.folder(folder_id='0'),
        lambda x: x.create_subfolder(folder_name),
        lambda x: x.upload_stream(upload_file.file, upload_file.filename),
        lambda x: dict(
            file_id=x.id,
            download_link=x.get_download_url()
        )
    )(config_file)


APP = FastAPI()  # pylint: disable=invalid-name


APP.add_middleware(
    CORSMiddleware,
    # allow_origins=[
    #     "http://127.0.0.1:4000",
    #     "https://pages.nist.gov",
    #     "https//travis-ci.org",
    # ],
    # allow_origins=["*"],
    allow_origin_regex=r"https://random-cat-.*\.surge\.sh",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@APP.post("/files/")
async def create_file_on_box(uuid: UUID, fileb: UploadFile = File(...)):
    return upload_to_box(fileb, str(uuid), CONFIG_FILE)


if __name__ == "__main__":
    # run with python main.py to debug
    import uvicorn
    uvicorn.run(APP, host="0.0.0.0", port=8000)
