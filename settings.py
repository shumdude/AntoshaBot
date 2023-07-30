LEXICON: dict[str, str] = {'cancel': 'Отменить',
                           '/start': 'Привет! Меня зовут Антон Павлович Чехов, но для своих - просто Антоша Чехонте.'
                                     '\n\nИспользуйте команду /commands для ознакомления с моими функциями.',
                           '/commands': 'Список команд:\n\n'
                                        '/catalog - просмотр каталога товаров\n\n'
                                        '/fsm - напоминание для сотрудника\n\n'
                                        '/booking - бронирование мест (в процессе разработки)\n\n',
                           'no_echo': 'TypeError with message.send_copy',
                           '/insert': 'Готово! Вставил данные в БД',
                           '/get': 'Лови',
                           'right': '>>>',
                           'left': '<<<',
                           'back': 'Вернуться назад',
                           '/load': 'Данные json загружены в БД успешно',
                           '/fsm': 'С помощью данной команды вы можете отправлять сотрудникам напоминания о задаче.\n'
                                   'Вводите данные в соответствии требованиям\n\n'
                                   '!!!Важно: tel_id - прямой ID пользователя (не ссылка и не имя)\n'
                                   'Чтобы узнать ваш ID, воспользуйтесь @getmyid_bot\n'
                                   'Кроме того, бот не может отправить сообщение пользователю, '
                                   'у которого нет переписки с ним\n\n'
                                   'В вашем распоряжении несколько полей для ввода формы: тест (задание), '
                                   'дата (срок выполения задания), время (до какого времени) и поле answer_time '
                                   '(время в секундах для ответа сотрудником на ваше напоминание)\n\n'
                                   'Для прекращения заполения формы вопользуйтесь /cancel\n\n'
                                   'P.S.: Данная задача реализована так, как требовал того заказчик',
                           '/booking': 'Бронирование'}


def get_product_caption(product: tuple) -> str:
    name: str = product[0]
    price: str = str(product[1])
    site: str = product[2]
    product_caption: str = f"Название: {name}\n\nЦена: {price}\n\nСайт: {site}"
    return product_caption


# сделать телеграм фото и хранить в БД в отдельной служебной таблице
NO_PHOTO = "https://topzero.com/wp-content/uploads/2020/06/topzero-products-Malmo-Matte-Black-TZ-PE458M-image-003.jpg"
