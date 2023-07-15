from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
import random
import json

from constants import character_list, tecno_list
from config import TOKEN
from states import OurStates
from user_class import User

from buttons import menu_keyboard, shop_keyboard, product_shop_keyboard, task_keyboard, characters_keyboard_callback, \
    get_characters_keyboard, menu_button, get_nedvishimost, tecno_keybord_callback, kazino_keybord, task2_keyboard, \
    task_global_keybord

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

bot = Bot(token=TOKEN)  # Создание объекта бота с использованием токена
dp = Dispatcher(
    bot=bot, storage=MemoryStorage()
)  # Создание диспетчера с использованием объекта бота и хранилища состояний в памяти


from aiogram import types


@dp.message_handler(commands=["start"], state="*")
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if user_id in player:
        if player[user_id].selected_character is not None:
            text = "У вас уже есть выбранный персонаж."
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
    Text(equals=("да", "yes", "конечно", "готов", "готова"), ignore_case=True),
    state=OurStates.ready
)
async def wait_for_partner_handler(message: types.Message):
    characters_keyboard = get_characters_keyboard(character_list)
    await message.answer(text="Выберите персонажа:", reply_markup=characters_keyboard)
    await OurStates.chosen_person.set()


@dp.callback_query_handler(characters_keyboard_callback.filter(), state=OurStates.chosen_person)
async def process_character_selection(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    selected_character_id = callback_data["character_id"]
    selected_character_id = int(selected_character_id)
    character = character_list[selected_character_id]

    user_id = call.from_user.id
    player[user_id].selected_character = character['name']

    caption = f"Вы выбрали персонажа: {character['name']}"
    await bot.send_photo(chat_id=user_id, caption=caption, photo=character['photo_url'], reply_markup=menu_button)
    await state.update_data(chosen_character=character['name'])  # Обновляем данные состояния

def save_players(self):
    with open(player_file, "w", encoding="utf-8") as file:
        player_data = {str(user_id): User.to_dict(self) for user_id, tecno_list, character_list in
                     player.items()}  # Преобразование идентификаторов в строки
        json.dump(player_data, file, ensure_ascii=False)

@dp.message_handler(Text(equals='МЕНЮ', ignore_case=True), state="*")
async def menu(message: types.Message):
    await OurStates.menu.set()
    user_id = message.from_user.id

    selected_character = player[user_id].selected_character
    character = next((c for c in character_list if c['name'] == selected_character), None)
    character_photo_url = character['photo_url']

    caption = f"Меню:\nВаш персонаж: {selected_character}\nБаланс: {player[user_id].coin}$"

    await bot.send_photo(chat_id=user_id, caption=caption, photo=character_photo_url, reply_markup=menu_keyboard)

@dp.message_handler(Text(equals='Карта', ignore_case=True), state=OurStates.menu)
async def process_kaz1(message: types.Message):
    user_id = message.from_user.id
    video_url = "https://yandex.ru/video/preview/17407417412192363873"
    await bot.send_video(chat_id=user_id, video=video_url, reply_markup=menu_button)



@dp.message_handler(Text(equals='Магазин', ignore_case=True), state=OurStates.menu)
async def process_shop(message: types.Message):
    text = "В какой магазин вы ходите сходить?"

    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=shop_keyboard)


@dp.message_handler(Text(equals=("Недвижимость"), ignore_case=True), state=OurStates.menu)
async def process_ned(message: types.Message):
    tecno_keyboard = get_nedvishimost(tecno_list)
    await message.answer(text="Выберите недвижимость:", reply_markup=tecno_keyboard)
    await OurStates.chosen_tecno.set()

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


@dp.callback_query_handler(tecno_keybord_callback.filter(), state=OurStates.chosen_tecno)
async def process_tecno_selection(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user_id = call.from_user.id
    selected_tecno_id = callback_data["tecno_id"]
    selected_tecno_id = int(selected_tecno_id)
    tecno = tecno_list[selected_tecno_id]

    if player[user_id].selected_tecno is True:
        text = "У вас уже есть недвижимость"
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)
        return

    user_id = call.from_user.id
    player[user_id].selected_tecno = tecno['name']

    await bot.send_message(text=f"Вы купили недвижимость: {tecno['name']}, {tecno['coin']}", chat_id=user_id)
    await bot.send_photo(chat_id=user_id, photo=tecno['photo_url'], reply_markup=menu_button)
    await state.update_data(chosen_tecno=tecno['name'])  # Обновляем данные состояния


