import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
import random
import json

from constants import character_list, tecno_list, shop_list, map_list, car_list, random_hello
from config import TOKEN
from states import OurStates
from user_class import User

from buttons import menu_keyboard, task_keyboard, characters_keyboard_callback, \
    get_characters_keyboard, menu_button, get_nedvishimost, tecno_keybord_callback, kazino_keybord, task2_keyboard, \
    task_global_keybord, buisness_keybord, shop_keybord_callback, shop1, map_keybord_callback, map1, \
    car_keybord_callback, car, shop3_keybord, menu2_keyboard

from aiogram import types


player_file = "user_data.json"
player = dict()
player: dict[User]


def load_player():
    global player
    try:
        with open(player_file, "r", encoding="utf-8") as file:
            player_data = json.load(file)
            for user_id, data in player_data.items():
                player[user_id] = User.from_dict(data)
    except FileNotFoundError:
        print("Файл не найден")

async def update_income():
    while True:
        for user_id, user in player.items():
            await asyncio.sleep(60)
            selected_tecno = user.selected_tecno
            if selected_tecno:
                tecno = next((t for t in tecno_list if t['name'] == selected_tecno), None)
                income_rate = tecno['income_rate']
                income_per_minute_rounded = round(income_rate)
                user.coin += income_per_minute_rounded

def save_players(self):
    with open(player_file, "w", encoding="utf-8") as file:
        player_data = {str(user_id): User.to_dict(self) for user_id, tecno_list, character_list in
                     player.items()}  # Преобразование идентификаторов в строки
        json.dump(player_data, file, ensure_ascii=False)

bot = Bot(token=TOKEN)  # Создание объекта бота с использованием токена
dp = Dispatcher(
    bot=bot, storage=MemoryStorage()
)  # Создание диспетчера с использованием объекта бота и хранилища состояний в памяти

@dp.message_handler(commands=["start"], state="*")
async def start_handler(message: types.Message):
    user_id = message.from_user.id

    if user_id in player:
        if player[user_id].selected_character is not None:
            text = "Вы уже создали персонажа"
            await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)
            return
        else:
            player.pop(user_id)

    await message.answer(
        text="Добро пожаловать! Ты попал на аркадного бота, в котором ты будешь играть Space Comet! Как вас зовут?")
    await OurStates.enter_name.set()

@dp.message_handler(state=OurStates.enter_name)
async def enter_name_handler(message: types.Message):
    user_id = message.from_user.id

    if user_id in player:
        await OurStates.menu.set()
    else:
        player[user_id] = User(user_id=user_id, name=message.text)  # Задать имя новому пользователю
        text = f"Отлично, {player[user_id].name}! Теперь мы можем перейти к началу игры."
        await message.answer(text=text)
        await message.answer(text="Ты готов? Напиши.")

        await OurStates.ready.set()  # Установить состояние ready

@dp.message_handler(
    Text(equals=("да", "yes", "конечно", "готов", "готова"), ignore_case=True), state=OurStates.ready)
async def wait_for_partner_handler(message: types.Message):
    characters_keyboard = get_characters_keyboard(character_list)
    await message.answer(text="Выберите персонажа:", reply_markup=characters_keyboard)
    await OurStates.chosen_person.set()


@dp.message_handler(Text(equals='МЕНЮ', ignore_case=True), state=[OurStates.menu, OurStates.menu2])
async def menu(message: types.Message):
    user_id = message.from_user.id
    random_message = random.choice(random_hello)
    name = player[user_id].name
    place = player[user_id].current_city
    dengi = player[user_id].coin

    selected_character = player[user_id].selected_character
    character = next((c for c in character_list if c['name'] == selected_character), None)
    character_photo_url = character['photo_url']

    caption = f"<b>{random_message}, {name}!</b> Сейчас ты находишься в городе <b>'{place}'.</b> Денег у тебя <b>{dengi}$.</b>"

    if player[user_id].current_city == 'Россия':
        await bot.send_photo(chat_id=user_id, caption=caption, photo=character_photo_url, reply_markup=menu_keyboard,
                             parse_mode="HTML")
    else:
        await bot.send_photo(chat_id=user_id, caption=caption, photo=character_photo_url, reply_markup=menu2_keyboard,
                             parse_mode="HTML")
