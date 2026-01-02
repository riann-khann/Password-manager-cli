import bcrypt

class Vault:
    def __init__(self,pin)->None:
        salt=bcrypt.gensalt()
        sampel=pin.encode("utf-8")
        self.__pin_hash=bcrypt.hashpw(sampel,salt)
        
    def check_pin(self,pin_input:str)->str:
        pin_input_user=pin_input.encode("utf-8")
        result=bcrypt.checkpw(pin_input_user,self.__pin_hash)
        if result is False:
            raise ValueError("pin incorett!")
        return result
    def to_dict(self)->str:
        return self.__pin_hash
    def run_load_pin(self,pin:str)->None:
        self.__pin_hash=pin
    