from string import Template

class PromptTemplates:
    SYSTEM_DEFAULT = "You are a helpful AI assistant."
    RAG_QA = """Answer the question based on the context below. If you don't know, say so.
    
    Context:
    $context
    
    Question:
    $question
    """
