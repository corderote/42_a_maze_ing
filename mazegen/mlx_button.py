from mlx import Mlx  # type: ignore[import-untyped]
from typing import Any, Callable


class MLX_Button():
    """
    Represents an interactive graphical button wrapper for the MiniLibX
    framework.

    This class binds a visual asset (image component) to a specific screen
    location, manages interactive bounding box collision detection, and
    hooks click triggers to executable Python functions.

    Attributes:
        _pos (tuple[int, int]): Screen layout coordinates expressed as (X, Y).
        _m (Mlx): Instance reference to the Core MiniLibX graphics controller.
        _p (Any): Pointer address representing the initialized MiniLibX
            context structure.
        _w (Any): Pointer address representing the target screen window object.
        _current_img (Any): Structural asset data containing the image
            identifier pointer at index 0, pixel width at index 1, and height
            at index 2.
        _function (Callable[[], Any]): Execution hook invoked when the element
            is clicked.
    """
    def __init__(self, m: Mlx, ptr: Any, window: Any,
                 img: Any, pos: tuple[int, int]) -> None:
        """
        Initializes an interactive MLX graphic element with default callback
        parameters.

        Args:
            m (Mlx): Core framework context wrapper reference.
            ptr (Any): MiniLibX connection identifier.
            window (Any): Targets screen window reference pointer.
            img (Any): Loaded image descriptor sequence containing (image_ptr,
                width, height).
            pos (tuple[int, int]): Coordinate pair positioning the upper-left
                apex of the asset.
        """
        self._pos: tuple[int, int] = pos
        self._m: Mlx = m
        self._p: Any = ptr
        self._w: Any = window
        self._current_img = img
        self._function: Callable[[], Any] = self._default_click

    def inside_button(self, pos: tuple[int, int]) -> bool:
        """
        Evaluates mouse pointer collision bounds against the interactive asset
        profile.

        Calculates whether a 2D cursor location falls within the bounding box
        dimensions of the current visual layout asset.

        Args:
            pos (tuple[int, int]): Current cursor layout coordinates as (X, Y).

        Returns:
            bool: True if the mouse position resides within button borders;
                False otherwise.
        """
        return (pos[0] > self._pos[0] and
                pos[0] < self._pos[0] + self._current_img[1] and
                pos[1] > self._pos[1] and
                pos[1] < self._pos[1] + self._current_img[2])

    def get_position(self) -> tuple[int, int]:
        """
        Retrieves the upper-left coordinate index location of the element.

        Returns:
            tuple[int, int]: The screen position pair (X, Y).
        """
        return self._pos

    def set_function(self, function: Callable[[], Any]) -> None:
        """
        Assigns a custom behavior callback mechanism onto the button interface.

        Args:
            function (Callable[[], Any]): The function object to register as a
            handler.
        """
        self._function = function

    def click(self) -> None:
        """
        Dispatches and executes the current action hook bound to this
        interface element.
        """
        self._function()

    def _default_click(self) -> None:
        """
        Fallback internal action handler printed if zero custom overrides are
        provided.
        """
        print("Click")

    def print(self) -> None:
        """
        Pushes and paints the underlying graphic asset texture onto the
        MiniLibX window layout.
        """
        self._m.mlx_put_image_to_window(self._p, self._w, self._current_img[0],
                                        self._pos[0], self._pos[1])

    def mlx_close_window(self) -> None:
        """
        Destroys the current graphical window and forces clean framework
        execution termination.

        This method detaches the display context layer from active memory
        buffers and shuts down the structural MiniLibX background rendering
        loop safely.
        """
        print("Closing ...")
        self._m.mlx_destroy_window(self._p, self._w)
        self._m.mlx_loop_exit(self._p)
