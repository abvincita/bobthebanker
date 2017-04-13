import microsoftbotframework.runcelery
from microsoftbotframework import MsBot
from tasks import *

bot = MsBot(verify_jwt_signature=False, debug=True)
bot.add_process(echo_response)
bot.run()
