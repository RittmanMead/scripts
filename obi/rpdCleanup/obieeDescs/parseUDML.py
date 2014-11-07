# Rittman Mead Presentation Layer Descriptions Tool
# --------------------------------------------------------------------------------------------------------
# This script parses a UDML Presentation Layer copied from an RPD and saved to Text.
# It produces a tab separated output file that allows users to enter against objects outside of the RPD.
# Another script is provided to consume this, providing a new UDML with the descriptions added.
# This can then be pasted into the RPD.
# --------------------------------------------------------------------------------------------------------
# Usage: parseUDML.py inputUDML
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

usage = '%prog [options] inputUDML'
opts = OptionParser(usage=usage)
opts.add_option("-o","--output",action="store",dest="outputFile",default="desc.txt",help="Output file for object descriptions.")
input_opts , args = opts.parse_args()

# Initiate required arguments and handle errors
try:
	if path.isfile(args[0]):
		INPUT_UDML = args[0]
	else:
		print '\n\nInput UDML File: "%s" does not exist. Exiting.' % args[0]
		sys.exit(0)
	
	DESC_OUT=input_opts.outputFile
	open(DESC_OUT, 'w')
	
except Exception, err:
	print '\n\nException caught:\n%s ' % (err)
        print '\nFailed to get command line arguments. Exiting.'
        sys.exit(1)
		
# Append to file
def write_output(line,filename):
	with open(filename,'a') as output: 
		output.write('%s\n' % line)

# Parse description UDML
def parseDesc(udml):
	desc = re.search('DESCRIPTION {(.*?)}', udml, re.DOTALL)
	if desc:
		desc = desc.group(1).replace('\n','\\n')
	else:
		desc = ''
	return desc
		
def parseUDML(udml):
	saUDML = udml.split('DECLARE CATALOG FOLDER ')
	
	# Loop through subject areas
	for i in range(1, len(saUDML)):
		saMatch = re.search('  AS "(.*?)"', saUDML[i])
		subjectArea = saMatch.group(1)
		
		print('Processing %s...' % (subjectArea))

		presTableUDML = saUDML[i].split('DECLARE ENTITY FOLDER ')
		
		# Get subject area description
		desc = parseDesc(presTableUDML[0])
		write_output('%s\t\t\t%s' % (subjectArea, desc), DESC_OUT)
		
		#presTable = re.findall('" AS "(.*?)"', saUDML[i])
		
		# Loop through presentation tables
		for j in range(1, len(presTableUDML)):
			presColUDML = presTableUDML[j].split('DECLARE FOLDER ATTRIBUTE ')
			
			# Get presentation table description
			presTable = re.search('" AS "(.*?)"', presTableUDML[j]).group(1)
			desc = parseDesc(presColUDML[0])
			write_output('%s\t%s\t\t%s' % (subjectArea, presTable, desc), DESC_OUT)
			
			# Loop through presentation columns
			for k in range(1, len(presColUDML)):
				
				# Get presentation column description
				presCol = re.search('" AS "(.*?)"', presColUDML[k]).group(1)
				desc = parseDesc(presColUDML[k])
				write_output('%s\t%s\t%s\t%s' % (subjectArea, presTable, presCol, desc), DESC_OUT)
		
# Main code body
def main():
	print '\n\n\t\t------------------------------------------------'
	print '\t\tRittman Mead Presentation Layer Description Tool'
	print '\t\t------------------------------------------------\n\n'
	
	with open(INPUT_UDML, 'r') as f:
		read_udml = f.read()
	f.closed
	
	# Header row
	write_output('Subject Area\tPresentation Table\tPresentation Column\tDescription', DESC_OUT)
	
	parseUDML(read_udml)
	
	print '\nUDML parsed successfully.'
	
if __name__ == "__main__":
	main()

