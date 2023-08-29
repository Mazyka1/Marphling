
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


menu_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

menu_button.add(
    KeyboardButton("МЕНЮ"),
)
# Buttons for the "Магазин" menu

shop_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
shop_keyboard.add(
    KeyboardButton("Автосалон")
)
shop_keyboard.add(
    KeyboardButton("МЕНЮ")
)

kazino_keybord = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kazino_keybord.add(
    KeyboardButton("Кости"),
    KeyboardButton("Слоты"),
)
kazino_keybord.add(
    KeyboardButton("МЕНЮ")
)

shop3_keybord = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
shop3_keybord.add(
    KeyboardButton("Недвижимость"),
    KeyboardButton("Продуктовый")
)
shop3_keybord.add(
    KeyboardButton("МЕНЮ")
)

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_keyboard.add(
    KeyboardButton("Автосалон"),
    KeyboardButton("Казино"),
    KeyboardButton("Задание"),
    KeyboardButton("Карта")
)

menu2_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu2_keyboard.add(
    KeyboardButton("Магазин"),
    KeyboardButton("Карта"),
    KeyboardButton("Бизнес")
)

# Buttons for the "Задание" menu
task_global_keybord = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
task_global_keybord.add(
    KeyboardButton("Легко"),
    KeyboardButton("Сложно")
)
task_global_keybord.add(
    KeyboardButton("МЕНЮ")
)

task_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
task_keyboard.add(
    KeyboardButton("Ударить")
)


task2_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
task2_keyboard.add(
    KeyboardButton("Слабо ударить"),
    KeyboardButton("Ударить мечом")
)

buisness_keybord = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buisness_keybord.add(
    KeyboardButton("Запустить"),
    KeyboardButton("Баланс"),
)
buisness_keybord.add(
    KeyboardButton("МЕНЮ")
)

characters_keyboard_callback = CallbackData("characters", "character_id")
tecno_keybord_callback = CallbackData("tecno", "tecno_id")
shop_keybord_callback = CallbackData("shop", "shop_id")
map_keybord_callback = CallbackData("map", "map_id")
car_keybord_callback = CallbackData("car", "car_id")


def get_characters_keyboard(character_list: list):
    characters_keyboard = InlineKeyboardMarkup(row_width=2)

    for idx, character in enumerate(character_list):
        button = InlineKeyboardButton(
            text=f"{idx + 1}. {character['name']}",
            callback_data=characters_keyboard_callback.new(character_id=idx)
        )
        characters_keyboard.add(button)

    return characters_keyboard

def get_nedvishimost(tecno_list: list):
    tecno_keybord = InlineKeyboardMarkup(row_width=2)

    for idx, tecno in enumerate(tecno_list):
        button = InlineKeyboardButton(
            text=f"{tecno['name']}, {tecno['coin']}, {tecno['cost2']}",
            callback_data=tecno_keybord_callback.new(tecno_id=idx)

        )
        tecno_keybord.add(button)

    return tecno_keybord

def shop1(shop_list: list):
    shop2_keyboard = InlineKeyboardMarkup(row_width=2)

    for idx, shop in enumerate(shop_list):
        button = InlineKeyboardButton(
            text=f"{shop['name']}, {shop['cost']}",
            callback_data=shop_keybord_callback.new(shop_id=idx)

        )
        shop2_keyboard.add(button)

    return shop2_keyboard

def map1(map_list: list, current_city: str):
    map_keyboard = InlineKeyboardMarkup(row_width=2)

    for idx, map1 in enumerate(map_list):
        if map1['name'] != current_city:
            button = InlineKeyboardButton(
                text=f"{map1['name']}, {map1['place']}",
                callback_data=map_keybord_callback.new(map_id=idx)

            )
            map_keyboard.add(button)

    return map_keyboard

def car(car_list: list):
    car_keyboard = InlineKeyboardMarkup(row_width=2)

    for idx, car in enumerate(car_list):
            button = InlineKeyboardButton(
                text=f"{car['name']}, {car['speed']}, {car['cost2']}",
                callback_data=car_keybord_callback.new(car_id=idx)

            )
            car_keyboard.add(button)

    return car_keyboard

