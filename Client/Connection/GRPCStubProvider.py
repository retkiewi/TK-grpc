from Message.Gen import SizeStub, BodyStub, StyleStub, AnimalStub, FormatStub


class GRPCStubProvider:
    @staticmethod
    def GetStub(name: str):
        return lambda channel: {
            'size': SizeStub(channel),
            'format': FormatStub(channel),
            'body': BodyStub(channel),
            'animal': AnimalStub(channel),
            'style': StyleStub(channel)
        }[name]