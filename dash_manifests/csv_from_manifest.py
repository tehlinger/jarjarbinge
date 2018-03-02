import re

ids = ["AntcyqJ6brc","oFkulzWMotY","x02xX2dv6bQ"]
#Transformers
#ID = "AntcyqJ6brc"
#Power rangers
#ID = "oFkulzWMotY"
#Black panther
ID = "x02xX2dv6bQ"


#249          webm       audio only DASH audio   52k , opus @ 50k, 355.54KiB
#242          webm       426x240    240p  292k , vp9, 24fps, video only, 1.67MiB

def generate_csv(video_id=ID):
    with open(video_id+".manifest","r") as f,open(video_id+'.csv',"w") as out:
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
    fields_list.append(line.split(',')[1].replace(" ",""))
    fields_list.append(line.split(',')[2].replace(" ",""))
    return fields_list


def is_format_line(l):
    return l[:2].isdigit() and ',' in l

def one_space_only(l):
    return ' '.join(l.split())

generate_csv()
