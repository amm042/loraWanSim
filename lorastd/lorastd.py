
class lora:
    BW_NA = 0
    BW_125 = 125
    BW_500 = 500

    SF_NA= 0
    SF_7 = 7
    SF_8 = 8
    SF_9 = 9

    SF_10 = 10
    SF_11 = 11
    SF_12 = 12

    CR_NA = 0
    CR_5 = 5
    CR_6 = 6
    CR_7 = 7
    CR_8 = 8


class channel():
    def __init__(self, freq_khz, bw, dr, cr):
        self.freq_khz = freq_khz
        self.bw = bw
        self.dr = dr
        self.cr = cr
