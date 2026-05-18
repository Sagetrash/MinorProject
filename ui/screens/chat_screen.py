from textual.screen import Screen
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Input, Static, Tree
from textual.widget import Widget
from textual.reactive import reactive
from agent.core import AgentEngine, AgentStep
from config.models import ModelRegistry
from config.storage import load_config
from textual.app import App
from pathlib import Path
from ui.file_tree import scan_directory, TreeRefreshManager

class MessageContainer(Widget):
    """Container for messages that scrolls"""
    def render(self):
        return ""

class Message(Static):
    def __init__(self, role: str, text: str, metadata: dict = None):
        super().__init__(markup=False)
        self.role = role
        self.text = text
        self.metadata = metadata
        self.set_classes(f"message {role}")
        self.update_content()

    def update_content(self):
        prefix = "👤 User: " if self.role == "user" else "🤖 Agent: " if self.role == "response" else "⚙️ Tool: "
        content = f"{prefix}{self.text}"
        if self.metadata and self.role == "function":
            args = self.metadata.get("args", "")
            content = f"{prefix}{self.text}\n   Args: {args}"
        self.update(content)

class ChatScreen(Screen):
    def compose(self):
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Static("Active Model:", id="model-label")
                yield Static("Loading...", id="current-model")
                yield Static("", id="divider-line")
                yield Static("Files:", id="files-label")
                yield Tree("Loading...", id="file-tree")
            with Vertical(id="chat-area"):
                with Vertical(id="messages"):
                    yield Static("Welcome to AI Agent TUI! Type your prompt below.", id="welcome")
                yield Input(placeholder="Enter your prompt here...", id="user-input")
        yield Footer()

    def on_mount(self) -> None:
        self.registry = ModelRegistry()
        self.engine = AgentEngine(self.registry)
        config = load_config()
        self.config = config if config else ModelRegistry().get_config()
        
        # Get the working directory from config
        project_root = Path(__file__).parent.parent.parent
        self.working_dir = project_root / self.config.working_directory
        
        self.update_model_display()
        self.build_file_tree()
        self.start_file_watcher()
    
    def start_file_watcher(self) -> None:
        """Start watching for file system changes."""
        try:
            self.tree_refresh_manager = TreeRefreshManager(self.working_dir, self.refresh_file_tree)
            self.tree_refresh_manager.start()
        except Exception:
            pass  # Silently fail if watchdog isn't available
    
    async def refresh_file_tree(self) -> None:
        """Refresh the file tree when files change."""
        try:
            # Clear the tree
            tree = self.query_one("#file-tree", Tree)
            tree.root.children.clear()
            
            # Rebuild it from the working directory
            self._add_tree_items(tree.root, self.working_dir)
        except Exception:
            pass  # Silently fail if tree refresh fails
    
    def build_file_tree(self) -> None:
        """Build the file tree from the working directory."""
        try:
            tree = self.query_one("#file-tree", Tree)
            # Update the root label to show the working directory
            working_dir_name = self.working_dir.name or str(self.working_dir)
            tree.root.label = working_dir_name
            
            # Recursively add items to tree
            self._add_tree_items(tree.root, self.working_dir)
        except Exception as e:
            pass  # Silently fail if tree building fails
    
    def _add_tree_items(self, parent_node, directory: Path) -> None:
        """Recursively add directory items to the tree."""
        items = scan_directory(directory, relative_to=directory)
        
        for display_name, path_str, is_dir, entry_path in items:
            node = parent_node.add(display_name, expand=False)
            node.data = path_str  # Store the relative path
            
            # If it's a directory, recursively add children
            if is_dir:
                try:
                    self._add_tree_items(node, entry_path)
                except (PermissionError, OSError):
                    pass

    def update_model_display(self):
        model = self.registry.get_active_model()
        model_name = model.name if model else "None Configured"
        self.query_one("#current-model", Static).update(model_name)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_input = event.value
        if not user_input:
            return

        input_widget = self.query_one("#user-input", Input)
        input_widget.value = ""
        
        # Add user message to display
        self.add_message("user", user_input)
        # Scroll to bottom after user message
        self.scroll_to_bottom()
        
        # Show loading indicator
        thinking_msg = Message("response", "Thinking...", {"loading": True})
        self.loading_widget = self.query_one("#messages", Vertical).mount(thinking_msg)
        self.scroll_to_bottom()
        
        # Run agent engine
        first_response = True
        try:
            async for step in self.engine.run(user_input):
                if step.step_type == "user":
                    continue # Already added
                
                # Remove loading indicator on first response
                if first_response:
                    if hasattr(self, 'loading_widget'):
                        # Remove the loading widget by finding and removing it
                        messages_container = self.query_one("#messages", Vertical)
                        # Find and remove the loading widget
                        for widget in messages_container.children:
                            if hasattr(widget, 'role') and widget.role == "response" and hasattr(widget, 'metadata') and widget.metadata and widget.metadata.get("loading"):
                                widget.remove()
                                break
                        del self.loading_widget
                    first_response = False
                
                self.add_message(step.step_type, step.content, step.metadata)
                
                # Refresh file tree if a write operation was performed
                if step.step_type == "function" and step.metadata and step.metadata.get("function") == "writeToFile":
                    await self.refresh_file_tree()
                
                # Auto-scroll to bottom
                self.scroll_to_bottom()
        except Exception as e:
            # Remove loading indicator if present
            if hasattr(self, 'loading_widget'):
                messages_container = self.query_one("#messages", Vertical)
                # Find and remove the loading widget
                for widget in messages_container.children:
                    if hasattr(widget, 'role') and widget.role == "response" and hasattr(widget, 'metadata') and widget.metadata and widget.metadata.get("loading"):
                        widget.remove()
                        break
                del self.loading_widget
            self.add_message("response", f"Agent Error: {str(e)}")
            self.scroll_to_bottom()

    def add_message(self, role: str, text: str, metadata: dict = None):
        msg = Message(role, text, metadata)
        self.query_one("#messages", Vertical).mount(msg)
    
    def scroll_to_bottom(self):
        # Simple approach: refresh the UI which should scroll to new content
        self.call_later(self._scroll_to_bottom)
    
    def _scroll_to_bottom(self):
        try:
            messages = self.query_one("#messages", Vertical)
            # Scroll to bottom by focusing the last child
            if messages.children:
                last_child = messages.children[-1]
                last_child.scroll_visible()
        except Exception:
            pass  # Ignore scroll errors

    def clear_chat(self):
        messages_container = self.query_one("#messages", Vertical)
        for child in list(messages_container.children):
            if isinstance(child, Message):
                child.remove()
        self.add_message("response", "Chat history cleared.")

    def on_app_command(self, command):
        # Handle model updates if needed
        if command == "update_model":
            self.update_model_display()
    
    def on_tree_select(self, event: Tree.Selected) -> None:
        """Handle file selection in the tree - insert path into chat input."""
        node = event.node
        if node.data:  # Only if it has a path
            file_path = node.data
            # Check if it's a file (not a directory)
            input_widget = self.query_one("#user-input", Input)
            current_text = input_widget.value.strip()
            
            # Append path to input
            if current_text:
                input_widget.value = current_text + f" {file_path}"
            else:
                input_widget.value = file_path
            
            # Focus the input for convenience
            input_widget.focus()
    
    def on_unmount(self) -> None:
        """Clean up file watcher when screen is removed."""
        try:
            if hasattr(self, 'tree_refresh_manager'):
                self.tree_refresh_manager.stop()
        except Exception:
            pass
