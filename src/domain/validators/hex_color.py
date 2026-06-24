from domain.value_objects.hex_color import HexColor

def validate_hex_color(value: str):
    try:
        hx = HexColor(value)
        return str(hx)
    except ValueError as e:
        raise ValueError("The color format is not supported. Use a valid hex color format.")
