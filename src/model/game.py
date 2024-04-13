import sys
from config import cfg
import pygame as pg
import pynkie as pk

from util import V2
from view.game import GameView


class Game(pk.model.Model):

    def __init__(self, view: GameView, pynkie: pk.run.Pynkie) -> None:
        pk.model.Model.__init__(self)
        self.view: GameView = view
        self.keys_down: set[int] = set()        
        self.pynkie: pk.run.Pynkie = pynkie
        self.min_fps: int = cfg.MAX_FRAMERATE
        self.max_fps: int = 0

    def update(self, dt: float) -> None:
        if dt > 0:
            fps: int = round(1 / dt)
            if fps < self.min_fps: self.min_fps = fps
            if fps > self.max_fps: self.max_fps = fps
        pk.debug.debug["FPS min/max"] = (self.min_fps, self.max_fps)

    def handle_event(self, event: pg.event.Event) -> None:
        pk.model.Model.handle_event(self, event)
        match event.type:
            case pg.KEYDOWN:
                self.on_key_down(event)
            case pg.KEYUP:
                self.on_key_up(event)
            case pg.MOUSEMOTION:
                self.on_mouse_motion(event)
            case _: pass

    def on_key_down(self, event: pg.event.Event) -> None:
        self.keys_down.add(event.key)
        if event.key == pg.K_q:
            pg.quit()
            sys.exit()
        if event.key == pg.K_f:
            self.min_fps = cfg.MAX_FRAMERATE
            self.max_fps = 0
        if event.key == pg.K_d:
            self.pynkie.set_debug_info(not self.pynkie.debug_info)
    
    def on_key_up(self, event: pg.event.Event) -> None:
        self.keys_down.remove(event.key)

    def on_mouse_motion(self, event: pg.event.Event) -> None:
        pos: V2[int] = V2(*pg.mouse.get_pos())
        offset: V2[int] = V2(*self.view.viewport.camera.topleft)
        pk.debug.debug["Mouse position"] = pos
        pk.debug.debug["Camera offset"] = offset