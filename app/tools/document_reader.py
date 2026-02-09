class DocumentReaderTool:
    """
    Tool to read local documents.
    """
    def read(self, path: str) -> str:
        with open(path, 'r') as f:
            return f.read()
