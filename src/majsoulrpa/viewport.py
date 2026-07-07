from majsoulrpa.constants import BASE_VIEWPORT_HEIGHT, BASE_VIEWPORT_WIDTH


def viewport_width_for_height(height: int) -> int:
    return round(height * BASE_VIEWPORT_WIDTH / BASE_VIEWPORT_HEIGHT)
