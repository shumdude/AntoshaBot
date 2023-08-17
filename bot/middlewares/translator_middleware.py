from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from fluentogram import TranslatorHub


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        hub: TranslatorHub = data.get('_translator_hub')
        # There you can ask your database for locale
        data['i18n'] = hub.get_translator_by_locale(event.from_user.language_code)
        return await handler(event, data)
