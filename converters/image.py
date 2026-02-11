from PIL import Image
from .base import BaseConverter
import os

class ImageConverter(BaseConverter):
    """Handles image format conversions for FileCon."""
    def convert(self, input_path, output_path, options=None):
        try:
            with Image.open(input_path) as img:
                fmt = options.get('format', 'PNG').upper()
                
                # Handle transparency for JPEG
                if fmt == 'JPEG' and img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Special handling for ICO
                if fmt == 'ICO':
                    img.save(output_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
                else:
                    img.save(output_path, format=fmt, quality=options.get('quality', 95))
                    
            return True, "Success"
        except Exception as e:
            return False, str(e)
