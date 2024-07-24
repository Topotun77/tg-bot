# Домашнее задание по теме "Доработка бота"
# Цель: подготовить Telegram-бота для взаимодействия с базой данных.
#
# Задача "Витамины для всех!":
# Подготовка:
# Подготовьте Telegram-бота из последнего домашнего задания 13 моудля сохранив код с
# ним в файл module_14_3.py.
# Если вы не решали новые задания из предыдущего модуля рекомендуется выполнить их.
#
# Дополните ранее написанный код для Telegram-бота:
# Создайте и дополните клавиатуры:
# 1. В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
# 2. Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3",
# "Product4". У всех кнопок назначьте callback_data="product_buying"
#
# Создайте хэндлеры и функции к ним:
# 1. Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию
# get_buying_list(message).
# 2. Функция get_buying_list должна выводить надписи
# 'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>'
# 4 раза. После каждой надписи выводите картинки к продуктам. В конце выведите ранее
# созданное Inline меню с надписью "Выберите продукт для покупки:".
# 3. Callback хэндлер, который реагирует на текст "product_buying" и оборачивает
# функцию send_confirm_message(call).
# 4. Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import logging
import time
from collections import defaultdict
from pprint import pprint

API = 'XXX'
PRODUCTS = [
    ['Лот #001', 'Очень бюджетный вариант', 199, 'image/006.JPG'],
    ['Лот #002', 'Разновидность бюджетного варианта', 299, 'image/003.JPG'],
    ['Лот #003', 'Инструкция для самостоятельной реализации на базе экранов Nextion', 2_999, 'image/009.JPG'],
    ['Лот #004', 'Высокоинтеллектуальное решение на базе ИИ', 29_999, 'image/007.JPG'],
    ['Лот #005', 'Высокоинтеллектуальное решение на базе ИИ с дактилоскопическим анализом состояния здоровья',
     69_999, 'image/008.JPG'],
    ['Лот #006', 'Самое эффективное решение по невероятно низкой цене', 9, 'image/010.JPG']
]
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ],
        [KeyboardButton(text='Купить')]
    ]
)

# Инлайн клавиатура для товаров формируется с использованием списковых сборок из базы PRODUCTS
inline_buy = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=PRODUCTS[i + j * 3][0], callback_data='product_buying') for i in range(3)
         if (i + j * 3) < len(PRODUCTS)
         ] for j in range((len(PRODUCTS) - 1) // 3 + 1)
    ]
)

inline_kb = InlineKeyboardMarkup()
inline_butt1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_butt2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.row(inline_butt1, inline_butt2)

logging.basicConfig(
    filename='tg-bot.log', filemode='a', encoding='utf-8',
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    level=logging.INFO)


def decor_log(func, message, txt):
    async def log_writer(*args, **kwargs):
        try:
            logging.info(f'Получено сообщение от {message.from_user.first_name}: {message["text"]}')
        except KeyError:
            logging.info(f'Получено сообщение от {message.from_user.first_name}: Нажата кнопка - {message["data"]}')
        logging.info(f'Вся информация: {message}')
        rez = await func(*args, **kwargs)
        logging.info(f'Отправлен ответ: {txt}')
        return rez

    return log_writer


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()


class UserData():
    DATA = defaultdict(dict, {})


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    txt = ('Привет! Я бот помогающий твоему здоровью. Хотите узнать сколько калорий '
           'Вам нужно потреблять в день для здорового питания? Нажмите на кнопку "Рассчитать".')
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    print(f'Сообщение от {message.from_user.first_name}')
    txt = 'Выберите опцию:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, reply_markup=inline_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    txt = ('Упрощенный вариант формулы Миффлина-Сан Жеора:\n\n'
           'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
           'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161\n\n'
           'Формула расчета индекса массы тела (ИМТ):\n\n'
           'ИМТ = вес (кг) / рост (м) ^ 2')
    call.answer = decor_log(call.answer, call, txt)
    await call.message.answer(txt)
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_gender(call: types.CallbackQuery):
    if call.from_user.first_name not in UserData.DATA:
        UserData.DATA[call.from_user.first_name] = {}
    txt = 'Введите свой пол (М/Ж):'
    call.answer = decor_log(call.answer, call, txt)
    await call.message.answer(txt)
    await UserState.gender.set()
    await call.answer()


@dp.message_handler(state=UserState.gender)
async def set_age(message: types.Message, state):
    await state.update_data(gender=message.text)
    txt = 'Введите свой возраст:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state):
    await state.update_data(age=message.text.replace(',', '.'))
    txt = 'Введите свой рост:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state):
    await state.update_data(growth=message.text.replace(',', '.'))
    txt = 'Введите свой вес:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state):
    await state.update_data(weight=message.text.replace(',', '.'))
    UserData.DATA[message.from_user.first_name] |= await state.get_data()
    # locals().update(UserData.DATA[message["from"]["first_name"]])
    pprint(UserData.DATA)

    data = UserData.DATA[message["from"]["first_name"]]

    try:
        if data['gender'].upper() == 'Ж':
            calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
        elif data['gender'].upper() == 'М':
            calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
        else:
            raise ValueError
        imb = round(float(data['weight']) / (float(data['growth']) / 100) ** 2, 1)
    except ValueError or ZeroDivisionError:
        txt = 'Вы ввели ошибочные данные'
    else:
        txt = (f'Ваша норма калорий по формуле Миффлина-Сан Жеора: {calories} калорий\n\n'
               f'Индекс массы тела (ИМТ): {imb} кг/кв.м\n\n'
               f'В соответствии с рекомендациями ВОЗ разработана следующая интерпретация показателей ИМТ:\n\n'
               f'16 и менее — Выраженный дефицит массы тела\n\n'
               f'16 - 18,5 — Недостаточная (дефицит) масса тела\n\n'
               f'18,5 - 25 — Норма\n\n'
               f'25 - 30 — Избыточная масса тела (предожирение)\n\n'
               f'30 - 35 — Ожирение 1 степени\n\n'
               f'35 - 40 — Ожирение 2 степени\n\n'
               f'40 и более — Ожирение 3 степени')
        if imb > 25:
            txt += ('\n\n\tВозможно, вас заинтересуют наши товары. Нажмите, пожалуйста, кнопку '
                    '"Купить" в основном меню. С пожеланием приятных покупок, команда Магазина здоровья!')
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    for product in PRODUCTS:
        txt = f'{product[0]} | Описание: {product[1]} | Цена: {product[2]} руб.'
        try:
            with open(product[3], mode='rb') as img:
                message_answer_log = decor_log(message.answer_photo, message, txt)
                await message_answer_log(img, txt)
        except Exception as err:
            print(err, err.args)
            message_answer_log = decor_log(message.answer, message, txt)
            await message_answer_log(txt)
    txt = 'Выберите продукт для покупки:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, reply_markup=inline_buy)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    txt = 'Вы успешно приобрели продукт!'
    call.answer = decor_log(call.answer, call, txt)
    await call.message.answer(txt)
    await call.answer()
    if 'buy' not in UserData.DATA[call.from_user.first_name]:
        UserData.DATA[call.from_user.first_name]['buy'] = {}
    UserData.DATA[call.from_user.first_name]['buy'][time.ctime()] = 'Приобретен продукт'
    pprint(UserData.DATA)


@dp.message_handler(text='Информация')
async def info(message: types.Message):
    txt = 'Я - невероятно крутой бот, который знает секрет как похудеть!'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)


@dp.message_handler()
async def all_massages(message: types.Message):
    txt = 'Введите команду /start, чтобы начать общение.'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
