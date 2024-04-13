from configparser import ConfigParser, SectionProxy
from pathlib import Path
import pygame as pg

from util import V2

class cfg:

    @staticmethod
    def init() -> None:
        cfg.read_general_config()

    # ==== GENERAL ==== #
    DEBUG_INFO: bool
    MAX_FRAMERATE: int
    USE_DEFAULT_CURSOR: bool
    PROFILE: bool

    SCREEN_WIDTH: int
    SCREEN_HEIGHT: int

    DRAG_MOVE_FACTOR: float
    ZOOM_STEP_FACTOR: float
    ZOOM_MOVE_FACTOR: float

    @staticmethod
    def read_general_config() -> None:
        config: ConfigParser = ConfigParser()
        config.read(Path(__file__).parent / "../config/general.cfg")

        general: SectionProxy = config["general"]
        cfg.DEBUG_INFO = general.getboolean("DEBUG_INFO")
        cfg.MAX_FRAMERATE = general.getint("MAX_FRAMERATE")
        cfg.USE_DEFAULT_CURSOR = general.getboolean("USE_DEFAULT_CURSOR")
        cfg.PROFILE = general.getboolean("PROFILE")

        screen: SectionProxy = config["screen"]
        cfg.SCREEN_WIDTH = screen.getint("SCREEN_WIDTH")
        cfg.SCREEN_HEIGHT = screen.getint("SCREEN_HEIGHT")

        view: SectionProxy = config["view"]
        cfg.DRAG_MOVE_FACTOR = view.getfloat("DRAG_MOVE_FACTOR")
        cfg.ZOOM_STEP_FACTOR = view.getfloat("ZOOM_STEP_FACTOR")
        cfg.ZOOM_MOVE_FACTOR = view.getfloat("ZOOM_MOVE_FACTOR")