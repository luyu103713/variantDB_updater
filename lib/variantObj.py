
import requests, sys, uuid
import os
import json
import shutil
class uniportVar:
    def __init__(self,name,pos,ref,alt,uType="swissprot"):
        self.name = name
        self.uniprot_type = uType
        self.pos = str(pos)
        self.OK = True
        self.debug_massage = []
        self.uid = str(uuid.uuid1())
        self.ref = self.__checkAminoAcids(ref)
        self.alt = self.__checkAminoAcids(alt)
        self.geneSymbol = None
        self.ENSG = None
        self.ENST = None
        self.uniparc = None


    def __checkAminoAcids(self,aa):
        aa = str(aa).upper()
        residue_20=['G','A','V','L','I','P','F','Y','W','S','T','C','M','N','Q','D','E','K','R','H']
        if aa not in residue_20:
            self.OK = False
            self.debug_massage.append("Illegal Residue!")
        return aa

    def outputDebug(self):
        if not self.OK:
            for err in self.debug_massage:
                print(err)

class variant:
    def __init__(self, chrname,pos,ref,alt,version="hg38"):
        self.OK = True
        self.debug_massage = [] 
        self.trans_ok = None
        self.chrname = self.__checkHomoChrname(chrname)
        self.pos = str(pos)
        self.ref = self.__checkDNA(ref)
        self.alt = self.__checkDNA(alt)
        self.version = self.__checkCoordVersion(version)
        self.uid = str(uuid.uuid1())
        self.index = None

        self.__toolPWD()
        if version == "hg38":
            self.hg38_pos = self.pos 
        else:

            self.hg38_pos = None


    def getIndex(self,index):
        self.index = index

    def __toolPWD(self):
        if os.path.exists("config.ini"):
            print("####")
            # finish it later
        else:
            self.__temp_file_pwd = "./tmp/" + self.uid + "/"
            self.__liftover_pwd = "/data/Luhy/tools/liftover/"
        if not os.path.exists(self.__temp_file_pwd):
            os.mkdir(self.__temp_file_pwd)

    def __checkCoordVersion(self,version):
        version = str(version).lower()
        if version not in ["hg19","hg38","grch37","grch38"]:
            self.OK = False
            self.debug_massage.append("Varinat error: Illegal release of gene coordinates")
        elif version == "grch37":
            version = "hg19"
        elif version == "grch38":
            version = "hg38"
        return version

    def __checkDNA(self,dna):
        dna = str(dna).lower()
        if dna in ['t','c','g','a']:
            return dna
        else:
            self.OK = False
            self.debug_massage.append("Varinat init error: Illegal DNA")

    def __checkHomoChrname(self,chrname):
        chrname = str(chrname)
        if chrname in ['x',"X"]:
            return "X"
        elif chrname in ['y',"Y"]:
            return "Y"
        elif chrname in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"]:
            return chrname
        else:
            self.OK = False
            self.debug_massage.append("Varinat init error: chromosome " + chrname + " is out of range")
    def coordinatesTrans(self,toVersion):
        if self.OK:
            toVersion = self.__checkCoordVersion(toVersion)
            if toVersion == self.version:
                print("Variant gene coordinates is " + self.version + " now.")
            else:

                self.trans_ok = self.__coordTransByLiftOver(toVersion)

        else:
            print("Variant object has error,please debug!\nCannot transfer coordinates!")

    def __coordTransByLiftOver(self,toVersion):
        if self.version == toVersion:
            print("Variant gene coordinates is " + self.version + " now.")
        else:
            tmp_bed_input = self.__write_tmp_bed()
            #./liftOver test_map.bed3 hg19ToHg38.over.chain.gz output1.text unmap.txt
            tmp_result = self.__temp_file_pwd + self.uid + '_result.bed3'
            tmp_unmap = self.__temp_file_pwd + self.uid + '_unmap.bed3'
            if toVersion == "hg38":
                tmp_sh = self.__liftover_pwd + "liftOver " + tmp_bed_input + " hg19ToHg38.over.chain.gz " + tmp_result + " " + tmp_unmap
            elif toVersion == "hg19":
                tmp_sh = self.__liftover_pwd + "liftOver " + tmp_bed_input + " hg38ToHg19.over.chain.gz " + tmp_result + " " + tmp_unmap

            os.system(tmp_sh)
            if (os.path.getsize(tmp_unmap)) and (not os.path.getsize(tmp_result)):
                print("Coordinates release transformation error!")
                trans_ok = False
            else:
                trans_ok = True
                f = open(tmp_result,'r')
                l = f.readline()

                self.pos = str(l.split("\t")[1])
                self.version = toVersion
                if self.version == "hg38":
                    self.hg38_pos = self.pos 
                print("Coordinates release transformation done!")
                print("Variant gene coordinates is " + self.version + " now.")


    def __write_tmp_bed(self):
        tmp_bed_file = self.__temp_file_pwd + self.uid + '.bed3'
        f = open(tmp_bed_file,'w')
        f.write("chr" + self.chrname + "\t" + self.pos + "\t" + str(int(self.pos) + 1) + "\n") 
        f.close()
        return tmp_bed_file
    def outputDebug(self):
        if not self.OK:
            for err in self.debug_massage:
                print(err)
    def cleanTmpFile(self):
        if os.path.exists(self.__temp_file_pwd):
            shutil.rmtree(self.__temp_file_pwd)
        print("Clean tmp files....")





class VEPmap:
    """docstring for ClassName"""
    def __init__(self, variant):
        a =1


def main():
    B = variant(1,743267,'A','C',"hg19")
    print(B.uid)
    print(B.pos)
    B.coordinatesTrans("hg38")
    B.cleanTmpFile()
    B.cleanTmpFile()

if __name__ == '__main__':
    main()

#test 

#'https://rest.ensembl.org/vep/human/hgvs/3:g.179218303G>A?uniprot=true;content-type=application/json'

'''
B = variant('x',1,'A','C')
print(B.uid)
B = variant('x',1,'A','C')
print(B.uid)

for i in range(30):
    B = variant(i+1,1,'A','C')
    print(B.uid)
    print(B.OK)
    if not B.OK:
        B.outputDebug()
'''