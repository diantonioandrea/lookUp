# lookUp

import lookUp
import os, sys, shutil, platform, requests, regex, CLIbrary
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
	print("\n" + Back.MAGENTA + Fore.WHITE + " " + version + " " + Back.WHITE + Fore.MAGENTA + " " + name + " " + Style.RESET_ALL) if production else print("\n" + Back.WHITE + Fore.MAGENTA + " " + name + " " + Style.RESET_ALL)
	print(Style.BRIGHT + "cat FILE | grep STRING" + Style.RESET_ALL  + " reimagined.")
	print("Developed by " + Style.BRIGHT + Fore.MAGENTA + "Andrea Di Antonio" + Style.RESET_ALL + ", more on " + Style.BRIGHT + "https://github.com/diantonioandrea/" + name + Style.RESET_ALL + "\n")

# HELP

def lookUpHelp():
	options = {"-s STR": "The string that gets searched throughout the file.", "--all": "Display full output.", "--install": "Installs lookUp."}
	options.update({"--noCase": "Disables case sensitivity.", "--uninstall": "Uninstalls lookUp.", "-r STR": "The pattern for a regular expression search."})

	spaces = max([len(key) + 4 for key in options])

	print("Usage: lookUp file [{}]".format("  ".join(sorted([key for key in options]))))

	# Double dash.
	print("\n\t" + "\n\t".join(sorted([Style.BRIGHT + key + Style.RESET_ALL + " " * (spaces - len(key)) + options[key] for key in options if "--" in key])))

	# Single dash.
	print("\n\t" + "\n\t".join(sorted([Style.BRIGHT + key + Style.RESET_ALL + " " * (spaces - len(key)) + options[key] for key in options if "--" not in key])) + "\n")


# Parses options in sys.argv.
sdOpts, ddOpts = lookUp.parser(sys.argv)

name = "lookUp"
version = "rolling"
production = True
if name.lower() not in "".join(sys.argv).lower(): # Local testing (python3 src/main.py).
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

# UNINSTALLATION

if "uninstall" in ddOpts and production:
	lookUpMotd()

	try:
		shutil.rmtree(installPath)
		CLIbrary.output({"type": "verbose", "string": name.upper() + " UNINSTALLED SUCCESFULLY FROM " + installPath})

		if name in path:
			CLIbrary.output({"type": "warning", "string": "MAKE SURE TO REMOVE ITS INSTALLATION DIRECTORY FROM PATH", "after": "\n"})
		
		else:
			print() # Blank space needed.
	
	except:
		CLIbrary.output({"type": "error", "string": "UNINSTALLATION ERROR", "after": "\n"})
		sys.exit(-1)

	finally:
		sys.exit(0)

# MAIN PROGRAM.

try: # Looks for file name.
	filename = [inst for inst in sys.argv if inst[0] != "-" and ((inst[0] + inst[1] != "-") if len(inst) > 1 else False)][1]

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

if "noCase" in ddOpts:
	content = content.lower()

# Colours.
sColour = Fore.RED
sColourName = " RED"
rColour = Fore.CYAN
rColourName = " CYAN"

# Results of search and regexp.
words = []

try:
	# Searches for "-s string".
	if "s" in sdOpts:
		sWord = sdOpts["s"]
		words += [sWord]

		# Case sensitivity search.
		if "noCase" in ddOpts:
			sWord = sWord.lower()

		# Colours content.
		sFlag = True
		content = content.replace(sWord, sColour + sWord + Fore.RESET)

		# Result.
		searchResult = "SEARCH: found {} istance(s) of \"{}\" inside \"{}\"{}".format(content.count(sWord), sWord, file.name, ", case ignored." if "noCase" in ddOpts else ".")
		print(searchResult + " |" + sColour + sColourName + Fore.RESET + "\n" + "-" * len(searchResult))

	else:
		sFlag = False

except:
	CLIbrary.output({"type": "error", "string": "SEARCH ERROR"})
	sys.exit(-3)

try:
	# Searches for "-r pattern".
	if "r" in sdOpts:
		# Case sensitivity regexp.
		if "noCase" in ddOpts:
			pattern = regex.compile(sdOpts["r"], regex.IGNORECASE)

		else:
			pattern = regex.compile(sdOpts["r"])

		# Finds all matches.
		rWords = regex.findall(pattern, content)
		words += rWords

		# Colours content.
		rFlag = True
		for rWord in rWords:
			content = content.replace(rWord, rColour + rWord + Fore.RESET)

		# Result.
		regularResult = "REGEXP: found {} match(es) of \"{}\" inside \"{}\"{} {}".format(sum([content.count(rString) for rString in rWords]), sdOpts["r"], file.name, ", case ignored:" if "noCase" in ddOpts else ":", ", ".join(set(rWords)) + "." if len(rWords) else "N/A.")
		print(regularResult + " |" + rColour + rColourName + Fore.RESET +  "\n" + "-" * len(regularResult))


	else:
		rFlag = False

except:
	CLIbrary.output({"type": "error", "string": "REGEXP ERROR"})
	sys.exit(-4)

# Prints the whole content either if:
# - The file has not been searched.
# - the user specified "--all"
if (not sFlag and not rFlag) or "all" in ddOpts:
	print(content)
	sys.exit(0)

# Prints only the lines where "-s string" and "-r pattern" has been found.
else:
	lines = content.split("\n")
	print("\n".join(["{}: ".format(lines.index(line) + 1) + line for line in lines if True in [word in line for word in words]]))