import colorsys

def adjust_colour(hex_color, saturation_factor=1.4, value_factor=0.85):
    """
    Adjusts the saturation and brightness of a color.
    
    :param hex_color: Color in hex format, e.g., "#4DB3C8"
    :param saturation_factor: >1 increases saturation, <1 decreases
    :param value_factor: >1 brighter, <1 darker
    :return: Adjusted color as hex string
    """
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Convert RGB to HSV
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    
    # Adjust saturation and value
    s = max(0, min(s * saturation_factor, 1))
    v = max(0, min(v * value_factor, 1))
    
    # Convert back to RGB
    r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
    
    # Convert to hex
    return f"#{int(r_new*255):02X}{int(g_new*255):02X}{int(b_new*255):02X}"
