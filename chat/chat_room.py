import uuid
import random

class ChatRoom:
    def __init__(self):
        self.messages = []
        ## Gerate a unique ID for the chat room
        self.chat_id = str(uuid.uuid4())

    def add_message(self, role, message):
        self.messages.append({"role": role, "message": message})

    def __len__(self):
        return len(self.messages)
    
    def __iter__(self):
        return iter(self.messages)
    
    def __str__(self):
        return "\n".join([f"{msg['role']}: {msg['message']}" for msg in self.messages])
    
    def __repr__(self):
        return f"ChatRoom({self.chat_id}, {len(self.messages)} messages)"

    def __getitem__(self, index):
        return self.messages[index]

    def get_message(self, index=None):
        if index is None:
            return self.messages
        else:
            try:
                return self.messages[index]
            except IndexError:
                raise IndexError("Index out of range")

    def clear_messages(self):
        self.messages = []