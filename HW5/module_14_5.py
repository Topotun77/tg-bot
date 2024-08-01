# Домашнее задание по теме "Написание примитивной ORM"
# Цель: написать простейшие CRUD функции для взаимодействия с базой данных.
#
# Задача "Регистрация покупателей":
# Подготовка:
# Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя
# пунктам задачи ниже.
#
# Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
# initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса.
# Эта таблица должна содержать следующие поля:
# 1. id - целое число, первичный ключ
# 2. username - текст (не пустой)
# 3. email - текст (не пустой)
# 4. age - целое число (не пустой)
# 5. balance - целое число (не пустой)
# add_user(username, email, age), которая принимает: имя пользователя, почту и возраст.
# Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными.
# Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте
# SQL запрос.
# is_included(username) принимает имя пользователя и возвращает True, если такой пользователь
# есть в таблице Users, в противном случае False. Для получения записей используйте SQL запрос.

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import logging
import time
from collections import defaultdict
from pprint import pprint
from crud_functions import *
from kandinsky import *

API = 'XXX'

bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ],
        [
            KeyboardButton(text='Регистрация'),
            KeyboardButton(text='Купить')
        ]
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
    """
    Декоратор для ведений логирования при отправке сообщений пользователю
    :param func: Функция, которую будем логировать
    :param message: Сообщение от пользователя, тип: types.Message или types.CallbackQuery
    :param txt: Текст для логирования
    :return: полученную обернутую функцию
    """
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

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

class UserData():
    DATA = defaultdict(dict, {})


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    txt = ('🌿 Привет! Я бот помогающий твоему здоровью. Хотите узнать сколько калорий '
           'Вам нужно потреблять в день для здорового питания? Нажмите на кнопку "Рассчитать".'
           '\n\nА еще, <b>в качестве развлечения</b>, Вы можете отправить запрос <b>Кандинскому 3.0</b> '
           'просто набрав его текст здесь и сейчас. '
           'Ответ возможно придется подождать около минуты 😎\n\n'
           'Например, можно отправить мне такой текст: <pre>бот помогающий твоему здоровью</pre>'
           'И я покажу Вам свой портрет.\n\n'
           f'Или, например, вот такой:<pre>За окном лето, прекрасная погода, а я - программист '
           f'{message.from_user.first_name} - сижу и проверяю домашние задания студентов</pre>'
           )
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, reply_markup=kb, parse_mode='HTML')


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    print(f'Сообщение от {message.from_user.first_name}')
    txt = 'Выберите опцию:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, reply_markup=inline_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    txt = ('🧮 Упрощенный вариант формулы Миффлина-Сан Жеора:\n\n'
           '<b><i>для мужчин:</i>\n🙎‍♂️‍ 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5</b>\n\n'
           '<b><i>для женщин:</i>\n🙍‍♀️ 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161</b>\n\n'
           'Формула расчета индекса массы тела (ИМТ):\n\n'
           '<b>✅ ИМТ = вес (кг) / рост (м) ^ 2</b>')
    call.answer = decor_log(call.answer, call, txt)
    await call.message.answer(txt, parse_mode='HTML')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_gender(call: types.CallbackQuery):
    if call.from_user.first_name not in UserData.DATA:
        UserData.DATA[call.from_user.first_name] = {}
    txt = '✍️ Введите свой пол (М/Ж):'
    call.answer = decor_log(call.answer, call, txt)
    await call.message.answer(txt)
    await UserState.gender.set()
    await call.answer()


@dp.message_handler(state=UserState.gender)
async def set_age(message: types.Message, state):
    await state.update_data(gender=message.text)
    txt = '✍️ Введите свой возраст:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state):
    await state.update_data(age=message.text.replace(',', '.'))
    txt = '✍️ Введите свой рост:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state):
    await state.update_data(growth=message.text.replace(',', '.'))
    txt = '✍️ Введите свой вес:'
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
        txt = (f'<b>Ваша норма калорий по формуле Миффлина-Сан Жеора: <u>{calories}</u> Ккал</b>\n\n'
               f'<b>Индекс массы тела (ИМТ): <u>{imb}</u> кг/кв.м</b>\n\n'
               f'В соответствии с рекомендациями ВОЗ разработана следующая интерпретация показателей ИМТ:\n\n'
               f'💙<b>16 и менее</b> — Выраженный дефицит массы тела\n\n'
               f'🩵 <b>16 - 18,5</b> — Недостаточная (дефицит) масса тела\n\n'
               f'💚 <b>18,5 - 25</b> — Норма\n\n'
               f'💛 <b>25 - 30</b> — Избыточная масса тела (предожирение)\n\n'
               f'🧡 <b>30 - 35</b> — Ожирение 1 степени\n\n'
               f'❤️ <b>35 - 40</b> — Ожирение 2 степени\n\n'
               f'🩷 <b>40 и более</b> — Ожирение 3 степени')
        if imb > 25:
            txt += ('\n\n\t<b>‼️‼️‼️ Возможно, вас заинтересуют наши товары. Нажмите, пожалуйста, кнопку '
                    '"Купить" в основном меню. С пожеланием приятных покупок, команда Магазина здоровья!</b>')
        set_user_info(message.from_user.first_name, data['gender'], data['age'], data['growth'], data['weight'])
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, reply_markup=kb, parse_mode='HTML')
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    products = get_all_products()
    # Инлайн клавиатура для товаров формируется с использованием списковых сборок из базы products
    inline_buy = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=products[i + j * 3][1], callback_data='product_buying') for i in range(3)
             if (i + j * 3) < len(products)
             ] for j in range((len(products) - 1) // 3 + 1)
        ]
    )
    for product in products:
        txt = f'🚀 <i>{product[1]}</i> \nОписание: <b>{product[2]}</b> \nЦена: {product[3]} ₽'
        try:
            with open(product[4], mode='rb') as img:
                message_answer_log = decor_log(message.answer_photo, message, txt)
                await message_answer_log(img, txt, parse_mode='HTML')
        except Exception as err:
            print(err, err.args)
            message_answer_log = decor_log(message.answer, message, txt)
            await message_answer_log(txt)
    txt = 'Выберите продукт для покупки:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, reply_markup=inline_buy)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    txt = '<b>Вы успешно приобрели продукт!</b>'
    call.answer = decor_log(call.answer, call, txt)
    await call.message.answer(txt, parse_mode='HTML')
    await call.answer()
    if 'buy' not in UserData.DATA[call.from_user.first_name]:
        UserData.DATA[call.from_user.first_name]['buy'] = {}
    UserData.DATA[call.from_user.first_name]['buy'][time.ctime()] = 'Приобретен продукт'
    pprint(UserData.DATA)


