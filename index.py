import telepot
import time
import os
import schedule
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

# Substitua 'YOUR_BOT_TOKEN' pelo seu token
TOKEN = '6640916825:AAGnzwy_-8RL7xHEYW--IGQHc8KNsO8rGFQ'

# Dicionário para armazenar o estado do usuário
user_state = {}

# Estados possíveis
STATE_START = "start"
STATE_CADASTRO = "cadastro"

# Defina os caminhos para as fotos
photo_path_jpg = os.path.join(os.getcwd(), 'img', 'foto1.jpg')
photo_path_png = os.path.join(os.getcwd(), 'img', 'aluno.jpg')

# Função para lidar com mensagens recebidas
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    # Verifica se a mensagem é do tipo 'text' e contém o comando '/start'
    if content_type == 'text' and msg['text'] == '/start':
        # Cria o botão "Cadastre-se"
        keyboard_cadastro = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Cadastre-se',url='https://www.seubet.com/?btag=1554727&AFFAGG=',callback_data=STATE_CADASTRO)],
            [InlineKeyboardButton(text='Continuar',callback_data=STATE_CADASTRO)],
            
        ])

        # Envia a mensagem inicial com o botão "Cadastre-se"
        message = (
            f"Olá! Parabéns por chegar até aqui! Vou liberar em alguns instantes uma vaga para meu GRUPO GRATUITO DE APOSTAS, "
            "mas antes disso, siga algumas instruções.\n\n"
            "Cadastre-se na casa de apostas que atende aos sinais pelo link abaixo. Após fazer o cadastro, irei liberar seu acesso ao meu grupo gratuito. ⬇️"
        )
        bot.sendMessage(chat_id, message, reply_markup=keyboard_cadastro)

        # Salva o nome do usuário e o chat_id no dicionário de estado
        user_state[chat_id] = {'user_name': msg['chat']['first_name'], 'chat_id': chat_id}

        # Agenda o envio das mensagens
        schedule.every().day.at("15:00").do(send_gift_message, chat_id)
        schedule.every().day.at("12:15").do(send_ebook_view_message, chat_id)
        schedule.every().day.at("12:30").do(send_live_message, chat_id)
        schedule.every().day.at("12:45").do(send_profit_message, chat_id)
# Função para lidar com callback queries (respostas aos botões)
def on_callback_query(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')

    if query_data == STATE_CADASTRO:
        # Envia a mensagem inicial sem o botão "Sim"
        initial_message = (
            "Essa é a única plataforma que atende e está sincronizada com os meus sinais. Cadastre-se pelo link acima para eu liberar seu acesso!!\n\n"
        )

        # Envia a mensagem inicial sem o botão "Sim"
        sent_message_initial = bot.sendMessage(chat_id, initial_message)

        # Espera alguns segundos (ajuste conforme necessário)
        time.sleep(5)

        # Cria o botão "Sim"
        keyboard_sim = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Sim', callback_data='sim')],
        ])

        # Envia a mensagem com o botão "Sim"
        sent_message_sim = bot.sendMessage(chat_id, f"Conseguiu concluir seu cadastro?, {user_state.get(chat_id, {}).get('user_name', 'usuário')} Aperte 'Sim' para continuar.", reply_markup=keyboard_sim)

        # Armazena o ID da mensagem inicial enviada
        user_state[chat_id]['message_id_initial'] = sent_message_initial['message_id']
        # Armazena o ID da mensagem com o botão "Sim" enviada
        user_state[chat_id]['message_id_sim'] = sent_message_sim['message_id']

    elif query_data == 'sim' and user_state.get(chat_id):
        # Responde à callback query para remover o botão "Sim"
        bot.answerCallbackQuery(query_id, text="Acesso liberado!")

        # Recupera os IDs das mensagens para responder a elas
        message_id_initial = user_state[chat_id].get('message_id_initial')
        message_id_sim = user_state[chat_id].get('message_id_sim')

        # Envia a mensagem final após clicar em "Sim"
        final_message = (
            f"Ótimo!! O acesso será liberado agora!! Preparado para lucrar com o Zanette, {user_state.get(chat_id, {}).get('user_name', 'usuário')}?\n\n"
            "Após clicar no link aperte 'ENTRAR' para você realmente fazer parte de nosso grupo."
        )
        bot.sendMessage(chat_id, final_message)

        # Remove o estado do usuário após clicar em "Sim"
        del user_state[chat_id]

        # Envia a foto com a mensagem e o botão "Quero Entrar"
        caption = f"Clique já no botão abaixo para entrar no grupo gratuito e começar a fazer dinheiro:"
        keyboard_entrar = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Quero Entrar',url='https://t.me/tibianofree', callback_data='quero_entrar')],
        ])

        # Envia a foto com a mensagem e o botão "Quero Entrar"
        bot.sendPhoto(chat_id, open(photo_path_jpg, 'rb'), caption=caption, reply_markup=keyboard_entrar)

