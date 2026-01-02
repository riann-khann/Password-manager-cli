from operasi import OperasiApp
from ui import UI

class AppRun:
    def __init__(self)->None:
        self.app=OperasiApp()
        self.ui=UI()
    def run(self)->None:
        self.app.cooldown()
        self.app.clear_screen()
        self.ui.Title(mode="title-home")
        while True:
            print("01.Login app\n02.Load data\n03.Keluar")
            menu=self.app.merge_input_select_menu()
            match menu:
                case "01"|"1":
                    self.app.login_with_pin()
                case "02"|"2":
                    self.app.load_with_pin()
                case "03"|"3":
                    print("selamat tinggal :)")
                    break
                case _:
                    print("input tidak valid!")
    
    

if __name__ == '__main__':
    app=AppRun()
    app.run()