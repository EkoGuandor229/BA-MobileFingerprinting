class Burst:

    def __init__(self, mac, frames):
        self.mac = mac
        self.frames = []
        self.frames = frames
        self.min_time = self.time_of_first_frame_in_burst()
        self.max_time = self.time_of_last_frame_in_burst()
        self.local_bit = self.check_local_bit()

    def time_of_first_frame_in_burst(self):
        time = []
        for frame in self.frames:
            time.append(frame.time)
        return min(time)

    def time_of_last_frame_in_burst(self):
        time = []
        for frame in self.frames:
            time.append(frame.time)
        return max(time)

    def add_frame_to_burst(self, frame):
        self.frames.append(frame)
        self.min_time = self.time_of_first_frame_in_burst()
        self.max_time = self.time_of_last_frame_in_burst()

    def check_local_bit(self):
        mac = self.frames[0].mac.split(":")
        if mac[0][1] == 2 or 6 or 'a' or 'e':
            return True
        else:
            return False
