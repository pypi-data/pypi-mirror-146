
import json
from sys import stdout, argv

from enum import Enum

class EntityType(Enum):
    """All types of Entity"""

    """NPC"""
    NPC = 1
    """Real player"""
    PERSON = 2
    """Unknown"""
    UNKNOWN = 3


class PluginWriter:
    """
    Help class for communications between server and plugin.
    """
    def __init__(self) -> None:
        pass

    """Communicate with server"""
    def write(self, content: str) -> None:
        print(content + ' ', end="")
        stdout.flush()

    """
    Encode data to server understanding format
    :param d: Object which contain all data you want to send.
    :return Encoded data:
    """
    def encode(self, d: dict) -> str:
        text = ""

        for key, value in d.items():
            if isinstance(value, dict):
                text += f"-{key} '{json.dumps(value)}'"
            elif isinstance(value, str):
                text += f"-{key} '{value}'"
            else:
                text += f"-{key} '{str(value)}'"

        return text

class PluginReader:
    """
    Help class for communications between server and plugin.
    """
    def __init__(self) -> None:
        pass

    """
    Read coming data from server about clients on server, command, sender...
    """
    def read(self) -> str:
        args = argv[1:]
        return ' '.join(args) if len(args) > 0 else ""

    """
    Decoding data from server
    :param argv: Arguments from cli.
    :return Parsed Data:
    """
    def decode(self, argv: list) -> dict:
        words = argv

        data = {}

        for (i, arg) in enumerate(words):
            if arg.startswith('-'):
                if len(words) > i + 1:
                    v = words[i + 1]
                    try:
                        v_json = json.loads(v)
                        data[arg[1:]] = v_json
                    except:
                        data[arg[1:]] = v
                else:
                    return self.writer.encode({
                        "status": False,
                        "reason": "parse-err"
                    })

        return data

class Entity:
    """
    Root class for all entities.
    :param type_: Enitity Type
    """
    def __init__(self, type_: EntityType) -> None:
        self.type = type_

class Sender(Entity):
    """
    Sender class needs to get information about command sender.
    :param entity_type: Entity Type
    :param addr: Address of sender (Ip)
    :param writer: Plugin Writer for communications.
    :return:
    """
    def __init__(self, entity_type: EntityType, addr: str, writer: PluginWriter) -> None:
        super().__init__(entity_type)
        self.addr = addr
        self.writer = writer
        
    """
    Send message to sender.
    :param message: Message to be sent.
    :return:
    """
    def send_message(self, message: str) -> None:
        self.writer.write(
            self.writer.encode({
                "send": {
                    "addr": self.addr,
                    "message": message
                }
            })
        )

    """
    Get sender IP.
    """
    def get_ip(self):
        return self.addr[0]


class Player(Sender):
    """
    Player class extends of entity and sender. Needs to storage nickname and other player's data.
    :param nickname: Player's name on server
    :param addr: Player's address (For Sender class)
    :return:
    """
    def __init__(self, nickname: str, addr: tuple) -> None:
        super().__init__(EntityType.PERSON, addr, PluginWriter())
        self.nickname = nickname
        

class CommandPlugin:
    """
    Main Plugin constructor
    :param argv: Arguments from cli.
    :return:
    """
    def __init__(self, argv: list) -> None:
        self.writer = PluginWriter()
        self.reader = PluginReader()
        self.argv = argv

        self.prefix = "/"

        self.sender: Sender = None
        self.clients: list[Player] = []

        self.parse_argv(argv)

    """
    On Command handler. Triggers when someone on server typed command.
    But triggers only for registered commands from plugins.
    :param sender: Command Sender
    :param command: Command Name
    :param args: Command Arguments
    :return:
    """
    def on_command(self, sender: Sender, command: str, args: list) -> None:
        self.writer.write(f"Message from: {sender.addr[0]}\nCommand: {command}\nArgs: {args}\n")

    """
    Static method to sender command.
    """
    @staticmethod
    def parse_command(prefix: str, command: str) -> tuple:
        if not command.startswith(prefix):
            return (None, [])
        else:
            words = command.split()
            return (words[0][1:], words[1:])


    """
    Parser for cli arguments.
    """
    def parse_argv(self, argv: list) -> None:
        data = self.reader.decode(argv)

        if isinstance(data, str):
            print(data)

        if "clients" in data:
            clients = data['clients']
            if isinstance(clients, list):
                for client in clients:
                    p = Player(client[0], client[1])
                    self.clients.append(p)
            else:
                return

        if "sender" in data:
            t_str = data['sender']['type']
            t: EntityType = None
            if t_str == "person":
                t = EntityType.PERSON
            elif t_str == "npc":
                t = EntityType.NPC
            else:
                t = EntityType.UNKNOWN
            self.sender = Sender(t, data['sender']['addr'], self.writer)
        
        if "command" in data:
            cmd = self.parse_command(self.prefix, data['command'])
            if cmd[0] is not None:
                self.on_command(self.sender, cmd[0], cmd[1])
            else:
                return


if __name__ == "__main__":
    plugin = CommandPlugin(argv)
