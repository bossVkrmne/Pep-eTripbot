from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog import DialogManager

from typing import Dict, Callable

I18N_FORMAT_KEY = "i18n_context"


class I18nFormat(Text):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when)
        self.text = text

    async def _render_text(self, data: Dict, manager: DialogManager) -> str:
        i18n: Callable = manager.middleware_data[I18N_FORMAT_KEY]
        return i18n(self.text, **data).format_map(data)


class I18nConst(Text):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when=when)
        self.text = text

    async def _render_text(self, data: Dict, manager: DialogManager) -> str:
        i18n: Callable = manager.middleware_data[I18N_FORMAT_KEY]
        return i18n(self.text)
