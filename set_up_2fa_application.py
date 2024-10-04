from infobip_channels.sms.channel import SMSChannel
from dotenv import load_dotenv

load_dotenv()

channel = SMSChannel.from_env()

response = channel.create_tfa_application(
    {
    "name": "gift exchange 2fa application",
    "enabled": "true",
    "configuration": {
        "pinAttempts": 7,
        "allowMultiplePinVerifications": "true",
        "pinTimeToLive": "11m",
        "verifyPinLimit": "2/4s",
        "sendPinPerApplicationLimit": "5000/12h",
        "sendPinPerPhoneNumberLimit": "2/1d",}
    }

)

response = channel.get_tfa_applications()
application_id = response.list[0].application_id
print("Application ID: ", application_id)

response = channel.create_tfa_message_template(
    application_id,
    {
            "pinType": "NUMERIC",
            "pinPlaceholder": "{{pin}}",
            "messageText": "Your pin is {{pin}}",
            "pinLength": 4,
            "language": "en",
            "senderId": "Infobip 2FA",
            "repeatDTMF": "1#",
            "speechRate": 1,
    }
)

template_id = response.message_id
print("Template ID: ", template_id)