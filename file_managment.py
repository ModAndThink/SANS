def open_a_file(file):
    data = ""
    file = open(file,"r")
    file = file.readlines()
    for i in file:
        data += i
    return data

def write_data(file,data):
    file = open(file,"w")
    file.write(data)
    file.close()
