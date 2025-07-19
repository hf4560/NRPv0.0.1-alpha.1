# core/UNode.py

from hashlib import blake2b
from core.environment import Environment
from core.tools import get_timestamp

class UNode:
    def __init__(self, environment: Environment):
        self.__environment = environment
        self.__qnodes = {}  # {hash: {"coords": (x, y, z), "timestamp": t}}

    def __blake2_hash(self, data: bytes, digest_size=32):
        return blake2b(data, digest_size=digest_size).hexdigest()

    def register_qnode(self, qnode_info: dict) -> str:
        """
        Регистрирует новый QNode, возвращает его хэш.
        qnode_info: {
            "coords": (x, y, z),
            "salt": bytes,
            "info": bytes (любые идентифицирующие данные)
        }
        """
        salt = qnode_info.get("salt")
        info = qnode_info.get("info")
        coords = qnode_info.get("coords")

        if not all([salt, info, coords]):
            raise ValueError("Недостаточно данных для регистрации QNode")

        qnode_hash = self.__blake2_hash(salt + info)
        self.__qnodes[qnode_hash] = {
            "coords": coords,
            "timestamp": get_timestamp(),
        }

        return qnode_hash

    def unregister_qnode(self, qnode_hash: str) -> bool:
        """Удаляет QNode по хэшу. Возвращает True, если удаление прошло успешно."""
        return self.__qnodes.pop(qnode_hash, None) is not None

    def get_qnode_config(self, qnode_hash: str) -> dict:
        """Возвращает конфигурацию среды для заданного QNode."""
        if qnode_hash not in self.__qnodes:
            raise ValueError("QNode не зарегистрирован")

        return self.__environment.get_qnode_config(qnode_hash)

    def get_active_qnodes(self) -> dict:
        """Возвращает текущий список зарегистрированных QNodes."""
        return self.__qnodes.copy()

    def validate_qnode(self, qnode_hash: str) -> bool:
        """Проверяет, зарегистрирован ли QNode с данным хэшем."""
        return qnode_hash in self.__qnodes
