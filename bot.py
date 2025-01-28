# MIT License
# 
# Copyright (c) 2024 S7 Airlines RBXL
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Token = 8042917833:AAHBX8lEdlsbmw9ma9PzQkw225nudBr5uug

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Установите уровень логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Замените токен на ваш
TELEGRAM_TOKEN = 'ваш_токен_бота'
OWNER_ID = 123456789  # Замените на ID владельца

# Инициализация переменной баланса
balance = 0

def start(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id == OWNER_ID:
        update.message.reply_text('Приветствую вас, создатель! Рад быть вашим помощником.')
    else:
        update.message.reply_text('Привет! Я бот для управления балансом. Используйте /balance для показа баланса, '
                                  'или /support, чтобы обратиться в службу поддержки.')

def balance_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Ваш баланс: {balance} рублей.')

def set_balance(update: Update, context: CallbackContext) -> None:
    global balance
    if update.message.from_user.id == OWNER_ID:
        if context.args:
            try:
                new_balance = int(context.args[0])
                balance = new_balance
                update.message.reply_text(f'Баланс успешно установлен на {balance} рублей.')
            except ValueError:
                update.message.reply_text('Пожалуйста, введите корректное число.')
        else:
            update.message.reply_text('Введите новое значение баланса, например: /set_balance 100')
    else:
        update.message.reply_text('У вас нет прав для изменения баланса.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Доступные команды:\n/start - запустить бота\n/balance - показать баланс\n/set_balance [номер] - установить баланс\n/help - помощь')

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    
    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher
    
    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("balance", balance_command))
    dispatcher.add_handler(CommandHandler("set_balance", set_balance))
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    # Запуск бота
    updater.start_polling()
    
    # Запуск бота до его отключения
    updater.idle()

if __name__ == '__main__':
    main()
    
