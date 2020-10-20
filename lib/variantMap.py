import requests, sys, uuid, json
from variantObj import variant,uniportVar
class variantMap(variant):
    """docstring for testVep"""
    def mapUniprotVar(self,method="vepApi"):
        if self.OK:
            self.uniprotMapList = []
            if method == "vepApi":
                #https://rest.ensembl.org/vep/human/hgvs/3:g.179218303G>A?uniprot=true;dbNSFP=LRT_pred;content-type=application/json
                if (self.version == "hg19") and (not self.hg38_pos):

                    self.__quickGetHg38()
                url = "https://rest.ensembl.org/vep/human/hgvs/" + self.chrname + ":g." + self.hg38_pos + self.ref.upper() + ">" + self.alt.upper() + "?uniprot=true;content-type=application/json"
                #print(url)
                self.debug_vep_url = url
                r = requests.get(url)
                if not r.ok:
                    #r.raise_for_status()
                    self.OK = False
                    self.debug_massage.append("Cannot access vep ebi api.")
                else:
                    #print(r.text)
                    result_dict = json.loads(r.text)[0]
                    if "transcript_consequences" in result_dict:
                        for var in result_dict["transcript_consequences"]:
                            #print(var)
                            if ("protein_start" in var or "protein_end" in var) and ("amino_acids" in var) and ("swissprot" in var or "uniparc" in var or "trembl" in var):
                                #begin read uniprot var
                                if "swissprot" in var:
                                    name = var["swissprot"][0]
                                    uni_type = "swissprot"
                                elif "trembl" in var:
                                	name = var["trembl"][0]
                                	uni_type = "trembl"
                                elif "uniparc" in var:
                                    name = var["uniparc"][0]
                                    uni_type = "uniparc"


                                if "protein_start" in var:
                                    pos = var["protein_start"]
                                elif "protein_end" in var:
                                    pos = var["protein_end"]
                                ref = var["amino_acids"][0]
                                alt = var["amino_acids"][-1]
                                #__init__(self,name,pos,ref,alt,uType="swissprot")
                                uniVar = uniportVar(name,pos,ref,alt,uni_type)
                                if "uniparc" in var:
                                    uniVar.uniparc = var["uniparc"][0]
                                    
                                if "transcript_id" in var:
                                    uniVar.ENST = var["transcript_id"]
                                if "gene_id" in var:
                                    uniVar.ENSG = var["gene_id"]
                                if "gene_symbol" in var:
                                    uniVar.geneSymbol = var["gene_symbol"]  
                                    
                                if uniVar.OK:
                                     self.uniprotMapList.append(uniVar)                             

                    else:
                        self.OK = False
                        self.debug_massage.append("transcript_consequences not in results.")


        else:

            print("Variant object has error,please debug!\nCannot map to Uniprot!")

    def __quickGetHg38(self):
        ##############################
        # easy but wasty,reversion later
        ##############################
        self.coordinatesTrans("hg38")
        self.coordinatesTrans("hg19")

def main():
    B = variantMap(7,140453136,'A','T',"hg19")
    print(B.uid)
    print(B.pos)

    B.mapUniprotVar()
    #print(B.debug_vep_url)
    for var in B.uniprotMapList:
        #print(var)
        print(var.name + ":" +var.ref + var.pos + var.alt )
        print(var.geneSymbol)



    B = variantMap(6,88060121,'C','T',"hg19")
    print(B.uid)
    print(B.pos)

    B.mapUniprotVar()    
    #print(B.debug_vep_url)
    for var in B.uniprotMapList:
        #print(var)
        print(var.name + ":" +var.ref + var.pos + var.alt )
        print(var.geneSymbol)

    B = variantMap(17,38788559,'C','T',"hg19")
    print(B.uid)
    print(B.pos)

    B.mapUniprotVar()    
    #print(B.debug_vep_url)
    for var in B.uniprotMapList:
        #print(var)
        print(var.name + ":" +var.ref + var.pos + var.alt )
        print(var.geneSymbol)
if __name__ == '__main__':
    main()