import gdown
import os
from zipfile import ZipFile



id = "1J3WUW2RGTZLXJKrcJQhm0rKdXbsCE1c1"
output = 'simulator.zip'
gdown.download(id=id, output=output, quiet=False)
with ZipFile(str(output), 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall()
path=os.path.dirname(os.path.abspath(__file__))
exec(open(str(path)+"\\test\\code\\gui_control-main\\demo.py").read())
