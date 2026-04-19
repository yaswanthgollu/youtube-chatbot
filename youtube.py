from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs


def extract_video_id(url):
    """
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    """
    parsed_url = urlparse(url)

    if "youtube.com" in parsed_url.netloc:
        return parse_qs(parsed_url.query).get("v", [None])[0]

    elif "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")

    return None


# Updated get_transcript_from_url function
def get_transcript_from_url(url):
    try:
        video_id = extract_video_id(url)
        if not video_id:
            print("Invalid YouTube URL")
            return None

        try:
            # 1. Initialize the API object
            api = YouTubeTranscriptApi()
            
            # 2. Use fetch() or list_transcripts() instead of the old static method
            # This is the modern way to get a single transcript
            transcript_list = api.fetch(video_id, languages=["en", "en-US"])

            transcript = " ".join(chunk.text for chunk in transcript_list)
            return transcript

        except TranscriptsDisabled:
            print("No captions available for this video!")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None