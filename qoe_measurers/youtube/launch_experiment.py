import time
import os
from subprocess import call

CHROME_ID="mdaahbifddgcfhaibfkfpeiombojjfhe"


def launch_experiment(qoe_params):
    """
    Launches the chrome extension and does the measures asked in qoe_params

    qoe_params : a dictionnary of wanted qoe params to run like video_res.
    """
    open_chrom_ext()
    return True

def open_chrom_ext():
    url_args="#?videoID="+"oFkulzWMotY"+"&resolution="+"hd720"
    call(["/opt/google/chrome/chrome",\
            "chrome-extension://"+CHROME_ID+"/headers.html",url_args])
