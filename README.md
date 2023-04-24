# lookUp

`cat FILE | grep STRING` reimagined.  
Make sure to take a look at the [contributing guidelines](https://github.com/diantonioandrea/lookUp/blob/main/.github/CONTRIBUTING.md).

## Usage

By:

	lookUp

you'll get everything you need to know to use **lookUp**:

	 rolling  lookUp 
	cat FILE | grep STRING reimagined.
	Developed by Andrea Di Antonio, more on https://github.com/diantonioandrea/lookUp

	Usage: lookUp file [--all  --install  --noCase  --uninstall  -r STR  -s STR]

			--all          Display full output.
			--install      Installs lookUp.
			--noCase       Disables case sensitivity.
			--uninstall    Uninstalls lookUp.

			-r STR         The pattern for a regular expression search.
			-s STR         The string that gets searched throughout the file.

This will also check for updates.

### Examples.

Here follows some examples for **lookUp**.  

Printing the content of [lookUp/Makefile](https://github.com/diantonioandrea/lookUp/blob/main/Makefile).

```
[diantonioandrea@GitHub/lookUp]: lookUp Makefile 
unix: # Linux and macOS
        pyinstaller --onefile --console src/main.py
        mv dist/main lookUp

windows: # Windows
        pyinstaller --onefile --console .\src\main.py
        move .\dist\main.exe .\lookUp.exe

clean: # Linux and macOS only
        rm -rf dist build data src/__pycache__ .vscode
        rm -rf *.spec lookUp
```

Searching for the word "Copyright" in [lookUp/LICENSE](https://github.com/diantonioandrea/lookUp/blob/main/LICENSE).
```
idk[diantonioandrea@GitHub/lookUp]: lookUp LICENSE -s Copyright
SEARCH: found 4 istance(s) of "Copyright" inside "LICENSE". | RED
-----------------------------------------------------------
4:  Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
77:   "Copyright" also means copyright-like laws that apply to other kinds of
635:     Copyright (C) <year>  <name of author>
655:     <program>  Copyright (C) <year>  <name of author>
```

Simple regex example in [lookUp/.gihub/CODE_OF_CONDUCT.md](https://github.com/diantonioandrea/lookUp/blob/main/.github/CODE_OF_CONDUCT.md)
```
[diantonioandrea@GitHub/lookUp]: lookUp .github/CODE_OF_CONDUCT.md -r "m..l"  
REGEXP: found 11 match(es) of "m..l" inside ".github/CODE_OF_CONDUCT.md": mptl, mful, mail. | CYAN
-------------------------------------------------------------------------------------------
34: * Publishing others' private information, such as a physical or email
44: or harmful.
55: Examples of representing our community include using an official e-mail address,
63: mail@diantonioandrea.com.
64: All complaints will be reviewed and investigated promptly and fairly.
```

## Installation

### Prerequisites

There are some Python modules that need to be installed in order to compile and use **lookUp**.

1. Compilation
	* pyinstaller: compilation of **lookUp**.
2. Usage
	* regex: Regular expressions.
	* [CLIbrary](https://github.com/diantonioandrea/CLIbrary): outputs.

As a one-liner:

	python3 -m pip install --upgrade pyinstaller regex CLIbrary

### Compiling and installing from source

**lookUp** can be compiled[^1] by:

	make PLATFORM

where PLATFORM must be replaced by:

* windows
* unix (Linux and macOS)

based on the platform on which **lookUp** will be compiled.  
**lookUp** can be then installed[^2] by:

	./lookUp --install

or

	.\lookUp.exe --install

on Windows.

[^1]: The Makefile for the Windows version is written for [NMAKE](https://learn.microsoft.com/en-gb/cpp/build/reference/nmake-reference?view=msvc-170).
[^2]: This is the only way to install **lookUp**.