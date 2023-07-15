__all__ = ["OurStates"]

from aiogram.dispatcher.filters.state import State, StatesGroup


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
