from .bases import ServiceController, Ext

class ServiceControllerEventV2(ServiceController):
    channel: str = "/service/controller"
    ext: Ext
    id: str
    successful: bool

    async def handle(self, instance):
        pass
