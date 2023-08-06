
def get_file_content(filepath):
    with open(filepath,"r",encoding="utf-8") as f:
        fileStr=f.read()
    return fileStr











if __name__=="__main__":
    filepath="./demo1.py"
    fileStr=get_file_content(filepath)
    print(fileStr[0:200])