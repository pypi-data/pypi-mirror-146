class Util:
    def __init__(self, node):
        self.node = node

    def createmultisig(self, nrequired, keys, address_type=None):  # 01
        return self.node._rpc.call("createmultisig", nrequired, keys, address_type)

    def deriveaddresses(self, descriptor, range=None):  # 02
        return self.node._rpc.call("deriveaddresses", descriptor, range)

    def estimatesmartfee(self, conf_target, estimate_mode=None):  # 03
        return self.node._rpc.call("estimatesmartfee", conf_target, estimate_mode)

    def getdescriptorinfo(self, descriptor):  # 04
        return self.node._rpc.call("getdescriptorinfo", descriptor)

    def signmessagewithprivkey(self, privkey, message):  # 05
        return self.node._rpc.call("signmessagewithprivkey", privkey, message)

    def validateaddress(self, address):  # 06
        return self.node._rpc.call("validateaddress", address)

    def verifymessage(self, address, signature, message):  # 07
        return self.node._rpc.call("verifymessage", address, signature, message)