@dp.message_handler(text='Информация')
async def info(message: types.Message):
    txt = '🌿 Я - невероятно крутой бот, который знает секрет как похудеть!'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)


@dp.message_handler(text='Регистрация')
async def sing_up(message: types.Message):
    txt = ('✍️ Введите имя пользователя (только латинский алфавит, <b>для прерывания ввода наберите '
           '/cancel в любой момент</b>):')
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, parse_mode='HTML')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state):
    if message.text == '/cancel':
        txt = '<b>Добавление пользователя прервано.</b>'
        message.answer = decor_log(message.answer, message, txt)
        await message.answer(txt, reply_markup=kb, parse_mode='HTML')
        await state.finish()
    elif not is_included(message.text):
        await state.update_data(username=message.text)
        txt = '✍️ Введите свой email:'
        message.answer = decor_log(message.answer, message, txt)
        await message.answer(txt)
        await RegistrationState.email.set()
    else:
        txt = 'Такой пользователь существует, введите другое имя:'
        message.answer = decor_log(message.answer, message, txt)
        await message.answer(txt)
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state):
    if message.text == '/cancel':
        txt = '<b>Добавление пользователя прервано.</b>'
        message.answer = decor_log(message.answer, message, txt)
        await message.answer(txt, reply_markup=kb, parse_mode='HTML')
        await state.finish()
    else:
        await state.update_data(email=message.text)
        txt = '✍️ Введите свой возраст:'
        message.answer = decor_log(message.answer, message, txt)
        await message.answer(txt)
        await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state):
    if message.text == '/cancel':
        txt = '<b>Добавление пользователя прервано.</b>'
        message.answer = decor_log(message.answer, message, txt)
        await message.answer(txt, reply_markup=kb, parse_mode='HTML')
        await state.finish()
    else:
        await state.update_data(age=message.text)
        data = await state.get_data()
        try:
            add_user(data['username'], data['email'], data['age'])
            txt = '🎉 Пользователь успешно добавлен.'
            message.answer = decor_log(message.answer, message, txt)
            await message.answer(txt, reply_markup=kb)
            await state.finish()
        except DataError as err:
            txt = err.args[0] + '✍️ Введите другое имя или наберите /stop:'
            message.answer = decor_log(message.answer, message, txt)
            await message.answer(txt)
            await RegistrationState.username.set()


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def save_photo(message: types.Message, state):
    print('Получено фото')
    await message.photo[-1].download(destination_file='image/photo.jpg')
    txt = '🌈 Вы отправили вот это фото. Зачем оно мне? 🤔'
    try:
        with open('image/photo.jpg', mode='rb') as img:
            message_answer_log = decor_log(message.answer_photo, message, txt)
            await message_answer_log(img, txt, parse_mode='HTML')
    except Exception as err:
        print(err, err.args)
        message_answer_log = decor_log(message.answer, message, txt)
        await message_answer_log(txt)


@dp.message_handler()
async def all_massages(message: types.Message):
    # dir_ = f'./image/' + message.text.replace("\n", "_").split(".")[0]
    dir_ = f'./image/kandinski'
    try:
        os.mkdir(os.getcwd().replace("\\", "/") + dir_)
    except FileExistsError:
        print('exist')

    try:
        file_name = await gen(message.text.replace("\n", " "), dir_)
        print(f'сделано {file_name}')
        txt = f'По вашему запросу: \n<pre><b>{message.text}</b></pre>\nсгенерирована эта картинка ☝️'
        with open(file_name, mode='rb') as img:
            message_answer_log = decor_log(message.answer_photo, message, txt)
            await message_answer_log(img, txt, parse_mode='HTML')
    except Exception as err:
        raise
        # print(err, err.args)
        # message_answer_log = decor_log(message.answer, message, str(err.args))
        # await message_answer_log(str(err.args))

    txt = 'Введите команду /start, чтобы начать общение.'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
