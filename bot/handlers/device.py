from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from services.api_client import BackendClient
from keyboards.buttons import main_menu
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = Router()
client = BackendClient()

@router.callback_query(F.data == "add_device")
async def add_device_callback(query: CallbackQuery):
    await query.message.answer("Enter device name:")
    await query.answer()

@router.message()
async def device_name_handler(message: Message):
    if hasattr(device_name_handler, 'expecting_device_name') and device_name_handler.expecting_device_name:
        try:
            user = await client.get_user_by_telegram(message.from_user.id)
            device = await client.create_device(user['id'], message.text)
            await message.answer(f"✅ Device '{device['name']}' created!")
            device_name_handler.expecting_device_name = False
        except Exception as e:
            logger.error(f"Error creating device: {e}")
            await message.answer("Error creating device")

@router.callback_query(F.data == "list_devices")
async def list_devices_callback(query: CallbackQuery):
    await query.message.answer("Your devices list feature coming soon...")
    await query.answer()