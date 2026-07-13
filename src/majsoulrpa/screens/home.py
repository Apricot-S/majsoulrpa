import asyncio
from logging import getLogger
from typing import override

from majsoulrpa.assets.templates.home import (
    EVENT_CLOSE_SETTINGS_PATH,
    EVENT_CLOSE_TEMPLATE_PATH,
    FRIENDLY_MATCH_SETTINGS_PATH,
    FRIENDLY_MATCH_TEMPLATE_PATH,
    JADE_SETTINGS_PATH,
    JADE_TEMPLATE_PATH,
    MAIL_CLOSE_SETTINGS_PATH,
    MAIL_CLOSE_TEMPLATE_PATH,
    NOTIFICATION_CLOSE_SETTINGS_PATH,
    NOTIFICATION_CLOSE_TEMPLATE_PATH,
    REWARDS_CONFIRM_SETTINGS_PATH,
    REWARDS_CONFIRM_TEMPLATE_PATH,
    REWARDS_SIGN_IN_SETTINGS_PATH,
    REWARDS_SIGN_IN_TEMPLATE_PATH,
    SUMMON_SETTINGS_PATH,
    SUMMON_TEMPLATE_PATH,
    TOURNAMENT_MATCH_SETTINGS_PATH,
    TOURNAMENT_MATCH_TEMPLATE_PATH,
)
from majsoulrpa.presentation.template import load_png_template_matcher
from majsoulrpa.screens.base import (
    Screen,
    ScreenDetectionSpec,
    _format_sniffer_message,
)
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenUnexpectedStateError,
)

MONTH_TICKET_API_NAME = ".lq.Lobby.payMonthTicket"
JADE_WAIT_TIMEOUT_SECONDS = 5.0

_logger = getLogger(__name__)


class HomeScreen(Screen):
    SUMMON_TEMPLATE = load_png_template_matcher(
        template_path=SUMMON_TEMPLATE_PATH,
        settings_path=SUMMON_SETTINGS_PATH,
    )
    JADE_TEMPLATE = load_png_template_matcher(
        template_path=JADE_TEMPLATE_PATH,
        settings_path=JADE_SETTINGS_PATH,
    )
    NOTIFICATION_CLOSE_TEMPLATE = load_png_template_matcher(
        template_path=NOTIFICATION_CLOSE_TEMPLATE_PATH,
        settings_path=NOTIFICATION_CLOSE_SETTINGS_PATH,
    )
    EVENT_CLOSE_TEMPLATE = load_png_template_matcher(
        template_path=EVENT_CLOSE_TEMPLATE_PATH,
        settings_path=EVENT_CLOSE_SETTINGS_PATH,
    )
    MAIL_CLOSE_TEMPLATE = load_png_template_matcher(
        template_path=MAIL_CLOSE_TEMPLATE_PATH,
        settings_path=MAIL_CLOSE_SETTINGS_PATH,
    )
    REWARDS_SIGN_IN_TEMPLATE = load_png_template_matcher(
        template_path=REWARDS_SIGN_IN_TEMPLATE_PATH,
        settings_path=REWARDS_SIGN_IN_SETTINGS_PATH,
    )
    REWARDS_CONFIRM_TEMPLATE = load_png_template_matcher(
        template_path=REWARDS_CONFIRM_TEMPLATE_PATH,
        settings_path=REWARDS_CONFIRM_SETTINGS_PATH,
    )
    TOURNAMENT_MATCH_TEMPLATE = load_png_template_matcher(
        template_path=TOURNAMENT_MATCH_TEMPLATE_PATH,
        settings_path=TOURNAMENT_MATCH_SETTINGS_PATH,
    )
    FRIENDLY_MATCH_TEMPLATE = load_png_template_matcher(
        template_path=FRIENDLY_MATCH_TEMPLATE_PATH,
        settings_path=FRIENDLY_MATCH_SETTINGS_PATH,
    )

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(predicate=cls.SUMMON_TEMPLATE.matches)

    @override
    async def before_callback(self) -> None:
        await self._process_month_ticket()

        # Wait for Home screen controls and announcements to finish
        # their entrance animations before taking the first screenshot.
        await asyncio.sleep(1.0)

        close_templates = {
            "notification-close": self.NOTIFICATION_CLOSE_TEMPLATE,
            "event-close": self.EVENT_CLOSE_TEMPLATE,
            "mail-close": self.MAIL_CLOSE_TEMPLATE,
        }
        processed_templates: set[str] = set()
        rewards_processed = False
        while True:
            screenshot = await self.context.browser.screenshot()
            for name, template in close_templates.items():
                result = template.find(screenshot)
                if result is None:
                    continue

                if name in processed_templates:
                    msg = f"{name} was detected more than once."
                    raise ScreenUnexpectedStateError(msg, screenshot)

                await self._click_region(result.region)
                processed_templates.add(name)
                await asyncio.sleep(1.0)
                break
            else:
                sign_in_result = self.REWARDS_SIGN_IN_TEMPLATE.find(
                    screenshot,
                )
                if sign_in_result is None:
                    # All announcements have been closed at this point.
                    self._require_match_buttons(screenshot)
                    self._discard_sniffer_messages()
                    return

                if rewards_processed:
                    msg = "rewards-sign-in was detected more than once."
                    raise ScreenUnexpectedStateError(msg, screenshot)

                await self._click_region(sign_in_result.region)
                await asyncio.sleep(2.0)
                await self.click_template(
                    self.REWARDS_CONFIRM_TEMPLATE,
                    message="rewards-confirm was not found after sign-in.",
                )
                await asyncio.sleep(0.5)
                rewards_processed = True

    async def _process_month_ticket(self) -> None:
        has_month_ticket = False
        messages = []
        try:
            while True:
                message = self._get_sniffer_message_nowait()
                if message is None:
                    break
                messages.append(message)
                if message.raw.name == MONTH_TICKET_API_NAME:
                    has_month_ticket = True
                    break
        finally:
            for message in messages:
                self._put_back_sniffer_message(message)

        if not has_month_ticket:
            return

        try:
            async with asyncio.timeout(JADE_WAIT_TIMEOUT_SECONDS):
                await self.wait_and_click_template(self.JADE_TEMPLATE)
        except TimeoutError as error:
            screenshot = await self.context.browser.screenshot()
            msg = "jade was not found within 5 seconds."
            raise ScreenDetectionError(msg, screenshot) from error

        await asyncio.sleep(0.5)

    def _discard_sniffer_messages(self) -> None:
        while (message := self._get_sniffer_message_nowait()) is not None:
            _logger.info(
                "Sniffer message: %s",
                _format_sniffer_message(message),
            )

    def _require_match_buttons(self, screenshot: bytes) -> None:
        match_templates = {
            "tournament-match": self.TOURNAMENT_MATCH_TEMPLATE,
            "friendly-match": self.FRIENDLY_MATCH_TEMPLATE,
        }
        for name, template in match_templates.items():
            if template.find(screenshot) is None:
                msg = f"{name} was not found after closing announcements."
                raise ScreenDetectionError(msg, screenshot)
