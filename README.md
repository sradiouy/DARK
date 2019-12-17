# DARK
*Deep annotation of representatives kinetoplastid proteins*


### 1. Clone or download this repo

```
git clone https://github.com/sradiouy/DARK
```

### 2. Enter to the project directory

```
cd DARK
```

### 3. Create and activate a python (3.6 or higher) virtual environment  


#### 3.1 On Linux

```
apt-get install python3-venv   --- (only if needed)

python -m venv vdark

source vdark/bin/activate
````

#### 3.2 On Mac

```
pip3 install virtualenv   --- (only if needed)

python3 -m venv vdark

source vidminer/bin/activate

If you have ntlk certificate problem please go to Macintosh HD > Applications > Python3.x folder 
(or whatever version of pyth
````

#### 3.3 On Windows 
 
 If it is your first time with python app, we recommend the following: 
  
  1. installation of visual studio code (https://code.visualstudio.com/docs/python/python-tutorial)
  1. Go to https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017 and download "Build Tools For Visual Studio" under "Tools for " Visual Studio"

Once python and visual sutdio are installed:

```
python -m venv vdark

vdark/Scripts/activate 
````
If the previous line has an error please run:

```
vdark/Scripts/activate.bat 

```

### 4. Install project requirements

```
pip install wheel
pip install -r requirements.txt
```

### 5. Run the application

```
python dark.py
```

### 6. Point to localhost in any web browser

````
http://127.0.0.1:8050/
````


**We hope that DARK will be useful for your research!** :v::v::v::v:
