from pathlib import Path
import json,os
from cryptography.fernet import Fernet


class StorageSystemFile:
    def __init__(self):
        self.path_folder="/storage/emulated/0/Documents/password_manager/data"
        self.__key=Fernet.generate_key()
        self.__f=Fernet(self.__key)
    def create_folder_path(self):
        Path(self.path_folder).mkdir(parents=True,exist_ok=True)


    def save_and_load_data_account(self,data_user,mode_file="w"):
        self.create_folder_path()
        try:
            with open(f"{self.path_folder}/account.json",mode=f"{mode_file}",encoding="utf-8") as f:
                
                # untuk save data account
                if mode_file == "w":
                    data=json.dumps([item.to_dict() for item in data_user])
                    encode_data=data.encode()
                    data_user=self.__f.encrypt(encode_data).decode()
                    json.dump(data_user,f)
                    return True
                # untuk load data_account
                elif mode_file =="r":
                    data=json.load(f).encode()
                    data_decypt=self.__f.decrypt(data).decode()
                    load_data=json.loads(data_decypt)
                    users=[]
                    for item in load_data:
                        user=data_user.from_dict(item)
                        users.append(user)
                    return users
                else:
                    return None
                
        except FileNotFoundError:
            print("file tidak ditemukan!")
            return []
        except json.JSONDecodeError:
            print("file json rusak!")
            return []
            
    def save_key_data_password(self,data_obj):
        try:
            all_key_old={}
            if os.path.exists(f"{self.path_folder}/master_keys.json"):
                with open(f"{self.path_folder}/master_keys.json",mode="r") as f:
                        all_key_old=json.load(f)
            # key_data=data_obj.to_dict(mode_save="key").encode()
            key_data=data_obj.to_dict(mode_save="key")
            data_kunci=json.dumps(key_data)
            key_endcode=self.__f.encrypt(data_kunci.encode()).decode("ascii")
            key_dict={data_obj.code:key_endcode}
            merge_key={**all_key_old,**key_dict}
            with open(f"{self.path_folder}/master_keys.json",mode="w") as f:
                json.dump(merge_key,f)
        except (FileNotFoundError,Exception) as e:
            print(e)


    def load_key_data_password(self,email):
        try:
            with open(f"{self.path_folder}/master_keys.json",mode="r") as f:
                data=json.load(f)
                if email in data:
                    key=data[email]
                    data_decypt=self.__f.decrypt(key.encode()).decode("ascii")
                    load_data=json.loads(data_decypt)
                    return load_data.encode("ascii")
        except (FileNotFoundError,json.JSONDecodeError,Exception) as e:
            print(f"error {e}")
        
    def save_and_load_key_json(self,mode_file="wb" ):
        self.create_folder_path()
        try:
            with open(f"{self.path_folder}/master_json.key",mode=mode_file) as f:
                
                if mode_file=="wb":
                    f.write(self.__key)
                    return True
                elif mode_file =="rb":
                    data=f.read()
                    self.__key=data
                    self.__f=Fernet(self.__key)
                    return True
                else:
                    return None
        except (FileNotFoundError,Exception) as e:
            print(e)
            return None

    def pin_operation_save_and_load(self,vault_obj=None,mode_format="wb"):
        """untuk simpen pin, method ini hanya semetara sampai aku menemukan pattern yang tepat"""
        self.create_folder_path()
        try:
            with open(f"{self.path_folder}/pin.hash",mode=f"{mode_format}") as f:
                if mode_format == "wb":
                    if vault_obj is not None:
                        get_pin=vault_obj.to_dict()
                        f.write(get_pin)
                        return True
                    return None
                elif mode_format == "rb":
                    data=f.read()
                    return data
                else:
                    return None
        except (FileNotFoundError,Exception) as e:
            print(e)
            return None