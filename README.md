
project-folder/
│
├── templates/
│   └── index.html         # Frontend interface
├── app.py                 # Flask backend
└── requirements.txt       # List of dependencies

#Running the Project#

terminal
	pip install flask
	python app.py

Visit: http://localhost:5000

As an executable:
Install PyInstaller: pip install pyinstaller

Run: pyinstaller --onefile app.py

Open the dist/app.exe file
