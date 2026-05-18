#!/usr/bin/env python3
"""
Verification script for AI Agent TUI
Tests all imports and basic functionality before running the app
"""

import sys
import os

def test_imports():
    print("Testing imports...")
    try:
        from config.settings import AppConfig, ModelConfig, ModelProvider
        print("  ✓ Config settings")
        
        from config.models import ModelRegistry
        print("  ✓ Model registry")
        
        from config.storage import load_config, save_config
        print("  ✓ Config storage")
        
        from agent.models import GeminiProvider, LLMProvider
        print("  ✓ Agent models")
        
        from agent.core import AgentEngine, AgentStep
        print("  ✓ Agent core")
        
        from functions.function_map import callFunction
        from functions.schemas import avail_functions
        print("  ✓ Functions")
        
        from textual.app import App
        print("  ✓ Textual")
        
        from ui.app import AIAgentApp
        print("  ✓ UI app")
        
        from ui.screens.chat_screen import ChatScreen
        print("  ✓ Chat screen")
        
        from ui.screens.model_config_screen import ModelConfigScreen
        print("  ✓ Model config screen")
        
        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_registry():
    print("\nTesting ModelRegistry...")
    try:
        from config.models import ModelRegistry
        registry = ModelRegistry()
        models = registry.get_available_models()
        print(f"  ✓ Registry loaded ({len(models)} models)")
        return True
    except Exception as e:
        print(f"  ✗ Registry failed: {e}")
        return False

def test_agent_engine():
    print("\nTesting AgentEngine...")
    try:
        from config.models import ModelRegistry
        from agent.core import AgentEngine
        registry = ModelRegistry()
        engine = AgentEngine(registry)
        print("  ✓ AgentEngine instantiated")
        return True
    except Exception as e:
        print(f"  ✗ AgentEngine failed: {e}")
        return False

def main():
    print("=" * 50)
    print("AI Agent TUI - Verification Script")
    print("=" * 50)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Model Registry", test_registry()))
    results.append(("Agent Engine", test_agent_engine()))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n✓ All tests passed! You can run the app with: python __main__.py")
        return 0
    else:
        print("\n✗ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
