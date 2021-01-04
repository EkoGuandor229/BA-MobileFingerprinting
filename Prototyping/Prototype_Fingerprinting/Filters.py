class Filters:

    @staticmethod
    def print_bust_dict_information(burst_dict):
        print("MAC | nof Bursts | Tag Numbers")
        for burst_list in burst_dict.values():
            mac = []
            burst_list_length = len(burst_list)
            for burst in burst_list:
                if burst.mac not in mac:
                    mac.append(burst.mac)
                for frame in burst.frames:
                    tag_numbers = []
                    for tag in frame.tags:
                        if tag not in tag_numbers:
                            tag_numbers.append(tag.tag_number)
            print(mac[0], "|", burst_list_length, "|", tag_numbers)
            tag_numbers.clear()
            mac.clear()
        print("Number of Devices:", len(burst_dict))

    @staticmethod
    def filter_by_ie_fields(burst_dict):
        buffer_burst_dict = {}
        ie_filtered_burst_dict = {}
        for burst_list in burst_dict.values():
            for burst in burst_list:
                for frame in burst.frames:
                    tag_numbers = []
                    for tag in frame.tags:
                        if tag not in tag_numbers:
                            tag_numbers.append(tag.tag_number)

                if len(tag_numbers) > 4:
                    if "'0', '1', '50'" in str(tag_numbers):
                        if str(tag_numbers) in buffer_burst_dict.keys():
                            buffer_burst_dict[str(tag_numbers)].append(burst)
                        else:
                            buffer_burst_dict[str(tag_numbers)] = [burst]

                tag_numbers.clear()

        for key, value in buffer_burst_dict.items():
            if len(value) > 1:
                ie_filtered_burst_dict[key] = value

        return ie_filtered_burst_dict

    @staticmethod
    def filter_devices_by_time(burst_dict):
        counter = 0
        for burst_list in burst_dict.values():
            if len(burst_list) >= 10:
                time_window = 15
                time_frame = burst_list[-1].max_time - burst_list[0].min_time
                time_iterations = int(time_frame / 5)
                device_counter = 0

                for i in range(1, 4):
                    for burst in burst_list:
                        if burst.min_time or burst.max_time in \
                                range(int(burst_list[0].min_time) + (i*time_iterations) - time_window,
                                      int(burst_list[0].min_time) + (i * time_iterations) + time_window):
                            device_counter += 1
                    device_counter /= 4

                counter += device_counter
        print(round(counter/10))
        return burst_dict

    @staticmethod
    def filter_devices_with_no_randomization(burst_dict):
        same_mac = {}
        for key, burst_list in burst_dict.items():
            check_mac = burst_list[0].mac
            check = True
            for burst in burst_list:
                if burst.mac != check_mac:
                    check = False
            if check:
                same_mac[key] = burst_list

        same_mac_keys = list(same_mac.keys())
        same_mac_values = list(same_mac.values())
        for i in range(len(same_mac)):
            for j in range(i + 1, len(same_mac)):
                if same_mac_values[i][0].mac == same_mac_values[j][0].mac:
                    burst_dict[same_mac_keys[i]] = same_mac_values[i] + same_mac_values[j]
                    del burst_dict[same_mac_keys[j]]

        return burst_dict

    def filter(self, unfiltered_burst_dict):
        ie_filtered_burst_dict = self.filter_by_ie_fields(unfiltered_burst_dict)
        self.print_bust_dict_information(ie_filtered_burst_dict)
        print("-----------------------------")
        ick = self.filter_devices_with_no_randomization(ie_filtered_burst_dict)
        self.print_bust_dict_information(ick)


