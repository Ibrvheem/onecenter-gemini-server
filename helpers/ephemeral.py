from werkzeug.datastructures import FileStorage
import os

class Ephemeral:
    """
    The Ephemeral class manages temporary file, it uses FileStorage to receive files and store then
    in the local computer and has a method to delete the file when no longer needed.
    """
    def __init__(self, file: FileStorage):
        self.file = file
    
    def save(self) -> str:
        """
        Save the file in the current directory.
        
        Returns:
        str: The full path of the saved file.
        """
        filename = self.file.filename
        filepath = os.path.join(os.getcwd(), filename)
        self.file.save(filepath)
        return filepath
    
    def delete(self):
        """
        Delete the temporary file.
        """
        os.remove(self.file.filename)
