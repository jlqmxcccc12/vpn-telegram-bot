from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from services.api_client import BackendClient
from keyboards.buttons import main_menu
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = Router()
client = BackendClient()

@router.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        user = await client.create_user(user_id, username)
        await message.answer(f"👋 Welcome to VPN Bot!\n\nYou've been given 7 days of FREE trial access. Enjoy!", reply_markup=main_menu())
        logger.info(f"User {user_id} started bot")
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await message.answer("An error occurred. Please try again.")

@router.message(F.text == "🚀 Get VPN")
async def get_vpn_handler(message: Message):
    user_id = message.from_user.id
    try:
        user = await client.get_user_by_telegram(user_id)
        sub = await client.get_active_subscription(user['id'])
        if sub:
            await message.answer("✅ You have an active subscription. Your VPN config is ready.")
        else:
            await message.answer("❌ No active subscription. Buy one to get VPN access.")
    except Exception as e:
        logger.error(f"Error in get_vpn_handler: {e}")
        await message.answer("An error occurred.")

@router.message(F.text == "💳 Buy")
async def buy_handler(message: Message):
    await message.answer("💳 Choose subscription:\n\n📅 Weekly: 50⭐\n📆 Monthly: 150⭐")

@router.message(F.text == "👤 Profile")
async def profile_handler(message: Message):
    user_id = message.from_user.id
    try:
        user = await client.get_user_by_telegram(user_id)
        sub = await client.get_active_subscription(user['id'])
        sub_text = f"Active until {sub['end_date']}" if sub else "No active subscription"
        await message.answer(f"👤 Profile\n\nUser ID: {user['id']}\nTelegram ID: {user['telegram_id']}\nUsername: {user['username']}\n\n📊 Subscription: {sub_text}")
    except Exception as e:
        logger.error(f"Error in profile_handler: {e}")
        await message.answer("An error occurred.")

@router.message(F.text == "📱 Instructions")
async def instructions_handler(message: Message):
    instructions = """📱 How to use WireGuard VPN:\n\n1. Download WireGuard app from App Store or Google Play\n2. Use the QR code or .conf file provided\n3. Connect to VPN\n4. Enjoy anonymous browsing!"""
    await message.answer(instructions)