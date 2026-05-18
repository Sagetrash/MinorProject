"""Utilities for building and managing file tree UI."""

from pathlib import Path
from typing import List, Callable, Optional
import asyncio

# Try to import watchdog for file system watching
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    # Provide stub classes if watchdog is not available
    class FileSystemEventHandler:
        pass
    class Observer:
        pass

# Directories and files to exclude from tree
EXCLUDE_DIRS = {
    "__pycache__",
    ".venv",
    "venv",
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    ".egg-info",
    "dist",
    "build",
}

EXCLUDE_FILES = {
    ".env",
    ".pyc",
    ".gitignore",
    ".gitkeep",
}


def should_exclude(path: Path) -> bool:
    """Check if a path should be excluded from the tree."""
    name = path.name
    
    # Exclude specific directories
    if path.is_dir() and name in EXCLUDE_DIRS:
        return True
    
    # Exclude specific files
    if path.is_file() and name in EXCLUDE_FILES:
        return True
    
    # Exclude hidden files except .env.example
    if name.startswith(".") and name not in {".env.example"}:
        return True
    
    return False


def get_file_icon(path: Path) -> str:
    """Get a simple text icon for a file/directory."""
    if path.is_dir():
        return "[DIR]"
    
    suffix = path.suffix.lower()
    extensions = {
        ".py": "[PY]",
        ".json": "[JSON]",
        ".toml": "[TOML]",
        ".yaml": "[YAML]",
        ".yml": "[YAML]",
        ".md": "[MD]",
        ".txt": "[TXT]",
        ".tcss": "[CSS]",
        ".sh": "[SH]",
        ".env": "[ENV]",
    }
    
    return extensions.get(suffix, "[FILE]")


def scan_directory(root_path: Path, relative_to: Path = None) -> List[tuple]:
    """
    Recursively scan directory and return list of (name, path_str, is_dir) tuples.
    Sorted with directories first, then alphabetically.
    """
    if relative_to is None:
        relative_to = root_path
    
    items = []
    
    try:
        entries = sorted(root_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        
        for entry in entries:
            if should_exclude(entry):
                continue
            
            rel_path = entry.relative_to(relative_to)
            path_str = str(rel_path).replace("\\", "/")
            icon = get_file_icon(entry)
            display_name = f"{icon} {entry.name}"
            
            items.append((display_name, path_str, entry.is_dir(), entry))
    
    except (PermissionError, OSError):
        pass
    
    return items


if WATCHDOG_AVAILABLE:
    class FileTreeWatcher(FileSystemEventHandler):
        """Watches for file system changes and triggers refresh callbacks."""
        
        def __init__(self, on_change: Callable, watch_path: Path):
            self.on_change = on_change
            self.watch_path = watch_path
            self._debounce_timer = None
            self._debounce_delay = 0.5  # Delay in seconds to avoid multiple rapid refreshes
        
        def _should_notify(self, event) -> bool:
            """Check if this event should trigger a refresh."""
            # Ignore excluded paths
            try:
                path = Path(event.src_path)
                if should_exclude(path):
                    return False
                # Ignore events in excluded directories
                for part in path.parts:
                    if part in EXCLUDE_DIRS:
                        return False
                return True
            except:
                return False
        
        def _trigger_refresh(self):
            """Debounced refresh trigger."""
            if self._debounce_timer:
                self._debounce_timer.cancel()
            
            self._debounce_timer = asyncio.Timer(
                self._debounce_delay,
                lambda: asyncio.run_coroutine_threadsafe(self.on_change(), asyncio.get_event_loop()).result()
            )
            self._debounce_timer.start()
        
        def on_created(self, event):
            if self._should_notify(event):
                self._trigger_refresh()
        
        def on_modified(self, event):
            if self._should_notify(event) and not event.is_directory:
                self._trigger_refresh()
        
        def on_deleted(self, event):
            if self._should_notify(event):
                self._trigger_refresh()
        
        def stop(self):
            """Stop the watcher and cancel any pending timers."""
            if self._debounce_timer:
                self._debounce_timer.cancel()


    class TreeRefreshManager:
        """Manages file system watching and tree refresh."""
        
        def __init__(self, watch_path: Path, on_change: Callable):
            self.watch_path = watch_path
            self.on_change = on_change
            self.observer: Optional[Observer] = None
            self.watcher: Optional[FileTreeWatcher] = None
        
        def start(self):
            """Start watching for file changes."""
            try:
                self.watcher = FileTreeWatcher(self.on_change, self.watch_path)
                self.observer = Observer()
                self.observer.schedule(self.watcher, str(self.watch_path), recursive=True)
                self.observer.start()
            except Exception as e:
                pass  # Silently fail if watchdog isn't available
        
        def stop(self):
            """Stop watching for file changes."""
            try:
                if self.watcher:
                    self.watcher.stop()
                if self.observer:
                    self.observer.stop()
                    self.observer.join()
            except Exception:
                pass
else:
    # Provide stub classes if watchdog is not available
    class FileTreeWatcher:
        def __init__(self, *args, **kwargs):
            pass
        def start(self):
            pass
        def stop(self):
            pass
    
    class TreeRefreshManager:
        def __init__(self, *args, **kwargs):
            pass
        def start(self):
            pass
        def stop(self):
            pass
