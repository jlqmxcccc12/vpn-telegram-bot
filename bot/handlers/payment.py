from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, LabeledPrice, ShippingOption
from services.api_client import BackendClient
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = Router()
client = BackendClient()

PRICES = {"weekly": 50, "monthly": 150}

@router.callback_query(F.data == "sub_weekly")
async def weekly_callback(query: CallbackQuery):
    await start_payment_flow(query, "weekly", 50)

@router.callback_query(F.data == "sub_monthly")
async def monthly_callback(query: CallbackQuery):
    await start_payment_flow(query, "monthly", 150)

async def start_payment_flow(query: CallbackQuery, sub_type: str, price: int):
    try:
        await query.bot.send_invoice(
            chat_id=query.from_user.id,
            title=f"{sub_type.capitalize()} Subscription",
            description=f"Get {sub_type} VPN access",
            payload=f"vpn_{sub_type}_{query.from_user.id}",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice(label=f"{sub_type.capitalize()} Plan", amount=price)]
        )
    except Exception as e:
        logger.error(f"Payment error: {e}")
        await query.answer("Error processing payment")

@router.pre_checkout_query()
async def pre_checkout(query: types.PreCheckoutQuery):
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment_handler(message: Message):
    payment = message.successful_payment
    try:
        user_id_str = payment.invoice_payload.split('_')[-1]
        sub_type = payment.invoice_payload.split('_')[1]
        
        await client.process_payment(
            user_id=int(user_id_str),
            telegram_payment_id=payment.telegram_payment_charge_id,
            subscription_type=sub_type,
            amount=payment.total_amount
        )
        
        await message.answer(f"✅ Payment successful! Your {sub_type} subscription is now active.")
        logger.info(f"Payment processed for user {user_id_str}")
    except Exception as e:
        logger.error(f"Error processing payment: {e}")
        await message.answer("Error processing payment")