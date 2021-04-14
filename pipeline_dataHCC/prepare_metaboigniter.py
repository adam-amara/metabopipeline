import subprocess
import sys
import os
import glob

import numpy as np
import pandas as pd

print('\n')
print('######################################')
print('################ START ###############')
print('######################################')
print('\n')

'''
- This part allows to organize the mzML files as described in https://github.com/nf-core/metaboigniter/blob/dev/docs/metaboigniter_guide.md 
- path2data is the relative path to the folder containing all the subfolders (one for each condition) which contain the mzML files
- It creates a folder
'''

path2data = input('Enter relative path to the folder containing all the subfolders (one for each condition) which contain the mzML files : ')

type_of_ionization = input('What type of ionization do you have ? Enter POS, NEG or BOTH : ')

need_centroiding = input('Does the workflow has to perform the centroiding ? Enter true or false : ')

blank_filter_pos = input('Do you want to remove signal from blank samples ? Enter true or false : ')

rename_output_pos_camera = input('Do you want to rename the samples in the output file ? Enter true or false : ')

blank_class = input('Enter the name of the class of the blank samples : ')

sample_class = input('Enter the name of the class of the biological samples : ')

QC_class = input('Entre the name of the class of the quality controls : ')

perform_identification = input('Do you want to perform identification ? Enter true or false : ')

MSMS_class = input('Enter the name of the class of the MS2 samples : ')

database_csv_files_pos_metfrag = input('Enter relative path to csv database : ')

print('\n')

#list_quant_files = [blank_class, sample_class, QC_class]

list_path2data = glob.glob(path2data + '/*')

list_path2data_quant = [elt for elt in list_path2data if MSMS_class not in elt]

quant_mzml_files_pos = '/'.join(path2data.split('/')[:-2]) + '/mzML_' + type_of_ionization + '_Quant'

print('==> All the mzML files will be copied in a same folder (', quant_mzml_files_pos, ') for the process')
subprocess.run(['mkdir', quant_mzml_files_pos])
print('==> Creation of the folder', quant_mzml_files_pos)

list_infos = []

for path in list_path2data_quant:
#for path in list_quant_files:

	list_mzMLfile = [mzMLfile for mzMLfile in os.listdir(path) if not mzMLfile.startswith('.')]

	for mzMLfile in list_mzMLfile:

		infos_curr = []

		old_path = path + '/' + mzMLfile

		#new_name = path.split('/')[-1] + mzMLfile

		subprocess.run(['cp', old_path, quant_mzml_files_pos])
		#subprocess.run(['mv', quant_mzml_files_pos + '/' + mzMLfile, quant_mzml_files_pos + '/' + new_name])
		#subprocess.run(['mv', quant_mzml_files_pos + '/' + mzMLfile, quant_mzml_files_pos + '/' + mzMLfile])

		#infos_curr.append(new_name)
		infos_curr.append(mzMLfile)
		infos_curr.append(path.split('/')[-1])

		if path.split('/')[-1] == 'Sample':
			if (mzMLfile.split('_')[-1] == '015.mzML' or mzMLfile.split('_')[-1] == '020.mzML'):
				infos_curr.append('Incident')
			else:
				infos_curr.append('Non-case')
		else:
			infos_curr.append('NA')

		list_infos.append(infos_curr)

print('==> The mzML files has been successfully copied in the same folder (', quant_mzml_files_pos, ')\n')

list_mzMLfile = [mzMLfile for mzMLfile in os.listdir(path2data + '/' + MSMS_class) if not mzMLfile.startswith('.')]
print(list_mzMLfile)

id_mzml_files_pos = '/'.join(path2data.split('/')[:-2]) + '/mzML_' + type_of_ionization + '_ID'
subprocess.run(['mkdir', id_mzml_files_pos])

for mzMLfile in list_mzMLfile :

	subprocess.run(['cp', path2data + '/' + MSMS_class + '/' + mzMLfile, id_mzml_files_pos])





print('==> Preparation of the phenotype files')
phenotype_file_infos = np.asarray(list_infos)
output_path_phenotype = '/'.join(path2data.split('/')[:-2]) + '/phenotype_files'
subprocess.run(['mkdir', output_path_phenotype])
print('==> Creation of the folder', output_path_phenotype)
phenotype_design_pos = output_path_phenotype + '/phenotype_' + type_of_ionization + '.csv'

with open(phenotype_design_pos, 'w') as myfile:
	myfile.write('RawFile,Class,Groups,\n')
	for elt in list_infos:
		myfile.write(elt[0] + ',' + elt[1] + ',' + elt[2] + ',\n')

