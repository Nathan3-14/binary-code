def hello() -> str:
    return "Hello from v-rye!"

def test() -> None:
    import sys
    main = Main(f"../{sys.argv[1]}")
    main.loop()

import datetime
from rich import print as rprint
class Main:
    def __init__(self, filename: str):
        self.current_command = "set"

        self.path = filename
        self.data: bytes = b""
        with open(self.path, "rb") as f:
            self.data = f.read()

        self.current_command = ""
        self.current_data: bytes = b"\x00"

        self.code_start_index = self.data.find(b"\x01")
        self.data_start_index = self.data.find(b"\x02")

        self.colours = ["red", "green", "blue", "yellow", "cyan"]
    
    def _01(self) -> None:
        self.colour_print(f"--> Code began on line {self.index}")
    def _02(self) -> None:
        self.colour_print(f"--> Data began on line {self.index}")
    
    def _11(self) -> None:
        load_index_address = self.index + 1
        load_index: int = (self.data[load_index_address]-240) #? 240 is F0 (which is what addresses start with)

        # temp_data: bytes = data[int.from_bytes(data_start_index.to_bytes()+load_index)].to_bytes() # type: ignore
        temp_data: bytes = (self.data[self.data_start_index + load_index + 1] - 224).to_bytes() # type: ignore #? +1 for skipping "\bx02"
        self.colour_print(f"--> Loading data at ({load_index}), is {str(temp_data)}")

        match self.current_command:
            case "add":
                self.current_data = (int.from_bytes(temp_data) + int.from_bytes(self.current_data)).to_bytes()
            case "subtract":
                self.current_data = (int.from_bytes(temp_data) - int.from_bytes(self.current_data)).to_bytes()
            case "set":
                self.current_data = temp_data
            case _:
                self.current_data = temp_data
        self.colour_print(f"--> Set current data to {str(self.current_data)}")
        self.index += 1
    def _12(self) -> None:
        save_index_address = self.index + 1
        save_index: int = (self.data[save_index_address]-240) + self.data_start_index + 1 # account for 0 index
        to_write = b""
        for index, byte in enumerate(self.data):
            byte = byte.to_bytes()
            if index == save_index:
                to_write += self.current_data
            else:
                to_write += byte
        open(self.path, "wb").write(to_write)
    def _13(self):
        rprint(f"[magenta bold]\[{datetime.datetime.now().strftime("%H:%M:%S")}] {int.from_bytes(self.current_data)}[/magenta bold]")
    
    def _21(self) -> None:
        self.current_command = "add"
        self.colour_print(f"--> Add function")
    def _22(self) -> None:
        self.current_command = "subtract"
        self.colour_print(f"--> Subtract function")
    def _23(self) -> None:
        self.current_command = "set"
        self.colour_print(f"--> Set function")
    
    def _31(self) -> None:
        goto_location = self.data[self.index+1] - 240 #? Because 240 is "Fx"
        
        self.colour_print(f"--> Goto {goto_location}")

        self.index = goto_location - 1
    def _32(self) -> None:
        self.colour_print("--> If Statement")

        condition = self.data[self.index+1].to_bytes()
        comparitive_address = self.data[self.index+2]
        comparitive = (self.data[self.data_start_index + comparitive_address + 1 - 240]-224).to_bytes() #? -240 becasuse "Fx" at start of address #? -224 because "Ex" at start of integer

        match condition:
            case b"\xA1":
                if self.current_data == comparitive:
                    self.index += 2
                else:
                    self.index += 3
            case b"\xA2":
                if self.current_data != comparitive:
                    self.index += 2
                else:
                    self.index += 3

        self.colour_print(f"--> if {str(self.current_data)} {condition} {comparitive}")

    def colour_print(self, message):
        rprint(f"[{self.colour}]{message}[/{self.colour}]")
    
    def loop(self):
        self.index = self.code_start_index
        self.colour_index = 0
        while self.index < len(self.data):
            self.colour = self.colours[self.colour_index]


            byte = self.data[self.index].to_bytes() 
            self.colour_print(f"{(str(self.index)+":").ljust(3)} {byte}")

            match byte:
                case b"\x01": #* Beginning of code
                    self._01()
                case b"\x02": #* Beginning of data
                    self._02()
                    break #? Skip data as it doesn't get interpreted
                
                case b"\x21": #* Add operator
                    self._21()
                case b"\x22": #* Subtract operator
                    self._22()
                case b"\x23": #* Set operator
                    self._23()

                case b"\x11": #* Load Data
                    self._11()
                case b"\x12": #* Save Data
                    self._12()
                case b"\x13": #* Output Data
                    self._13()

                case b"\x31": #* Goto Statment
                    self._31()
                case b"\x32": #* If statement
                    self._32()

            
            self.index += 1
            self.colour_index += 1
            if self.colour_index >= len(self.colours):
                self.colour_index = 0




#! Code References
#? 0x = Related to type of data
#* 01 = Start of Code
#* 02 = Start of Data
#? 1x = Related to manipulation of saved data
#* 11 = Load
#* 12 = Save
#* 13 = Outut data
#? 2x = Related to manipulation of active data
#* 21 = Add
#* 22 = Subtract
#? 3x = Related to code itself
#* 31 = Goto Line (address)
#* 32 = If data (condition) (address) do (command)
#* Ax = Condition
#* A1 = '=='
#* A2 = '!='
#? Ex = A stored integer
#? Fx = Address of code in data (can be chained if large amounts of data present)
