from  pymongo import MongoClient
import pprint
import json
import datetime

def save_results(results,exp_name,ip='localhost'):
    clean_results(results)
    results["date"] = datetime.datetime.now().strftime("%d/%m-%H:%M")
    c = get_collection(exp_name,ip)
    c.insert_one(results)

def clean_results(results):
    delete_keys([
        'QoE','availableQualityLevels','bitrate_switch',
        'clen_audio','clen_video','httpInfo','resolution','stallingNumber',
        'ts_firstBuffering','ts_onPlayerReadyEvent','ts_onYTIframeAPIReady',
        'ts_startPlaying','ts_start_js','timeout'],results)
    format_entries(results)

def format_entries(results):
    for k,v in results.items():
        if must_become_float(k):
            try:
                results[k] = float(v[0])
            except :
                results[k] = None
        else:
            if k == "true_resolutions" or k == 'stallingInfo':
                to_convert = results[k]
                if k == "true_resolutions":
                    results[k] = [i for i in
                     json.loads("["+str(to_convert[0])+"]")\
                     if '0x0' not in i['true_res']]
                else:
                    results[k] = [i for i in
                     json.loads("["+str(to_convert[0])+"]")]
        if k == "video_id":
            results[k] = v[0]

def must_become_float(k):
    return k != "video_id" and k != "true_resolutions" \
            and "MOS" not in k and k != "stallingInfo"

def delete_keys(k_list,dic):
    for k in k_list:
        check_and_del(k,dic)

def check_and_del(key,dic):
    if key in dic.keys():
        del(dic[key])

def get_collection(collec,ip,db="jarjarbinge"):
	client = MongoClient(ip, 27017)
	db = client[db]
	return db[collec]
