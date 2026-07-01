from maze import Maze
from mlx import Mlx
from typing import Any

class MLX_Maze():
    
    def __init__(self, m, ptr, window, maze, img_lst) -> None:
        self._m: Any = m
        self._p: Any = ptr
        self._w: Any = window
        self._maze: Maze = maze
        self._img_dict = img_lst
        
    def set_img_list(self, new_list:list[Any]):
        self._img_lst = new_list

    def _print_fixed(self, pos: tuple[int, int], cell_pos: tuple[int, int]):
        fixed = self._img_lst[2]
        x = pos[0] + ((2*cell_pos[0] + 1) * fixed[1])
        y = pos[1] + ((2*cell_pos[1] + 1) * fixed[2])
        for fy in range(y - fixed[2], y + fixed[2] + 1, fixed[2]):
            for fx in range(x - fixed[1], x + fixed[1] + 1, fixed[1]):
                self._m.mlx_put_image_to_window(self._p, self._w, fixed[0], fx, fy)

    def mlx_print_maze(self, pos: tuple[int, int] = (0, 0)) -> None:
        wall = self._img_lst[0]
        path = self._img_lst[1]
        for row in range(self._maze.get_height()):
            # TOP
            if row == 0:
                np = [pos[0], pos[1]]
                for col in range(self._maze.get_width()):
                    self._m.mlx_put_image_to_window(self._p, self._w, wall[0], np[0], np[1])
                    np[0] += wall[1]
                    cell = self._maze._grid[(col, row)]
                    if cell.get_north() == 0:
                        self._m.mlx_put_image_to_window(self._p, self._w, path[0], np[0], np[1])
                    else:
                        self._m.mlx_put_image_to_window(self._p, self._w, wall[0], np[0], np[1])
                    np[0] += wall[1]
                self._m.mlx_put_image_to_window(self._p, self._w, wall[0], np[0], np[1])
                np[0] = pos[0]
                np[1] += wall[2]
            # Mid
            for col in range(self._maze.get_width()):
                # Right
                cell = self._maze._grid[(col, row)]
                if cell.get_west() == 0:
                    self._m.mlx_put_image_to_window(self._p, self._w, path[0], np[0], np[1])
                else:
                    self._m.mlx_put_image_to_window(self._p, self._w, wall[0], np[0], np[1])
                np[0] += wall[1]
                # Center
                if cell.walls == 15:
                    self._m.mlx_put_image_to_window(self._p, self._w, wall[0], np[0], np[1])
                else:
                    self._m.mlx_put_image_to_window(self._p, self._w, path[0], np[0], np[1])
                np[0] += wall[1]
            #MAY NEED TO CHECK EAST HERE.
            self._m.mlx_put_image_to_window(self._p, self._w, wall[0], np[0], np[1])
            np[0] = pos[0]
            np[1] += wall[2]
            # BOT
            for col in range(self._maze.get_width()):
                self._m.mlx_put_image_to_window(self._p, self._w, wall[0], np[0], np[1])
                np[0] += wall[1]
                cell = self._maze._grid[(col, row)]
                if cell.get_south() == 0:
                    self._m.mlx_put_image_to_window(self._p, self._w, path[0], np[0], np[1])
                else:
                    self._m.mlx_put_image_to_window(self._p, self._w, wall[0], np[0], np[1])
                np[0] += wall[1]
            self._m.mlx_put_image_to_window(self._p, self._w, wall[0], np[0], np[1])
            np[0] = pos[0]
            np[1] += wall[2]
        for p, cell in self._maze._grid.items():
            if cell.fixed is True:
                self._print_fixed(pos, p)

    def mlx_print_path(self, pos: tuple[int, int] = (0, 0)):
        s_img = self._img_lst[3]
        e_img = self._img_lst[4]
        p_img = self._img_lst[5]
        #START
        x = (2*self._maze._start[0] + 1)*s_img[1] + pos[0]
        y = (2*self._maze._start[1] + 1)*s_img[1] + pos[1]
        self._m.mlx_put_image_to_window(self._p, self._w, s_img[0], x, y)
        # PATH
        for cell in self._maze._path:
            x_p = (2*cell[0] + 1)*p_img[1] + pos[0]
            y_p = (2*cell[1] + 1)*p_img[1] + pos[1]
            self._m.mlx_put_image_to_window(self._p, self._w, p_img[0], x_p, y_p)
            x_aux = (x + x_p)//2
            y_aux = (y + y_p)//2
            self._m.mlx_put_image_to_window(self._p, self._w, p_img[0], x_aux, y_aux)
            x = x_p
            y = y_p
        #END
        x = (2*self._maze._end[0] + 1)*e_img[1] + pos[0]
        y = (2*self._maze._end[1] + 1)*e_img[1] + pos[1]
        self._m.mlx_put_image_to_window(self._p, self._w, e_img[0], x, y)


if __name__ == "__main__":
    # Maze
    maze = Maze.load_from_file("example_maze.txt")
    
    # Mlx
    m = Mlx()
    p = m.mlx_init()
    w_width = (maze.get_width()*2+1)*16
    w_height = (maze.get_height()*2+1)*16 + 50
    w = m.mlx_new_window(p, w_width, w_height, "test")

    imgs = []
    imgs.append(m.mlx_png_file_to_image(p, "Images/wall_0.png"))
    imgs.append(m.mlx_png_file_to_image(p, "Images/path_0.png"))
    imgs.append(m.mlx_png_file_to_image(p, "Images/fixed_0.png"))
    imgs.append(m.mlx_png_file_to_image(p, "Images/start_0.png"))
    imgs.append(m.mlx_png_file_to_image(p, "Images/end_0.png"))
    imgs.append(m.mlx_png_file_to_image(p, "Images/solution_0.png"))

    mlx_maze = MLX_Maze(m, p, w, maze, imgs)
    m.mlx_clear_window(p, w)
    mlx_maze.mlx_print_maze()
    mlx_maze.mlx_print_path()
    m.mlx_loop(p)
