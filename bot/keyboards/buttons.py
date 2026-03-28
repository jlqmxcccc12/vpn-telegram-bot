from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Get VPN")],
            [KeyboardButton(text="💳 Buy"), KeyboardButton(text="👤 Profile")],
            [KeyboardButton(text="📱 Instructions")]
        ],
        resize_keyboard=True
    )

def subscription_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📅 Weekly (50⭐)", callback_data="sub_weekly")],
            [InlineKeyboardButton(text="📆 Monthly (150⭐)", callback_data="sub_monthly")],
            [InlineKeyboardButton(text="Back", callback_data="back")]
        ]
    )

def device_menu(max_devices: int, current_devices: int) -> InlineKeyboardMarkup:
    kb = []
    if current_devices < max_devices:
        kb.append([InlineKeyboardButton(text="➕ Add Device", callback_data="add_device")])
    kb.extend([
        [InlineKeyboardButton(text="📋 My Devices", callback_data="list_devices")],
        [InlineKeyboardButton(text="Back", callback_data="back")]
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)