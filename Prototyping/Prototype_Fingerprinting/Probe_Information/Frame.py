class Frame:

    def __init__(self, resolved_mac, mac,  sequence_number, time, tags):
        self.resolved_mac = resolved_mac
        self.mac = mac
        self.sequence_number = sequence_number
        self.time = time
        self.tags = tags
