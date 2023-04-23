unix: # Linux and macOS
	pyinstaller --onefile --console src/main.py
	mv dist/main lookUp

windows: # Windows
	pyinstaller --onefile --console .\src\main.py
	move .\dist\main.exe .\lookUp.exe

clean: # Linux and macOS only
	rm -rf dist build data src/__pycache__ .vscode
	rm -rf *.spec lookUp