@dp.message_handler(Text(equals='Карта', ignore_case=True), state=[OurStates.menu, OurStates.menu2])
async def process_map1call(message: types.Message):
    user_id = message.from_user.id
    if player[user_id].buy_car is False:
        text = "У вас нет машины, вы можете купить её в магазине."
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)
    else:
        current_city = player[user_id].current_city
        map_keyboard = map1(map_list, current_city)
        photo_url = "https://ibb.co/wwLKj1g"
        caption = f"Вы сейчас находитесь в '{current_city}'. Куда вы хотите поехать?"
        await bot.send_photo(chat_id=user_id, photo=photo_url, caption=caption, reply_markup=map_keyboard)

@dp.message_handler(Text(equals='Автосалон', ignore_case=True), state=OurStates.menu)
async def process_donate(message: types.Message):
    car_keyboard = car(car_list)
    user_id = message.from_user.id

    text = "Здесь вы можете купить машину:"
    await bot.send_message(chat_id=user_id, text=text, reply_markup=car_keyboard)

@dp.message_handler(Text(equals='Магазин', ignore_case=True), state=OurStates.menu2)
async def process_shop(message: types.Message):
    text = "В какой магазин вы ходите сходить?"

    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=shop3_keybord)

# Продуктовый
@dp.message_handler(Text(equals='Продуктовый', ignore_case=True), state=OurStates.menu2)
async def process_shop(message: types.Message):
    shop2_keyboard = shop1(shop_list)

    photo_url = "https://ibb.co/WPsf792"  # Замените на URL-адрес фотографии из вашего магазина
    caption = "Добро пожаловать в магазин! Вот наше предложение."
    text = "Выбор:"

    await bot.send_photo(chat_id=message.chat.id, photo=photo_url, caption=caption, reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=shop2_keyboard)
    await OurStates.buy_burger.set()

@dp.message_handler(Text(equals=("Недвижимость"), ignore_case=True), state=OurStates.menu2)
async def process_ned(message: types.Message):
    tecno_keyboard = get_nedvishimost(tecno_list)
    await message.answer(text="Выберите недвижимость:", reply_markup=tecno_keyboard)
    await OurStates.chosen_tecno.set()

# Бизнес
@dp.message_handler(Text(equals='Бизнес', ignore_case=True), state=OurStates.menu2)
async def process_business(message: types.Message):
    user_id = message.from_user.id

    if player[user_id].selected_tecno is None:
        text = "У вас еще нет выбранного бизнеса. Пожалуйста, выберите недвижимость в магазине."
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)
        return

    text = "У вас есть бизнес: " + player[user_id].selected_tecno
    await message.answer(text=text, reply_markup=buisness_keybord)
@dp.message_handler(Text(equals='Запустить', ignore_case=True), state=OurStates.menu2)
async def process_buisnes(message: types.Message):
    user_id = message.from_user.id
    if player[user_id].selected_tecno is None:
        text = "У вас еще нет выбранного бизнеса. Пожалуйста, выберите недвижимость в магазине."
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)

    if player[user_id].start_buisnes is True:
        text = "У вас уже запущен бизнес"
        await bot.send_message(chat_id=user_id, text=text)
        await OurStates.menu.set()
    else:
        player[user_id].start_buisnes = True
        selected_tecno = player[user_id].selected_tecno
        tecno = next((t for t in tecno_list if t['name'] == selected_tecno), None)
        income_rate = tecno['income_rate']
        text = f"Запускаю бизнес...\nДоход: {income_rate}$\мин"
        await message.answer(text=text)
        await asyncio.create_task(update_income())
        await OurStates.menu.set()

@dp.message_handler(Text(equals='Баланс', ignore_case=True), state=OurStates.menu2)
async def process_buisnes(message: types.Message):
    user_id = message.from_user.id
    if player[user_id].selected_tecno is None:
        text = "У вас еще нет выбранного бизнеса. Пожалуйста, выберите недвижимость в магазине."
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)
        return
    text = f"Баланс: {player[user_id].coin}$"
    await bot.send_message(chat_id=user_id, text=text)

@dp.message_handler(Text(equals='08102008', ignore_case=True), state=OurStates.menu)
async def process_sword(message: types.Message):
    user_id = message.from_user.id
    player[user_id].coin += 10000000


# Казино
@dp.message_handler(Text(equals='Казино', ignore_case=True), state=OurStates.menu)
async def process_kaz(message: types.Message):
    text = "Добро пожаловать в казино! Куда пойдете?"

    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=kazino_keybord)

@dp.message_handler(Text(equals='Кости', ignore_case=True), state=OurStates.menu)
async def process_kaz1(message: types.Message):
    user_id = message.from_user.id
    video_url = "https://yandex.ru/video/preview/17407417412192363873"
    await bot.send_video(chat_id=user_id, video=video_url, reply_markup=menu_button)


