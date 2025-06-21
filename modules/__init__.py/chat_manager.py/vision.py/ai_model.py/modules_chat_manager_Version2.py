class ChatManager:
    def __init__(self):
        self.history = []

    def add_user_message(self, content, image_bytes=None):
        msg = {"role": "user", "content": content}
        if image_bytes:
            msg["image"] = image_bytes
        self.history.append(msg)

    def add_ai_message(self, content):
        self.history.append({"role": "assistant", "content": content})