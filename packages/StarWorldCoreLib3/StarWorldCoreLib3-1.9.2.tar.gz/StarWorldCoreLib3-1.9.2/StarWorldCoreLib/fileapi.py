"""
 ____  _           __        __         _     _  ____               _     _ _    _____       _____ _ _         _    ____ ___ 
/ ___|| |_ __ _ _ _\ \      / /__  _ __| | __| |/ ___|___  _ __ ___| |   (_) |__|___ /      |  ___(_) | ___   / \  |  _ \_ _|
\___ \| __/ _` | '__\ \ /\ / / _ \| '__| |/ _` | |   / _ \| '__/ _ \ |   | | '_ \ |_ \ _____| |_  | | |/ _ \ / _ \ | |_) | | 
 ___) | || (_| | |   \ V  V / (_) | |  | | (_| | |__| (_) | | |  __/ |___| | |_) |__) |_____|  _| | | |  __// ___ \|  __/| | 
|____/ \__\__,_|_|    \_/\_/ \___/|_|  |_|\__,_|\____\___/|_|  \___|_____|_|_.__/____/      |_|   |_|_|\___/_/   \_\_|  |___|
"""

import os
import json


def file_locate(file="",fl=__file__):
    """
    Default files for locating starworldcorelib3 only.
    If you want to locate another directory, change the 'fl' parameter.
    """
    ic = str(os.path.split(os.path.realpath(fl))[0]).replace("\\","/")+"/"+file
    return ic

class JsonConfigurator:
    def __init__(self,file) -> None:
        """
        The 'file' parameter must use an existing file.
        Please do not terminate the program during writing, which may cause file corruption and data loss.
        """
        self.file = file
        self.file_output = open(file,"rb")
        self.dict_content = json.loads(self.file_output.read())
    def parse(self) -> dict:
        """
        Get the json content.
        """
        return self.dict_content
    def addition(self,key,value) -> None:
        """
        Addition a new key-value pair.
        """
        self.dict_content[key] = value
        file_input = open(self.file,"wb")
        file_input.write(json.dumps(self.dict_content).encode("utf-8"))
        file_input.close()
    def remove(self,key) -> None:
        """
        Remove a key-value pair.
        """
        self.dict_content.pop(key)
        file_input = open(self.file,"wb")
        file_input.write(json.dumps(self.dict_content).encode("utf-8"))
        file_input.close()
    def save(self,file) -> None:
        """
        Save the json content.
        """
        file_input = open(file,"wb")
        file_input.write(json.dumps(self.dict_content).encode("utf-8"))
        file_input.close()
    def __del__(self) -> None:
        """
        Delete JsonConfigurator.
        """
        self.file_output.close()
    def __str__(self) -> str:
        """
        Convert JsonConfigurator to string.
        """
        return json.dumps(self.dict_content,indent=4)

