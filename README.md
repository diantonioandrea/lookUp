![GitHub last commit](https://img.shields.io/github/last-commit/diantonioandrea/lookUp)

# lookUp

`grep STRING FILE` reimagined.  

**lookUp** is an intuitive, cross-platform command line utility written in Python which allows you to *quickly and easily print the contents of files and webpages*, search through them using a *string or regex search*, and *highlight the search results* for easy identification.  

Make sure to take a look at the [contributing guidelines](https://github.com/diantonioandrea/lookUp/blob/main/.github/CONTRIBUTING.md) and at the [examples](#examples).

## Usage

By:

	lookUp

you'll get everything you need to know to use **lookUp**:

```
 rolling  lookUp 
cat FILE | grep STRING reimagined.
Developed by Andrea Di Antonio, more on https://github.com/diantonioandrea/lookUp

Usage: lookUp OPTIONS

        --all          Display full output.
        --install      Installs lookUp.
        --noCase       Disables case sensitivity.
        --uninstall    Uninstalls lookUp.

        -s FILE        Uses the specified file as a source.
        -w LINK        Uses the specified web page as a source.
        -r STR         The pattern for a regular expression search.
        -s STR         The string that gets searched throughout the source.
```

This will also check for updates.

## Installation

### Prerequisites

There are some Python modules that need to be installed in order to compile and use **lookUp**.

1. Compilation
	* pyinstaller: compilation of **lookUp**.
2. Usage
	* regex: Regular expressions.
	* bs4: HTML parsing.
	* [CLIbrary](https://github.com/diantonioandrea/CLIbrary): outputs.

As a one-liner:

	python3 -m pip install --upgrade pyinstaller regex bs4 CLIbrary

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

## Examples

Here follows some examples for **lookUp**.  

### Printing the content of [lookUp/Makefile](https://github.com/diantonioandrea/lookUp/blob/main/Makefile)

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

### Searching for the word "lookUp" word in [lookUp's security policy](https://github.com/diantonioandrea/lookUp/security/policy)

	[diantonioandrea@GitHub/lookUp]: python src/main.py -w https://github.com/diantonioandrea/lookUp/security/policy -s lookUp
	SEARCH: found 4 istance(s) of "lookUp" inside "https://github.com/diantonioandrea/lookUp/security/policy". | RED
	----------------------------------------------------------------------------------------------------------
	Security Policy · diantonioandrea/lookUp · GitHub
	lookUp
	Security: diantonioandrea/lookUp
	Keeping lookUp up to date is the best way to protect yourself against security vulnerabilities, so please make sure you're keeping it up to date.

### Simple regex example in [lookUp/.gihub/CODE_OF_CONDUCT.md](https://github.com/diantonioandrea/lookUp/blob/main/.github/CODE_OF_CONDUCT.md)

	[diantonioandrea@GitHub/lookUp]: lookUp .github/CODE_OF_CONDUCT.md -r "m..l"  
	REGEXP: found 11 match(es) of "m..l" inside ".github/CODE_OF_CONDUCT.md": mptl, mful, mail. | CYAN
	-------------------------------------------------------------------------------------------
	34: * Publishing others' private information, such as a physical or email
	44: or harmful.
	55: Examples of representing our community include using an official e-mail address,
	63: mail@diantonioandrea.com.
	64: All complaints will be reviewed and investigated promptly and fairly.
