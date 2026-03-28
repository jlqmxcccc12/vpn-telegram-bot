from aiogram import Dispatcher, Router
from handlers.start import router as start_router
from handlers.payment import router as payment_router
from handlers.device import router as device_router

def setup_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(payment_router)
    dp.include_router(device_router)