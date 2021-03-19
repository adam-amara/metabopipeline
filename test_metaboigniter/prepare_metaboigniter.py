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
print('\n')

list_path2data = glob.glob(path2data + '/*')

quant_mzml_files_pos = '/'.join(path2data.split('/')[:-1]) + '/mzML_' + type_of_ionization + '_Quant'
print('==> All the mzML files will be copied in a same folder (', quant_mzml_files_pos, ') for the process')
subprocess.run(['mkdir', quant_mzml_files_pos])
print('==> Creation of the folder', quant_mzml_files_pos)

list_infos = []

for path in list_path2data:

	list_mzMLfile = [mzMLfile for mzMLfile in os.listdir(path) if not mzMLfile.startswith('.')]

	for mzMLfile in list_mzMLfile:

		infos_curr = []

		infos_curr.append(mzMLfile)
		infos_curr.append(path.split('/')[-1])

		list_infos.append(infos_curr)

		subprocess.run(['cp', path + '/' + mzMLfile, quant_mzml_files_pos])

print('==> The mzML files has been successfully copied in the same folder (', quant_mzml_files_pos, ')\n')

print('==> Preparation of the phenotype files')
phenotype_file_infos = np.asarray(list_infos)
output_path_phenotype = '/'.join(path2data.split('/')[:-1]) + '/phenotype_files'
subprocess.run(['mkdir', output_path_phenotype])
print('==> Creation of the folder', output_path_phenotype)
phenotype_design_pos = output_path_phenotype + '/phenotype_' + type_of_ionization + '.csv'
pd.DataFrame(phenotype_file_infos).to_csv(phenotype_design_pos, header=['RawFile', 'Class'])
print('==> The phenotype files has been successfully copied in the folder', output_path_phenotype, '\n')




print("==> Modification of parameter's values in parameters.config file")

with open('metaboigniter/conf/parameters.config', 'r') as myfile:

	filedata = myfile.read()


line_input_param = filedata[filedata.find("input = ''"):filedata.find('\n', filedata.find("input = ''"))]
quant_mzml_files_pos = quant_mzml_files_pos + '/*.mzML'
line_input_param_replaced = line_input_param.replace("''", "'" + quant_mzml_files_pos + "'", 1)

line_ionization_param = filedata[filedata.find("type_of_ionization = "):filedata.find('\n', filedata.find("type_of_ionization = "))]
type_of_ionization = type_of_ionization.lower()
line_ionization_param_replaced = line_ionization_param.replace('pos', type_of_ionization, 1)

line_phenotype_param = filedata[filedata.find("phenotype_design_pos = ''"):filedata.find('\n', filedata.find("phenotype_design_pos = ''"))]
line_phenotype_param_replaced = line_phenotype_param.replace("''", "'" + phenotype_design_pos + "'", 1)

line_centroiding_param = filedata[filedata.find("need_centroiding"):filedata.find('\n', filedata.find("need_centroiding"))]
need_centroiding = need_centroiding.lower()
line_centroiding_param_replaced = line_centroiding_param.replace('false', need_centroiding, 1)

filedata = filedata.replace(line_input_param, line_input_param_replaced)
filedata = filedata.replace(line_ionization_param, line_ionization_param_replaced)
filedata = filedata.replace(line_phenotype_param, line_phenotype_param_replaced)
filedata = filedata.replace(line_centroiding_param, line_centroiding_param_replaced)


with open('metaboigniter/conf/parameters.config', 'w') as myfile:

	myfile.write(filedata)

print('==> parameters (input, type_of_ionization, phenotype_design_pos, need_centroiding) has been successfully modified in parameters_replaced.config file')




'''
TODO :
Manage the following parameters :
- input = '' ### OK
- quant_mzml_files_neg = '' ### No NEG for now
- type_of_ionization = '' ### OK
- phenotype_design_pos = '' ### OK
- phenotype_design_neg = '' ### No NEG for now

'''

print('\n')
print('######################################')
print('################  END  ###############')
print('######################################')
print('\n')





