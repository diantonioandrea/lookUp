# lookUp

import lookUp
import os, sys, shutil, platform, requests, CLIbrary
from colorama import Fore, Back, Style
from datetime import datetime

# ---
# From an answer of Ciro Santilli on https://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python
import stat

def get_umask():
    umask = os.umask(0)
    os.umask(umask)

    return umask

def executable(filePath):
    os.chmod(filePath, os.stat(filePath).st_mode | ((stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) & ~get_umask()))
# ---

# MOTD

def lookUpMotd():
	print("\n" + Back.MAGENTA + Fore.WHITE + " " + version + " " + Back.WHITE + Fore.MAGENTA + " " + name + " " + Style.RESET_ALL) if production else print("\n" + Back.WHITE + Fore.BLUE + " " + name + " " + Style.RESET_ALL)
	print(Style.BRIGHT + "cat FILE | grep STRING" + Style.RESET_ALL  + " reimagined.")
	print("Developed by " + Style.BRIGHT + Fore.MAGENTA + "Andrea Di Antonio" + Style.RESET_ALL + ", more on " + Style.BRIGHT + "https://github.com/diantonioandrea/" + name + Style.RESET_ALL + "\n")

# HELP

def lookUpHelp():
	options = {"-s": "[STR] The string that gets searched throughout the file.", "--all": "Display full output.", "--install": "Installs lookUp."}

	print("Usage: lookUp file [{}]\n".format(" ".join(sorted([key for key in options]))))

	# Double dash.
	print("\t[--] options:\n\t" + "\n\t".join(sorted([Style.BRIGHT + key.replace("-", "") + Style.RESET_ALL + "\t\t" + options[key] for key in options if "--" in key])) + "\n")

	# Single dash.
	print("\t[-] options:\n\t" + "\n\t".join(sorted([Style.BRIGHT + key.replace("-", "") + Style.RESET_ALL + "\t\t" + options[key] for key in options if "--" not in key])) + "\n")


# Parses options in sys.argv.
sdOpts, ddOpts = lookUp.parser(sys.argv)

name = "lookUp"
version = "rolling"
production = True
if name not in "".join(sys.argv): # Local testing.
	production = False

system = platform.system()
path = os.getenv("PATH")

# PATHS

if production: # Production.
	homePath = os.path.expanduser("~") + "/"
	installPath = homePath
	
	if system == "Darwin":
		installPath += "Library/" + name + "/"
	
	elif system == "Linux":
		installPath += ".local/bin/" + name + "/"

	elif system == "Windows":
		installPath += "AppData/Roaming/" + name + "/"

else: # Testing.
	installPath = str(os.getcwd()) + "/"

# INSTALLATION

if "install" in ddOpts and production:
	lookUpMotd()

	try:
		currentPath = os.getcwd() + "/"

		if not os.path.exists(installPath):
			os.makedirs(installPath)

		if system != "Windows":
			shutil.copy(currentPath + name, installPath + name)

		else:
			shutil.copy(currentPath + name + ".exe", installPath + name + ".exe")

		CLIbrary.output({"type": "verbose", "string": name.upper() + " INSTALLED SUCCESFULLY TO " + installPath})

		if name not in path:
			CLIbrary.output({"type": "warning", "string": "MAKE SURE TO ADD ITS INSTALLATION DIRECTORY TO PATH TO USE IT ANYWHERE", "after": "\n"})
		
		else:
			print() # Blank space needed.
	
	except:
		CLIbrary.output({"type": "error", "string": "INSTALLATION ERROR", "after": "\n"})
		sys.exit(-1)

	finally:
		sys.exit(0)

try: # Looks for file name.
	filename = [inst for inst in sys.argv if inst[0] != "-" and inst[0] + inst[1] != "-"][1]

except(IndexError):
	lookUpMotd()

	# UPDATE NOTIFICATION
	# Does not check for updates "while working".

	if production:
		try:
			commits = requests.get("https://api.github.com/repos/diantonioandrea/" + name + "/commits").json()
			localVersion = datetime.fromtimestamp(os.path.getmtime(installPath + name + (".exe" if system == "Windows" else "")))
			localVersion = localVersion.replace(tzinfo=datetime.now().astimezone().tzinfo)

			changes = sum([localVersion < datetime.fromisoformat(commit["commit"]["author"]["date"]) for commit in commits])

			if changes:
				CLIbrary.output({"type": "verbose", "string": "{} NEW COMMIT(S), CHECK https://github.com/diantonioandrea/".format(changes) + name, "after": "\n"})

		except:
			pass

	lookUpHelp()
	sys.exit(0)

# MAIN PROGRAM.

try: # Tries to open the specified file.
	file = open(filename, "r+")
	content = file.read()
	file.close()

except(FileNotFoundError):
	CLIbrary.output({"type": "error", "string": "FILE NOT FOUND"})
	sys.exit(-1)

except:
	CLIbrary.output({"type": "error", "string": "CANNOT OPEN OR READ FILE"})
	sys.exit(-2)

# Searches for "-s string".
if "s" in sdOpts:
	string = sdOpts["s"]
	content = content.replace(string, Fore.RED + string + Fore.RESET)
	searched = True

else:
	searched = False

# Numbers of "-s string" found in file.
if searched:
	searchResult = "Found {} istance(s) of \"{}\" inside \"{}\"".format(content.count(string), string, file.name)
	print(searchResult + "\n" + "-" * len(searchResult))

# Prints the whole content if:
# - The file has not been searched.
# - the user specified "--all"
if not searched or "all" in ddOpts:
	print(content)

# Prints only the lines where "-s string" has been found.
else:
	lines = content.split("\n")
	print("\n".join(["{}: ".format(lines.index(line) + 1) + line for line in lines if string in line]))