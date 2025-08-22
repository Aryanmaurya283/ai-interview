from typing import Dict

# In-memory storage for resume texts. Key: client_uid, Value: resume_text
# Note: This is a simple solution for PoC. For production, use a more persistent storage.
resume_texts: Dict[str, str] = {}
