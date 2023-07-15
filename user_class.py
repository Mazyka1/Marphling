__all__ = ["User"]
1

class User:
    user_id: int
    name: str
    coin: int
    selected_character: None

    def __init__(self, user_id: int, name: str = None):
        self.selected_character = None
        self.user_id = user_id
        self.name = name
        self.coin = 0
        self.selected_tecno = None
        self.hp = 0
        self.boss_life = 0
        self.boss2_life = 0

    def to_dict(self):
        return {
            "selected_character": self.selected_character,
            "coin": self.coin,
            "user_id": self.user_id,
            "name": self.name,
            "selected_tecno": self.selected_tecno,
            "hp": self.hp,
            "boss_life": self.boss_life,
            "boss2_life": self.boss2_life
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name"),
            coin=data.get("coin"),
            selected_character=data.get("selected_character"),
            user_id=data.get("user_id"),
            selected_tecno= data.get("selected_tecno"),
            hp=data.get('hp'),
            boss_life = data.get('boss_life'),
            boss2_life = data.get("boss2_life")
        )