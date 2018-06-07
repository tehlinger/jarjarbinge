from  pymongo import MongoClient
import pprint
import json
import datetime

def save_results(qoe_results,qos,exp_name,dataset,ip='localhost',must_format=True):
    """
    Dataset : identify the dataset to wich this point belongs
    """
    #pprint.pprint(qoe_results)
    if must_format:
        clean_results(qoe_results)
    d = datetime.datetime.now().strftime("%d/%m-%H:%M:%S")
    results = {**qos,**qoe_results}
    results["date"] = d
    results["dataset"] = dataset
    #pprint.pprint(results)
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
        if must_become_float(k):
            try:
                results[k] = float(v[0])
            except :
                results[k] = None
        else:
            if k == "true_resolutions" or k == 'stallingInfo'\
                    or k == 'est_rates':
                to_convert = str(results[k])
                #if k == 'est_rates':
                #    print("GOT IT : "+str(results[k]))
        if k == "video_id":
            results[k] = v[0]

def must_become_float(k):
    return k != "video_id" and k != "true_resolutions" \
            and "MOS" not in k and k != "stallingInfo"\
            and k != "est_rates"

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

def export_results(output,collec="rand_linear_3",ip="localhost",db="jarjarbinge"):
    c = get_collection(collec,ip,db=db)
    with open(output,"w") as f:
        for entry in c.find():
            f.write(str(entry)+"\n")

def test():
    d={'bufferSizeWhenStart':0.0,'date':'09/03-09:30','dl_del_ms':1,'dl_jit_ms':None,'dl_los':0,'dl_rat_kb':None,'dur':59.426,'end_time':0.0,'getVideoLoadedFraction':0.0,'join_time':0.0,'player_load_time':310000.0,'totalStallDuration':0.0,'ul_del_ms':1,'ul_jit_ms':None,'ul_los':None,'ul_rat_kb':None}
    #d={'bufferSizeWhenStart':0.0,'date':'09/03-09:30','dl_del_ms':1,'dur':59.426,'player_load_time':310000.0,'totalStallDuration':0.0,'ul_del_ms':1,'ul_jit_ms':None}
    c = get_collection("test","acqua-db")
    print("Got collection")
    c.insert_one(d)