@dp.message_handler(Text(equals='Продуктовый', ignore_case=True), state=OurStates.menu)
async def process_shop(message: types.Message):

    photo_url = "https://ibb.co/WPsf792"  # Замените на URL-адрес фотографии из вашего магазина
    caption = "Добро пожаловать в магазин! Вот наше предложение."
    text = "Выбор:"

    await bot.send_photo(chat_id=message.chat.id, photo=photo_url, caption=caption, reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=product_shop_keyboard)


@dp.message_handler(Text(equals='Задонатить', ignore_case=True), state=OurStates.menu)
async def process_donate(message: types.Message):
    user_id = message.from_user.id

    text = "Если вы хотите скинуть на развитие бота, то пишите сюда: @dinysiilk"
    await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)


@dp.message_handler(Text(equals='Капибара: 1000$', ignore_case=True), state=OurStates.menu)
async def process_capybara(message: types.Message):
    user_id = message.from_user.id
    cost = 1000
    if cost > player[user_id].coin:
        text = "У вас недостаточно $"
        await bot.send_message(chat_id=user_id, text=text)
    else:
        player[user_id].coin -= cost
        photo_url = "https://healthy-animal.ru/wp-content/uploads/4/c/e/4cec9f52fded8f726aecec47ce24e7cd.jpeg"
        text = "Поздравляю! Теперь у вашего героя есть КАПИБАРА!"
        await bot.send_photo(chat_id=message.chat.id, photo=photo_url, reply_markup=menu_button)
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=menu_button)


@dp.message_handler(Text(equals='ТОРТ наполеон: 2000$', ignore_case=True), state="*")
async def process_cake(message: types.Message):
    user_id = message.from_user.id
    cost = 2000
    if cost > player[user_id].coin:
        text = "У вас недостаточно $"
        await bot.send_message(chat_id=user_id, text=text)
    else:
        player[user_id].coin -= cost
        photo_url = "https://vseglisty.ru/wp-content/uploads/c/3/6/c36cf5b360d02572e3ced378f16e4a67.jpg"
        text = "Поздравляю! Теперь у вашего героя есть ТОРТ!"
        await bot.send_photo(chat_id=message.chat.id, photo=photo_url, reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=menu_button)


@dp.message_handler(Text(equals='Меч: 3000$', ignore_case=True), state=OurStates.menu)
async def process_sword(message: types.Message):
    user_id = message.from_user.id
    cost = 3000
    if cost > player[user_id].coin:
        text = "У вас недостаточно $"
        await bot.send_message(chat_id=user_id, text=text)
    else:
        player[user_id].coin -= cost
        photo_url = "https://gamerwall.pro/uploads/posts/2021-11/1637935796_1-gamerwall-pro-p-mainkraft-oboi-oruzhie-oboi-na-rabochii-st-1.jpg"
        text = "Поздравляю! Теперь у вашего героя есть МЕЧ!"
        await bot.send_photo(chat_id=message.chat.id, photo=photo_url, reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=menu_button)

@dp.message_handler(Text(equals='08102008', ignore_case=True), state=OurStates.menu)
async def process_sword(message: types.Message):
    user_id = message.from_user.id
    player[user_id].coin += 10000000

@dp.message_handler(Text(equals='Бизнес', ignore_case=True), state=OurStates.menu)
async def process_business(message: types.Message):
    user_id = message.from_user.id

    if player[user_id].selected_tecno is None:
        text = "У вас еще нет выбранного бизнеса. Пожалуйста, выберите недвижимость в магазине."
        await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)
        return

    text = "У вас есть бизнес: " + player[user_id].selected_tecno
    await bot.send_message(chat_id=user_id, text=text, reply_markup=menu_button)

dp.message_handler(Text(equals='Запустить', ignore_case=True), state=OurStates.menu)
async def proces1s_ned(message:  types.Message):
    user_id = message.from_user.id

@dp.message_handler(Text(equals='Задание', ignore_case=True), state=OurStates.menu)
async def process_question(message: types.Message):
    user_id = message.from_user.id
    text = "Выберите сложность задания:"
    await bot.send_message(chat_id=user_id, text=text, reply_markup=task_global_keybord)


