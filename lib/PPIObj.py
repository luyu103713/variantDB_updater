import json
#from lib.jobObj import *
import requests
import uuid,shutil,os


class single_PPI:
    """docstring for PPI"""
    def __init__(self, base, other,database, identifier="gene"):
        self.gene1 = base
        self.gene2 = other
        self.database = database
        self.identifier = identifier

        self.string_score = None
        self.pmid=''
        self.uniprot1 = ""
        self.uniprot2 = ""
        self.intact_miscore = None
def ensp_to_uniprot(ensp):
    requestURL = "https://www.ebi.ac.uk/proteins/api/proteins/Ensembl:"+ ensp + "?offset=0&size=100"

    r = requests.get(requestURL, headers={ "Accept" : "application/json"})
    response_dict = json.loads(r.text)
    try:
        result = response_dict[0]['accession']
    except:
        result = ""
    return result
class genePPI:
    """docstring for ClassName"""
    #def __init__(self, gene,jobid):
    def __init__(self, gene):
        self.gene = gene #gene obj
        self.gene_name = gene.gene_name
        #self.jobid = jobid
        self.PPI_all_list = []
    def get_gene_from_mitab(self,l):
        temp = l.split('|')
        gene = ''
        for s in temp:
            if len(s) > 12:
                if s[-11:] == "(gene name)":
                    gene = s.split(':')[1][:-11]
        return gene
    def get_pmid_from_mitab(self,l):
        temp = l.split('|')
        pmid = ''
        for s in temp:
            if len(s) > 8:
                if s[:7].lower() == "pubmed:":
                    pmid = "PMID:" + s[7:]
        return pmid
    def check_taxid(temp):
    	
    def get_mitab_info(self,l):
        ok = True
        temp = l.strip().split('\t')

        index = 0
        for col in temp:
            print(index)
            print(col)
            index += 1


        gene1 = self.get_gene_from_mitab(temp[4])
        gene2 = self.get_gene_from_mitab(temp[5])
        uniprot1 = temp[0].split(':')[1]
        uniprot2 = temp[1].split(':')[1]
        PMID = self.get_pmid_from_mitab(temp[8])
        if temp[14].split(':')[0] == 'intact-miscore':
        	intact_miscore = temp[14].split(':')[1]
        #print(PMID)
        taxid = self.check_taxid(temp)

    def stringJob(self,score_limit = 0.4):
        #https://string-db.org/api/tsv-no-header/interaction_partners?identifiers=TP53%0dCDK2&limit=1
        string_api_url = "https://string-db.org/api"
        output_format = "tsv-no-header"
        method = "interaction_partners"
        request_url = "/".join([string_api_url, output_format, method])
        #print(request_url)
        params = {
            "identifiers" : self.gene_name,    
            "species" : 9606, # species NCBI identifier 
            "limit" : 1000,
        }
        #url = string_api_url + output_format + '/' + method + '?identifiers=' 
        response = requests.post(request_url, data=params)
        #print(response.text)
        ensp_list = []
        ensp_dict = {}
        string_ppi_list = []
        for line in response.text.strip().split("\n"):
            #print(line)
            l = line.strip().split("\t")
            query_ensp = l[0]
            query_name = l[2]
            partner_ensp = l[1]
            partner_name = l[3]
            combined_score = l[5]  
            if float(combined_score) >= 0.4:
                temp_PPI = single_PPI(query_name,partner_name,'string')
                temp_PPI.string_score = combined_score
                temp_PPI.uniprot1 = query_ensp[5:]
                temp_PPI.uniprot2 = partner_ensp[5:]
                #print(temp_PPI.uniprot1)
                ensp_list.append(temp_PPI.uniprot1)
                #print(temp_PPI.uniprot2)
                ensp_list.append(temp_PPI.uniprot2)
                string_ppi_list.append(temp_PPI)
            
        ensp_list = list(set(ensp_list))
        for ensp in ensp_list:
            ensp_dict[ensp] = ensp_to_uniprot(ensp)
        for PPI in string_ppi_list:
            PPI.uniprot1 = ensp_dict[PPI.uniprot1]
            PPI.uniprot2 = ensp_dict[PPI.uniprot2]
        self.PPI_all_list = self.PPI_all_list + string_ppi_list

            #print("\t".join([query_ensp, query_name, partner_name, combined_score]))

    def mintJob(self):
        gene = self.gene
        #mint_url = http://www.ebi.ac.uk/Tools/webservices/psicquic/mint/webservices/current/search/query/p53



    def biogridJob(self):
        '''
        sh = "cd /data/Luhy/tools/variantDB_updater/biogridpy\npython biogridUI.py " + self.gene
        temp_sh_name = str(uuid.uuid1()) + "_temp.sh"
        f = open(temp_sh_name,'w')
        f.write(sh)
        f.close()
        os.system('sh '+ temp_sh_name)
        if os.path.exists(temp_sh_name):
            https://webservice.thebiogrid.org/evidence/?accesskey=acc29f7f34613d02128e331a46859e51&format=json
            os.remove(temp_sh_name)        
        '''
        #use api not biogridpy
        #https://webservice.thebiogrid.org/interactions?searchNames=true&geneList=TP53&includeInteractors=true&includeInteractorInteractions=false&taxId=9606&accesskey=acc29f7f34613d02128e331a46859e51&format=json
        url = "https://webservice.thebiogrid.org/interactions?searchNames=true&geneList=" + self.gene_name + "&includeInteractors=true&includeInteractorInteractions=false&taxId=9606&accesskey=acc29f7f34613d02128e331a46859e51&format=json"
        response = requests.get(url)
        result_dict = json.loads(response.text)
        print(url)

        for key in result_dict:
            #print(key)

            if (result_dict[key]["PUBMED_ID"] != "") and (result_dict[key]["EXPERIMENTAL_SYSTEM_TYPE"] == "physical"):#from reference only/physical contact only
                #print(key)
                #print(result_dict[key])
                gene1 = result_dict[key]["OFFICIAL_SYMBOL_A"]
                gene2 = result_dict[key]["OFFICIAL_SYMBOL_B"]
                if gene1 == self.gene_name:
                    temp_PPI = single_PPI(gene1,gene2,'biogrid')
                    temp_PPI.pmid = "PMID:" + str(result_dict[key]["PUBMED_ID"])
                    self.PPI_all_list.append(temp_PPI)
                elif gene2 == self.gene_name:
                    temp_PPI = single_PPI(gene2,gene1,'biogrid')
                    temp_PPI.pmid ="PMID:" + str(result_dict[key]["PUBMED_ID"])
                    self.PPI_all_list.append(temp_PPI)
        for PPI in self.PPI_all_list:
            print(PPI.gene1 + '\t' + PPI.gene2 + '\t' + PPI.pmid)




def main():
    gene = "TP53"
    testObj = genePPI(gene)
    #testObj.stringJob()
    testObj.keggJob()
    #test



if __name__ == '__main__':
    main()