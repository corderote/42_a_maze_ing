from mlx import Mlx  # type: ignore[import-untyped]
from typing import Any, Callable


class MLX_Button():
    def __init__(self, m: Mlx, ptr: Any, window: Any,
                 img: Any, pos: tuple[int, int]) -> None:
        self._pos: tuple[int, int] = pos
        self._m: Mlx = m
        self._p: Any = ptr
        self._w: Any = window
        self._current_img = img
        self._function: Callable[[], Any] = self._default_click

    def inside_button(self, pos: tuple[int, int]) -> bool:
        return (pos[0] > self._pos[0] and
                pos[0] < self._pos[0] + self._current_img[1] and
                pos[1] > self._pos[1] and
                pos[1] < self._pos[1] + self._current_img[2])

    def get_position(self) -> tuple[int, int]:
        return self._pos

    def set_function(self, function: Callable[[], Any]) -> None:
        self._function = function

    def click(self) -> None:
        self._function()

    def _default_click(self) -> None:
        print("Click")

    def print(self) -> None:
        self._m.mlx_put_image_to_window(self._p, self._w, self._current_img[0],
                                        self._pos[0], self._pos[1])

    def mlx_close_window(self) -> None:
        print("Cerrando.")
        self._m.mlx_destroy_window(self._p, self._w)
        self._m.mlx_loop_exit(self._p)
