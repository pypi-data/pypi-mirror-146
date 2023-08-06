import cppimport,os,CppHeaderParser
def valid(s:str):
    if s[0].isalpha() or s[0] == '_':
        for i in s[1:]:
            if not(i.isalnum() or i == '_' or i.isalpha()):
                return False
        return True
    else:
        return False
all_cppfiles=set()
class Cppfile:
    def __init__(self,module_name="Cppcode_template"):
        if module_name in all_cppfiles:
            raise Exception("The cppfilename \"{}\" is already in use!".format(module_name))
        else:
            self.module_name=module_name
            all_cppfiles.add(module_name)
    def compile(self,code:str):
        module_name=self.module_name
        pyi=""
        elems=CppHeaderParser.CppHeader(code,"string")
        code="#include <pybind11/pybind11.h>\n#include <pybind11/stl.h>\nnamespace py = pybind11;\nusing namespace std;\n"+code
        code+="\nPYBIND11_MODULE({}, m) {{\n".format(module_name)
        for i in elems.functions:
            if valid(i["name"]):
                code+="m.def(\"{}\", py::overload_cast<{}>(&{}));\n".format(i["name"],",".join(j["type"] for j in i["parameters"]),i["name"])
                pyi+="def {}({}):\n\tpass\n".format(i["name"],",".join(j["name"] for j in i["parameters"]))
        for i in elems.classes:
            if valid(i):
                code+="py::class_<{}>(m, \"{}\")\n".format(i,i)
                pyi+="class {}:\n".format(i)
                flag=0
                for j in elems.classes[i]["methods"]["public"]:
                    if j["constructor"]:
                        code+=".def(py::init<{}>())\n".format(",".join([k["type"] for k in j["parameters"]]))
                        pyi+="\tdef __init__(self,{}):\n{}\n".format(",".join([k["name"] for k in j["parameters"]]),(lambda i:i if i else "\t\tpass\n")("".join(["\t\tself.{}=None\n".format(j["name"]) for j in elems.classes[i]["properties"]["public"]])))
                        flag=1
                    elif j["destructor"]:continue
                    else:
                        code+=".def(\"{}\", py::overload_cast<{}>(&{}::{}))\n".format(j["name"],",".join(k["type"] for k in j["parameters"]),i,j["name"])
                        pyi+="\tdef {}(self,{}):\n\t\tpass\n".format(j["name"],",".join([k["name"] for k in j["parameters"]]))
                if not flag:
                    pyi+="\tdef __init__(self):\n{}\n".format((lambda i:i if i else "\t\tpass\n")("".join(["\t\tself.{}=None\n".format(j["name"]) for j in elems.classes[i]["properties"]["public"]])))
                for j in elems.classes[i]["properties"]["public"]:
                    code+=".def_readwrite(\"{}\", &{}::{})\n".format(j["name"],i,j["name"])
                code+=';\n';
        code+="}\n"
        with open("{}.cpp".format(module_name),"w") as f:
            f.write(code+"\n/*\n<%\nsetup_pybind11(cfg)\n%>\n*/")
        ret=cppimport.imp_from_filepath("{}.cpp".format(module_name))
        if os.path.exists(".rendered.{}.cpp".format(module_name)):
            os.remove(".rendered.{}.cpp".format(module_name))
        with open("{}.pyi".format(module_name),"w",encoding="utf-8") as f:
            f.write(pyi)
        return ret
    def __del__(self):
        all_cppfiles.remove(self.module_name)
if __name__=="__main__":
    a=Cppfile("Hello").compile("""
    int add(int a,int b){
        return a+b;
    }
    """)
    print(a.add(1,2))
    # or
    import Hello
    print(Hello.add(3,4))
        