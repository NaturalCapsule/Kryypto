import pypresence
import time

class DiscordPresence:
    def __init__(self):
        self.client_id = "1413125982319280188"
        self.RPC = None
        self.connected = False
        self.start_time = int(time.time())
        
    def connect(self):
        try:
            self.RPC = pypresence.Presence(self.client_id)

            self.RPC.connect()
            self.connected = True
            print("Discord Rich Presence connected!")
        except Exception as e:
            print(f"Failed to connect to Discord: {e}")
            self.connected = False
    
    def disconnect(self):
        if self.connected and self.RPC:
            self.RPC.close()
            self.connected = False
    
    def update_file(self, file_name, directory=None, cursor_position = None):
        if not self.connected:
            return
        try:
            if file_name:
                self.RPC.update(
                    details=f"Editing {file_name}",
                    state=f"In {directory} | {cursor_position}",

                    start=self.start_time,
                    small_image=r'icons\fileIcons\python.svg'
                )
            else:
                self.RPC.update(
                    details="Text Editor",
                    state="No file open",
                    start=self.start_time
                )
        except Exception as e:
            print(f"Failed to update Discord presence: {e}")