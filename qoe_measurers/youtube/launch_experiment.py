import time
import os
from subprocess import call
import random

CHROME_ID="ophdohnncbmfeikcgcjopnploippgbjk"
#CHROME_ID="mdaahbifddgcfhaibfkfpeiombojjfhe"

IDS = ["dW1BIid8Osg","AntcyqJ6brc","oFkulzWMotY","iVAgTiBrrDA"]


def launch_experiment(qoe_params):
    """
    Launches the chrome extension and does the measures asked in qoe_params

    qoe_params : a dictionnary of wanted qoe params to run like video_res.
    """
    open_chrom_ext()
    return True

def open_chrom_ext():
    chosen_id = random.choice(IDS)
    url_args="#?videoID="+chosen_id+"&resolution="+"hd720"
    call(["/opt/google/chrome/chrome",\
            #"--disable-web-security","--user-data-dir","-–allow-file-access-from-files",\
            "chrome-extension://"+CHROME_ID+"/headers.html",url_args,\
            ])
