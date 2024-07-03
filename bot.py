import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timedelta

# Carrega as variáveis de ambiente do arquivo .env e pega o token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Defina os intents
intents = discord.Intents.default()
intents.members = True  # Habilite o evento de membros
intents.messages = True

# Inicializa o bot com o prefixo desejado e os intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento quando o bot estiver pronto
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

# Função para pedir informações ao usuário via DM
async def ask_for_input(user, question):
    await user.send(question)
    try:
        message = await bot.wait_for(
            'message',
            timeout=300.0,
            check=lambda message: message.author == user and isinstance(message.channel, discord.DMChannel)
        )
        return message.content
    except asyncio.TimeoutError:
        await user.send('Você me deixou no vácuo seu Zé cu. Inicia de novo.')
        return None

# Função para formatar a resposta com quebras de linha
def format_response_with_bullets(response):
    lines = response.split('\n')
    formatted_response = '\n'.join(f"- {line.strip()}" for line in lines if line.strip())
    return formatted_response

# Comando para gerar o relatório
@bot.command(name='report')
async def report(ctx):
    # Envia uma mensagem inicial em DM
    user = ctx.author
    await user.send("Por favor, responda às próximas perguntas.")

    def get_yesterday():
        today = datetime.today()
        if today.weekday() == 0: #0 representa segunda feira
            yesterday = today - timedelta(days=3) #pega a data de sexta
        else:
            yesterday = today - timedelta(days=1) #pega o dia anterior normal
        return yesterday

    today = datetime.today()
    yesterday = get_yesterday()
    
    # Formatar datas
    today_str = today.strftime("%d/%m/%Y")
    yesterday_str = yesterday.strftime("%d/%m/%Y")
    
    # Perguntas
    questions = [
        f"Quais atividades você fez no dia {yesterday_str}?",
        "Quais atividades você tem para hoje?",
        "Algum impedimento?"
    ] 
    
    # Coletar respostas
    answers = []
    for question in questions:
        answer = await ask_for_input(user, question)
        if answer is None:
            return
        formatted_answer = format_response_with_bullets(answer)
        answers.append(formatted_answer)
    
    # Formatar relatório
    report_message = (
        f"## Relatório {today_str}\n\n"
        f"**DIA {yesterday_str}**\n"
        f"{answers[0]}\n\n"
        f"**HOJE - {today_str}**\n"
        f"{answers[1]}\n\n"
        f"**IMPEDIMENTOS?**\n"
        f"{answers[2]}\n"
    )
    
    print(f'{report_message}')
    
    # Formatar a mensagem como código Markdown
    markdown_report_message = f"```markdown\n{report_message}\n```"
    
    await user.send("Aqui está o seu relatório em formato Markdown, pronto para ser copiado:")
    await user.send(markdown_report_message)
    
# Comando para gerar o relatório de esteira
@bot.command(name='esteira')
async def esteira(ctx):
    user = ctx.author
    await user.send("Responda sobre a esteira feita.")
    
    today = datetime.today()
    today_str = today.strftime("%d/%m/%Y")
    
    questions = [
        "Em qual satélite foi feito a esteira?",
        "Qual a palavra foco do satélite?",
        "Link do doc da esteira",
        "Data que foi feita"
    ]
    
    answers = []
    for question in questions:
        answer = await ask_for_input(user, question)
        if answer is None:
            return
        formatted_answer = format_response_with_bullets(answer)
        answers.append(formatted_answer)
    
    # Formatar relatório
    esteiraReport = (
        f"# Relatório - Esteiras {today_str}\n\n"
        f"### Satélite e palavra foco da esteira realizada:\n{answers[0]} - satelite;\n{answers[1]} - palavra foco;\n\n"
        f"### Doc do que foi realizado:\n{answers[2]};\n\n"
        f"### Data de conclusão da esteira:\n{answers[3]}\n\n"
        f"Realizada por: **{user}** "
    )
    print(f'{esteiraReport}')
    
    # Formatar a mensagem como código Markdown
    markdown_report_message = f"```markdown\n{esteiraReport}\n```"
    
    await user.send("Aqui está o seu relatório em formato Markdown, pronto para ser copiado:")
    await user.send(markdown_report_message)
    
@bot.command(name='ajuda')
async def ajuda(ctx):
    help_message = (
        "Olá! Aqui estão os comandos disponíveis:\n\n"
        "**!report** - Gera um relatório de daily.\n"
        "**!esteira** - Gera um relatório de esteiras.\n\n"
        "Ao usar esses comandos, o bot enviará alguns perguntas para montar o seu relatório.\n"
        "Caso tenha feito várias atividades, use Shift + Enter para dar quebra de linha na resposta para o bot.\n"
        "Não é preciso formatar a resposta, ele fará isso para você. Não se preocupe com as datas também, elas são incluídas automaticamente. Outro ponto é que toda segunda-feira, o bot pega a data de sexta-feira automaticamente também. Não é necessário se preocupar em atualizar a data na mão. TMJ :saluting_face: \n"
    )
    await ctx.author.send(help_message)

# Adicione seu token aqui
bot.run(TOKEN)