@dp.message_handler(Text(equals='Слоты', ignore_case=True), state=OurStates.menu)
async def process_kaz2(message: types.Message):
    user_id = message.from_user.id
    video_url = "https://yandex.ru/video/preview/17407417412192363873"
    await bot.send_video(chat_id=user_id, video=video_url, reply_markup=menu_button)

# Задание
@dp.message_handler(Text(equals='Задание', ignore_case=True), state=OurStates.menu)
async def process_question(message: types.Message):
    user_id = message.from_user.id
    text = "Выберите сложность задания:"
    await bot.send_message(chat_id=user_id, text=text, reply_markup=task_global_keybord)


@dp.message_handler(Text(equals='Легко', ignore_case=True), state=OurStates.menu)
async def process_question1(message: types.Message):
    user_id = message.from_user.id
    player[user_id].reward_received = False
    user_id = message.from_user.id
    if player[user_id].boss_life != 1000:
        player[user_id].boss_life = 1000
    text = "Вы попали на легкое задание! Вы должны убить босса!"
    photo_url = "https://funik.ru/wp-content/uploads/2018/12/5b2a140f049ea4992ca4.jpg"
    await bot.send_message(chat_id=user_id, text=text, reply_markup=task_keyboard)
    await bot.send_photo(chat_id=user_id, photo=photo_url)

    await OurStates.question.set()
@dp.message_handler(Text(equals='Сложно', ignore_case=True), state=OurStates.menu)
async def process_question2(message: types.Message):
    user_id = message.from_user.id
    player[user_id].reward_received = False
    if player[user_id].hp != 1000:
        player[user_id].hp = 1000
    if player[user_id].boss2_life != 3000:
        player[user_id].boss2_life = 3000

    text = "Вы попали на сложное задание! Вы должны убить босса!"
    photo_url = "https://funik.ru/wp-content/uploads/2018/12/5b2a140f049ea4992ca4.jpg"
    await bot.send_message(chat_id=user_id, text=text, reply_markup=task2_keyboard)
    await bot.send_photo(chat_id=user_id, photo=photo_url)

    await OurStates.question2.set()

@dp.message_handler(Text(equals='Ударить', ignore_case=True), state=OurStates.question)
async def process_ydar(message: types.Message):
    user_id = message.from_user.id
    random_number = random.randint(1, 10)

    if random_number < 5:
        if player[user_id].reward_received:
            await bot.send_message(chat_id=user_id, text="Вы уже получили награду", reply_markup=menu_button)
            await OurStates.menu.set()
        else:
            hp_damage = random.randint(300, 500)
            text = f"Вы промахнулись, и Босс наносит вам {hp_damage} единиц урона. "
            photo = 'https://catherineasquithgallery.com/uploads/posts/2021-03/1614550176_49-p-memi-na-belom-fone-53.jpg'
            await bot.send_photo(chat_id=user_id, caption=text, photo=photo)
    else:
        boss_damage = random.randint(100, 300)
        player[user_id].boss_life -= boss_damage
        photo = 'https://ae01.alicdn.com/kf/U414704f8c7d94885a731e958a20dd445m.jpg'
        text = f"Вы наносите боссу {boss_damage} единиц урона. Осталось {player[user_id].boss_life} единиц жизни у босса."

        if player[user_id].boss_life <= 0:
            if player[user_id].reward_received:
                await bot.send_message(chat_id=user_id, text="Вы уже получили награду", reply_markup=menu_button)
                await OurStates.menu.set()
            else:
                player[user_id].reward_received = True
                reward = random.randint(100, 200)
                player[user_id].coin += reward
                txt1 = f"Поздравляю! Вы победили босса и получаете {reward} монет!"
                await bot.send_message(chat_id=user_id, text=txt1, reply_markup=menu_button)
                await OurStates.menu.set()

        await bot.send_photo(chat_id=user_id, photo=photo, caption=text)


