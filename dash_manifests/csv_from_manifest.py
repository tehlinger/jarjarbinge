import re

ids = [
    "bUhdSs0VK9c",
    "im_2tkN4VKY",
    "O3zza3ofZ0Q",
    "oFkulzWMotY",
    "RSzD92Rl8j4",
    "tSjhLFWj9TU"
    ]


#249          webm       audio only DASH audio   52k , opus @ 50k, 355.54KiB
#242          webm       426x240    240p  292k , vp9, 24fps, video only, 1.67MiB

def generate_csv(video_id):
    with open(video_id+".manifest","r") as f,open(video_id+'.csv',"w") as out:
        out.write("id,web_format,resolution,bitrate,codec,fps\n")
        lines = f.readlines()
        for l in lines:
            if is_format_line(l):
                s = one_space_only(l)
                if 'audio' in s:
                    l = get_fields_from_audio(s)
                else:
                    if len(l.split(',')) > 3:
                        l = get_fields_from_video(s)
                    else:
                        continue
                out.write(','.join(l)+"\n")


def get_fields_from_audio(line):
    description = line.split(',')[0]
    description = description.replace(" audio only DASH audio"," audio ")
    description = one_space_only(description)
    desc_list = description.split(" ")
    codec_name = line.split(',')[1]
    desc_list.append(codec_name.replace(" ",""))
    desc_list.append('')
    return desc_list

def get_fields_from_video(line):
    description = line.split(',')[0]
    fields_list = description.split(' ')[:3]
    fields_list.append(description.split(' ')[4])
    if "webm container" in line:
        line = line.replace("webm container,","")
    fields_list.append(line.split(',')[1].replace(" ",""))
    fields_list.append(line.split(',')[2].replace(" ",""))
    return fields_list


def is_format_line(l):
    return l[:2].isdigit() and ',' in l

def one_space_only(l):
    return ' '.join(l.split())

ids = [
    "bUhdSs0VK9c",
    "im_2tkN4VKY",
    "O3zza3ofZ0Q",
    "oFkulzWMotY",
    "RSzD92Rl8j4",
    "tSjhLFWj9TU",
    "6tz1_znrbmc",
    "DcBU57z7CpY",
    "aVtO8uQrPXc"
    ]

for i in ids:
    generate_csv(i)
