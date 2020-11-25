"""
Stores the official US902-928MHz configuration parameters. 
"""

from .lorastd import lora, channel

#ref https://lora-alliance.org/sites/default/files/2018-05/lorawan-regional-parameters-v1.1ra.pdf
class us902():

    DR = [
        (lora.SF_10, lora.BW_125), #0
        (lora.SF_9, lora.BW_125),
        (lora.SF_8, lora.BW_125),
        (lora.SF_7, lora.BW_125),
        (lora.SF_8, lora.BW_500), #4

        (lora.SF_NA, lora.BW_NA), #5
        (lora.SF_NA, lora.BW_NA),
        (lora.SF_NA, lora.BW_NA), #7

        (lora.SF_12, lora.BW_500), #8
        (lora.SF_11, lora.BW_500),
        (lora.SF_10, lora.BW_500),
        (lora.SF_9, lora.BW_500),  #11
        (lora.SF_8, lora.BW_500),
        (lora.SF_7, lora.BW_500),

        (lora.SF_NA, lora.BW_NA), #14
        (lora.SF_NA, lora.BW_NA), #15
    ]

    def __init__(self):
        self.upstream = [channel(freq_khz=902300+200*i,
                                 bw=lora.BW_125,
                                 dr=[us902.DR[0:4]],
                                 cr=lora.CR_5) for i in range(64)]
        self.upstream += [channel(freq_khz=903000+1600*i,
                                  bw=lora.BW_500,
                                  dr=[us902.DR[4]],
                                  cr=lora.CR_NA) for i in range(8)]
        self.downstream = [channel(freq_khz=923300+600*i,
                                  bw=lora.BW_500,
                                  dr=[us902.DR[8:14]],
                                  cr=lora.CR_NA) for i in range(8)]
