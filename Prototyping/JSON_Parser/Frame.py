class Frame:

    def __init__(self, mac, sequence_number, time, len, tags, oui):
        self.mac = mac
        self.sequence_number = []
        self.sequence_number.append(sequence_number)
        self.time = []
        self.time.append(time)
        self.frame_length = []
        self.frame_length.append(len)
        self.tags = []
        self.tags.append(tags)
        self.oui = []
        self.oui = oui

    def get_mac_adress(self):
        return self.mac