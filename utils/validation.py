import re

# Validate if the link is from YouTube or Instagram
def validate_link(link):
    youtube_pattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/(?:[\w\-]+\?v=|embed/|v/|\?v=)?([\w\-]+)"
    instagram_pattern = r"(?:https?://)?(?:www\.)?instagram\.com/[\w\-]+"
    return bool(re.match(youtube_pattern, link) or re.match(instagram_pattern, link))