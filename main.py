

#! Code References
#? 0x = Related to type of data
#* 01 = Start of Code
#* 02 = Start of Data
#? 1x = Related to manipulation of saved data
#* 11 = Load
#*! 12 = Save
#* 13 = Outut data
#? 2x = Related to manipulation of active data
#* 21 = Add
#* 22 = Subtract
#? Ex = A stored integer
#? Fx = Address of code in data (can be chained if large amounts of data present)


# with open("./test.bin", "wb") as f:
#     f.write(b"\x01\x11\xF1\x21\x11\xF2\x13\x02\x07\x0A")
#     # add \x12\xF3 before \x02 for saving


data: bytes = b""
with open("./test.bin", "rb") as f:
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
        

        case b"\x21":
            current_command = "add"
            print(f"--> Add function")
        

        case b"\x11":
            load_index_address = index + 1
            load_index = (data[load_index_address]-240).to_bytes() #? 240 is F0 (which is what addresses start with)

            # temp_data: bytes = data[int.from_bytes(data_start_index.to_bytes()+load_index)].to_bytes() # type: ignore
            temp_data: bytes = data[data_start_index + int.from_bytes(load_index)].to_bytes() # type: ignore #! ERROR CANNOT GET ADDRESS 1
            print("aaa" + str(data_start_index + int.from_bytes(load_index)))
            # print(f"--> Loading data at ({load_index}), is {current_data}") #TODO Make work

            match current_command:
                case "add":
                    current_data += temp_data
                case _:
                    current_data = temp_data
        
        case b"\x13":
            print(int.from_bytes(current_data))

    
    index += 1
