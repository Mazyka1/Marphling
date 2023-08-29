# user_class.py

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.selected_character = None
        self.selected_tecno = None
        self.selected_shop = None
        self.buy_food = None
        self.buy_ned = False
        self.start_buisnes = None
        self.coin = 0
        self.reward_received = False
        self.boss_life = None
        self.hp = None
        self.boss2_life = None
        self.current_city = None
        self.buy_car = False
        self.user_items = []

    @classmethod
    def from_dict(cls, data):
        user = cls(user_id=data["user_id"], name=data["name"])
        user.selected_character = data["selected_character"]
        user.selected_tecno = data["selected_tecno"]
        user.selected_shop = data["selected_shop"]
        user.buy_food = data["buy_food"]
        user.buy_ned = data["buy_ned"]
        user.start_buisnes = data["start_buisnes"]
        user.coin = data["coin"]
        user.reward_received = data["reward_received"]
        user.boss_life = data["boss_life"]
        user.hp = data["hp"]
        user.boss2_life = data["boss2_life"]
        user.current_city = data["current_city"]  # Load the current_city attribute from the dictionary
        user.buy_car = data["buy_car"]
        return user

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "selected_character": self.selected_character,
            "selected_tecno": self.selected_tecno,
            "selected_shop": self.selected_shop,
            "buy_food": self.buy_food,
            "buy_ned": self.buy_ned,
            "start_buisnes": self.start_buisnes,
            "coin": self.coin,
            "reward_received": self.reward_received,
            "boss_life": self.boss_life,
            "hp": self.hp,
            "boss2_life": self.boss2_life,
            "current_city": self.current_city,  # Save the current_city attribute to the dictionary
            "buy_car": self.buy_car
        }
