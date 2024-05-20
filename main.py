

#! Code References
#? 0x = Related to type of data
#* 01 = Start of Code
#* 02 = Start of Data
#? 1x = Related to manipulation of saved data
#* 11 = Load
#* 12 = Save
#? 2x = Related to manipulation of active data
#* 21 = Add
#* 22 = Subtract
#? Fx = Address of code in data (can be chained if high amounts of data present)



with open("./test.bin", "wb") as f:
    f.write(b"\x01\x11\xF1\x21\x11\xF2\x12\xF3\x02\x07\x0A")


data: bytes = b""
with open("./test.bin", "rb") as f:
    data = f.read()

current_command = ""
current_data: int | None = None
for index in range(len(data)): #TODO CHANGE TO _ AND INCREASE INDEX SO 'GOTO' WORKS
    byte = data[index].to_bytes()
    print(f"{(str(index)+":").ljust(3)} {byte}")


    match byte:
        case b"\x01":
            print(f"--> Code began on line {index}")
        case b"\x02":
            print(f"--> Data began on line {index}")
        
        case b"\x11":
            print(f"--> Load data") #TODO Make work

        case b"\x21":
            print(f"--> Add function")
