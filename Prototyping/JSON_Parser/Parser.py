from collections import OrderedDict
from json import JSONDecoder
from xlwt import Workbook


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


def combine_cells(name, value):
    combined_value = '{}_{}'.format(name, value)
    return combined_value


class Parser:
    source_file = './Captures/A51_10_Ruhemodus_MobileNetworkOn_Langzeitmessung_1_json.json'

    with open(source_file) as f:
        data = f.read()

    decoder = JSONDecoder(object_pairs_hook=parse_object_pairs)
    obj = decoder.decode(data)
    wb = Workbook()
    sheet1 = wb.add_sheet("Sheet1")

    #Add Titles
    sheet1.write(10, 1, "Frame Time")
    sheet1.write(10, 2, "Frame Number")
    sheet1.write(10, 3, "Frame Length")
    sheet1.write(10, 4, "Destination Resolved")
    sheet1.write(10, 5, "Source Resolved")
    sheet1.write(10, 6, "Sequence Number")
    sheet1.write(10, 7, "BSSID")
    sheet1.write(9, 8, "Tags")
    sheet1.write(10, 8, "SSID")
    sheet1.write(10, 9, "Support Rates")
    sheet1.write(10, 13, "Extended Support Rates")
    sheet1.write(10, 21, "Capabilities")
    sheet1.write(10, 36, "Extended Capabilities")

    counter = 11
    tag_offset = 8

    #Add Entries
    for packets in obj:
        sheet1.write(counter, 1, packets["_source"]["layers"]["frame"]["frame.time"])
        sheet1.write(counter, 2, int(packets["_source"]["layers"]["frame"]["frame.number"]))
        sheet1.write(counter, 3, int(packets["_source"]["layers"]["frame"]["frame.len"]))

        if "wlan.ra_resolved" in packets["_source"]["layers"]["wlan"]:
            sheet1.write(counter, 4, packets["_source"]["layers"]["wlan"]["wlan.ra_resolved"])

        if "wlan.sa_resolved" in packets["_source"]["layers"]["wlan"]:
            sheet1.write(counter, 5, packets["_source"]["layers"]["wlan"]["wlan.sa_resolved"])

        if "wlan.seq" in packets["_source"]["layers"]["wlan"]:
            sheet1.write(counter, 6, int(packets["_source"]["layers"]["wlan"]["wlan.seq"]))

        if "wlan.bssid" in packets["_source"]["layers"]["wlan"]:
            sheet1.write(counter, 7, packets["_source"]["layers"]["wlan"]["wlan.bssid"])

        # Tags
        if "wlan_1" in packets["_source"]["layers"]:
            if "wlan.tagged.all" in packets["_source"]["layers"]["wlan.mgt"]:
                for tags in packets["_source"]["layers"]["wlan_1"]["wlan.tagged.all"].values():
                    #SSID
                    if "wlan.ssid" in tags:
                        sheet1.write(counter, tag_offset, tags["wlan.ssid"])
                        tag_offset += 1

                    #Supported Rates
                    if "wlan.supported_rates" in tags:
                        value = int(tags["wlan.supported_rates"]) / 2
                        sheet1.write(counter, tag_offset, value)
                        tag_offset += 1

                    for i in range(10):
                        if combine_cells("wlan.supported_rates", i+1) in tags:
                            value = int(tags[combine_cells("wlan.supported_rates", i+1)]) /2
                            sheet1.write(counter, tag_offset, value)
                            tag_offset += 1

                    #Extended Supported Rates
                    if "wlan.extended_supported_rates" in tags:
                        value = int(tags["wlan.extended_supported_rates"]) /2
                        sheet1.write(counter, tag_offset, value)
                        tag_offset += 1

                    for i in range(10):
                        if combine_cells("wlan.extended_supported_rates", i+1) in tags:
                            value = int(tags[combine_cells("wlan.extended_supported_rates", i+1)]) /2
                            sheet1.write(counter, tag_offset, value)
                            tag_offset += 1

                    #Capabilities
                    if "wlan.ht.capabilities" in tags:
                        sheet1.write(counter, tag_offset, tags["wlan.ht.capabilities"])
                        tag_offset += 1

                    if "wlan.ht.capabilities_tree" in tags:
                        for capabilities in tags["wlan.ht.capabilities_tree"].values():
                            sheet1.write(counter, tag_offset, capabilities)
                            tag_offset += 1

                    #Extended Capabilities
                    if "wlan.extcap" in tags:
                        sheet1.write(counter, tag_offset, tags["wlan.extcap"])
                        tag_offset += 1

                    if "wlan.extcap_tree" in tags:
                        for extcap in tags["wlan.extcap_tree"].values():
                            sheet1.write(counter, tag_offset, extcap)
                            tag_offset += 1

        #Alternative Tags
        if "wlan.mgt" in packets["_source"]["layers"]:
            if "wlan.tagged.all" in packets["_source"]["layers"]["wlan.mgt"]:
                for tags in packets["_source"]["layers"]["wlan.mgt"]["wlan.tagged.all"].values():
                    #SSID
                    if "wlan.ssid" in tags:
                        sheet1.write(counter, tag_offset, tags["wlan.ssid"])
                        tag_offset += 1

                    #Supported Rates
                    if "wlan.supported_rates" in tags:
                        value = int(tags["wlan.supported_rates"]) / 2
                        sheet1.write(counter, tag_offset, value)
                        tag_offset += 1

                    for i in range(10):
                        if combine_cells("wlan.supported_rates", i+1) in tags:
                            value = int(tags[combine_cells("wlan.supported_rates", i+1)]) /2
                            sheet1.write(counter, tag_offset, value)
                            tag_offset += 1

                    #Extended Supported Rates
                    if "wlan.extended_supported_rates" in tags:
                        value = int(tags["wlan.extended_supported_rates"]) /2
                        sheet1.write(counter, tag_offset, value)
                        tag_offset += 1

                    for i in range(10):
                        if combine_cells("wlan.extended_supported_rates", i+1) in tags:
                            value = int(tags[combine_cells("wlan.extended_supported_rates", i+1)]) /2
                            sheet1.write(counter, tag_offset, value)
                            tag_offset += 1

                    #Capabilities
                    if "wlan.ht.capabilities" in tags:
                        sheet1.write(counter, tag_offset, tags["wlan.ht.capabilities"])
                        tag_offset += 1

                    if "wlan.ht.capabilities_tree" in tags:
                        for capabilities in tags["wlan.ht.capabilities_tree"].values():
                            sheet1.write(counter, tag_offset, capabilities)
                            tag_offset += 1

                    #Extended Capabilities
                    if "wlan.extcap" in tags:
                        sheet1.write(counter, tag_offset, tags["wlan.extcap"])
                        tag_offset += 1

                    if "wlan.extcap_tree" in tags:
                        for extcap in tags["wlan.extcap_tree"].values():
                            sheet1.write(counter, tag_offset, extcap)
                            tag_offset += 1

        tag_offset = 8
        counter += 1

    wb.save('A51_10_Ruhemodus_MobileNetworkOn_Langzeitmessung_1.xls')
