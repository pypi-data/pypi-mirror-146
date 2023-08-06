import os

class yc_e:
    def __init__(self):
        while True:
            ret = os.popen("e z").readlines()
            if ret[0].find("sync 0 = 02")!=-1:
                break
            
    def e_k(self):
        os.system("e k")
        
    def e_p(self):
        while True:
            ret = os.popen("e p").readline()
            print(ret)
            if ret.find("Stopped") != -1:
                break
    
    def tohex(self,d):
        return hex(d).replace("0x","")
            
    def get_mem_data(self,addr,len):
        result = os.popen("e "+self.tohex(addr)+"l"+self.tohex(len)).readlines()
        odata=[]
        for line in result[1:]:
            for data in line.split(":")[1].strip().split(" "):
                odata.append(int(data,16))
        return odata
    
    def get_byte(self,addr):
        ret = self.get_mem_data(addr,1)
        return ret[0]

    def get_word(self,addr):
        ret = self.get_mem_data(addr,2)
        return ret[0] + (ret[1] << 8)

    def get_dword(self,addr):
        ret = self.get_mem_data(addr,4)
        return ret[0] + (ret[1] << 8) + (ret[2] << 16) + (ret[3] << 24)
    