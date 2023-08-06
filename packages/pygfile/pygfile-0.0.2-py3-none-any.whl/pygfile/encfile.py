import struct
import pickle
import base64
#所有加密模块
import easygui as eg
import os


def main():
    file = eg.fileopenbox("请选择加密的文件，不是二进制文件")
    if file!=None:
        r = []
        f = open(file,"r",encoding="utf-8")
        i = f.read()
        f.close()
        i = i.strip()
        
        name = os.path.basename(file)
        size = len(i)
        enc = struct.pack("128sl",name.encode(),size)
        r.append(enc)

        enc = base64.b85encode(i.encode())
        r.append(enc)

        enc_over = pickle.dumps(r)
        print(enc_over)
    
if __name__ == "__main__":
    main()
