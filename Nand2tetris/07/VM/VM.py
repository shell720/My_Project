from pathlib import Path
import sys
import os
import re

class Parser:
    def __init__(self):
        self.cnt=0
        self.func_name=""
    def file_open(self,dirname):
        path=Path(dirname)
        if path.is_dir():
            shokika=CodeWriter2(["C_CALL",["call", "Sys.init", "0"]], self.cnt, "",self.func_name)
            shokika.setSP()
            self.cnt = shokika.func_address
            for each_file in path.glob("*.vm"):
                self.read_file(each_file)
                #print(each_file)
        if path.is_file():
            self.read_file(each_file)
            #print(dirname)


    def read_file(self,path):
        file_name=path.stem
        #print(file_name)
        with open(path) as f:
            for s_line in f:
                cmd = self.commandType(s_line)
                if cmd != None:
                    henkan=CodeWriter2(cmd,self.cnt,file_name,self.func_name)
                    if henkan.CmdType=="C_ARITHMETIC":
                        henkan.writeArithmetic()
                        self.cnt=henkan.jmpAddress
                    elif henkan.CmdType=="C_PUSH":
                        henkan.writePush()
                    elif henkan.CmdType=="C_POP":
                        henkan.writePop()
                    elif henkan.CmdType=="C_LABEL":
                        henkan.writeLabel()
                    elif henkan.CmdType=="C_GOTO":
                        henkan.writeGoto()
                    elif henkan.CmdType=="C_IF":
                        henkan.writeIf()
                    elif henkan.CmdType=="C_CALL":
                        henkan.writeCall()
                        self.cnt=henkan.func_address
                    elif henkan.CmdType=="C_RETURN":
                        henkan.writeReturn()
                    elif henkan.CmdType=="C_FUNCTION":
                        henkan.writeFunction()
                        self.func_name=henkan.func_name



    def commandType(self,read_line):
        arithmetic = ["add","sub","neg","eq","gt","lt","and","or","not"]
        result = re.sub(r'\/\/[^\n]*',"",read_line)
        result = re.sub(r'\n',"",result)
        if result:
            command = result.split(" ")
            if command[0] in arithmetic:
                return ["C_ARITHMETIC",command]
            elif command[0] == "push":
                return ["C_PUSH",command]
            elif command[0] == "pop":
                return ["C_POP",command]
            elif command[0] == "label":
                return ["C_LABEL",command]
            elif command[0] == "goto":
                return ["C_GOTO",command]
            elif command[0] == "if-goto":
                return ["C_IF",command]
            elif command[0] == "function":
                return ["C_FUNCTION",command]
            elif command[0] == "call":
                return ["C_CALL",command]
            elif command[0] == "return":
                return ["C_RETURN",command]
            #return command #コメントや空行の場合はNoneが返る

