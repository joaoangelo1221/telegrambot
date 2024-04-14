import logging
from telegram.constants import ParseMode
from telegram import LabeledPrice, ShippingOption, Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ( 
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    filters, CallbackQueryHandler
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

TOKEN = "6619560022:AAGJuP2mKG0KB_K8STz2x3yn-yheHbjCvyQ"
application = Application.builder().token(TOKEN).build()

###################START/INICIO#####################
async def start(update: Update, context) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Olá {user.first_name}!\n"
        "Escolha a opção para começarmos seu atendimento:\n"
        "1. Ver nosso /catalogo.\n"
        "3. Endereço da nossa /loja.\n"
        "4. /contato"
    )
application.add_handler(CommandHandler("start", start))

#################CATALOGO#####################
async def catalogo(update: Update, context) -> None:
    mensagem = (
        "Ficamos felizes que queira olhar o nosso catálogo!\n"
        "Escolha o nicho que deseje ver:\n"
    )
    teclado = [
        [
            InlineKeyboardButton("Sapatos", callback_data='sapato'),
            InlineKeyboardButton("Camisas", callback_data='camisa'),
            InlineKeyboardButton("Calças", callback_data='calca'),
        ]
    ]
    resposta_markup = InlineKeyboardMarkup(teclado)
    await update.message.reply_text(mensagem, reply_markup=resposta_markup)
#############CATALOGO/SAPATOS#################
async def sapato(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(update.effective_user.id)
#############CATALOGO/CAMISAS#################
async def camisa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(update.effective_user.id)
#############CATALOGO/CALÇAS#################
async def calca(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(update.effective_user.id)
#############CONTATO#################
async def contato(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensagem = (
        "Nossos contatos: N/D\n"

    )
    await context.bot.send_message(update.effective_user.id, mensagem)
#############ENDEREÇOS#################
async def endereco(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensagem = (
        "Nosso endereço: N/D\n"
    )
    await context.bot.send_message(update.effective_user.id, mensagem)
###########CONFIGURAÇÃO DOS BOTÕES########################
async def processar_botao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    botao_clicado = query.data
    if botao_clicado == 'sapato':
        await enviar_foto(update, ['pasta-aberta.png', 'pasta-aberta.png'], ["Sapato XXX - R$100 (Valor Fictício)", "Sapato XXX - R$180 (Valor Fictício)"], ["Disponíveis", "Disponíveis"])
    elif botao_clicado == 'camisa':
        await enviar_foto(update, ['pasta-aberta.png', 'pasta-aberta.png',], ["Camisa XXX - R$150 (Valor Fictício)", "Camisa XXX - R$50 (Valor Fictício)"], ["Disponíveis", "Disponíveis"])
    elif botao_clicado == 'calca':
        await enviar_foto(update, ['pasta-aberta.png', 'pasta-aberta.png',], ["Calça XXX - R$80 (Valor Fictício)", "Calça XXX - R$280 (Valor Fictício)"], ["Disponíveis", "Disponíveis"])
############FOTOS#################
async def enviar_foto(update, fotos, legendas, titulos):
    try:
        for titulo, foto_path, caption in zip(titulos, fotos, legendas):
            # Adiciona um título em negrito
            mensagem = f"<b>{titulo}</b>\n{caption}"

            # Verifica se há uma mensagem original para responder
            if update.callback_query and update.callback_query.message:
                # Envia a mensagem do Instagram
                await update.callback_query.message.reply_text("Para efetuar o pagamento, entre em /contato. Siga também nosso Instagram para mais novidades @")

                # Envia a foto com a mensagem de texto
                media = [InputMediaPhoto(media=open(foto_path, 'rb'), caption=mensagem, parse_mode=ParseMode.HTML)]
                await update.effective_message.reply_media_group(media=media)
            else:
                print("Mensagem original não encontrada.")

    except Exception as e:
        print(f"Erro ao enviar foto: {e}")
########COMANDOS##########
application.add_handler(CallbackQueryHandler(processar_botao))
application.add_handler(CommandHandler("contato", contato))
application.add_handler(CommandHandler("loja", endereco))
application.add_handler(CommandHandler("catalogo", catalogo))
################RUN#####################
application.run_polling(allowed_updates=Update.ALL_TYPES)
