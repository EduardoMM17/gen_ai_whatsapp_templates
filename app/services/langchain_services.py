from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate

from app.core.chat_open_ai import chat_process_conversation

ticket_schema = ResponseSchema(name="ticketId", description="The ticketId from the object")
name_schema = ResponseSchema(name="name", description="The name from the object")
contact_reason_schema = ResponseSchema(name="contactReason", description="The contactReason from the object")
nps_score_schema = ResponseSchema(name="npsScore", description="The npsScore from the object")
conversation_details_schema = ResponseSchema(name="conversationDetails", description="The summary from the rawConversation field from the object")

response_schemas = [ticket_schema, name_schema, contact_reason_schema, nps_score_schema, conversation_details_schema]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

example = """
    rawConversation: "ticketId	time	name	detail \
                    147719	12 may. 11:12	Marcos por WhatsApp	Buenos dias \
                    147719	12 may. 11:12	Ada Bot por WhatsApp	¡Hola, MARCOS! Gracias por usar Yape en tu negocio. Te conectaré con un asesor especializado para que pueda seguir con tu atención. \
                    147719	12 may. 11:14	Marcos por WhatsApp	Hola \
                    147719	12 may. 11:15	S65916-RUMAY ESPINO CHRISTIAN FREDDY por WhatsApp	Hola, Marcos👋. Espero que estés bien, soy Christian y estoy aquí para apoyarte en lo que necesites ☺️. Cuéntame, ¿cómo te puedo ayudar? \
                    147719	12 may. 11:16	Marcos por WhatsApp	Mi problema es el siguiente ,hice un yapeo erróneo de 240 soles ,quería saber si pueden a ayudarme a q extorne a mi cuenta \
                    147719	12 may. 11:16	Marcos por WhatsApp	JPEG \
                    147719	12 may. 11:16	Marcos por WhatsApp	A esta persona \
                    147719	12 may. 11:17	S65916-RUMAY ESPINO CHRISTIAN FREDDY por WhatsApp	Marcos, lamentamos que hayas pasado por esta situación. En esta ocasión, te recomendamos contactar a la persona que recibió tu yapeo para que le puedas solicita la devolución. Debido a que somos un intermediario para que puedas enviar y recibir dinero, no podemos deshacer las operaciones que hayas realizado. Por eso es muy importante que antes de ingresar el monto a yapear, verifiques que el nombre que aparece en la aplicación es el de la persona que quieres que reciba tu yapeo. 🙌💜 \
                    147719	12 may. 11:18	Marcos por WhatsApp	Pero se supone q para tener yape tienen q tener cuenta bcp \
                    147719	12 may. 11:18	Marcos por WhatsApp	Como yo lo tengo \
                    147719	12 may. 11:18	Marcos por WhatsApp	Ud pueden descontar de eso cuenta cuando hay un error en la transferencia \
                    147719	12 may. 11:18	Marcos por WhatsApp	A mi me lo hicieron,cuando por error depositaron 500 soles a mi cuenta \
                    147719	12 may. 11:25	S65916-RUMAY ESPINO CHRISTIAN FREDDY por WhatsApp	Marcos, entiendo lo que me comentas, nosotros como Yape, no podemos entrar a la cuenta de un cliente, retirar el dinero, para luego abonarlo hacia otra cuenta, ese proceso esta penado, no es un proveso correcto. \
                    147719	12 may. 12:11	S65916-RUMAY ESPINO CHRISTIAN FREDDY por WhatsApp	¡Yapero! 🤓 Estuve atento e intenté contactarme nuevamente, pero no fue posible. ¡Descuida! Para retomar la conversación escribe Hola y con gusto resolveremos juntos tus dudas y consultas. 💜 Recuerda que nuestro horario de atención es de 6 a.m. a 11:30 p.m.💜 ¡Bendiciones, cuidate mucho!🙏", \
    
    summary: "El 12 de mayo, Marcos contactó al servicio de atención al cliente a través de WhatsApp. Inicialmente, fue atendido por un asesor automatizado llamado Ada Bot, quien luego lo derivó a un asesor humano. \
    Christian se presentó como el asesor y ofreció su ayuda. Marcos explicó que había realizado un yapeo erróneo por 240 soles y quería saber si podían ayudarlo a revertir la operación. Christian lamentó la situación \
    de Marcos y le recomendó que contactara a la persona que recibió el yapeo para solicitar la devolución, ya que Yape no puede deshacer las operaciones realizadas. Marcos planteó la pregunta de si Yape podría deducir \
    el monto del error de su propia cuenta bancaria, mencionando una situación anterior en la que depositaron por error 500 soles en su cuenta. Christian explicó que Yape no tiene la capacidad de acceder a la cuenta de un cliente y realizar transferencias sin su consentimiento. \
    Marcos intentó retomar la conversación, pero no fue posible contactarse nuevamente. Christian ofreció retomar la conversación si Marcos lo deseaba y le recordó el horario de atención." \
"""

template_string = """
        Your task is to create a summary of the raw conversation found inside the rawConversation field object provided. \
        The summary must: \
            - Be written spanish \
            - Include the date \
        {format_instructions} \
        In order to be able to attribute a message in the conversation to someone, you must always take into account the column called "name". \        
        ticketObject: {ticketObject} \
        Use the following as an example of the summary generation based on the raw conversation field: \n
        {example}\
        
"""

# def process_raw_conversations()