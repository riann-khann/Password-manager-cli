from rich.console import Console
import re,stdiomask,os
from typing import Tuple,Optional
from rich.table import Table
from rich import box

class UI:
    @staticmethod
    def merge_console_rich(mode:Optional[str]="vanila",warna:Optional[str]=None)->Tuple:
        console=Console()
        if mode == "vanila":
            table=Table(expand=True)
            table.add_column("NO",width=2)
            return console,table
        elif mode == "expended":
            table=Table(show_header=False,style=f"{warna}",expand=True)
            return console,table
            
    @staticmethod
    def Title(mode:Optional[str]="title-app")->None:
        console,table=UI.merge_console_rich(mode="expended",warna="bold light_sky_blue1")
        table.add_column(justify="center",style="bold cyan1")
        if mode == "title-app":
            table.add_row("password manager")
        elif mode=="title-home":
            if os.path.exists("/storage/emulated/0/Documents/password_manager/data/account.json"):
                table.add_row("WELCOME BACK")
            else:
                table.add_row("WELCOME")
                
        console.print(table)

    @staticmethod
    def daftar_menu()->None:
        console,table=UI.merge_console_rich(mode="expended",warna="bold blue")
        table.add_row("01.add account","02.show account")
        table.add_row("03.update data","04.delete account")
        table.add_row("05.save account","06.search data")
        table.add_row("07.exit","08.clear screen")
        console.print(table)

    @staticmethod
    def show_sosmed()->str:
         console,table=UI.merge_console_rich()
         SOSMED_OPTION=("Facebook","Google","Tiktok","Instagram")
         kode_menu={str(i):item for i,item in enumerate(SOSMED_OPTION,1)}
         table.add_column("LIST SOSMED",justify="center")
         for i,item in kode_menu.items():
             table.add_row(i,item)
         console.print(table)
         while True:
             nama=input("pilih sosmed (input dengan angka):")
             if nama in kode_menu:
                 nama_sosmed=kode_menu[nama]
                 break
             else:
                 print("kode menu tidak tersedia!")
                 continue
         return nama_sosmed
    
    @staticmethod
    def input_pin_and_password(value:str)->str:
        pattern_password = r"^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z0-9]{6,}$"


        pattern_pin=r"^(?!1234$|4321$|123456$|1111$|2222$|3333$|4444$|5555$|6666$|7777$|8888$|9999$|0000$)(?!.*(?:0123|1234|2345|3456|4567|5678|6789|9876|8765|7654|6543|5432|4321|3210))\d{4,6}$"


        data=stdiomask.getpass(prompt=f"masukan {value}:",mask="*")

        if ("pin" in value or "repeat pin" in value) and not re.match(pattern_pin,data):
            raise ValueError("pin terlalu lemah!")

        if "password" in value and not re.match(pattern_password,data):
                raise ValueError("password minimal 6 karakter!,harus mengandung huruf dan angka!")
        return data
            

    @staticmethod
    def input_user(value:str)->str:
            pattern_email = r"^[a-zA-Z0-9]+([._%+-][a-zA-Z0-9]+)*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            pattern_number_phone = r"^(\+62|62|0)8[1-9][0-9]{6,9}$"
            huruf=input(f"masukan {value}:")
            if "username" in value and len(huruf) < 4:
                raise ValueError("username minimal harus 4 karakter atau lebih!")
            if "email" in value and not re.match(pattern_email,huruf):
                raise ValueError("email tidak valid!")
            if "nomor handphone" in value:
                if huruf == "1":
                    huruf=None
                    return "tidak di isi"
                elif not re.match(pattern_number_phone,huruf):
                    raise ValueError("nomor handphone tidak valid!")
            if "code" in value and not huruf.isdigit():
                raise ValueError("code must digit!")
            
            return huruf
    @staticmethod
    def merge_table_title_show_account(table:Tuple)->None:
        table.add_column("CODE",width=4)
        table.add_column("SOSMED")
        table.add_column("NAME",)
        table.add_column("EMAIL")
        table.add_column("PHONE NUMBER",max_width=12)
    
    @staticmethod
    def merge_table_add_row(table,i,data):
        table.add_row(str(i),data.code,data.sosial_media,data.name,data.email,str(data.number))


    @staticmethod
    def show_account(data:list[object])->None:
        console,table=UI.merge_console_rich()
        UI.merge_table_title_show_account(table)
        for i,data in enumerate(data,1):
            UI.merge_table_add_row(table,i,data)
        console.print(table)
    
    @staticmethod
    def search_show_account(data:list[object],code:str=None,name:str=None,email:str=None,sosmed:str=None,phone_number:str=None)->None|bool:
        console,table=UI.merge_console_rich()
        UI.merge_table_title_show_account(table)
        found_data=None
        for i,data in enumerate(data,1):

            if name is not None and name == data.name:
                UI.merge_table_add_row(table,i,data)
                found_data=True

            elif code is not None and code==data.code:
                UI.merge_table_add_row(table,i,data)
                found_data=True

            elif email is not None and email in data.email:
                UI.merge_table_add_row(table,i,data)
                found_data=True

            elif sosmed is not None and sosmed == data.sosial_media:
                UI.merge_table_add_row(table,i,data)
                found_data=True

            elif phone_number is not None and phone_number == data.number:
                UI.merge_table_add_row(table,i,data)
                found_data=True

        if found_data:
            console.print(table)
            is_done=input("exit? y/n:")
            if is_done == "y":
                return True
            else:
                console.print("[bold red3] input tidak valid[/bold red3]")
                return False
                
        else:
            console.print("[bold red3]data tidak ditemukan[/bold red3]")
            return None
        


    @staticmethod
    def ui_update_data_and_search_data(mode:Optional[str]="ui-update")->None:
        INPUT_UPDATE_DATA_OPTION=("update username","update email","update password","update phone number","Exit")
        INPUT_SEARCH_DATA_OPTION=("search by name","search by code","search by sosmed","search by email","search by phone number","Exit")

        console,table=UI.merge_console_rich()
        table=Table(expand=True,box=box.SIMPLE)
        table.add_column("NO")
        table.add_column("AKSI",justify="center")

        if mode == "ui-update":
            for i,data in enumerate(INPUT_UPDATE_DATA_OPTION,1):
                table.add_row(f"{i:02d}",data.capitalize())

        elif mode == "ui-search":
            for i,data in enumerate(INPUT_SEARCH_DATA_OPTION,1):
                table.add_row(f"{i:02d}",data.capitalize())
        console.print(table)