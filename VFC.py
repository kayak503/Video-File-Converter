#Video File Converter or VFC 
import argparse
import os  
import subprocess, shlex

programMode = ['file', 'folder']
outputFileTypes = ['.mp4', '.mov','.avi','.mkv','.flv']
intputFileTypes = ['.mp4', '.mov','.avi','.mkv','.flv']

class ERRORS:
	NOT_VALID_PATH = 1
	NOT_VALID_FILE_TYPE = 2
	DUPLICATED_RESPONCE = 3



# need to know if file or folder and input and output file 
mFormatRestriction = []
m_Mode = []

parser = argparse.ArgumentParser(description='Video File converter NEEDS FFMPEG installed in path')

#parser.add_argument('-t','--type' , choices=programMode , required=True, 
#					help='Choose to convert one video file or all video files in a folder') 
parser.add_argument('-i','--input' , type=str, required=True, 
					help='The input path of your file or folder that contains the video file(s)') 
parser.add_argument('-e','--inFormat' ,  
					help="Specifies witch video formats will be converted to the output file [user can add multiple formats with comma seperation] if field is left blank, program will convert all possible video files to the selected output folder [only applies to t- Folder] Acceptable formats : {}".format(intputFileTypes)) 
parser.add_argument('-o','--output' , type=str, required=True, 
					help='The output path of you video file(s) [must be a folder]') 
parser.add_argument('-f','--format' , choices=outputFileTypes, required=True, 
					help='Choose the output video format of the selected files') 

arguments = parser.parse_args()

def ValidateInfo(arguments):
	print("Validateing Request:")
	
	# Checks if input path is real
	if os.path.isdir(arguments.input): # path is a real path that dose not end in a file ...
		print("		[Program mode set to folder]\n		[Program Input path set to {}]\n".format(arguments.output))
		m_Mode.append("folder")
	elif os.path.isfile(arguments.input): # path is a real path and ends in a file ...
		print("		[Program mode set to file]\n")
		m_Mode.append("file")
	else:
		print("		[Error Input path not found]")
		return ERRORS.NOT_VALID_PATH

	# Checks if inFormat was filled and if it is good 
	if arguments.inFormat == None:
		print("		[No File Format Constraints]")
	else:
		listOfConstraints = arguments.inFormat.split(",")
		for constraint in listOfConstraints:
			try:
				intputFileTypes.index(constraint.lower())
				print("		[New File Format Constraint {}]".format(constraint.upper()))
				mFormatRestriction.append(constraint.lower())
				numberOfDuplicated = len(list( filter(lambda x: x.lower() == constraint.lower(), listOfConstraints)))
				if numberOfDuplicated >= 2:
					print("		[Error duplicate File Format Constraint detected, {} duplicated {} times; Program Terminated]".format(constraint.upper(), numberOfDuplicated))
					return ERRORS.DUPLICATED_RESPONCE

			except ValueError:
				print("		[Error File Format Constraint {} Not Valid; Program Terminated]".format(constraint.upper()))
				return ERRORS.NOT_VALID_FILE_TYPE
	
	# Checks if output path is real

	if os.path.isdir(arguments.output): # path is a real path that dose not end in a file ...
		print("\n		[Program Output path set to {}]".format(arguments.output))
	else:
		print("\n		[Error Output path not found]")
		return ERRORS.NOT_VALID_PATH

	print("\n		[Program Output format set to {}]".format(arguments.format))
	
	return 0
	
def ConvertFolder(arguments,FileFormats):
	BigFilelist = os.listdir(arguments.input)
	Filelist = []
	for Format in FileFormats:
		Filelist.append(list(filter(lambda x: x.split(".")[-1].lower() == Format.split(".")[-1].lower() ,BigFilelist)))
	for File in Filelist:
		inputFolder =str(arguments.input)
		NewFile = File[0].split(".")[0] + arguments.format
		cmd = "ffmpeg -loglevel fatal -i '{}' -q:v 0 '{}'".format(inputFolder+"/"+File[0], arguments.output+"/"+NewFile )
		print("		[{}] process starting...".format(NewFile))
		subprocess.run(shlex.split(cmd))
		print("		[{}] process finished continuing...".format(NewFile))

	


def ConvertFile(arguments):
	NewFile = arguments.input.split("\\")[-1].split(".")[0] + arguments.format
	cmd = "ffmpeg -loglevel fatal -i '{}' -q:v 0 '{}'".format(arguments.input, arguments.output+"\\"+NewFile )
	print("		[{}] process starting...".format(NewFile))
	subprocess.run(shlex.split(cmd))
	print("		[{}] process finished continuing...".format(NewFile))

if ValidateInfo(arguments) == 0:
	#print(m_Mode)

	if len(mFormatRestriction) == 0:
		mFormatRestriction = intputFileTypes

	if m_Mode[0] == 'file':
		ConvertFile(arguments)
	else:
		ConvertFolder(arguments,mFormatRestriction)
	print("Program finished")
