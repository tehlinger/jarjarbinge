from  pymongo import MongoClient
import pprint
import json
import datetime

def save_results(qoe_results,qos,exp_name,ip='localhost',must_format=True):
    if must_format:
        clean_results(qoe_results)
    d = datetime.datetime.now().strftime("%d/%m-%H:%M")
    results = {**qos,**qoe_results}
    results["date"] = d
    pprint.pprint(results)
    c = get_collection(exp_name,ip)
    i = c.insert_one(results).inserted_id
    print("["+d+"] "+"host:"+str(ip)+"-id:"+str(i))

def clean_results(results):
    delete_keys([
        'QoE','availableQualityLevels','bitrate_switch',
        'clen_audio','clen_video','httpInfo','resolution','stallingNumber',
        'ts_firstBuffering','ts_onPlayerReadyEvent','ts_onYTIframeAPIReady',
        'ts_startPlaying','ts_start_js','timeout'],results)
    format_entries(results)

def format_entries(results):
    for k,v in results.items():
        print("KEY : "+k)
        pprint.pprint(v)
        if must_become_float(k):
            try:
                results[k] = float(v[0])
            except :
                results[k] = None
        else:
            if k == "true_resolutions" or k == 'stallingInfo':
                to_convert = results[k]
                if k == "true_resolutions":
                    if len(to_convert) == 1:
                        results[k] = [json.loads(to_convert[0])]
                    else:
                        l =  [i for i in to_convert[0]]
                        d =  [json.loads(i) for i in l]
                        results[k] = [i for i in lst
                         if '0x0' not in i['true_res']]
                else:
                    if results[k] is not None:
                        if results [k][0] is not None:
                            if type(results[k][0]) == str:
                                results[k] = None
                            else:
                                results[k] = [i for i in json.loads(to_convert[0])]
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

def test():
    d={'bufferSizeWhenStart':0.0,'date':'09/03-09:30','dl_del_ms':1,'dl_jit_ms':None,'dl_los':0,'dl_rat_kb':None,'dur':59.426,'end_time':0.0,'getVideoLoadedFraction':0.0,'join_time':0.0,'player_load_time':310000.0,'totalStallDuration':0.0,'ul_del_ms':1,'ul_jit_ms':None,'ul_los':None,'ul_rat_kb':None}
    #d={'bufferSizeWhenStart':0.0,'date':'09/03-09:30','dl_del_ms':1,'dur':59.426,'player_load_time':310000.0,'totalStallDuration':0.0,'ul_del_ms':1,'ul_jit_ms':None}
    c = get_collection("test","acqua-db")
    print("Got collection")
    c.insert_one(d)
