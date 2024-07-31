def text_formatter(text: str) -> str:
    """
    Reformats the text param for output. Changes the logical operations in the output
    Changes
        '>>' -> '⊃'
        '~' -> '¬'
        '&' -> '∧'
        '|' -> '∨'

    Args:
        text: text to be reformatted

    Returns:
        reformatted text
    """

    if not isinstance(text, str):
        return ''

    text = text.replace('>>', '⊃')
    text = text.replace('~', '¬')
    text = text.replace('&', '∧')
    text = text.replace('|', '∨')
    return text
