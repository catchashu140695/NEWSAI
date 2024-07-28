import re

def parse_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove time frames and numbers
    content = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', content)
    # Remove "[Unintelligible]"
    content = content.replace('[Unintelligible]', '')
    # Remove empty lines and concatenate
    result = ' '.join(content.splitlines()).strip()
    
    return result

# Example usage
file_path = r'AI-video-maker\final work\raw_video\transcript.srt'
parsed_text = parse_srt(file_path)
print(parsed_text)