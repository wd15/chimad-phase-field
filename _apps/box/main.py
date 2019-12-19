import json
from boxsdk import JWTAuth

with open('1014649_e91k0tua_config.json') as json_file:
    data = json.load(json_file)
    print(data)

settings = data['boxAppSettings']
appAuth = settings['appAuth']

auth = JWTAuth(
    client_id=settings['clientID'],
    client_secret=settings['clientSecret'],
    enterprise_id=data['enterpriseID'],
    jwt_key_id=appAuth['publicKeyID'],
    rsa_private_key_file_sys_path='./cert.pem',
    rsa_private_key_passphrase=appAuth['passphrase']
)

access_token = auth.authenticate_instance()

#from boxsdk import Client

#client = Client(auth)
#print('got here')

#root_folder = client.folder(folder_id='0')
#print('got here')
#shared_folder = root_folder.create_subfolder('test3')
#uploaded_file = shared_folder.upload('./main.py')
