from mlx import Mlx
from typing import Any, Callable


class MLX_Button():
    def __init__(self, m: Mlx, ptr, window, img, pos: tuple[int, int]) -> None:
        self._pos: tuple[int, int] = pos
        self._m: Mlx = m
        self._p: Any = ptr
        self._w: Any = window
        self._current_img = img
        self._function: Callable = self._default_click

    def inside_button(self, pos: tuple[int, int]) -> bool:
        return (pos[0] > self._pos[0] and 
                pos[0] < self._pos[0] + self._current_img[1] and
                pos[1] > self._pos[1] and 
                pos[1] < self._pos[1] + self._current_img[2])

    def get_position(self):
        return self._pos

    def set_function(self, function: Callable):
        self._function = function

    def click(self):
        self._function()

    def _default_click(self):
        print("Click")

    def print(self) -> None:
        self._m.mlx_put_image_to_window(self._p, self._w, self._current_img[0], self._pos[0], self._pos[1])

    def mlx_close_window(self) -> None:
        print("Cerrando.")
        self._m.mlx_destroy_window(self._p,self._w)
        self._m.mlx_loop_exit(self._p)


def mouse_click(button, x, y, button_list:list[MLX_Button]):
    for b in button_list:
        if b.inside_button((x, y)):
            print(f"[{button}] ", end='')
            b.click()


if __name__ == "__main__":
    m = Mlx()
    p = m.mlx_init()
    w = m.mlx_new_window(p, 320, 320, "MLX Buttons")

    eb = m.mlx_png_file_to_image(p, "Images/exit_button.png")

    button = MLX_Button(m, p, w, eb, (80, 80))
    button.set_function(button.mlx_close_window)

    m.mlx_clear_window(p, w)

    m.mlx_mouse_hook(w, mouse_click, [button])

    button.print()
    m.mlx_loop(p)
    m.mlx_release(p)
