import os
from collections import OrderedDict
from json import JSONDecoder
from Probe_Information.Frame import Frame
from Probe_Information.Tag import Tag
from Probe_Information.Burst import Burst
from Filters import Filters


def make_unique(key, dct):
    counter = 0
    unique_key = key

    while unique_key in dct:
        counter += 1
        unique_key = '{}_{}'.format(key, counter)
    return unique_key


def parse_object_pairs(pairs):
    dct = OrderedDict()
    for key, value in pairs:
        if key in dct:
            key = make_unique(key, dct)
        dct[key] = value
    return dct


def calculate_time_in_seconds(time):
    total_time = time.split(":")
    hours = int(total_time[0])
    minutes = int(total_time[1])
    seconds = float(total_time[2])

    minutes += hours * 60
    seconds += minutes * 60

    return round(seconds, 6)


class Main:
    source_file = './Captures/All_the_Phones_Realistic.json'

    with open(source_file) as f:
        data = f.read()

    decoder = JSONDecoder(object_pairs_hook=parse_object_pairs)
    obj = decoder.decode(data)

    frame_list = []

    for packets in obj:
        resolved_mac = packets["_source"]["layers"]["wlan"]["wlan.sa_resolved"]
        mac = packets["_source"]["layers"]["wlan"]["wlan.sa"]
        seq = int(packets["_source"]["layers"]["wlan"]["wlan.seq"])
        time = packets["_source"]["layers"]["frame"]["frame.time"].split()

        if "wlan.mgt" in packets["_source"]["layers"]:
            tag_list = []
            for tags in packets["_source"]["layers"]["wlan.mgt"]["wlan.tagged.all"].values():
                tag_parameters = []
                for parameter_name, parameter_value in tags.items():
                    if parameter_name == "wlan.tag.number":
                        tag_number = parameter_value
                    elif parameter_name == "wlan.tag.length":
                        tag_legth = parameter_value
                    else:
                        tag_parameters.append(parameter_value)
                tag_list.append(Tag(tag_number, tag_legth, tag_parameters))

            frame_list.append(Frame(resolved_mac, mac, seq, calculate_time_in_seconds(time[3]), tag_list))

    #Sort Frames by MAC resulting in a dict-> { mac : [frame, frame, etc] }
    mac_sorted_frame_dict = {}
    for frame in frame_list:
        if frame.resolved_mac in mac_sorted_frame_dict.keys():
            mac_sorted_frame_dict[frame.resolved_mac].append(frame)
        else:
            mac_sorted_frame_dict[frame.resolved_mac] = [frame]

    burst_list = []
    #Create Burst Object based on Frame Times
    for mac_sorted_frame_list in mac_sorted_frame_dict.values():
        burst_frame_list = []
        frame_time_buffer = mac_sorted_frame_list[0].time
        for mac_sorted_frame in mac_sorted_frame_list:
            #New Burst
            if mac_sorted_frame.time - frame_time_buffer > 1:
                burst_list.append(Burst(mac_sorted_frame.resolved_mac, burst_frame_list))
                del burst_frame_list
                burst_frame_list = [mac_sorted_frame]
                frame_time_buffer = mac_sorted_frame.time
            #Same Burst
            else:
                burst_frame_list.append(mac_sorted_frame)
                frame_time_buffer = mac_sorted_frame.time

        burst_list.append(Burst(mac_sorted_frame_list[0].resolved_mac, burst_frame_list))

    burst_list_buffer = []
    time_buffer = burst_list[0].min_time
    for burst in burst_list:
        if time_buffer + 1200 >= burst.min_time >= time_buffer:
            burst_list_buffer.append(burst)

    unfiltered_burst_dict = {"Burst": burst_list_buffer}

    #Apply the Filters
    filters = Filters()
    filters.filter(unfiltered_burst_dict)
