import sys
import types

# Provide a dummy google.genai module to avoid ImportError during tests
if 'google' not in sys.modules:
    google_mod = types.ModuleType('google')
    sys.modules['google'] = google_mod
else:
    google_mod = sys.modules['google']

if not hasattr(google_mod, 'genai'):
    google_mod.genai = types.ModuleType('genai')
