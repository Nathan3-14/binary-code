def hello() -> str:
    return "Hello from v-rye!"

def test() -> None:
    import sys
    main = Main(f"../{sys.argv[1]}")
    main.loop()


class Main:
    def __init__(self, filename: str):
        self.current_command = ""

        self.path = filename
        self.data: bytes = b""
        with open(self.path, "rb") as f:
            self.data = f.read()

        self.current_command = ""
        self.current_data: bytes = b"\x00"

        self.code_start_index = self.data.find(b"\x01")
        self.data_start_index = self.data.find(b"\x02")
    
    def _01(self) -> None:
        print(f"--> Code began on line {self.index}")
    def _02(self) -> None:
        print(f"--> Data began on line {self.index}")
    
    def _11(self) -> None:
        load_index_address = self.index + 1
        load_index: int = (self.data[load_index_address]-240) #? 240 is F0 (which is what addresses start with)

        # temp_data: bytes = data[int.from_bytes(data_start_index.to_bytes()+load_index)].to_bytes() # type: ignore
        temp_data: bytes = (self.data[self.data_start_index + load_index + 1] - 224).to_bytes() # type: ignore #? +1 for skipping "\bx02"
        print(f"--> Loading data at ({load_index}), is {str(temp_data)}")

        match self.current_command:
            case "add":
                self.current_data = (int.from_bytes(temp_data) + int.from_bytes(self.current_data)).to_bytes()
            case "subtract":
                self.current_data = (int.from_bytes(temp_data) - int.from_bytes(self.current_data)).to_bytes()
            case _:
                self.current_data = temp_data
        print(f"--> Set current data to {str(self.current_data)}")
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
        print(int.from_bytes(self.current_data))
    
    def _21(self) -> None:
        self.current_command = "add"
        print(f"--> Add function")
    def _22(self) -> None:
        self.current_command = "subtract"
        print(f"--> Subtract function")
    
    def _32(self) -> None:
        print("--> If Statement")

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

        print(f"--> if {str(self.current_data)} {condition} {comparitive}")

    def loop(self):
        self.index = self.code_start_index
        while self.index < len(self.data):
            byte = self.data[self.index].to_bytes() 
            print(f"{(str(self.index)+":").ljust(3)} {byte}")

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

                case b"\x11": #* Load Data
                    self._11()
                case b"\x12": #* Save Data
                    self._12()
                case b"\x13": #* Output Data
                    self._13()

                case b"\x32": #* If statement
                    self._32()

            
            self.index += 1




# def execute_code(path: str) -> None:
#     #! Code References
#     #? 0x = Related to type of data
#     #* 01 = Start of Code
#     #* 02 = Start of Data
#     #? 1x = Related to manipulation of saved data
#     #* 11 = Load
#     #* 12 = Save
#     #* 13 = Outut data
#     #? 2x = Related to manipulation of active data
#     #* 21 = Add
#     #* 22 = Subtract
#     #? 3x = Related to code itself
#     #* 31 = Goto Line (address)
#     #* 32 = If data (condition) (address) do (command)
#     #* Ax = Condition
#     #* A1 = '=='
#     #* A2 = '!='
#     #? Ex = A stored integer
#     #? Fx = Address of code in data (can be chained if large amounts of data present)


#     # with open(path, "wb") as f:
#     #     f.write(b"\x01\x11\xF1\x21\x11\xF2\x13\x02\x07\x0A")
#     #     # add \x12\xF3 before \x02 for saving


#     # data: bytes = b""
#     # with open(path, "rb") as f:
#     #     data = f.read()

#     # current_command = ""
#     # current_data: bytes = b"\x00"

#     # code_start_index = data.find(b"\x01")
#     # data_start_index = data.find(b"\x02")
#     # index = code_start_index

#     while index < len(data):
#         byte = data[index].to_bytes() 
#         print(f"{(str(index)+":").ljust(3)} {byte}")

#         match byte:
#             case b"\x01": #* Beginning of code
#                 print(f"--> Code began on line {index}")
#             case b"\x02": #* Beginning of data
#                 print(f"--> Data began on line {index}")
#                 break
            

#             case b"\x21": #* Add operator
#                 current_command = "add"
#                 print(f"--> Add function")
#             case b"\x22": #* Subtract operator
#                 current_command = "subtract"
#                 print(f"--> Subtract function")
            

#             case b"\x11": #* Load Data
#                 load_index_address = index + 1
#                 load_index: int = (data[load_index_address]-240) #? 240 is F0 (which is what addresses start with)

#                 # temp_data: bytes = data[int.from_bytes(data_start_index.to_bytes()+load_index)].to_bytes() # type: ignore
#                 temp_data: bytes = data[data_start_index + load_index + 1].to_bytes() # type: ignore #? +1 for skipping "\bx02"
#                 temp_data: bytes = (int.from_bytes(temp_data) - 224).to_bytes() #? -224 is 14*16 (E0)
#                 print(f"--> Loading data at ({load_index}), is {temp_data}")

#                 match current_command:
#                     case "add":
#                         current_data = (int.from_bytes(temp_data) + int.from_bytes(current_data)).to_bytes()
#                     case "subtract":
#                         current_data = (int.from_bytes(temp_data) - int.from_bytes(current_data)).to_bytes()
#                     case _:
#                         current_data = temp_data
#                 print(f"--> Set current data to {current_data}")
#                 index += 1
            
#             case b"\x12": #* Save Data
#                 save_index_address = index + 1
#                 save_index: int = (data[save_index_address]-240) + data_start_index + 1 # account for 0 index
#                 to_write = b""
#                 for index, byte in enumerate(data):
#                     byte = byte.to_bytes()
#                     if index == save_index:
#                         to_write += current_data
#                     else:
#                         to_write += byte
#                 open(path, "wb").write(to_write)

#             case b"\x32": #* If statement
#                 print("--> If Statement")
#                 condition = data[index+1]
#                 comparitive_address = data[index+2]
#                 comparitive = data[data_start_index + comparitive_address + 1 - 240] #? -240 becasuse Fx at start of address
#                 if_true = data[index+3]
#                 print(f"--> if {current_data} {condition} {comparitive}; then {if_true}")

#             case b"\x13": #* Output Data
#                 print(int.from_bytes(current_data))

        
#         index += 1
