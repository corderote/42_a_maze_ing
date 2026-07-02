from mlx import Mlx  # type: ignore[import-untyped]
from typing import Any
from mazegen.maze import Maze


class MLX_Maze():
    _config_filepath = ''
    _pos: tuple[int, int] = (0, 0)

    def __init__(self, m: Mlx, ptr: Any, window: Any,
                 maze: Maze, img_lst: list[str]) -> None:
        self._m: Any = m
        self._p: Any = ptr
        self._w: Any = window
        self._maze: Maze = maze
        self._img_lst = img_lst

    def gen_new_maze(self) -> None:
        if self._config_filepath != '':
            self._maze = Maze.generate_maze_output(self._config_filepath)

    def set_img_list(self, new_list: list[Any]) -> None:
        self._img_lst = new_list

    def set_config_filepath(self, new_filepath: str) -> None:
        self._config_filepath = new_filepath

    def set_maze_pos(self, new_pos: tuple[int, int]) -> None:
        self._pos = new_pos

    def get_maze_pos(self) -> tuple[int, int]:
        return self._pos

    def _print_fixed(self, pos: tuple[int, int],
                     c_pos: tuple[int, int]) -> None:
        img = self._img_lst[2]
        x = pos[0] + ((2*c_pos[0] + 1) * int(img[1]))
        y = pos[1] + ((2*c_pos[1] + 1) * int(img[2]))
        for fy in range(y - int(img[2]), y + int(img[2]) + 1, int(img[2])):
            for fx in range(x - int(img[1]), x + int(img[1]) + 1, int(img[1])):
                self._m.mlx_put_image_to_window(self._p, self._w,
                                                img[0], fx, fy)

    def mlx_print_maze(self, pos: tuple[int, int] = (0, 0)) -> None:
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
