class Tag:

    def __init__(self, tag_number, tag_length, tag_parameters):
        self.tag_number = tag_number
        self.tag_length = tag_length
        self.tag_parameters = tag_parameters
        self.tag_description = self.get_tag_description()

    def get_tag_description(self):
        tag_description_dict = {
            0: "SSID",
            1: "Supported Rates",
            3: "DS Capabilities",
            45: "HT Capabilities",
            50: "Extended Supported Rates",
            107: "Interworking",
            127: "Extended Capabilities",
            152: "DMG BSS Parameter Change",
            191: "VHT Capabilites",
            221: "Vendor Specifics",
            255: "HE Capabilities",
        }

        if self.tag_number in tag_description_dict:
            return tag_description_dict[int(self.tag_number)]