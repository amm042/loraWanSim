"""
A default class A lora device which periodically sends packets.
"""
class loraapp_default:
    def __init__(self):
        pass
    def tx_event(self):
        "when the simulator wants the node to TX."
        pass
    def rx_event(self, packet):
        "the node recieved a packet."
        pass

        