class CodeWriter(object):
    def __init__(self,cmd,jmpAddress,file_name):
        self.CmdType =cmd[0]
        self.cmd = cmd[1]
        self.jmpAddress=jmpAddress #分岐命令で個々を区別する為の数字
        self.file_name=file_name
    def writeArithmetic(self):
        if self.cmd[0]=="add":
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            #print("M=0") #SPの外を初期化する為に追加してるが、いらなそう
            print("A=A-1")
            print("M=M+D")
        elif self.cmd[0]=="sub":
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            #print("M=0")
            print("A=A-1")
            print("M=M-D")
        elif self.cmd[0]=="neg":
            print("@SP")
            print("A=M-1")
            print("M=-M")
        elif self.cmd[0]=="and":
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            print("M=0")
            print("A=A-1")
            print("M=M&D")
        elif self.cmd[0]=="or":
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            print("M=0")
            print("A=A-1")
            print("M=M|D")
        elif self.cmd[0]=="not":
            print("@SP")
            print("A=M-1")
            print("M=!M")
        elif self.cmd[0]=="eq":
            print("@SP")
            print("M=M-1")
            print("A=M //アドレスをRAM[SPベース]に") 
            print("D=M")
            print("M=0")
            print("A=A-1")
            print("D=M-D //二つの値の比較をDに代入")
            print("@TrueEQ{0}".format(self.jmpAddress))
            print("D;JEQ")
            print("@SP")
            print("A=M-1")
            print("M=0")
            print("@TrueEQ_END{0}".format(self.jmpAddress))
            print("0;JMP")
            print("(TrueEQ{0})".format(self.jmpAddress))
            print("@SP")
            print("A=M-1")
            print("M=-1")
            print("(TrueEQ_END{0})".format(self.jmpAddress))
            self.jmpAddress+=1
        elif self.cmd[0]=="gt":
            print("@SP")
            print("M=M-1")
            print("A=M //アドレスをRAM[SPベース]に") 
            print("D=M")
            print("M=0")
            print("A=A-1")
            print("D=M-D //二つの値の比較をDに代入")
            print("@TrueGT{0}".format(self.jmpAddress))
            print("D;JGT")
            print("@SP")
            print("A=M-1")
            print("M=0")
            print("@TrueGT_END{0}".format(self.jmpAddress))
            print("0;JMP")
            print("(TrueGT{0})".format(self.jmpAddress))
            print("@SP")
            print("A=M-1")
            print("M=-1")
            print("(TrueGT_END{0})".format(self.jmpAddress))
            self.jmpAddress+=1
        elif self.cmd[0]=="lt":
            print("@SP")
            print("M=M-1")
            print("A=M //アドレスをRAM[SPベース]に") 
            print("D=M")
            print("M=0")
            print("A=A-1")
            print("D=M-D //二つの値の比較をDに代入")
            print("@TrueLT{0}".format(self.jmpAddress))
            print("D;JLT")
            print("@SP")
            print("A=M-1")
            print("M=0")
            print("@TrueLT_END{0}".format(self.jmpAddress))
            print("0;JMP")
            print("(TrueLT{0})".format(self.jmpAddress))
            print("@SP")
            print("A=M-1")
            print("M=-1")
            print("(TrueLT_END{0})".format(self.jmpAddress))
            self.jmpAddress+=1
    
    def writePush(self):
        if self.cmd[1]=="argument":
            print("@"+self.cmd[2])
            print("D=A")
            print("@ARG")
            print("A=M+D")
            print("D=M")
            print("@SP")
            print("A=M")
            print("M=D")
            print("@SP")
            print("M=M+1")
        if self.cmd[1]=="local":
            print("@"+self.cmd[2])
            print("D=A")
            print("@LCL")
            print("A=M+D")
            print("D=M")
            print("@SP")
            print("A=M")
            print("M=D")
            print("@SP")
            print("M=M+1")
        if self.cmd[1]=="static":
            print("@"+self.file_name+"."+self.cmd[2])
            print("D=M")
            print("@SP")
            print("M=M+1")
            print("A=M-1")
            print("M=D")
        if self.cmd[1]=="constant":
            print("@"+self.cmd[2])
            print("D=A")
            print("@SP")
            print("A=M")
            print("M=D")
            print("@SP")
            print("M=M+1")
        if self.cmd[1]=="this":
            print("@"+self.cmd[2])
            print("D=A")
            print("@THIS")
            print("A=M+D")
            print("D=M")
            print("@SP")
            print("A=M")
            print("M=D")
            print("@SP")
            print("M=M+1")
        if self.cmd[1]=="that":
            print("@"+self.cmd[2])
            print("D=A")
            print("@THAT")
            print("A=M+D")
            print("D=M")
            print("@SP")
            print("A=M")
            print("M=D")
            print("@SP")
            print("M=M+1")
        if self.cmd[1]=="pointer":
            print("@3")
            print("D=A")
            print("@"+self.cmd[2])
            print("A=A+D")
            print("D=M")
            print("@SP")
            print("M=M+1")
            print("A=M-1")
            print("M=D")
        if self.cmd[1]=="temp":
            print("@5")
            print("D=A")
            print("@"+self.cmd[2])
            print("A=A+D")
            print("D=M")
            print("@SP")
            print("M=M+1")
            print("A=M-1")
            print("M=D")

    def writePop(self):
        if self.cmd[1]=="argument":
            print("@"+self.cmd[2])
            print("D=A")
            print("@ARG")
            print("D=D+M")
            print("@R13")
            print("M=D")
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            print("@R13")
            print("A=M")
            print("M=D")
        if self.cmd[1]=="local":
            print("@"+self.cmd[2])
            print("D=A")
            print("@LCL")
            print("D=D+M")
            print("@R13") #pop先のアドレスを一時的に
            print("M=D")
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            print("@R13")
            print("A=M")
            print("M=D")
        if self.cmd[1]=="static":
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            print("@"+self.file_name+"."+self.cmd[2])
            print("M=D")
        if self.cmd[1]=="constant":
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            print("@"+self.cmd[2])
            print("M=D")
        if self.cmd[1]=="this":
            print("@"+self.cmd[2])
            print("D=A")
            print("@THIS")
            print("D=D+M")
            print("@R13")
            print("M=D")
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            print("@R13")
            print("A=M")
            print("M=D")
        if self.cmd[1]=="that":
            print("@"+self.cmd[2])
            print("D=A")
            print("@THAT")
            print("D=D+M")
            print("@R13")
            print("M=D")
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            print("@R13")
            print("A=M")
            print("M=D")
        if self.cmd[1]=="pointer":
            print("@3")
            print("D=A")
            print("@"+self.cmd[2])
            print("D=A+D")
            print("@R13")
            print("M=D")
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            print("@R13")
            print("A=M")
            print("M=D")
        if self.cmd[1]=="temp":
            print("@5")
            print("D=A")
            print("@"+self.cmd[2])
            print("D=A+D")
            print("@R13")
            print("M=D")
            print("@SP")
            print("M=M-1")
            print("A=M")
            print("D=M")
            print("@R13")
            print("A=M")
            print("M=D")

