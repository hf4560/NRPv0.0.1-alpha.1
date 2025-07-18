from core.crypto.hashing import generate_hash
from core.utils.env import SEED_CORDS, R_VIEW
from core.utils.cords import cordsToSq
from core.map.local_map import LocalMap
import math

class QNode:
    def __init__(self, coords):
        self.__hash = generate_hash()
        self.__coords = coords
        self.__map = LocalMap()

    def getHash(self):
        return self.__hash

    def getCoords(self):
        return self.__coords

    def handle_packet(self, packet):
        packet_type = packet.get("type")
        payload = packet.get("payload")

        if packet_type == "connect_request":
            return self.__handle_connect(payload)

        return {
            "status": 400,
            "response": {
                "type": "error",
                "payload": {"message": f"Unknown packet type '{packet_type}'"}
            }
        }

    def __handle_connect(self, data):
        hash_ = data.get('hash')
        ip = data.get('own_ip')
        port = data.get('own_port')
        x = float(data.get('ping'))
        y = float(data.get('hops'))
        cords = (x, y, 0)

        if not self.__map.getNearNodes():
            sq = cordsToSq(SEED_CORDS)
            self.__map.addNearNode(hash_, {
                'ip': ip, 'port': port, 'sq': sq, 'cords': SEED_CORDS
            })
            return {
                "status": 200,
                "response": {
                    "type": "connect_seed_accept",
                    "payload": {"sq": sq, "cords": SEED_CORDS}
                }
            }

        if math.sqrt(x*x + y*y) < R_VIEW:
            sq = cordsToSq(cords)
            self.__map.addNearNode(hash_, {
                'ip': ip, 'port': port, 'sq': sq, 'cords': cords
            })
            return {
                "status": 200,
                "response": {
                    "type": "connect_accept",
                    "payload": {
                        "sq": sq,
                        "cords": cords,
                        "near_nodes": self.__map.getNearNodes()
                    }
                }
            }

        min_dist = float('inf')
        closest_node = None
        for node in self.__map.getNearNodes().values():
            nx, ny, _ = node['cords']
            dist = math.sqrt((x - nx) ** 2 + (y - ny) ** 2)
            if dist < min_dist:
                min_dist = dist
                closest_node = node

        if closest_node:
            return {
                "status": 200,
                "response": {
                    "type": "connect_redirect",
                    "payload": {
                        "redirect_to": closest_node['ip'],
                        "port": closest_node['port'],
                        "recommended_sq": closest_node['sq']
                    }
                }
            }

        return {
            "status": 202,
            "response": {
                "type": "connect_hold",
                "payload": {
                    "reason": "no_visible_nodes",
                    "message": "wait_for_network_seed"
                }
            }
        }
