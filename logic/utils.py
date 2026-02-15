def mask_string(text: str, visible_start: int=3, visible_end: int=2) -> str:
    
    #Replaces the middle of a string with asterisks
    if not text or len(text) <= (visible_start + visible_end):
        return '****'
    
    middle_len = len(text) - (visible_start + visible_end)
    return text[:visible_start] + ('*' * middle_len) + text[-visible_end:]