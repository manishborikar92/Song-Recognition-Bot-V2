
async def start(update, context):
    await update.message.reply_text(
        "👋 Hi! I can process music requests concurrently for multiple users."
    )