# Função para lidar com a resposta do botão "Quero Entrar"
def on_entrar_callback(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')

    if query_data == 'quero_entrar':
        # Responde à callback query para remover o botão "Quero Entrar"
        bot.answerCallbackQuery(query_id, text="Bem-vindo ao grupo gratuito!")

# Função para enviar a mensagem após 50 segundos
def send_live_message(chat_id):
    live_message = (
        "Vou entrar ao vivo hoje!!! Conseguiu entrar no meu grupo?\n"
        "Se ainda não entrou, está perdendo uma oportunidade única…\n"
        "Clique abaixo e entre no meu grupo⬇️⬇️"
    )
    keyboard_entrar_grupo = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Entrar no Grupo',url='https://t.me/tibianofree', callback_data='entrar_no_grupo')],
    ])
    bot.sendMessage(chat_id, live_message, reply_markup=keyboard_entrar_grupo)

# Função para enviar a mensagem de presente após 30 segundos
def send_gift_message(chat_id):
    # Envia a mensagem de presente
    gift_message = (
        f" já fez seu depósito para fazer dinheiro comigo?? 🎁🎁 "
        "Irei liberar para você um presente ESPECIAL que somente é liberado aos meus alunos. "
        "Você terá acesso a um ebook secreto com tudo que é necessário para iniciar seus ganhos comigo!!! "
        "Veja aqui⬇️"
    )
    bot.sendMessage(chat_id, gift_message)

    # Envia o arquivo PDF
    pdf_path = os.path.join(os.getcwd(), 'img', 'TutorialRoleta.pdf')  # Caminho para o arquivo PDF
    bot.sendDocument(chat_id, open(pdf_path, 'rb'))

# Função para enviar a mensagem "Viu o ebook???" após 40 segundos
def send_ebook_view_message(chat_id):
    ebook_view_message = "Viu o ebook???"
    bot.sendMessage(chat_id, ebook_view_message)

# Função para enviar a mensagem de lucro após 60 segundos
def send_profit_message(chat_id):
    profit_message = (
        "Já começou a lucrar? Olha esse aluno que conseguiu mais que duplicar o valor de sua banca em poucos dias no grupo🔽\n"
        "Viuu?? Por isso é importante um investimento em sua banca!! Quando maior seu investimento, maior seu retorno."
    )
    # Cria o botão "Cadastro Novamente"
    keyboard_cadastro_novamente = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Cadastre-se Novamente',url='https://www.seubet.com/?btag=1554727&AFFAGG=', callback_data=STATE_CADASTRO)],
    ])
    # Envia a mensagem com a imagem e o botão "Cadastro Novamente"
    bot.sendPhoto(chat_id, open(photo_path_jpg, 'rb'), caption=profit_message, reply_markup=keyboard_cadastro_novamente)

# Criação do objeto bot
bot = telepot.Bot(TOKEN)

# Associa as funções de tratamento de mensagens e callback queries ao bot
bot.message_loop({'chat': handle, 'callback_query': on_callback_query, 'photo': on_entrar_callback})
print("Bot está pronto para receber comandos. Aguarde...")

while True:
    schedule.run_pending()
    time.sleep(10)