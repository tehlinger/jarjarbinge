import pandas as pd

def prepare_json_for_mos(res_dic,video_ID="oFkulzWMotY"):
    return {}

class codecGetter:
    def __init__(self,video_ID):
        self.df = pd.read_csv("../dash_manifests/"+video_ID+".csv")

    def get(self,codec_id):
        """Returns the codec dic matching the codec_id"""
        entry = self.df.loc[self.df.id == int(codec_id)].iloc[0].to_dict()
        #If the codec is a video codec
        if 'audio' not in entry['resolution']:
            name = "h264" if "avc" in entry['codec'] else "vp9"
            res  = entry['resolution']
            bitrate = entry['bitrate']
            fps = int(entry['fps'][:-3])
            return {'codec':name, 'res':res,
                    'bitrate':bitrate,'fps':fps}
        #If the codec is an audio codec
        else:
            name = "heaac" if "opus" in entry['codec'] else "aaclc"
            return {"codec":name,"bitrate":entry['bitrate']}