class CodeWriter2(CodeWriter):
    def __init__(self,cmd,cnt,file_name,func_name):
        super().__init__(cmd,cnt,file_name)
        self.func_address=cnt
        self.func_name=func_name
    
    def writeLabel(self):
        print("("+self.func_name+"$"+self.cmd[1]+")")
    
    def writeGoto(self):
        print("@"+self.func_name+"$"+self.cmd[1])
        print("0;JMP")
    
    def writeIf(self):
        print("@SP")
        print("M=M-1")
        print("A=M")
        print("D=M")
        print("@"+self.func_name+"$"+self.cmd[1])
        print("D;JNE")
    
    def writeFunction(self):
        self.func_name=self.cmd[1]
        print("("+self.cmd[1]+")")
        for i in range(int(self.cmd[2])):
            print("@SP")
            print("A=M")
            print("M=0")
            print("@SP")
            print("M=M+1")

    
    def writeReturn(self):
        #FRAME(R15) = LCL
        print("@LCL")
        print("D=M")
        print("@R15")
        print("M=D")
        # RET = 
        print("@5")
        print("AD=D-A")
        print("D=M")
        print("@R14")
        print("M=D")
        #*ARG = pop()
        print("@SP")
        print("M=M-1")
        print("A=M")
        print("D=M")
        print("@ARG")
        print("A=M")
        print("M=D")
        #SP = ARG+1
        print("@ARG")
        print("D=M+1")
        print("@SP")
        print("M=D")
        #THAT =
        print("@R15")
        print("D=M")
        print("@1")
        print("AD=D-A")
        print("D=M")
        print("@THAT")
        print("M=D")
        #THIS 
        print("@R15")
        print("D=M")
        print("@2")
        print("AD=D-A")
        print("D=M")
        print("@THIS")
        print("M=D")
        # ARG
        print("@R15")
        print("D=M")
        print("@3")
        print("AD=D-A")
        print("D=M")
        print("@ARG")
        print("M=D")
        # LCL
        print("@R15")
        print("D=M")
        print("@4")
        print("AD=D-A")
        print("D=M")
        print("@LCL")
        print("M=D")
        # Return address
        print("@R14")
        print("A=M")
        print("0;JMP")

    def writeCall(self):
        #push リターンアドレス
        print("@return_address{0}".format(self.func_address))
        print("D=A")
        print("@SP")
        print("A=M")
        print("M=D")
        print("@SP")
        print("M=M+1")
        # push LCL
        print("@LCL")
        print("D=M")
        print("@SP")
        print("A=M")
        print("M=D")
        print("@SP")
        print("M=M+1")
        #push ARG
        print("@ARG")
        print("D=M")
        print("@SP")
        print("A=M")
        print("M=D")
        print("@SP")
        print("M=M+1")
        #push THIS
        print("@THIS")
        print("D=M")
        print("@SP")
        print("A=M")
        print("M=D")
        print("@SP")
        print("M=M+1")
        #push THAT
        print("@THAT")
        print("D=M")
        print("@SP")
        print("A=M")
        print("M=D")
        print("@SP")
        print("M=M+1")
        #ARG=SP-n-5
        print("@"+self.cmd[2])
        print("D=A")
        print("@5")
        print("D=D+A")
        print("@SP")
        print("D=M-D")
        print("@ARG")
        print("M=D")
        # LCL=SP
        print("@SP")
        print("D=M")
        print("@LCL")
        print("M=D")
        # goto function
        print("@"+self.cmd[1])
        print("0;JMP")
        print("(return_address{0})".format(self.func_address))
        self.func_address+=1
    def setSP(self):
        print("@256")
        print("D=A")
        print("@SP")
        print("M=D")
        self.writeCall()




if __name__=="__main__":
    argc= len(sys.argv)
    if (argc== 1):
        print("Error 一つのファイルを引数にしてください")
        print("使用方法: VM.py <ファイル名>\n")
    else:
        vm=Parser()
        vm.file_open(sys.argv[1])
