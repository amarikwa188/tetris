from pygame.mixer import Sound


class AudioHandler:
    """Represents an instance of the audio handler."""
    def __init__(self) -> None:
        """Initializes an audio handler object."""
        self.click_sfx: Sound = Sound("assets/audio/click3.mp3")
        self.landed: Sound = Sound("assets/audio/landed.mp3")
        self.full_line: Sound = Sound("assets/audio/full_line.mp3")
        self.pause_click: Sound = Sound("assets/audio/click.mp3")