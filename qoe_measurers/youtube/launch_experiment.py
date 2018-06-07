import time
import os
from subprocess import call
import random

#CHROME_ID="ophdohnncbmfeikcgcjopnploippgbjk"
CHROME_ID="mdaahbifddgcfhaibfkfpeiombojjfhe"

IDS = ["dW1BIid8Osg","AntcyqJ6brc","oFkulzWMotY","iVAgTiBrrDA"]


def launch_experiment(qoe_params,go_clear=False):
    """
    Launches the chrome extension and does the measures asked in qoe_params

    qoe_params : a dictionnary of wanted qoe params to run like video_res.
    """
    open_chrom_ext(go_clear)
    return True

def open_chrom_ext(go_clear):
    if go_clear is not True:
        chosen_id = random.choice(IDS)
        url_args="#?videoID="+chosen_id+"&resolution="+"hd720"
    else:
        chosen_id = "RK1K2bCg4J8"
        url_args="#?videoID="+chosen_id+"&resolution="+"hd720"
    call(["/opt/google/chrome/chrome",\
            #"--disable-web-security","--user-data-dir","-–allow-file-access-from-files",\
            #"--new-window",
            "--incognito",
            #"--user-data-dir=~/fake_chrome_cache",
            "chrome-extension://"+CHROME_ID+"/headers.html",url_args,\
            ])
