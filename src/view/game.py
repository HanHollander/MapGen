from typing import Any
import pygame as pg
from pygame.event import Event
import pynkie as pk

from util import RMB, V2
from config import cfg


class GameView(pk.view.ScaledView):

    def __init__(self, viewport: pk.view.Viewport) -> None:
        pk.view.ScaledView.__init__(self, viewport)
        # mouse related
        self.mouse_pos: V2[int] = V2(0, 0)
        self.mouse_down: tuple[bool, bool, bool] = (False, False, False)
        self.zoom = 1

    # utility

    def move_viewport(self, diff: V2[int | float]) -> None:
        self.viewport.camera.x = self.viewport.camera.x + round(diff[0])
        self.viewport.camera.y = self.viewport.camera.y + round(diff[1])

    def get_mouse_pos_offset(self)-> V2[int]:
        return V2(*pg.mouse.get_pos()) + V2(*self.viewport.camera.topleft)

    # drawing

    # override ScaledView.draw
    def draw(self, surface: pg.Surface, *_: Any) -> list[pg.Rect]:  
        w: int = self.view_surface.get_width()
        h: int = self.view_surface.get_height()  
        self.view_surface.blit(self.background, pg.Rect(0, 0, w, h), None, 0)  
        surface.blit(self.view_surface, (0, 0))
        return []

    # event handling

    def handle_event(self, event: Event) -> None:
        pk.view.ScaledView.handle_event(self, event)
        match event.type:
            case pg.MOUSEBUTTONDOWN:
                self.on_mouse_down(event)
            case pg.MOUSEBUTTONUP:
                self.on_mouse_up(event)
            case pg.MOUSEMOTION:
                self.on_mouse_motion(event)
            case pg.MOUSEWHEEL:
                self.on_mouse_wheel(event)
            case _: pass    

    def on_mouse_down(self, event: pg.event.Event) -> None:
        self.mouse_down = pg.mouse.get_pressed()
        pk.debug.debug["Mouse down"] = self.mouse_down
    
    def on_mouse_up(self, event: pg.event.Event) -> None:
        self.mouse_down = pg.mouse.get_pressed()
        pk.debug.debug["Mouse down"] = self.mouse_down

    def on_mouse_motion(self, event: pg.event.Event) -> None:
        new_mouse_pos: V2[int] = V2(*pg.mouse.get_pos())
        pk.debug.debug["Mouse pos (screen, real)"] = [new_mouse_pos, self.get_mouse_pos_offset()]
        if (self.mouse_down[RMB]):
            mouse_diff: V2[int] = self.mouse_pos - new_mouse_pos
            self.move_viewport(V2(cfg.DRAG_MOVE_FACTOR * mouse_diff[0], cfg.DRAG_MOVE_FACTOR * mouse_diff[1]))
        self.mouse_pos = new_mouse_pos

    def on_mouse_wheel(self, event: pg.event.Event) -> None:
        # -1: zoom out, 1: zoom in
        scale: float = 1 / cfg.ZOOM_STEP_FACTOR if event.y == -1 else cfg.ZOOM_STEP_FACTOR
        self.zoom *= scale
        pk.debug.debug["Zoom scale"] = self.zoom
    
        mouse_px: V2[int] = V2(*pg.mouse.get_pos()) + V2(*self.viewport.camera.topleft)
        diff_px: V2[float] = V2(mouse_px[0] * scale - mouse_px[0], mouse_px[1] * scale - mouse_px[1])
        self.move_viewport(diff_px)

    
            


