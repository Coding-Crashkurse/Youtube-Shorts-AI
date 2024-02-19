from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client import client, file, tools


def initialize_youtube_api():
    CLIENT_SECRETS_FILE = "client_secret.json"
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    store = file.Storage("storage.json")
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
        creds = tools.run_flow(flow, store)
    return build("youtube", "v3", credentials=creds)


def upload_video(video_path, topic):
    # Initialize YouTube API
    youtube = initialize_youtube_api()

    body = {
        "snippet": {
            "title": f"Five facts about {topic} you did not know!",
            "description": f"Learn 5 facts about {topic} which you probably did not know",
            "tags": ["shorts", topic],
            "categoryId": "15",
        },
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    response = (
        youtube.videos()
        .insert(part="snippet,status", body=body, media_body=media)
        .execute()
    )
    print("Upload complete. Video ID:", response["id"])
