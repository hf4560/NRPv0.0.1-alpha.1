class Environment:
    def get_qnode_config(self, qnode_hash: str) -> dict:
        # Можно на будущее отдавать кастомную конфигурацию
        return {
            "heartbeat_interval": 5,
            "max_neighbors": 12,
            "encryption": "blake3",
        }
