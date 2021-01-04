import os
from collections import OrderedDict
from json import JSONDecoder
from xlwt import Workbook

from Frame import Frame


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


def calculate_ibat(frame_time_one, frame_time_two):
    time_one = frame_time_one.split(":")
    time_two = frame_time_two.split(":")

    ibat_hours = int(time_two[0]) - int(time_one[0])
    ibat_minutes = int(time_two[1]) - int(time_one[1])
    ibat_seconds = float(time_two[2]) - float(time_one[2])

    ibat_minutes += int(ibat_hours) * 60
    ibat_seconds += int(ibat_minutes) * 60

    return round(ibat_seconds, 6)


class Parser:
    wb = Workbook()

    #Int Counter FOr Sheet Names
    int_sheet_counter = 0

    path = './Captures/'
    #Loop through all Files in Captures Folder
    for filename in os.listdir(path):

        start_path = "./Captures/"
        source_file = start_path + filename

        with open(source_file) as f:
            data = f.read()

        decoder = JSONDecoder(object_pairs_hook=parse_object_pairs)
        obj = decoder.decode(data)

        sheet_counter = str(int_sheet_counter)
        worksheet_name = "Sheet" + sheet_counter
        sheet1 = wb.add_sheet(worksheet_name)

        #Add some Titles
        sheet1.write(0, 0, filename)
        sheet1.write(9, 1, "MAC")
        sheet1.write(9, 2, "Time")
        sheet1.write(9, 3, "Sequence Number")
        sheet1.write(9, 4, "Frame Length")
        sheet1.write(9, 5, "Nof Frames")
        sheet1.write(9, 6, "Missed Frames")
        sheet1.write(9, 7, "Inter Burst Arrival Time")
        sheet1.write(9, 8, "0 SSID Tag")
        sheet1.write(9, 9, "1 Supported Rates")
        sheet1.write(9, 10, "50 Extended Supported Rates")
        sheet1.write(9, 11, "3 DS Parameters")
        sheet1.write(9, 12, "45 HT Capabilities")
        sheet1.write(9, 13, "127 Extended Capabilities")
        sheet1.write(9, 14, "107 Interworking Tag")
        sheet1.write(9, 15, "221 Vendor Specifics")

        frame_dict = {}
        frame_count = 0

        for packets in obj:
            mac = packets["_source"]["layers"]["wlan"]["wlan.sa_resolved"]
            seq = int(packets["_source"]["layers"]["wlan"]["wlan.seq"])
            time = packets["_source"]["layers"]["frame"]["frame.time"].split()
            frame_length = packets["_source"]["layers"]["frame"]["frame.len"]
            frame_count += 1

            vspec_oui = []
            wlan_tags = []
            if "wlan.mgt" in packets["_source"]["layers"]:
                if "wlan.tagged.all" in packets["_source"]["layers"]["wlan.mgt"]:
                    for tags in packets["_source"]["layers"]["wlan.mgt"]["wlan.tagged.all"].values():
                        wlan_tags.append(tags["wlan.tag.number"])
                        if tags["wlan.tag.number"] == "221":
                            vspec_oui.append(tags["wlan.tag.oui"])

            #If Frame already exists add the parameters
            if mac in frame_dict:
                x = frame_dict[mac]
                x.sequence_number.append(seq)
                x.time.append(time[3])
                x.frame_length.append(frame_length)
                x.tags.append(wlan_tags)
                x.oui = vspec_oui
            else:
                #Create a new Frame
                frame_dict[mac] = Frame(mac, seq, time[3], frame_length, wlan_tags, vspec_oui)

        row_offset = 10
        time_buffer = 0
        burst_size_list = []
        total_missed_frames = 0

        for x in frame_dict.values():
            sheet1.write(row_offset, 1, x.mac)

            time_offset = row_offset
            for t in x.time:
                sheet1.write(time_offset, 2, t)
                time_offset += 1

            seq_offset = row_offset
            for s in x.sequence_number:
                sheet1.write(seq_offset, 3, s)
                seq_offset += 1

            len_offset = row_offset
            for l in x.frame_length:
                sheet1.write(len_offset, 4, l)
                len_offset += 1

            length = len(x.time)
            burst_size_list.append(length)
            sheet1.write(row_offset, 5, length)

            off = max(x.sequence_number) - min(x.sequence_number) - len(x.sequence_number) + 1
            total_missed_frames += off
            sheet1.write(row_offset, 6, off)

            if time_buffer != 0:
                ibat = calculate_ibat(time_buffer, x.time[0])
                sheet1.write(row_offset - 1, 7, ibat)

            tag_offset = row_offset
            for tag_numbers in x.tags:
                if "0" in tag_numbers:
                    sheet1.write(tag_offset, 8, "Yes")
                else:
                    sheet1.write(tag_offset, 8, "No")
                if "1" in tag_numbers:
                    sheet1.write(tag_offset, 9, "Yes")
                else:
                    sheet1.write(tag_offset, 9, "No")
                if "50" in tag_numbers:
                    sheet1.write(tag_offset, 10, "Yes")
                else:
                    sheet1.write(tag_offset, 10, "No")
                if "3" in tag_numbers:
                    sheet1.write(tag_offset, 11, "Yes")
                else:
                    sheet1.write(tag_offset, 11, "No")
                if "45" in tag_numbers:
                    sheet1.write(tag_offset, 12, "Yes")
                else:
                    sheet1.write(tag_offset, 12, "No")
                if "127" in tag_numbers:
                    sheet1.write(tag_offset, 13, "Yes")
                else:
                    sheet1.write(tag_offset, 13, "No")
                if "107" in tag_numbers:
                    sheet1.write(tag_offset, 14, "Yes")
                else:
                    sheet1.write(tag_offset, 14, "No")
                if "221" in tag_numbers:
                    column_offset = 15
                    for ouis in x.oui:
                        sheet1.write(tag_offset, column_offset, ouis)
                        column_offset += 1
                else:
                    sheet1.write(tag_offset, 15, "No Vendor Specific Tags")
                tag_offset += 1

            time_buffer = x.time[-1]
            row_offset = time_offset
            row_offset += 1

        sheet1.write(1, 1, "Total Nof Frames")
        sheet1.write(2, 1, frame_count)

        sheet1.write(1, 2, "Total Nof Bursts")
        sheet1.write(2, 2, len(frame_dict))

        sheet1.write(1, 3, "Avg Burst Size")
        sheet1.write(2, 3, sum(burst_size_list) / len(burst_size_list))

        sheet1.write(1, 4, "Min Burst Size")
        sheet1.write(2, 4, min(burst_size_list))

        sheet1.write(1, 5, "Max Burst Size")
        sheet1.write(2, 5, max(burst_size_list))

        sheet1.write(1, 6, "Total Missed Frames")
        sheet1.write(2, 6, total_missed_frames)

        int_sheet_counter += 1

    wb.save('Test.xls')
