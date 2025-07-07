import base64
import quopri
import re
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# store what was already visited and remove it

def get_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return build('gmail', 'v1', credentials=creds)

def get_message_content(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = msg['payload']

    # Helper to decode a part
    def decode_part(part):
        data = part.get('body', {}).get('data')
        if not data:
            return None

        decoded_bytes = base64.urlsafe_b64decode(data)
        # DO NOT apply quoted-printable decoding here
        return decoded_bytes.decode('utf-8', errors='ignore')

    # Case 1: Multipart email (has parts)
    parts = payload.get('parts')
    if parts:
        for part in parts:
            mime = part.get('mimeType')
            if mime in ['text/plain', 'text/html']:
                content = decode_part(part)
                if content:
                    return content

    # Case 2: Single-part email
    elif 'body' in payload and 'data' in payload['body']:
        return decode_part(payload)

    return None
def extract_target_url(text):
    target = "/marketplace/selling/?action=publish"
    start = text.find(target)

    if start != -1:
        end = start
        while end < len(text) and text[end] not in (' ', '\n'):
            end += 1
        result = text[start:end]
        print("Matched:", 'https://www.facebook.com' + result)
    else:
        print("Target not found.")

def main():
    service = get_service()
    results = service.users().messages().list(
        userId='me',
        q='from:noreply@marketplace.facebook.com',
        maxResults=5
    ).execute()
    messages = results.get('messages', [])
   
    for msg in messages:
        msg_id = msg['id']
        content = get_message_content(service, msg_id)
        # print(content)
        if content:
            target = extract_target_url(content)
            
        else:
            print(f"[ERROR] Could not read message {msg_id}")

if __name__ == '__main__':
    main()


# https://www.facebook.com

# /marketplace/selling/?action=3Dpublish&token=3DE7GTWXM4lml6NHjaMeOwiQSwX2yQ=
# iOiC3poAHal7W870ip76SqwWO2fMTXPFcNNj&listing_id=3D1095907759094146




