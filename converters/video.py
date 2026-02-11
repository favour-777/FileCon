from moviepy.editor import VideoFileClip
from .base import BaseConverter
import os

class VideoConverter(BaseConverter):
    """Handles video format conversions and audio extraction for FileCon."""
    def convert(self, input_path, output_path, options=None):
        try:
            fmt = options.get('format', 'mp4').lower()
            codec = options.get('codec', 'libx264')
            
            # Extract audio only if format is audio
            if fmt in ['mp3', 'wav', 'ogg', 'aac']:
                clip = VideoFileClip(input_path)
                clip.audio.write_audiofile(output_path)
                clip.close()
            else:
                clip = VideoFileClip(input_path)
                # Resize if needed
                if options.get('resolution'):
                    res = options.get('resolution') # e.g., (1280, 720)
                    clip = clip.resize(height=res[1])
                
                clip.write_videofile(output_path, codec=codec, audio_codec='aac')
                clip.close()
                
            return True, "Success"
        except Exception as e:
            return False, str(e)
