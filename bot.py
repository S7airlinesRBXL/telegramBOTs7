from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

# Включаем ведение логов
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Список ID администратора
ADMIN_IDS = {5764625744}  # Замените это на свои реальные ID администраторов
SUPPORT_CHAT_ID = -2396512980  # Замените на ID вашей группы поддержки

def start(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение пользователю."""
    user_id = update.message.from_user.id
    if user_id in ADMIN_IDS:
        greeting = admin_greet(user_id)
    else:
        greeting = 'Привет! Я бот, который помогает управлять балансом и поддержкой. Если у вас есть вопросы, вы можете обратиться в нашу группу поддержки!'
    
    update.message.reply_text(greeting)

def admin_greet(user_id: int) -> str:
    """Приветственное сообщение для администратора."""
    return (f'👋 Привет, администратор! Вы успешно вошли в систему управления ботом.\n\n' 
            f'💼 Вот некоторые команды, которые вы можете использовать:\n' 
            f'/set_balance <user_id> <баланс> - Установить баланс пользователя.\n' 
            f'/get_balance <user_id> - Узнать баланс пользователя.\n' 
            f'/support - Обратиться в группу поддержки.\n')

def set_balance(update: Update, context: CallbackContext) -> None:
    """Устанавливает баланс пользователя."""
    if not update.message.from_user.id in ADMIN_IDS:
        update.message.reply_text('У вас нет прав для выполнения этой команды!')
        return
        
    if len(context.args) != 2:
        update.message.reply_text('Использование: /set_balance <user_id> <баланс>')
        return

    user_id, balance = context.args
    # Здесь вы можете добавить код для обновления баланса пользователя в базе данных
    update.message.reply_text(f'Баланс пользователя {user_id} установлен на {balance}.')

def get_balance(update: Update, context: CallbackContext) -> None:
    """Получает баланс пользователя."""
    if not update.message.from_user.id in ADMIN_IDS:
        update.message.reply_text('У вас нет прав для выполнения этой команды!')
        return
    
    if not context.args:
        update.message.reply_text('Использование: /get_balance <user_id>')
        return
    
    user_id = context.args[0]
    # Здесь вы можете добавить код для получения баланса пользователя из базы данных
    balance = 100  # Заглушка, замените на фактическое значение
    update.message.reply_text(f'Баланс пользователя {user_id}: {balance}.')

def support(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение в группу поддержки."""
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        update.message.reply_text('Вы можете обратиться в поддержку, написав сообщение в группу поддержки.')
        return

    update.message.reply_text('Отправляю ваш вопрос в группу поддержки...')
    message_text = " ".join(context.args) if context.args else "Пользователь не указал вопрос."
    context.bot.send_message(chat_id=SUPPORT_CHAT_ID, text=f'Запрос от администратора: {message_text}')
    update.message.reply_text('Ваш запрос был отправлен в группу поддержки.')

def main() -> None:
    """Запуск бота."""
    updater = Updater("8042917833:AAHBX8lEdlsbmw9ma9PzQkw225nudBr5uug")  # Замените YOUR_API_TOKEN на ваш токен
    dispatcher = updater.dispatcher

    # Добавляем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("set_balance", set_balance))
    dispatcher.add_handler(CommandHandler("get_balance", get_balance))
    dispatcher.add_handler(CommandHandler("support", support))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
