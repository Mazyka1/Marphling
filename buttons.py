
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


menu_button = ReplyKeyboardMarkup(resize_keyboard=True)

menu_button.add(
    KeyboardButton("МЕНЮ"),
)
# Buttons for the "Магазин" menu

shop_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
shop_keyboard.add(
    KeyboardButton("Продуктовый"),
    KeyboardButton("Недвижимость")
)

kazino_keybord = ReplyKeyboardMarkup(resize_keyboard=True)
kazino_keybord.add(
    KeyboardButton("Кости"),
    KeyboardButton("Слоты")
)

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add(
    KeyboardButton("Магазин"),
    KeyboardButton("Казино"),
    KeyboardButton("Задание"),
    KeyboardButton("Карта"),
    KeyboardButton("Бизнес")
)

product_shop_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

product_shop_keyboard.add(
    KeyboardButton("Капибара: 1000$"),
    KeyboardButton("ТОРТ напалеон: 2000$"),
    KeyboardButton("Меч: 3000$"),
    KeyboardButton("Задонатить")
)

# Buttons for the "Задание" menu
task_global_keybord = ReplyKeyboardMarkup(resize_keyboard=True)
task_global_keybord.add(
    KeyboardButton("Легко"),
    KeyboardButton("Сложно")
)

task_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
task_keyboard.add(
    KeyboardButton("Ударить")
)


task2_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
task2_keyboard.add(
    KeyboardButton("Слабо ударить"),
    KeyboardButton("Ударить мечом")
)

start_ned = ReplyKeyboardMarkup(resize_keyboard=True)
start_ned.add(
    KeyboardButton("Запустить")
)
characters_keyboard_callback = CallbackData("characters", "character_id")
tecno_keybord_callback = CallbackData("tecno", "tecno_id")


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
            text=f"{tecno['name']} {tecno['coin']} ",
            callback_data=tecno_keybord_callback.new(tecno_id=idx)

        )
        tecno_keybord.add(button)

    return tecno_keybord


