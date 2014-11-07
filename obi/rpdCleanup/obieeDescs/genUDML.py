# Rittman Mead Presentation Layer Descriptions Tool
# --------------------------------------------------------------------------------------------------------
# This script generates some UDML to be copied into the RPD presentation layer.
# It requires the input UDML from the existing RPD presentation layer and a tab delimited table
# containing the descriptions that are to be updated. This can be generated using parseUDML.py and 
# edited using a text editor or Excel.
# --------------------------------------------------------------------------------------------------------
# Usage: parseUDML.py inputUDML inputTable
# --------------------------------------------------------------------------------------------------------
# Standard python distribution libraries: 
# 	glob is used for checking and iterating through directories of files
from glob import glob
# 	re is used for regex matching of HTTP responses from Presentation Services to derive the scid. 
import re
#	unlink  is used to delete (unlink/remove) temporary files
#	path is for manipulating and deriving paths
#	rename is used to rename files
#	makedirs is used to create output folders
from os import unlink
from os import path
from os import rename
from os import makedirs
#	sys.exit is used to bail out 
import	sys
#	optparse is used for command line option parsing
from optparse import OptionParser
#	rmtree is used to delete the baseline/comparison folders when requested
from shutil import rmtree, copyfile
#	codecs is required for UTF-8 file writing
import codecs

# Options, mainly used for help text
usage = '%prog [options] inputUDML'
opts = OptionParser(usage=usage)
opts.add_option("-o","--output",action="store",dest="outputFile",default="presLayer.udml",help="Output file for UDML presentation layer.")
input_opts , args = opts.parse_args()

# Error check: File Exists
def errorFileExist(filepath):
	if not path.isfile(filepath):
		print '\n\nFile: "%s" does not exist. Exiting.' % filepath
		sys.exit(1)
		
# Append to file
def write_output(line,filename):
	with codecs.open(filename,'a') as output: 
		output.write('%s\n' % line)

# Parse input description
def parseInDesc(match):
	desc = match.group(1)
	if desc:
		desc = re.sub('^"|"$', '', desc)
		desc = desc.replace('""','"')
		desc = 'DESCRIPTION {' + desc.replace('\\n', '\n') + '}'
	else:
		desc = ''
	return desc	

# Escape function to deal with special characters in RegEx
def escape(string):
	string = re.sub('^"|"$', '', string)
	string = string.replace('(','\(')
	string = string.replace(')','\)')
	string = string.replace('$','\$')
	string = string.replace('+','\+')
	string = string.replace('^','\^')
	return string

# Replaces or adds the description in the UDML
def replaceDesc(udml, desc):
	descMatch = re.search('DESCRIPTION {.*?}', udml, re.DOTALL)
	if descMatch:
		udml = udml.replace(descMatch.group(), desc)
	else:
		privString = re.search('PRIVILEGES.*;', udml, re.DOTALL)
		desc = desc + '\n' + privString.group()
		udml = udml.replace(privString.group(), desc)
	return udml
	
def modifyUDML(udml, table):
	saUDML = udml.split('DECLARE CATALOG FOLDER ')
	
	# Loop through subject areas
	for i in range(1, len(saUDML)):
	
		# Get subject area name
		saMatch = re.search('  AS "(.*?)"', saUDML[i])
		subjectArea = saMatch.group(1)
		
		print('Processing %s...' % (subjectArea))

		presTableUDML = saUDML[i].split('DECLARE ENTITY FOLDER ')
		
		# Find matching row in descriptions table
		saMatch = re.search(escape(subjectArea) + '\t\t\t(.*?)\n', table, re.DOTALL)
		if saMatch:
			inputDesc = parseInDesc(saMatch)
			presTableUDML[0] = replaceDesc(presTableUDML[0], inputDesc)
			
		write_output('DECLARE CATALOG FOLDER ' + presTableUDML[0], UDML_OUT)
		
		
		# Loop through presentation tables
		for j in range(1, len(presTableUDML)):
			presColUDML = presTableUDML[j].split('DECLARE FOLDER ATTRIBUTE ')
			
			# Get presentation table name
			presTable = re.search('" AS "(.*?)"', presTableUDML[j]).group(1)
			
			# Find matching row in descriptions table
			ptMatch = re.search(escape(subjectArea) + '\t' + escape(presTable) + '\t\t(.*?)\n', table, re.DOTALL)
			if ptMatch:
				inputDesc = parseInDesc(ptMatch)
				presColUDML[0] = replaceDesc(presColUDML[0], inputDesc)
				
			write_output('DECLARE ENTITY FOLDER ' + presColUDML[0], UDML_OUT)

			# Loop through presentation columns
			for k in range(1, len(presColUDML)):
				
				# Get presentation column name
				presCol = re.search('" AS "(.*?)"', presColUDML[k]).group(1)

				# Find matching row in descriptions table
				pcMatch = re.search(escape(subjectArea) + '\t' + escape(presTable) + '\t' + escape(presCol) + '\t(.*?)\n', table, re.DOTALL)
				if pcMatch:
					inputDesc = parseInDesc(pcMatch)
					presColUDML[k] = replaceDesc(presColUDML[k], inputDesc)
				
				write_output('DECLARE FOLDER ATTRIBUTE ' + presColUDML[k], UDML_OUT)

# Initiate required arguments and handle errors
try:
	INPUT_UDML = args[0]
	errorFileExist(INPUT_UDML)
	INPUT_TABLE = args[1]
	errorFileExist(INPUT_TABLE)
	
	UDML_OUT=input_opts.outputFile
	open(UDML_OUT, 'w')
	
except Exception, err:
	print '\n\nException caught:\n%s ' % (err)
        print '\nFailed to get command line arguments. Exiting.'
        sys.exit(1)
				
# Main code body
def main():
	print '\n\n\t\t------------------------------------------------'
	print '\t\tRittman Mead Presentation Layer Description Tool'
	print '\t\t------------------------------------------------\n\n'
	
	# Read input UDML
	with open(INPUT_UDML, 'r') as f:
		read_udml = f.read()
	f.closed
	
	# Read descriptions table
	with open(INPUT_TABLE, 'r') as f:
		read_table = f.read()
	f.closed
	
	modifyUDML(read_udml, read_table)
	
	print '\nUDML parsed successfully.'
	
	
if __name__ == "__main__":
	main()

