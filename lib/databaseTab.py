databaseList = ['transfit','testdb','oncokb','civic','test01','transfic_3_base_score','transfic_score','interactome3d_by_dssp']
database_key_default_dict = {'transfit':'variant','testdb':'variant','oncokb':'gene-mutaAA','civic':'gene-mutaAA','test01':'gene','transfic_3_base_score':'index','transfic_score':'index','interactome3d_by_dssp':'index'}
database_head = {
	'transfit':'chromosome	chromosome_start	mutated_from_allele	mutated_to_allele\n',
	'testdb':'chromosome	chromosome_start	mutated_from_allele	mutated_to_allele	test1	test2\n',
	'oncokb':'gene	aa_muta	oncoKB_id	evidenceType	cancerType	subtype	curatedRefSeq	curatedIsoform	level\n',
	'civic':'gene	variant	variant_id	variant_civic_url	entrez_id	summary	variant_groups	chromosome	start	stop	reference_bases	variant_bases	representative_transcript	ensembl_version	reference_build	chromosome2	start2	stop2	representative_transcript2	variant_types	hgvs_expressions	last_review_date	civic_variant_evidence_score	allele_registry_id	clinvar_ids	variant_aliases	assertion_ids	assertion_civic_urls\n',
	'test01':'index	test01	test02\n',
	'transfic_3_base_score':'index	SIFT_score	Polyphen2_score	MutationAssessor_score\n',
	'transfic_score':'index	uid	gene_id	SIFT_score	Polyphen2_score	MutationAssessor_score	SIFT_transfic_score	Polyphen2_transfic_score	MutationAssessor_transfic_score	SIFT_transfic_label	Polyphen2_transfic_label	MutationAssessor_transfic_label\n',
	'interactome3d_by_dssp':'i3dpdbname	chainA_surface_single	chainB_surface_single	chainA_surface_dimer	chainB_surface_dimer	chainA_interface	chainB_interface\n'
}