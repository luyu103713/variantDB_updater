import json
#from lib.jobObj import *
import requests
import uuid,shutil,os

class pathway:
	"""docstring for pathway"""
	def __init__(self, gene,database,pathway_name,pathway_url,pathway_all_info,pathway_reference_list=[]):
		self.gene = gene
		self.database = database
		self.pathway_name = pathway_name
		self.pathway_url = pathway_url
		self.pathway_all_info  = pathway_all_info
		self.pathway_reference_list = pathway_reference_list
		self.wikiScore = -999
		self.kegg_drug_list = []
		self.kegg_disease_list = []



class genePathway:
	"""docstring for genePathway"""

	def __init__(self, gene):
		self.gene = gene    #gene obj
		self.gene_name = gene.gene_name
		self.pathway_list = []
	def get_all_database(self):
		self.keggJob()
		self.wikipathwayJob()
		self.reactomeJob()
	def get_kegg_map(self):
		f = open("kegg_hsa_map.txt","r")
		ls = f.readlines()
		kegg_map = {}
		for l in ls:
			temp = l.strip().split('\t')
			kegg_map[temp[0]] = temp[1][5:]

		return kegg_map

	def keggJob(self):
		kegg_has_map = self.get_kegg_map()
		gene = self.gene_name
		kegg_gene_list = []
		kegg_pathway_list = []
		#http://rest.kegg.jp/find/genes/braf     step1
		gene_url = "http://rest.kegg.jp/find/genes/" + gene
		response = requests.get(gene_url)
		#print(response.text)
		for l in response.text.split('\n'):
			kegg_gene_id = l.split('\t')[0]
			if kegg_gene_id[0:4] == "hsa:":
				kegg_gene_list.append(kegg_gene_id)
				if kegg_gene_id in kegg_has_map:
					kegg_pathway_list.append(kegg_has_map[kegg_gene_id])

		kegg_pathway_list = list(set(kegg_pathway_list))
		#print(kegg_pathway_list)
		#step2:http://rest.kegg.jp/get/hsa05130
		for pid in kegg_pathway_list:
			pathway_url = "http://rest.kegg.jp/get/" + pid
			#print(pathway_url)
			r = requests.get(pathway_url)
			ls = r.text.split('\n')
			#print(pathway_url)
			pathway_url = "https://www.kegg.jp/kegg-bin/show_pathway?" + pid
			disease_list = []
			pm_list = []
			drug_list = []
			name = None
			description = ""
			for l in ls:
				if l[:12] == "DESCRIPTION ":
					description = l[12:]
				elif l[:12] == "NAME        ":
					name = l[12:] 	
				elif l[:12] == "DISEASE     ":
					disease_list.append(l[20:]) 
				elif l[:12] == "REFERENCE   ":
					pm_list.append(l[12:]) 
				elif l[:12] == "DRUG        ":
					drug_list.append(l[20:]) 
			'''
			print(disease_list)
			print(pm_list)
			print(drug_list)
			'''
			if name:
				pathwayObj = pathway(gene,"kegg",name,pathway_url,description,pm_list)
				pathwayObj.kegg_drug_list = drug_list
				pathwayObj.kegg_disease_list = disease_list
				self.pathway_list.append(pathwayObj)

	def wikipathwayJob(self):
		gene = self.gene_name
		#https://webservice.wikipathways.org/findInteractions?query=braf&format=json
		url = "https://webservice.wikipathways.org/findInteractions?query=" + gene + "&format=json"
		response = requests.get(url)
		result_list = json.loads(response.text)["result"]
		#print(result_dict)
		wpid_list = []
		for info in result_list:
			wikiScore = info["score"]['0']
			pathway_url = info["url"]
			pathway_name = info["name"]
			pathUid = info["id"]
			species = info["species"]
			if (pathUid not in wpid_list) and (species == "Homo sapiens"):
				wpid_list.append(pathUid)
				pathwayObj = pathway(gene,"wikipathways",pathway_name,pathway_url,"",[])
				pathwayObj.wikiScore = wikiScore
				self.pathway_list.append(pathwayObj)
				#detail is complex , 
				'''
				#https://webservice.wikipathways.org/getPathway?pwId=WP3676&format=json
				detail_url = "https://webservice.wikipathways.org/getPathway?pwId=" + pathUid + "&format=json"
				r = requests.get(detail_url)
				pathDetail = json.loads(r.text)["pathway"]
				description = pathDetail["gpml"].split('<Comment Source=\\"WikiPathways-description\\">')[0].split('>')[-1]
				print(description)
				'''


			#print(pathway_url)

	def reactomeJob(self):
		gene = self.gene_name
		#https://reactome.org/ContentService/data/mapping/UniProt/BRAF/pathways?species=9606&format=json
		#https://reactome.org/ContentService/data/discover/R-HSA-9660537
		url = "https://reactome.org/ContentService/data/mapping/UniProt/" + gene  + "/pathways?species=9606&format=json"
		response = requests.get(url)
		result_dict = json.loads(response.text)
		#print(url)
		#print(result_dict)
		pathway_name_list = []
		for info in result_dict:
			pathway_name_list.append(info["stId"])
		#print(pathway_name_list)
		for paid in pathway_name_list:
			url = "https://reactome.org/ContentService/data/discover/" + paid
			response = requests.get(url)
			pathway_dict = json.loads(response.text)
			refer_list = []
			if pathway_dict["citation"]:
				for pm_url in pathway_dict["citation"]:
					pmid = "PMID:" + pm_url.split('/')[-1]
					refer_list.append(pmid)
			pathwayObj = pathway(gene,"reactome",pathway_dict["name"],pathway_dict["url"],pathway_dict["description"],refer_list)
			self.pathway_list.append(pathwayObj)

		for pw in self.pathway_list:
			print(pw.pathway_reference_list)












