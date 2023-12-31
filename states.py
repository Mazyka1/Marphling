__all__ = ["OurStates"]

from aiogram.dispatcher.filters.state import State, StatesGroup

from constants import map_list


class OurStates(StatesGroup):
    enter_name = State()
    ready = State()
    chosen_person = State()
    start_game = State()
    question = State()
    end_question = State()
    chosen_tecno = State()
    menu = State()
    question2 = State()
    reward = State()
    menu2 = State()
    buy_burger = State()
