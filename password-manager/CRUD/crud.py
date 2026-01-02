import string,random,base64,json,os
from cryptography.fernet import Fernet
from custom_error import CodeNotFoundError

class User:
    def __init__(self,sosial_media:str,name:str,email:str,number_handphone:str)->None:
        
        self.sosial_media=sosial_media
        self.code="".join(random.choice(string.digits)for i in range(4))

        self.name=name
        self.email=email
        self.number=number_handphone

        self.password=None
        self.__key=Fernet.generate_key()
        self.__f=Fernet(self.__key)
        

    @property
    def get_password(self)->str:
        decrypted_password=self.__f.decrypt(self.password)
        original_password=decrypted_password.decode()
        return original_password

    @get_password.setter
    def get_password(self,password:str)->None:
        data=password.encode()
        pw_encrypt=self.__f.encrypt(data)
        self.password=pw_encrypt


    def verify_password(self,password_input:str)->bool:
        decrypted=self.__f.decrypt(self.password).decode()
        return password_input == decrypted



    def to_dict(self,mode_save:str="account")->dict|str:
        if mode_save=="account":
            return {
                "code":self.code,
                "sosial media":self.sosial_media,
                "nama":self.name,
                "email":self.email,
                "password":base64.b64encode(self.password).decode("ascii"),
                "nomor handphone":self.number
            }
        elif mode_save=="key":
            return self.__key.decode("ascii")

    @classmethod
    def from_dict(cls,data:dict)->object:
            user=cls(
                data["sosial media"],
                data["nama"],
                data["email"],
                data["nomor handphone"])
            user.code=data["code"]
            user.password=base64.b64decode(data["password"].encode("ascii"))
            return user
            
    def run_load_key(self,key:bytes)->None:
        self.__key=key
        self.__f=Fernet(self.__key)

    



class Crud:
    def __init__(self)->None:
        self.daftar_account=[]

    def _merge_for(self,code)->None:
        for user in self.daftar_account:
            if code == user.code:
                return user
        return None

    def _merge_print_error(self):
        raise CodeNotFoundError("code tidak ditemukan!")


    def create_account(self,data_user:User,storage:object)->bool:
        if not isinstance(data_user,User):
            raise TypeError("data user bukan object!")
        for user in self.daftar_account:
            if data_user.code == user.code:
                return False
        self.daftar_account.append(data_user)
        return True

    def delete_account(self,code:str,email:str,password_input:str):
        user=self._merge_for(code)
        if user is None:
            self._merge_print_error()
        if email == user.email and user.verify_password(password_input):
            self.daftar_account.remove(user)
            return 
        raise ValueError("email atau password salah!")

    def update_account(self,code:str,email_new:str=None,name_new:str=None,password_new:str=None,number_phone_new:str=None)->None:
        user=self._merge_for(code)
        if not user:
            self._merge_print_error()
            return None
        if email_new:
            user.email=email_new
        elif name_new:
            user.name=name_new
        elif password_new:
            user.get_password=password_new
        elif number_phone_new:
            user.number=number_phone_new