@dp.message_handler(Text(equals='Слабо ударить', ignore_case=True), state=OurStates.question2)
async def process_slow_ydar(message: types.Message):
    user_id = message.from_user.id

    random_number = random.randint(1, 10)

    if random_number >= 10:
        if player[user_id].reward_received:
            await bot.send_message(chat_id=user_id, text="Вы уже получили награду", reply_markup=menu_button)
            await OurStates.menu.set()
        else:
            hp_damage = random.randint(400, 500)
            player[user_id].hp -= hp_damage
            text = f"Вы промахнулись, и Босс наносит вам {hp_damage} единиц урона. У вас осталось {player[user_id].hp}."
            photo = 'https://catherineasquithgallery.com/uploads/posts/2021-03/1614550176_49-p-memi-na-belom-fone-53.jpg'
            await bot.send_photo(chat_id=user_id, caption=text, photo=photo)
            if player[user_id].hp <= 0:
                txt = f"Вы проиграли, попробуйте еще раз!"
                await message.answer(text=txt, reply_markup=menu_button)
                await OurStates.menu.set()
    else:
        boss_damage = random.randint(100, 300)
        player[user_id].boss2_life -= boss_damage
        photo = 'https://ae01.alicdn.com/kf/U414704f8c7d94885a731e958a20dd445m.jpg'
        text = f"Вы наносите боссу {boss_damage} единиц урона. "

        if player[user_id].boss2_life <= 0:
            if player[user_id].reward_received:
                await bot.send_message(chat_id=user_id, text="Вы уже получили награду", reply_markup=menu_button)
                await OurStates.menu.set()
            else:
                player[user_id].reward_received = True
                reward = random.randint(800, 1000)
                player[user_id].coin += reward
                txt1 = f"Поздравляю! Вы победили босса и получаете {reward} монет!"
                await OurStates.menu.set()
                await message.answer(text=txt1, reply_markup=menu_button)
        if player[user_id].boss2_life >= 0:
            if player[user_id].reward_received:
                await bot.send_message(chat_id=user_id, text="Вы уже получили награду", reply_markup=menu_button)
                await OurStates.menu.set()
            else:
                text += f"Осталось {player[user_id].boss2_life} единиц жизни у босса. "

        await bot.send_photo(chat_id=user_id, photo=photo, caption=text)

@dp.message_handler(Text(equals='Ударить мечом', ignore_case=True), state=OurStates.question2)
async def process_sword_ydar(message: types.Message):
    user_id = message.from_user.id
    random_number = random.randint(1, 10)

    if random_number > 5:
        if player[user_id].reward_received:
            await bot.send_message(chat_id=user_id, text="Вы уже получили награду", reply_markup=menu_button)
            await OurStates.menu.set()
        else:
            hp_damage = random.randint(400, 500)
            player[user_id].hp -= hp_damage
            text = f"Вы промахнулись, и Босс наносит вам {hp_damage} единиц урона. У вас осталось {player[user_id].hp}."
            photo = 'https://catherineasquithgallery.com/uploads/posts/2021-03/1614550176_49-p-memi-na-belom-fone-53.jpg'
            await bot.send_photo(chat_id=user_id, caption=text, photo=photo)
            if player[user_id].hp <= 0:
                txt = f"Вы проиграли, попробуйте еще раз!"
                await message.answer(text=txt, reply_markup=menu_button)
                await OurStates.menu.set()
    else:
        boss_damage = random.randint(600, 700)
        player[user_id].boss2_life -= boss_damage
        photo = 'https://ae01.alicdn.com/kf/U414704f8c7d94885a731e958a20dd445m.jpg'
        text = f"Вы наносите боссу {boss_damage} единиц урона. "

        if player[user_id].boss2_life <= 0:
            if player[user_id].reward_received:
                await bot.send_message(chat_id=user_id, text="Вы уже получили награду", reply_markup=menu_button)
                await OurStates.menu.set()
            else:
                player[user_id].reward_received = True
                reward = random.randint(800, 1000)
                player[user_id].coin += reward
                txt1 = f"Поздравляю! Вы победили босса и получаете {reward} монет!"
                await message.answer(text=txt1, reply_markup=menu_button)
                await OurStates.menu.set()

        if player[user_id].boss2_life >= 0:
            if player[user_id].reward_received:
                await bot.send_message(chat_id=user_id, text="Вы уже получили награду", reply_markup=menu_button)
                await OurStates.menu.set()
            else:
                text += f"Осталось {player[user_id].boss2_life} единиц жизни у босса. "

        await bot.send_photo(chat_id=user_id, photo=photo, caption=text)


