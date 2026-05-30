class StreamToStreamlit:
    """
    Runtime log execution context manager trap.
    Intercepts system standard stdout prints and channels them to a Streamlit code window.
    """
    def __init__(self, text_placeholder):
        self.text_placeholder = text_placeholder
        self.log_buffer = ""

    def write(self, text):
        self.log_buffer += text
        self.text_placeholder.code(self.log_buffer)

    def flush(self):
        pass