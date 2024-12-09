import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
import google.generativeai as genai
from channels.db import database_sync_to_async
from datetime import datetime
from app.helper.datastr import data_str

@database_sync_to_async
def get_user_by_phone_number(user_id):
    from customuser.models import CustomUser
    user = CustomUser.objects.get(phone_number=str(user_id)[2:])

    return f"""
    Olá essa mensagem inicial é para te passar um contexto de como você deve responder!
    Você deve responder mensagens baseadas nos beneficios encontrado nessa mensagem, qualquer mensagem
    que fuja do contexto de beneficios que um funcionário de uma empresa possa ter, não poderá ser responida.
    Responda a primeira mensagem dizendo Ola (nome do funcionado) sou um assistente virtual da vale e estou aqui
    para te ajudar a entender mais sobre os seus beneficios, caso não conheça seus beneficios, eu posso te enviar a lista de beneficios.
    Caso o funcionario peça a lista, Primeiro envie a lista de categorias dos beneficios em forma de lista, e deixe o funcionario aprofundar a conversa.
    Mas depois responda apenas o que for perguntado, para simular uma conversa humana!
    a descrição do beneficio costuma ter o faq, onde responde a maioria das dúvidas.
    abaixo estará todas informações com quem você deve conversar
    (dia de hoje: {datetime.now().strftime("%d/%m/%Y")})
    {user.get_full_name()}
    {data_str}
    """ 


# Configurar a API do Gemini
genai.configure(api_key="AIzaSyAuXzSRmBXYhW8jgDVnxHcXSfeHJm72dak")

# Conectar ao Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Dicionário para conexões WebSocket ativas (opcional em memória, Redis recomendado para escalabilidade)
active_connections = {}


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # Aceitar a conexão WebSocket
        await self.accept()

        print("foi?")

        # Identificar o user_id pela URL
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        # Armazenar a conexão ativa
        active_connections[self.user_id] = self

        # Configurar histórico do chat
        self.history_key = f"chat_history:{self.user_id}"
        self.history = redis_client.get(self.history_key)

        if self.history:
            self.history = json.loads(self.history)
        else:
            print("não tem hisotrico!!!!!")
            user_json = await get_user_by_phone_number(self.user_id)
            self.history = [{'sender': 'user', 'message': user_json}]
  
        print("historico", self.history)
        # Configurar sessão do Gemini
        self.session_key = f"session_key:{self.user_id}"
        self.session_id = redis_client.get(self.session_key)

        if self.session_id:
            # Recuperar sessão existente
            self.session = genai.GenerativeModel(self.session_id)
        else:
            # Criar uma nova sessão
            self.session = genai.GenerativeModel("gemini-1.5-flash")
            redis_client.set(self.session_key, "gemini-1.5-flash")

    async def disconnect(self, close_code):
        # Remover a conexão ativa ao desconectar
        active_connections.pop(self.user_id, None)

        # Salvar histórico no Redis
        redis_client.set(self.history_key, json.dumps(self.history))

        # Encerrar a sessão do Gemini (opcional)
        self.session = None

    async def receive(self, text_data):
        # Processar mensagem recebida do WebSocket
        data = json.loads(text_data)
        prompt = data.get("message", "")

        # Adicionar mensagem do usuário ao histórico
        self.history.append({"sender": "user", "message": prompt})

        # Gerar resposta com o Gemini
        response = await self.generate_response(prompt)

        # Adicionar resposta do bot ao histórico
        self.history.append({"sender": "bot", "message": response})

        # Enviar resposta para o WebSocket
        await self.send(text_data=json.dumps({
            "response": response
        }))

    async def generate_response(self, prompt):
        try:
            # Contexto do histórico
            conversation_context = "\n".join([f"{msg['sender']}: {msg['message']}" for msg in self.history])
            # Gerar resposta usando o Gemini
            input_data = f"{conversation_context}\nUser: {prompt}\nBot:"
            response = self.session.generate_content(input_data)

            return response.text
        except Exception as e:
            return f"Erro ao gerar resposta: {str(e)}"
