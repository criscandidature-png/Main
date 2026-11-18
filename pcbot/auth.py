import os
from functools import wraps

ALLOWED = {int(x) for x in os.getenv("ALLOWED_USERS", "").split(",") if x.strip()}


def restricted(func):
    """Solo gli utenti in ALLOWED_USERS possono usare il comando."""
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user = update.effective_user
        if not user or user.id not in ALLOWED:
            if update.effective_message:
                await update.effective_message.reply_text("⛔ Non autorizzato.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
