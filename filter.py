import pandas as pd
import matplotlib.pyplot as plt
from app import db
from app import files
from flask import Flask


downloaded_file=db.fs.files.find_one({})
outputdata=files.get(downloaded_file['_id']).read()
# file_path="static/files/"
data=pd.DataFrame(list(outputdata))
print(data.head())