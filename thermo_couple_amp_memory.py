class Memory:
    registermap = {'configuration_0_register': 0,
                   'configuration_1_register': 1,
                   'fault_mask_register': 2,
                   'linearised_tc_temperature_2': 0xc,
                   'linearised_tc_temperature_1': 0xd,
                   'linearised_tc_temperature_0': 0xe,
                   'fault_status_register': 0xf}

    def getAddress(self, registername):
        return self.registermap[registername]
