import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.transaction import Transaction
from solana.system_program import transfer

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Solana client setup
client = Client("https://api.mainnet-beta.solana.com")  # Solana mainnet URL
wallet = Keypair.from_secret_key(bytes.fromhex("YOUR_PRIVATE_KEY"))  # Replace with your private key

# Define a function to handle /balance command
def balance(update: Update, context: CallbackContext):
    # Retrieve wallet balance
    balance = client.get_balance(wallet.public_key)["result"]["value"]
    update.message.reply_text(f"Your balance is {balance / 1e9} SOL.")  # Convert to SOL (1 SOL = 1e9 lamports)

# Define a function to handle /send command
def send(update: Update, context: CallbackContext):
    try:
        recipient = context.args[0]  # Address to send SOL to
        amount = float(context.args[1])  # Amount of SOL to send
        
        # Create a transfer transaction
        transaction = Transaction().add(
            transfer(
                TransferParams(
                    from_pubkey=wallet.public_key,
                    to_pubkey=recipient,
                    lamports=int(amount * 1e9)  # Convert SOL to lamports
                )
            )
        )
        
        # Sign and send the transaction
        client.send_transaction(transaction, wallet)
        update.message.reply_text(f"Successfully sent {amount} SOL to {recipient}.")
    except IndexError:
        update.message.reply_text("Usage: /send <recipient_address> <amount>")

# Define main function to start the bot
def main():
    # Get Telegram bot token from BotFather
    updater = Updater("7715313927:AAGxaLub3FnsGYezHSc-M4uA1TGDW0axTHo", use_context=True)
    
    dp = updater.dispatcher
    
    # Command handlers
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("send", send))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
