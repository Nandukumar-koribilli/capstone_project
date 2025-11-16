"""
Patch to make graphviz optional in ADK web server.
This allows the web server to run even if Graphviz is not installed.
"""

import sys
import types

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

# Inject the mock graphviz module into sys.modules before importing ADK
sys.modules['graphviz'] = graphviz_module

print("[INFO] Graphviz mock module loaded successfully", file=sys.stderr)
