from twilio.rest import Client

account_sid = 'AC3702cc3f63fed23e1b571eb911e83d6f'
auth_token = 'cd19e24a44f92f2f4d3823ea6424b29c'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+12053509383',
                     to='+79299478156'
                 )

print(message.sid)