# Кнопки
@dp.callback_query_handler(shop_keybord_callback.filter(), state=OurStates.buy_burger)
async def process_shopo_selection(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    selected_shop_id = callback_data["shop_id"]
    selected_shop_id = int(selected_shop_id)
    shop = shop_list[selected_shop_id]
    user_id = call.from_user.id
    user_items = player[user_id].user_items

    await bot.answer_callback_query(
        call.id
    )

    if shop['name'] in user_items:
        text = "Вы уже купили эту вещь"
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)
        await OurStates.menu2.set()
    elif player[user_id].coin < shop['cost2']:
        text = "У вас недостаточно средств"
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)
        await OurStates.menu2.set()
    else:
        player[user_id].buy_food = shop['name']
        text = f"Вы купили: {shop['name']}"
        player[user_id].coin -= shop['cost2']
        await bot.send_photo(chat_id=user_id, photo=shop['photo_url'], caption=text, reply_markup=menu_button)
        await state.update_data(chosen_shop=shop['name'])  # Обновляем данные состояния
        await OurStates.menu2.set()
        player[user_id].user_items.append(shop['name'])

@dp.callback_query_handler(map_keybord_callback.filter(), state=[OurStates.menu, OurStates.menu2])
async def process_map_selection(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    selected_map_id = callback_data["map_id"]
    selected_map_id = int(selected_map_id)
    selected_map = map_list[selected_map_id]
    user_id = call.from_user.id

    await bot.answer_callback_query(
        call.id
    )
    text = f"Вы приехали в: '{selected_map['name']}'"
    await bot.send_photo(chat_id=user_id, photo=selected_map['photo_url'], caption=text, reply_markup=menu_button)
    await state.update_data(chosen_map=selected_map['name'])
    player[user_id].current_city = selected_map['name']
    if selected_map_id == 0:
        await OurStates.menu.set()
    elif selected_map_id == 1:
        await OurStates.menu2.set()

@dp.callback_query_handler(car_keybord_callback.filter(), state=OurStates.menu)
async def process_tecno_selection(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    selected_car_id = callback_data["car_id"]
    selected_car_id = int(selected_car_id)
    selected_car = car_list[selected_car_id]
    user_id = call.from_user.id
    car_cost = selected_car['cost']

    await bot.answer_callback_query(
        call.id
    )
    if player[user_id].buy_car is True:
        text = "У вас уже есть машина"
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)

    elif player[user_id].coin < car_cost:
        text = "У вас недостаточно средств"
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)
        await OurStates.menu.set()
    else:
        player[user_id].coin -= car_cost
        text = f"Вы купили: '{selected_car['name']}, {selected_car['speed']}'"
        await bot.send_photo(chat_id=user_id, photo=selected_car['photo_url'], caption=text, reply_markup=menu_button)
        await state.update_data(chosen_car=selected_car['name'])
        player[user_id].buy_car = True

@dp.callback_query_handler(tecno_keybord_callback.filter(), state=OurStates.chosen_tecno)
async def process_tecno_selection(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    selected_tecno_id = callback_data["tecno_id"]
    selected_tecno_id = int(selected_tecno_id)
    tecno = tecno_list[selected_tecno_id]
    user_id = call.from_user.id
    tecno_cost = tecno['cost']


    await bot.answer_callback_query(
        call.id
    )

    if player[user_id].buy_ned is True:
        text = "У вас уже есть бизнес"
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)
        await OurStates.menu2.set()

    elif player[user_id].coin < tecno_cost:
        text = "У вас недостаточно средств"
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)
        await OurStates.menu2.set()
    else:
        player[user_id].coin -= tecno_cost
        player[user_id].selected_tecno = tecno['name']
        text = f"Вы купили недвижимость: {tecno['name']}, {tecno['coin']}"
        await bot.send_photo(chat_id=user_id, photo=tecno['photo_url'], caption=text, reply_markup=menu_button)
        await state.update_data(chosen_tecno=tecno['name'])  # Обновляем данные состояния
        player[user_id].buy_ned = True
        await OurStates.menu2.set()

@dp.callback_query_handler(characters_keyboard_callback.filter(), state=OurStates.chosen_person)
async def process_character_selection(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    selected_character_id = callback_data["character_id"]
    selected_character_id = int(selected_character_id)
    character = character_list[selected_character_id]
    user_id = call.from_user.id
    player[user_id].current_city = "Россия"

    await bot.answer_callback_query(
        call.id
    )

    user_id = call.from_user.id
    player[user_id].selected_character = character['name']

    caption = f"Вы выбрали персонажа: {character['name']}"
    await OurStates.menu.set()
    await bot.send_photo(chat_id=user_id, caption=caption, photo=character['photo_url'], reply_markup=menu_button)
    await state.update_data(chosen_character=character['name'])  # Обновляем данные состояния


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)