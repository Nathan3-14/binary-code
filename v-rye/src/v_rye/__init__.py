def hello() -> str:
    return "Hello from v-rye!"

def test() -> None:
    execute_code("../test.bin")

def execute_code(path: str) -> None:
    from rich.console import Console

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
    #? Ex = A stored integer
    #? Fx = Address of code in data (can be chained if large amounts of data present)


    # with open(path, "wb") as f:
    #     f.write(b"\x01\x11\xF1\x21\x11\xF2\x13\x02\x07\x0A")
    #     # add \x12\xF3 before \x02 for saving


    data: bytes = b""
    with open(path, "rb") as f:
        data = f.read()

    current_command = ""
    current_data: bytes = b"\x00"

    code_start_index = data.find(b"\x01")
    data_start_index = data.find(b"\x02")
    index = code_start_index

    while index < len(data):
        byte = data[index].to_bytes()
        print(f"{(str(index)+":").ljust(3)} {byte}")

        match byte:
            case b"\x01":
                print(f"--> Code began on line {index}")
            case b"\x02":
                print(f"--> Data began on line {index}")
                break
            

            case b"\x21":
                current_command = "add"
                print(f"--> Add function")
            

            case b"\x11":
                load_index_address = index + 1
                load_index: int = (data[load_index_address]-240) #? 240 is F0 (which is what addresses start with)

                # temp_data: bytes = data[int.from_bytes(data_start_index.to_bytes()+load_index)].to_bytes() # type: ignore
                temp_data: bytes = data[data_start_index + load_index + 1].to_bytes() # type: ignore #? +1 for skipping "\bx02"
                current_data = temp_data
                print(f"--> Loading data at ({load_index}), is {temp_data}")

                # match current_command:
                #     case "add":
                #         current_data += temp_data
                #     case _:
                #         current_data = temp_data
                index += 1
            
            case b"\x13":
                print(int.from_bytes(current_data))
        

        
        index += 1