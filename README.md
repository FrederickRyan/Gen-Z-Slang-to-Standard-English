MODEL FILES (IMPORTANT)

Due to GitHub file size limitations, trained BART model files
are NOT stored in this repository.

Please download the model folders from Google Drive:

BART Proposed Model:
https://drive.google.com/drive/folders/15\_RbymihgCHQ8aDSaq0GnaQEAGPrHUMe?usp=sharing

BART Baseline Model:
https://drive.google.com/drive/folders/1hGP9vbsiiDdfTC8rWEtOFmUO6tZKvUXL?usp=sharing

After downloading, extract and place them in the project root:

project/

│── app.py

│── requirements.txt

│── bart\_proposed\_final/

│── bart\_baseline\_final/



IMPORTANT

1. install dependencies
   
   a. create env (make sure to cd-ed into the folder that has requirements.txt)
   
   python -m venv \[insert\_name]
   
   .\[insert\_name]\\Scripts\\activate
   
   pip install -r requirements.txt # wait and profit

   b. install the enviorments
   
   pip install -r requirements.txt

2. launch app
   
   streamlit run app.py
