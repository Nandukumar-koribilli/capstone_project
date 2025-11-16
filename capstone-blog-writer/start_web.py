#!/usr/bin/env python
"""
Wrapper to start ADK web server with graphviz mock module.
"""
import sys
import types
import os

# Create a mock graphviz module
graphviz_module = types.ModuleType('graphviz')

class MockDigraph:
    """Mock Digraph class for graphviz."""
    def __init__(self, *args, **kwargs):
        pass
    
    def render(self, *args, **kwargs):
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass

graphviz_module.Digraph = MockDigraph

# Inject the mock graphviz module
sys.modules['graphviz'] = graphviz_module

print("[INFO] Graphviz mock module injected", file=sys.stderr)

# Set environment variables
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'False'
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCKXY6XAOUcd67_Ly3-IZwikj3_8RV_udc'

# Now import and run ADK
from google.adk.cli import main

if __name__ == '__main__':
    sys.argv = ['adk', 'web']
    main()
