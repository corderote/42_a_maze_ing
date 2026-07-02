from mlx import Mlx  # type: ignore[import-untyped]
from typing import Any
from mazegen.maze import Maze


class MLX_Maze():
    """
    Manages the graphical layout parsing and drawing of a labyrinth structure.

    This coordinator tracks configuration files, handles runtime maze
    regenerations, manages active tile texture arrays, and maps logical
    abstract maze coordinates onto explicit 2D screen positions for rendering
    walls, paths, solution tracks, start anchors, and exit points.

    Attributes:
        _config_filepath (str): Class-level variable tracking the system file
            path to the labyrinth configuration schema.
        _pos (tuple[int, int]): Class-level offset coordinate pairing (X, Y)
            for positioning the printed maze canvas.
        _m (Any): Instance reference to the core MiniLibX graphics controller
            layer.
        _p (Any): Pointer connection address representing the initialized
            MiniLibX context.
        _w (Any): Pointer identifier targeting the active application display
            window.
        _maze (Maze): Core back-end data structure holding dimensions, cells,
            and paths.
        _img_lst (list[Any]): Collection of loaded graphical textures map
            records.
    """
    _config_filepath = ''
    _pos: tuple[int, int] = (0, 0)

    def __init__(self, m: Mlx, ptr: Any, window: Any,
                 maze: Maze, img_lst: list[str]) -> None:
        """
        Initializes the graphical maze rendering pipeline with runtime window
        contexts.

        Args:
            m (Mlx): Base graphics engine framework wrapper instance.
            ptr (Any): MiniLibX connection tracking identifier.
            window (Any): Destination window wrapper reference address.
            maze (Maze): Logical multi-dimensional layout puzzle object
                instance.
            img_lst (list[str]): Initialized image descriptor pointer
                structures sequence.
        """
        self._m: Any = m
        self._p: Any = ptr
        self._w: Any = window
        self._maze: Maze = maze
        self._img_lst = img_lst

    def gen_new_maze(self) -> None:
        """
        Triggers a puzzle data rebuild cycle utilizing the active
        configuration resource path.
        """
        if self._config_filepath != '':
            self._maze = Maze.generate_maze_output(self._config_filepath)

    def set_img_list(self, new_list: list[Any]) -> None:
        """
        Swaps the current reference tile image collection sequence out for an
        alternate set.

        Args:
            new_list (list[Any]): Sequence containing the new set of texture
                structures.
        """
        self._img_lst = new_list

    def set_config_filepath(self, new_filepath: str) -> None:
        """
        Registers an updated structural blueprint file layout target directory
        path.

        Args:
            new_filepath (str): Target physical text source resource location
                string.
        """
        self._config_filepath = new_filepath

    def set_maze_pos(self, new_pos: tuple[int, int]) -> None:
        """
        Adjusts the rendering margin offset coordinate positioning for
        structural grids.

        Args:
            new_pos (tuple[int, int]): Coordinate pixel location layout pair
                (X, Y).
        """
        self._pos = new_pos

    def get_maze_pos(self) -> tuple[int, int]:
        """
        Retrieves the layout offset location value where drawing routines
        place elements.

        Returns:
            tuple[int, int]: Screen positioning coordinate index data (X, Y).
        """
        return self._pos

    def _print_fixed(self, pos: tuple[int, int],
                     c_pos: tuple[int, int]) -> None:
        """
        Paints an immutable localized obstacle block configuration around
        static coordinates.

        Calculates localized sub-tile coordinate alignments matching grid
        block points, and updates a 3x3 fragment area with lock textures to
        denote structural anchors.

        Args:
            pos (tuple[int, int]): Root base canvas positioning offset
                coordinates.
            c_pos (tuple[int, int]): Logical grid indexing column and row map
                point.
        """
        img = self._img_lst[2]
        x = pos[0] + ((2*c_pos[0] + 1) * int(img[1]))
        y = pos[1] + ((2*c_pos[1] + 1) * int(img[2]))
        for fy in range(y - int(img[2]), y + int(img[2]) + 1, int(img[2])):
            for fx in range(x - int(img[1]), x + int(img[1]) + 1, int(img[1])):
                self._m.mlx_put_image_to_window(self._p, self._w,
                                                img[0], fx, fy)

    def mlx_print_maze(self, pos: tuple[int, int] = (0, 0)) -> None:
        """
        Deconstructs and parses abstract matrix items into concrete pixel tile
        map rows.

        Iterates sequentially across the vertical rows of the back-end
        labyrinth object.
        For each row index, it builds three separate sub-tile graphical bands
        (Top edge, Middle section, and Bottom edge) out of wall and path
        textures. After painting the standard geometry, it superimposes
        immutable block overlays over fixed cells.

        Args:
            pos (tuple[int, int]): Initial drawing anchor pixel offset.
                Defaults to (0, 0).
        """
        wall = self._img_lst[0]
        path = self._img_lst[1]
        for row in range(self._maze.get_height()):
            # TOP
            if row == 0:
                np = [pos[0], pos[1]]
                for col in range(self._maze.get_width()):
                    self._m.mlx_put_image_to_window(self._p, self._w,
                                                    wall[0], np[0], np[1])
                    np[0] += int(wall[1])
                    cell = self._maze.get_maze_cells()[(col, row)]
                    if cell.get_north() == 0:
                        self._m.mlx_put_image_to_window(self._p, self._w,
                                                        path[0], np[0], np[1])
                    else:
                        self._m.mlx_put_image_to_window(self._p, self._w,
                                                        wall[0], np[0], np[1])
                    np[0] += int(wall[1])
                self._m.mlx_put_image_to_window(self._p, self._w,
                                                wall[0], np[0], np[1])
                np[0] = pos[0]
                np[1] += int(wall[2])
            # Mid
            for col in range(self._maze.get_width()):
                # Right
                cell = self._maze.get_maze_cells()[(col, row)]
                if cell.get_west() == 0:
                    self._m.mlx_put_image_to_window(self._p, self._w,
                                                    path[0], np[0], np[1])
                else:
                    self._m.mlx_put_image_to_window(self._p, self._w,
                                                    wall[0], np[0], np[1])
                np[0] += int(wall[1])
                # Center
                if cell.walls == 15:
                    self._m.mlx_put_image_to_window(self._p, self._w,
                                                    wall[0], np[0], np[1])
                else:
                    self._m.mlx_put_image_to_window(self._p, self._w,
                                                    path[0], np[0], np[1])
                np[0] += int(wall[1])
            self._m.mlx_put_image_to_window(self._p, self._w,
                                            wall[0], np[0], np[1])
            np[0] = pos[0]
            np[1] += int(wall[2])
            # BOT
            for col in range(self._maze.get_width()):
                self._m.mlx_put_image_to_window(self._p, self._w,
                                                wall[0], np[0], np[1])
                np[0] += int(wall[1])
                cell = self._maze.get_maze_cells()[(col, row)]
                if cell.get_south() == 0:
                    self._m.mlx_put_image_to_window(self._p, self._w,
                                                    path[0], np[0], np[1])
                else:
                    self._m.mlx_put_image_to_window(self._p, self._w,
                                                    wall[0], np[0], np[1])
                np[0] += int(wall[1])
            self._m.mlx_put_image_to_window(self._p, self._w,
                                            wall[0], np[0], np[1])
            np[0] = pos[0]
            np[1] += int(wall[2])
        for p, cell in self._maze.get_maze_cells().items():
            if cell.fixed is True:
                self._print_fixed(pos, p)

    def mlx_print_path(self, pos: tuple[int, int] = (0, 0),
                       print_path: bool = True) -> None:
        """
        Draws navigation points, connecting route tracks, entry points, and
        targets.

        Projects the navigation route across screen coordinates when active.
        It loops through ordered navigation steps, calculates the path vector
        intersections to avoid visual breaking, and marks terminal anchors
        by overlaying individual Start and Exit indicators.

        Args:
            pos (tuple[int, int]): Canvas location layout placement offset.
                Defaults to (0, 0).
            print_path (bool): Visibility controller flag toggling path
                overlays. Defaults to True.
        """
        s_img = self._img_lst[3]
        e_img = self._img_lst[4]
        p_img = self._img_lst[5]
        x = (2*self._maze.start[0] + 1)*int(s_img[1]) + pos[0]
        y = (2*self._maze.start[1] + 1)*int(s_img[1]) + pos[1]
        # PATH
        if print_path:
            for cell in self._maze.path:
                x_p = (2*cell[0] + 1)*int(p_img[1]) + pos[0]
                y_p = (2*cell[1] + 1)*int(p_img[2]) + pos[1]
                self._m.mlx_put_image_to_window(self._p, self._w,
                                                p_img[0], x_p, y_p)
                x_aux = (x + x_p)//2
                y_aux = (y + y_p)//2
                self._m.mlx_put_image_to_window(self._p, self._w,
                                                p_img[0], x_aux, y_aux)
                x = x_p
                y = y_p
        # START
        x = (2*self._maze.start[0] + 1)*int(s_img[1]) + pos[0]
        y = (2*self._maze.start[1] + 1)*int(s_img[1]) + pos[1]
        self._m.mlx_put_image_to_window(self._p, self._w, s_img[0], x, y)
        # END
        x = (2*self._maze.exit[0] + 1)*int(e_img[1]) + pos[0]
        y = (2*self._maze.exit[1] + 1)*int(e_img[1]) + pos[1]
        self._m.mlx_put_image_to_window(self._p, self._w, e_img[0], x, y)
