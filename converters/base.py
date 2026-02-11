from abc import ABC, abstractmethod
from pathlib import Path

class BaseConverter(ABC):
    """Base class for all FileCon converters."""
    def __init__(self):
        self.is_converting = False

    @abstractmethod
    def convert(self, input_path, output_path, options=None):
        """Perform a single file conversion."""
        pass

    def batch_convert(self, files, output_dir, options=None, progress_callback=None):
        """Perform batch conversion of multiple files."""
        results = []
        total = len(files)
        
        for i, file_path in enumerate(files):
            try:
                input_p = Path(file_path)
                output_ext = options.get('format', 'png').lower()
                output_p = Path(output_dir) / f"{input_p.stem}.{output_ext}"
                
                success, message = self.convert(file_path, str(output_p), options)
                results.append({'file': file_path, 'success': success, 'message': message})
            except Exception as e:
                results.append({'file': file_path, 'success': False, 'message': str(e)})
            
            if progress_callback:
                progress_callback((i + 1) / total * 100)
                
        return results
