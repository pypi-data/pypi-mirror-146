import base64
import pickle
import struct
#解密
import easygui as eg
import os

class MaliciousCodeError(Exception):
    pass

def main():
    n = eg.enterbox("请输入加密的数据， b' 和 ' 也要带")
    if n != "" or n != None:
        if n[0] == "b" and n[1] == "'" and n[-1] == "'":
            n = eval(n) #如果直接eval，有可能是恶意代码
        else:
            raise MaliciousCodeError()
        #解密开始
        data = pickle.loads(n)

        file_info = data[0]
        file_info = struct.unpack("128sl",file_info)
        print("文件名称："+file_info[0].decode())
        print("文件大小："+str(file_info[1]))

        s = data[1]
        s = base64.b85decode(s)
        print("文件内容："+s.decode())

        if eg.boolbox("是否保存文件？（克隆文件）",choices=("保存","不保存")):
            d = eg.diropenbox("请选择路径")
            os.chdir(d)
            with open(file_info[0].decode().strip("\x00"),"w") as f:
                f.write(s.decode())
            eg.msgbox(title="提示",msg="OK")

if __name__ == "__main__":
    main()
