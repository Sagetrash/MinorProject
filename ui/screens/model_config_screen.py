from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Select, Static
from textual.binding import Binding

from config.models import ModelConfig, ModelProvider, ModelRegistry


class ModelConfigScreen(Screen):
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("escape", "back_to_chat", "Back to Chat"),
        Binding("ctrl+b", "back_to_chat", "Back"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="config-container"):
            yield Static("Model Management", id="title")

            with Vertical(id="active-model-section"):
                yield Label("Currently Active Model:")
                yield Container(id="model-select-container")
                yield Button("Set Active", id="set-active-btn")

            yield Static("--- Add New Model ---", id="divider")

            with Vertical(id="add-model-form"):
                yield Label("Model Name:")
                yield Input(placeholder="e.g. Gemini 2.0 Flash", id="name-input")

                yield Label("Provider:")
                yield Select(
                    id="provider-select",
                    options=[(p.value, p.name) for p in ModelProvider],
                )

                yield Label("Model ID:")
                yield Input(placeholder="e.g. gemini-2.0-flash-lite", id="id-input")

                yield Label("API Key:")
                yield Input(placeholder="Enter API Key", id="key-input", password=True)

                yield Button("Add Model", id="add-model-btn", variant="success")
                yield Button("Remove Selected", id="remove-model-btn", variant="error")
                yield Button("Back to Chat", id="back-btn")

        yield Footer()

    def on_mount(self) -> None:
        self.registry = ModelRegistry()
        self.refresh_model_list()
    
    def action_back_to_chat(self) -> None:
        """Action to go back to chat screen."""
        self.app.pop_screen()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "model-select":
            self.handle_set_active()

    def refresh_model_list(self):
        models = self.registry.get_available_models()
        options = [(m.model_id, m.name) for m in models]
        self.app.notify(f"Refreshing list: {len(options)} models found")

        container = self.query_one("#model-select-container", Container)
        container.remove_children()
        container.mount(Select(id="model-select", options=options))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        self.app.notify(f"Button pressed: {btn_id}", severity="information")

        if btn_id == "add-model-btn":
            self.handle_add_model()
        elif btn_id == "set-active-btn":
            self.handle_set_active()
        elif btn_id == "remove-model-btn":
            self.handle_remove_model()
        elif btn_id == "back-btn":
            try:
                self.app.notify("Returning to chat...", severity="information")
                self.app.pop_screen()
            except Exception as e:
                self.app.notify(f"Error returning to chat: {str(e)}", severity="error")

    def handle_add_model(self):
        try:
            name = self.query_one("#name-input", Input).value
            provider_val = self.query_one("#provider-select", Select).value
            model_id = self.query_one("#id-input", Input).value
            api_key = self.query_one("#key-input", Input).value

            if not name or not model_id or not api_key or not provider_val:
                self.app.notify("Please fill all fields", severity="error")
                return

            new_model = ModelConfig(
                name=name,
                model_id=model_id,
                provider=ModelProvider(provider_val),
                api_key=api_key,
            )

            if self.registry.add_model(new_model):
                self.app.notify(f"Added {name} successfully")
                self.refresh_model_list()
                # Clear inputs
                self.query_one("#name-input", Input).value = ""
                self.query_one("#id-input", Input).value = ""
                self.query_one("#key-input", Input).value = ""
            else:
                self.app.notify("Failed to add model", severity="error")
        except Exception as e:
            self.app.notify(f"Error: {str(e)}", severity="error")

    def handle_set_active(self):
        try:
            select = self.query_one("#model-select", Select)
            model_id = select.value
            if model_id and self.registry.set_active_model(str(model_id)):
                self.app.notify(f"Active model set to {model_id}")
            else:
                self.app.notify("Failed to set active model", severity="error")
        except Exception as e:
            self.app.notify(f"Error setting active model: {str(e)}", severity="error")

    def handle_remove_model(self):
        model_id = self.query_one("#model-select", Select).value
        if model_id and self.registry.remove_model(str(model_id)):
            self.app.notify(f"Removed {model_id}")
            self.refresh_model_list()
        else:
            self.app.notify("Failed to remove model", severity="error")
