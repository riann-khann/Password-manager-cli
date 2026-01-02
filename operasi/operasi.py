import sys,os,time,typing
from CRUD import Crud,User
from ui import UI
from custom_error import AccountNotYetCreated,CodeNotFoundError
from storage_sistem import StorageSystemFile
from vault import Vault


class OperasiApp:
    def __init__(self)->None:
        self.crud=Crud()
        self.ui=UI()
        self.storage=StorageSystemFile()
        self.vault= None
        self.path_data_account=f"{self.storage.path_folder}/account.json"
    def run(self)->None:
        self.ui.Title()
        has_save=None
        while True:
            self.ui.daftar_menu()
            select_menu=self.merge_input_select_menu()
            match select_menu:
                case "01"|"1":
                    self.cooldown()
                    self.clear_screen()
                    self.run_add_account()
                case "02"|"2":
                    self.cooldown()
                    self.clear_screen()
                    self.run_show_account()
                case "03"|"3":
                    self.cooldown()
                    self.clear_screen()
                    self.run_update_account()
                case "04"|"4":
                    self.cooldown()
                    self.clear_screen()
                    self.run_delete_data_account()
                case "05"|"5":
                    self.cooldown()
                    self.clear_screen()
                    self.run_save_data_account()
                    has_save=True
                case "06"|"6":
                    self.cooldown()
                    self.clear_screen()
                    self.run_search_data_account()
                case "07"|"7":
                    if not has_save or not self.path_data_account:
                        select=input("data belum disimpen!, apakah kamu yakin ingin keluar? y/n:")
                        if select.lower() == "y":
                            break
                        else:
                            continue
                    break
                case "08"|"8":
                    self.clear_screen()
                case _:
                    print("input tidak valid!")


    def run_add_account(self)->None:
        sosial_media=self.ui.show_sosmed()
        data=self.merge_input_user()
        password=self.merge_input_data_pin_and_password(mode="password")
        try:
            data_user=User(sosial_media,data[0],data[1],data[2])
            data_user.get_password=password
            if self.crud.create_account(data_user,self.storage):
                self.storage.save_key_data_password(data_user)
                print("data berhasil ditambahkan")
                self.cooldown()
                self.clear_screen()

            else:
                print("data gagal ditambahkan,terjadi dulpikat code!")
        except (TypeError) as e:
            print(e)

    def run_show_account(self)->None:
        try:
            self._validate()
            data=self.crud.daftar_account
            self.ui.show_account(data)
            self.show_password()
        except AccountNotYetCreated as e:
            print(e)
            return None

    def run_update_account(self)->None:
        try:
            self._validate()
            code=self.merge_input_user("code")
            self.crud.update_account(code)
        except (AccountNotYetCreated,Exception) as e:
            print(e)
            return
        while True:
            self.ui.ui_update_data_and_search_data(mode="ui-update")
            select_menu=self.merge_input_select_menu()
            match select_menu:
                case "01"|"1":
                    self.merge_update_account_user(code,mode="update_username")

                case "02"|"2":
                    self.merge_update_account_user(code,mode="update_email")

                case "03"|"3":
                    self.merge_update_account_user(code,mode="update_password")

                case "04"|"4":
                    self.merge_update_account_user(code,mode="update_number_phone")

                case "05"|"5":
                    break
                case _:
                    print("input tidak valid!")
                    continue
    def run_search_data_account(self)->None:
        try:
            self._validate()
        except (AccountNotYetCreated,Exception) as e:
            print(e)
            return None
        while True:
            self.ui.ui_update_data_and_search_data(mode="ui-search")
            select_menu=self.merge_input_select_menu()

            match select_menu:

                case "01"|"1":
                    self.merge_search_data(mode="search_by_username")
                    
                    
                case "02"|"2":
                    self.merge_search_data(mode="search_by_code")


                case "03"|"3":
                    self.merge_search_data(mode="search_by_sosmed")

                case "04"|"4":
                    self.merge_search_data(mode="search_by_email")
                    

                case "05"|"5":
                    self.merge_search_data(mode="search_by_phone_number")

                case "06"|"6":
                    self.cooldown()
                    self.clear_screen()
                    break

                case _:
                    print("input tidak valid!")
            
    def run_delete_data_account(self)->None:
        try:
            data=self.merge_input_data_delete_account()
            password=self.merge_input_data_pin_and_password()
            user=self.merge_for_user(data[0])

            if not user:
                print("code tidak ditemukan")
                return None
            self.merge_key_password(user,data[0])
            self.crud.delete_account(data[0],data[1],password)

            print("data berhasil dihapus")

        except (ValueError,Exception) as e:
            print(e)
    
    def run_save_data_account(self)->None:
        try:
            self._validate()
        except AccountNotYetCreated as e:
            print(e)
            return None

        if  self.storage.save_and_load_data_account(self.crud.daftar_account,mode_file="w"):
                self.storage.save_and_load_key_json(mode_file="wb")
                print("data berhasil di simpan")
        else:
                print("data gagal di simpen terjadi kesalahan")



    
    def merge_update_account_user(self,code:str,mode:str=None)->None:
        messages:None|str=None
        try:
            if mode == "update_username":
                username=self.ui.input_user("username")
                self.crud.update_account(code,name_new=username)
                messages="username"

            elif mode =="update_email":
                email=self.ui.input_user("email")
                self.crud.update_account(code,email_new=email)
                messages="email"

            elif mode == "update_password":
                password=self.ui.input_pin_and_password("password")
                self.crud.update_account(code,password_new=password)
                messages="password"

            elif mode == "update_number_phone":
                phone_number=self.ui.input_user("nomor handphone")
                self.crud.update_account(code,number_phone_new=phone_number)
                messages="phone number"
                
            print(f"{messages} berhasil diubah")

        except (ValueError,Exception) as e:
            print(e)


    def _validate(self)->None:
        if not self.crud.daftar_account:
            raise AccountNotYetCreated("buat akun terlebih dahulu!")


    def merge_key_password(self,user:object,code:str)->None:
        data_key=self.storage.load_key_data_password(code)
        user.run_load_key(data_key)

    def merge_input_select_menu(self)->str:
        try:
            select_menu=input("select menu:")
            return select_menu
        except KeyboardInterrupt:
            sys.exit(0)

    def merge_input_data_delete_account(self)->list:
        fields=["code","email"]
        data_user=[]
        for field in fields:
            while True:
                try:
                        self._validate()
                        data=self.ui.input_user(field)
                        data_user.append(data)
                        break
        
                except (ValueError,AccountNotYetCreated) as e:
                    print(e)
        return data_user
    
    def merge_input_data_pin_and_password(self,mode="password"):
        while True:
            try:
                if mode=="password":
                    password=self.ui.input_pin_and_password("password")
                    return password
                else:
                    pin=self.ui.input_pin_and_password("pin")
                    return pin

            except (ValueError,Exception) as e:
                print(e)
                continue

    def merge_input_user(self,mode:typing.Optional[str]="all")->list:
        fields=["username","email","nomor handphone"]
        data_input_user=[]
        for field in fields:
            while True:
                try:
                    if mode == "code": # untuk update data user
                        code=self.ui.input_user("code")
                        return code
                    else:
                        data=self.ui.input_user(field)
                        data_input_user.append(data)
                        break
                except (ValueError,CodeNotFoundError,Exception) as e:
                    print(e)
        return data_input_user
    
    def merge_search_data(self,mode:str=None)->None:
        data=self.crud.daftar_account
        try:
            match mode:
                case "search_by_username":
                    username=self.ui.input_user("username")
                    self.ui.search_show_account(data,name=username)
                case "search_by_code":
                    code=self.ui.input_user("code")
                    self.ui.search_show_account(data,code=code)
                case "search_by_sosmed":
                    sosmed=self.ui.show_sosmed()
                    self.ui.search_show_account(data,sosmed=sosmed)
                case "search_by_email":
                    email=self.ui.input_user("email")
                    self.ui.search_show_account(data,email=email)
                case "search_by_phone_number":
                    phone_number=self.ui.input_user("nomor handphone")
                    self.ui.search_show_account(data,phone_number=phone_number)
                    
        except (ValueError,Exception) as e:
            print(e)
    
    def merge_for_user(self,code:str)->str|None:
        for user in self.crud.daftar_account:
            if user.code == code:
                return user
        return None
        


    def login_with_pin(self)->None:
        if os.path.exists(self.path_data_account):
            print("kamu sudah mempunyai data account!")
            return None
        pin=self.merge_input_data_pin_and_password(mode="pin")
        self.vault=Vault(pin)
        if self.storage.pin_operation_save_and_load(self.vault):
            print("selamat datang")
            self.cooldown()
            self.clear_screen()
            self.run()
        else:
            print("pin gagal dibuat terjadi kesalahan")

    def show_password(self)->None:
        select_menu=input("show password? Y/N:")
        if select_menu.lower()=="n":
            return None
        while True:
            try:
                pin_input=self.merge_input_data_pin_and_password(mode="pin")
                self.vault=Vault(pin_input)
                pin=self.storage.pin_operation_save_and_load(mode_format="rb")
                self.vault.run_load_pin(pin)

                if self.vault.check_pin(pin_input):
                    repeat_pin=self.ui.input_pin_and_password("repeat pin")
                    if repeat_pin != pin_input:
                        print("pin incorret!")
                        continue
                    code=self.ui.input_user("code")
                    user=self.merge_for_user(code)
                    if not user:
                        print("code tidak ditemukan")
                        break
                    self.merge_key_password(user,code)
                    password=user.get_password
                    print(10*"="+"Your Account"+10*"=")
                    print(f"Email:{user.email}\nPhone Number:{user.number}\nPassword:{password}\n")
                    is_done=input("EXIT? Y/N:")
                    if is_done.lower() == "y":
                        self.cooldown()
                        self.clear_screen()
                        break
                        
            except ValueError as e:
                print(e)
                

    def load_with_pin(self)->None:
            if not os.path.exists(self.path_data_account):
                print("file tidak ditemukan!")
                return None

            try:
                pin_input=self.merge_input_data_pin_and_password(mode="pin")
                self.vault=Vault(pin_input)
                pin=self.storage.pin_operation_save_and_load(mode_format="rb")
                self.vault.run_load_pin(pin)

                if self.vault.check_pin(pin_input):
                    self.storage.save_and_load_key_json(mode_file="rb")
                    data=self.storage.save_and_load_data_account(User,mode_file="r")

                    if data:
                        self.crud.daftar_account=data
                        print("data berhasil di load")
                        self.cooldown()
                        self.clear_screen()
                        self.run()
                    else:
                        print("data gagal di load terjadi kesalahan!")


                else:
                    print("data gagal dimuat,kemungkinan pin rusak!")

            except (ValueError,Exception) as e:
                print(e)

    def clear_screen(self)->None:
        SYSTEM=os.name
        match SYSTEM:
            case "nt":
                os.system("cls")
            case "posix":
                os.system("clear")

    def cooldown(self)->None:
        time.sleep(1.3)



if __name__ == '__main__':
    operasi=OperasiApp()
    operasi.run()