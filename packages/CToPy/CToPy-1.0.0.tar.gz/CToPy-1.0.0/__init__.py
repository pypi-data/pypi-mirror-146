import os
from numpy.ctypeslib import ndpointer
import ctypes
import numpy as np
import pickle
from zipfile import ZipFile
from copy import deepcopy

class compiler:
    class _runer:
        def __init__(self):
            pass

        def setRuner(self, fun, recominfo):
            self.recominfo = recominfo
            self.fun = fun
            return self.run

        def run(self, *args):
            args = list(args)
            for i in self.recominfo:
                args[i] = args[i].reshape(-1)
                args[i] = (compiler.NP_TO_C[args[i].dtype] * len(args[i]))(*args[i])
            self.fun(*args)

    TYPE_TO_C = {"void":ctypes.c_void_p, "bool":ctypes.c_bool, "char":ctypes.c_char, "short":ctypes.c_short, "int":ctypes.c_int, "long":ctypes.c_long, "float":ctypes.c_float, "double":ctypes.c_double, "unsignedint":ctypes.c_uint, "unsignedbyte":ctypes.c_ubyte, "unsignedlong":ctypes.c_ulong, "unsignedlonglong":ctypes.c_ulonglong, "unsignedshort":ctypes.c_ushort}
    NP_TO_C = {np.dtype(np.bool_):ctypes.c_bool, np.dtype(np.byte): ctypes.c_char, np.dtype(np.short): ctypes.c_short, np.dtype(np.intc): ctypes.c_int, np.dtype(np.uintc): ctypes.c_uint, np.dtype(np.int_):ctypes.c_long, np.dtype(np.uint): ctypes.c_ulong, np.dtype(np.longlong): ctypes.c_ulonglong, np.dtype(np.single): ctypes.c_float, np.dtype(np.double): ctypes.c_double, np.dtype(np.longdouble): ctypes.c_longdouble, np.dtype(np.ushort): ctypes.c_ushort, np.dtype(np.uintc): ctypes.c_uint, np.dtype(np.uint): ctypes.c_ulong, np.dtype(np.ulonglong): ctypes.c_ulonglong}

    def printNumpyToC():
        keys = compiler.NP_TO_C.keys()
        for i in keys:
            print(i, end=" : ")
            print(str(compiler.NP_TO_C[i]).replace("<class 'ctypes.c_","").replace("'>",""))

    def compileC(filename = "fun"):
        os.system(f"gcc -fPIC -c {filename}.c -m64")
        os.system(f"gcc -shared {filename}.o -o {filename}.dll")
        os.remove(f"{filename}.o")
        path = f"{os.getcwd()}\\{filename}.dll"
        lib = ctypes.cdll.LoadLibrary(path)

        finfo = compiler._extractor(filename)
        save_finfo = deepcopy(finfo)
        for f in finfo:
            recombinate = []
            c_res = eval(f"lib.{f[0][1]}")
            if "*" in f[0][0]:
                c_res.restype = ndpointer(dtype=compiler.TYPE_TO_C[f[0][0][0:-1]], shape=f[2])
            else:
                c_res.restype = compiler.TYPE_TO_C[f[0][0]]

            for idx2, c_type in enumerate(f[1]):
                if "*" in c_type:
                    f[1][idx2] = ctypes.POINTER(compiler.TYPE_TO_C[c_type[0:-1]])
                    recombinate.append(idx2)
                elif not "void" in c_type:
                    f[1][idx2] = compiler.TYPE_TO_C[c_type]
                else:
                    f[1] = []
            c_res.argtypes = f[1]
            
            if not recombinate == []:
                runer = compiler._runer()
                run = runer.setRuner(c_res, recombinate)
                exec(f"lib.{f[0][1]} = run")

        with open(f"{filename}.inf", "wb") as f:
            pickle.dump(save_finfo, f)

        with ZipFile(f"{filename}.cxp", "w") as z:
            z.write(f"{filename}.inf")
            z.write(f"{filename}.dll")
        os.remove(f"{filename}.inf")

        return lib

    def loadC(filename = "fun"):
        with ZipFile(f"{filename}.cxp", "r") as z:
            z.extract(f"{filename}.dll")
            z.extract(f"{filename}.inf")

        
        path = f"{os.getcwd()}\\{filename}.dll"
        lib = ctypes.cdll.LoadLibrary(path)

        with open(f"{filename}.inf", "rb") as f:
            finfo = pickle.load(f)
        os.remove(f"{filename}.inf")

        for f in finfo:
            recombinate = []
            c_res = eval(f"lib.{f[0][1]}")
            if "*" in f[0][0]:
                c_res.restype = ndpointer(dtype=compiler.TYPE_TO_C[f[0][0][0:-1]], shape=f[2])
            else:
                c_res.restype = compiler.TYPE_TO_C[f[0][0]]

            for idx2, c_type in enumerate(f[1]):
                if "*" in c_type:
                    f[1][idx2] = ctypes.POINTER(compiler.TYPE_TO_C[c_type[0:-1]])
                    recombinate.append(idx2)
                elif not "void" in c_type:
                    f[1][idx2] = compiler.TYPE_TO_C[c_type]
                else:
                    f[1] = []
            c_res.argtypes = f[1]
            
            if not recombinate == []:
                runer = compiler._runer()
                run = runer.setRuner(c_res, recombinate)
                exec(f"lib.{f[0][1]} = run")

        return lib
        
    def _extractor(filename):
        with open(f"{filename}.c") as f:
            lines = f.readlines()

        program = ""
        for line in lines:
            if line[0] == '#':
                line = ""
            program += line

        start = 0
        brackets = 0
        functionsinit = []
        for idx,charakter in enumerate(program):
            if charakter == "{":
                if brackets == 0:
                    functionsinit.append(program[start:idx])
                brackets += 1

            if charakter == "}":
                brackets -= 1
                if brackets == 0:
                    start = idx + 1

        for idx, finit in enumerate(functionsinit):
            finit = str(finit)
            finit = finit.replace("(", " ( ").replace(")", " ) ").replace("[", " [ ").replace("]", " ] ").replace("\n", " ").replace("*", " * ").replace("="," = ")
            while "  " in finit: 
                finit = finit.replace("  ", " ")
            finit = finit.replace("unsigned ", "unsigned")
            finit = finit.replace(" [", "[").replace(" ]", "]").replace("/ *","//").replace("* /","")
            shape = 0
            if "//" in finit:
                shape = eval(finit.split("//")[1].replace("shape = ",""))

            finit = finit.split("(")
            finit = ([finit[0]] + finit[1].split(")"))[0:-1]
            finit.append(shape)
            finit[0] = finit[0][1:-1]
            finit[1] = finit[1][1:-1]
            if "*" in finit[0]:
                finit[0] = finit[0].split(" * ")
                finit[0][0] += "*"
            else:
                 finit[0] = finit[0].split(" ")
            finit[1] = finit[1].split(" ")
            out = []
            for idx2, arg in enumerate(finit[1]):
                if idx2 % 2 == 0:
                    out.append(arg)
                else:
                    if "[]" in arg:
                        out[-1] += "*"
            if out[0] == "":
                out = ["void"]
            finit[1] = out
            functionsinit[idx] = finit

        return  functionsinit
