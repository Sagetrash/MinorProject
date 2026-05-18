from textual.app import App, ComposeResult
from textual.containers import Container
from textual.binding import Binding
from ui.screens.chat_screen import ChatScreen
from ui.screens.model_config_screen import ModelConfigScreen

class AIAgentApp(App):
    CSS_PATH = "style.tcss"
    
    BINDINGS = [
        Binding("ctrl+s", "toggle_model_config", "Model Config"),
        Binding("ctrl+n", "new_chat", "New Chat"),
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen(ChatScreen())

    def action_toggle_model_config(self) -> None:
        self.push_screen(ModelConfigScreen())

    def action_new_chat(self) -> None:
        # The ChatScreen handles its own history, 
        # but we can trigger a reset if we want.
        self.app.notify("Chat history cleared")
        # We'll implement this in ChatScreen
        if isinstance(self.screen, ChatScreen):
            self.screen.clear_chat()

if __name__ == "__main__":
    app = AIAgentApp()
    app.run()
