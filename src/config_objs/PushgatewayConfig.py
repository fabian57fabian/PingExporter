
class PushgatewayConfig:
    ip_pushgateway: str
    port_pushgateway: int
    username_pushgateway: str
    pass_pushgateway: str

    def __init__(self, ip_pushgateway: str, port_pushgateway: int, username_pushgateway: str, pass_pushgateway: str) -> None:
        self.ip_pushgateway = ip_pushgateway
        self.port_pushgateway = port_pushgateway
        self.username_pushgateway = username_pushgateway
        self.pass_pushgateway = pass_pushgateway