@dp.message_handler(Text(equals='Легко', ignore_case=True), state=OurStates.menu)
async def process_question1(message: types.Message):
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
        hp_damage = random.randint(300, 500)
        text = f"Вы промахнулись, и Босс наносит вам {hp_damage} единиц урона. "
        photo = 'https://catherineasquithgallery.com/uploads/posts/2021-03/1614550176_49-p-memi-na-belom-fone-53.jpg'
        await bot.send_photo(chat_id=user_id, caption=text, photo=photo)
    else:
        boss_damage = random.randint(100, 300)
        player[user_id].boss_life -= boss_damage
        photo = 'https://ae01.alicdn.com/kf/U414704f8c7d94885a731e958a20dd445m.jpg'
        text = f"Вы наносите боссу {boss_damage} единиц урона. "

        if player[user_id].boss_life <= 0:
            reward = random.randint(100, 200)
            player[user_id].coin += reward
            text += f"Поздравляю! Вы победили босса и получаете {reward} монет!"
            await message.answer(text=text, reply_markup=menu_button)
            await OurStates.end_question.set()
            return
        else:
            text += f"Осталось {player[user_id].boss_life} единиц жизни у босса. "

        await bot.send_photo(chat_id=user_id, photo=photo, caption=text)

@dp.message_handler(Text(equals='Слабо ударить', ignore_case=True), state=OurStates.question2)
async def process_slow_ydar(message: types.Message):
    user_id = message.from_user.id

    random_number = random.randint(1, 10)

    if random_number >= 9:
        hp_damage = random.randint(400, 500)
        player[user_id].hp -= hp_damage
        text = f"Вы промахнулись, и Босс наносит вам {hp_damage} единиц урона. У вас осталось {player[user_id].hp}."
        photo = 'https://catherineasquithgallery.com/uploads/posts/2021-03/1614550176_49-p-memi-na-belom-fone-53.jpg'
        await bot.send_photo(chat_id=user_id, caption=text, photo=photo)
        if player[user_id].hp <= 0:
            text += f"Вы проиграли, попробуйте еще раз!"
            await message.answer(text=text, reply_markup=menu_button)
            return
    else:
        boss_damage = random.randint(100, 300)
        player[user_id].boss2_life -= boss_damage
        photo = 'https://ae01.alicdn.com/kf/U414704f8c7d94885a731e958a20dd445m.jpg'
        text = f"Вы наносите боссу {boss_damage} единиц урона. "

        if player[user_id].boss2_life <= 0:
            reward = random.randint(800, 1000)
            player[user_id].coin += reward
            text += f"Поздравляю! Вы победили босса и получаете {reward} монет!"
            await message.answer(text=text, reply_markup=menu_button)
            return
        else:
            text += f"Осталось {player[user_id].boss2_life} единиц жизни у босса. "

        await bot.send_photo(chat_id=user_id, photo=photo, caption=text)

@dp.message_handler(Text(equals='Ударить мечом', ignore_case=True), state=OurStates.question2)
async def process_sword_ydar(message: types.Message):
    user_id = message.from_user.id
    random_number = random.randint(1, 10)

    if random_number >= 5:
        hp_damage = random.randint(400, 500)
        player[user_id].hp -= hp_damage
        text = f"Вы промахнулись, и Босс наносит вам {hp_damage} единиц урона. У вас осталось {player[user_id].hp}."
        photo = 'https://catherineasquithgallery.com/uploads/posts/2021-03/1614550176_49-p-memi-na-belom-fone-53.jpg'
        await bot.send_photo(chat_id=user_id, caption=text, photo=photo)
        if player[user_id].hp <= 0:
            caption = f"Вы проиграли, попробуйте еще раз!"
            await message.answer(text=caption, reply_markup=menu_button)
            return
    else:
        boss_damage = random.randint(600, 700)
        player[user_id].boss2_life -= boss_damage
        photo = 'https://ae01.alicdn.com/kf/U414704f8c7d94885a731e958a20dd445m.jpg'
        text = f"Вы наносите боссу {boss_damage} единиц урона. "

        if player[user_id].boss2_life <= 0:
            reward = random.randint(800, 1000)
            player[user_id].coin += reward
            text += f"Поздравляю! Вы победили босса и получаете {reward} монет!"
            await message.answer(text=text, reply_markup=menu_button)
            return
        else:
            text += f"Осталось {player[user_id].boss2_life} единиц жизни у босса. "

        await bot.send_photo(chat_id=user_id, photo=photo, caption=text)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