# pd.DataFrame(phenotype_file_infos).to_csv(phenotype_design_pos, header=['RawFile', 'Class'])
print('==> The phenotype files has been successfully copied in the folder', output_path_phenotype, '\n')




print("==> Modification of parameter's values in parameters.config file")

with open('metaboigniter/conf/parameters.config', 'r') as myfile:

	filedata = myfile.read()



line_perform_identification = filedata[filedata.find("perform_identification = "):filedata.find('\n', filedata.find("perform_identification = "))]
line_perform_identification_replaced = line_perform_identification.replace('false', perform_identification, 1)

line_perform_identification_metfrag = filedata[filedata.find("perform_identification_metfrag = "):filedata.find('\n', filedata.find("perform_identification_metfrag = "))]
line_perform_identification_metfrag_replaced = line_perform_identification_metfrag.replace('false', perform_identification, 1)

line_type_of_ionization = filedata[filedata.find("type_of_ionization = "):filedata.find('\n', filedata.find("type_of_ionization = "))]
type_of_ionization = type_of_ionization.lower()
line_type_of_ionization_replaced = line_type_of_ionization.replace('pos', type_of_ionization, 1)

line_need_centroiding = filedata[filedata.find("need_centroiding"):filedata.find('\n', filedata.find("need_centroiding"))]
need_centroiding = need_centroiding.lower()
line_need_centroiding_replaced = line_need_centroiding.replace('false', need_centroiding, 1)

line_input = filedata[filedata.find("input = ''"):filedata.find('\n', filedata.find("input = ''"))]
quant_mzml_files_pos = quant_mzml_files_pos + '/*.mzML'
line_input_replaced = line_input.replace("''", "'" + quant_mzml_files_pos + "'", 1)

line_phenotype_design_pos = filedata[filedata.find("phenotype_design_pos = ''"):filedata.find('\n', filedata.find("phenotype_design_pos = ''"))]
line_phenotype_design_pos_replaced = line_phenotype_design_pos.replace("''", "'" + phenotype_design_pos + "'", 1)

line_id_mzml_files_pos = filedata[filedata.find("id_mzml_files_pos = ''"):filedata.find('\n', filedata.find("id_mzml_files_pos = ''"))]
id_mzml_files_pos = id_mzml_files_pos + '/*.mzML'
line_id_mzml_files_pos_replaced = line_id_mzml_files_pos.replace("''", "'" + id_mzml_files_pos + "'", 1)

line_ipo_valueToSelect_pos = filedata[filedata.find("ipo_valueToSelect_pos"):filedata.find('\n', filedata.find("ipo_valueToSelect_pos"))]
line_ipo_valueToSelect_pos_replaced = line_ipo_valueToSelect_pos.replace('QC', QC_class, 1)

line_sampleclass_quant_pos_xcms = filedata[filedata.find("sampleclass_quant_pos_xcms"):filedata.find('\n', filedata.find("sampleclass_quant_pos_xcms"))]
line_sampleclass_quant_pos_xcms_replaced = line_sampleclass_quant_pos_xcms.replace('Sample', sample_class, 1)

line_blank_filter_pos = filedata[filedata.find("blank_filter_pos"):filedata.find('\n', filedata.find("blank_filter_pos"))]
blank_filter_pos = blank_filter_pos.lower()
line_blank_filter_pos_replaced = line_blank_filter_pos.replace('false', blank_filter_pos, 1)

line_blank_blankfilter_pos_xcms = filedata[filedata.find("blank_blankfilter_pos_xcms"):filedata.find('\n', filedata.find("blank_blankfilter_pos_xcms"))]
line_blank_blankfilter_pos_xcms_replaced = line_blank_blankfilter_pos_xcms.replace('Blank', blank_class, 1)

line_sample_blankfilter_pos_xcms = filedata[filedata.find("sample_blankfilter_pos_xcms"):filedata.find('\n', filedata.find("sample_blankfilter_pos_xcms"))]
line_sample_blankfilter_pos_xcms_replaced = line_sample_blankfilter_pos_xcms.replace('Sample', sample_class, 1)

line_qc_cvfilter_pos_xcms = filedata[filedata.find("qc_cvfilter_pos_xcms"):filedata.find('\n', filedata.find("qc_cvfilter_pos_xcms"))]
line_qc_cvfilter_pos_xcms_replaced = line_qc_cvfilter_pos_xcms.replace('QC', QC_class, 1)

line_selected_type_output_pos_camera = filedata[filedata.find("selected_type_output_pos_camera"):filedata.find('\n', filedata.find("selected_type_output_pos_camera"))]
line_selected_type_output_pos_camera_replaced = line_selected_type_output_pos_camera.replace('Sample', sample_class, 1)

