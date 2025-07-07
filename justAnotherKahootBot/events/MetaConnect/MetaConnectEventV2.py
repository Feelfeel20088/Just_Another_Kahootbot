from .bases import MetaConnect, Ext 


class MetaConnectEventV2(MetaConnect):
    channel: str = "/meta/connect"
    ext: Ext
    id: str
    successful: bool

    async def handle(self, instance):
        pass


