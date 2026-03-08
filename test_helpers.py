import base64
import os


def pre_tests():
    os.system("cp savedata.toml savedatacopy.toml")
    os.system("cp -r testing testing_backup")


def cleanup(exit_code):
    os.system("mv savedatacopy.toml savedata.toml")
    os.system("mv testing_backup testing")
    quit(exit_code)


def base64_encode(img_path):
    with open(img_path, "rb") as i:
        contents = i.read()
    return base64.b64encode(contents)


def write_config(config_file_contents):
    with open("savedata.toml", "w") as f:
        f.write(config_file_contents)