line_database_csv_files_pos_metfrag = filedata[filedata.find("database_csv_files_pos_metfrag"):filedata.find('\n', filedata.find("database_csv_files_pos_metfrag"))]
line_database_csv_files_pos_metfrag_replaced = line_database_csv_files_pos_metfrag.replace("''", "'" + database_csv_files_pos_metfrag + "'", 1)

line_selected_type_output_pos_camera = filedata[filedata.find("selected_type_output_pos_camera"):filedata.find('\n', filedata.find("selected_type_output_pos_camera"))]
line_selected_type_output_pos_camera_replaced = line_selected_type_output_pos_camera.replace("''", "'" + sample_class + "'", 1)

line_rename_output_pos_camera = filedata[filedata.find("rename_output_pos_camera"):filedata.find('\n', filedata.find("rename_output_pos_camera"))]
line_rename_output_pos_camera_replaced = line_rename_output_pos_camera.replace('true', rename_output_pos_camera, 1)

line_sampleclass_quant_library_pos_xcms = filedata[filedata.find("sampleclass_quant_library_pos_xcms"):filedata.find('\n', filedata.find("sampleclass_quant_library_pos_xcms"))]
line_sampleclass_quant_library_pos_xcms_replaced = line_sampleclass_quant_library_pos_xcms.replace('Sample', sample_class, 1)






filedata = filedata.replace(line_perform_identification, line_perform_identification_replaced)
filedata = filedata.replace(line_perform_identification_metfrag, line_perform_identification_metfrag_replaced)
filedata = filedata.replace(line_type_of_ionization, line_type_of_ionization_replaced)
filedata = filedata.replace(line_need_centroiding, line_need_centroiding_replaced)
filedata = filedata.replace(line_input, line_input_replaced)
filedata = filedata.replace(line_phenotype_design_pos, line_phenotype_design_pos_replaced)
filedata = filedata.replace(line_id_mzml_files_pos, line_id_mzml_files_pos_replaced)
filedata = filedata.replace(line_ipo_valueToSelect_pos, line_ipo_valueToSelect_pos_replaced)
filedata = filedata.replace(line_sampleclass_quant_pos_xcms, line_sampleclass_quant_pos_xcms_replaced)
filedata = filedata.replace(line_blank_filter_pos, line_blank_filter_pos_replaced)
filedata = filedata.replace(line_blank_blankfilter_pos_xcms, line_blank_blankfilter_pos_xcms_replaced)
filedata = filedata.replace(line_sample_blankfilter_pos_xcms, line_sample_blankfilter_pos_xcms_replaced)
filedata = filedata.replace(line_qc_cvfilter_pos_xcms, line_qc_cvfilter_pos_xcms_replaced)
filedata = filedata.replace(line_selected_type_output_pos_camera, line_selected_type_output_pos_camera_replaced)
filedata = filedata.replace(line_database_csv_files_pos_metfrag, line_database_csv_files_pos_metfrag_replaced)
filedata = filedata.replace(line_selected_type_output_pos_camera, line_selected_type_output_pos_camera_replaced)
filedata = filedata.replace(line_rename_output_pos_camera, line_rename_output_pos_camera_replaced)
filedata = filedata.replace(line_sampleclass_quant_library_pos_xcms, line_sampleclass_quant_library_pos_xcms_replaced)



with open('metaboigniter/conf/parameters.config', 'w') as myfile:

	myfile.write(filedata)

print('==> parameters (input, type_of_ionization, phenotype_design_pos, need_centroiding, ...) has been successfully modified in parameters_replaced.config file')




'''
TODO :
Manage the following parameters :
- type_of_ionization = '' ### set to pos
- need_centroiding = false ### set to false
- input = '' ### set to data/mzML
- quant_mzml_files_neg = '' ### No NEG for now
- phenotype_design_pos = '' ### set to 'data/phenotype_files/phenotype_POS.csv"
- phenotype_design_neg = '' ### No NEG for now
- ipo_valueToSelect_pos = 'QC' ### set to 'QCs'
- sampleclass_quant_pos_xcms = 'Sample' ### set to 'Samples'
- blank_filter_pos = false ### set to true
- blank_blankfilter_pos_xcms = 'Blank' ### set to 'Blanks'
- sample_blankfilter_pos_xcms = 'Sample' ### set to 'Samples'
- qc_cvfilter_pos_xcms = 'QC' ### set to 'QCs'
- selected_type_output_pos_camera = 'Sample' ### set to 'Samples'
- sampleclass_quant_library_pos_xcms = 'Sample' ### set to 'Samples'
'''

print('\n')
print('######################################')
print('################  END  ###############')
print('######################################')
print('\n')





