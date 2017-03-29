import shutil, bioservices, os
path_copasi_data = "/home/labestiol/Work/code/Notebooks/copasi/biomodels_copasi/"

db = bioservices.BioModels()

for model_id in sorted(db.getAllCuratedModelsId()):
	xml_filename = model_id + ".xml"
	xml_file = os.path.join(path_copasi_data, xml_filename)
	dest_file = os.path.join(model_id, "model.xml")
	
	if os.path.exists(xml_file):
		shutil.copy(xml_file, dest_file)

	results_filename = model_id + ".csv"
	results_file = os.path.join(path_copasi_data, results_filename)
	dest_file = os.path.join(model_id, "results.csv")
	
	if os.path.exists(results_file):
		shutil.copy(results_file, dest_file)

	

