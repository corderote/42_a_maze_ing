#!/usr/bin/python3
from mlx import Mlx
from maze import Maze
from mlx_maze import MLX_Maze
from mlx_button import MLX_Button, mouse_click
from typing import Any, Callable


def path_click_function() -> tuple[Callable[[], None], Callable[[], bool]]:
    with_path:bool = True

    def path_click() -> None:
        nonlocal with_path
        with_path = not with_path

    def get_path_bool() -> bool:
        nonlocal with_path
        return with_path

    return (path_click, get_path_bool)


def color_click_function() -> tuple[Callable[[], None], Callable[[], bool]]:
    count: int = 0

    def color_click() -> None:
        nonlocal count
        count += 1
        if count > 1:
            count = 0

    def get_color_idx() -> bool:
        nonlocal count
        return count

    return (color_click, get_color_idx)

def mlx_update(data):
    data[0].mlx_clear_window(data[1], data[2])
    data[3].set_img_list(data[5][data[7]()])
    data[3].mlx_print_maze()
    if data[6]() is True:
        data[3].mlx_print_path()
    for btn in data[4]:
        btn.print()


def mouse_click(button, x, y, data):
    for b in data[4]:
        if b.inside_button((x, y)):
            b.click()
            if b is data[4][3]:
                return
            mlx_update(data)


if __name__ == "__main__":
    # Maze
    maze = Maze.generate_maze_output()
    
    # Mlx
    m = Mlx()
    p = m.mlx_init()
    w_width = (maze.get_width()*2+1)*16
    w_height = (maze.get_height()*2+1)*16 + 80
    if w_width < 640:
        w_width = 640
    w = m.mlx_new_window(p, w_width, w_height, "test")

    img_dict = {}
    for nbr in range(0, 2):
        img_lst = []
        img_lst.append(m.mlx_png_file_to_image(p, f"Images/wall_{nbr}.png"))
        img_lst.append(m.mlx_png_file_to_image(p, f"Images/path_{nbr}.png"))
        img_lst.append(m.mlx_png_file_to_image(p, f"Images/fixed_{nbr}.png"))
        img_lst.append(m.mlx_png_file_to_image(p, f"Images/start_{nbr}.png"))
        img_lst.append(m.mlx_png_file_to_image(p, f"Images/end_{nbr}.png"))
        img_lst.append(m.mlx_png_file_to_image(p, f"Images/solution_{nbr}.png"))
        img_dict[nbr] = img_lst

    mlx_maze = MLX_Maze(m, p, w, maze, img_dict[1])
    
    nb_img = m.mlx_png_file_to_image(p, "Images/new_button.png")
    nb = MLX_Button(m, p, w, nb_img, (0, w_height - 80))
    nb.set_function(mlx_maze.gen_new_maze)

    pb_img = m.mlx_png_file_to_image(p, "Images/path_button.png")
    pb = MLX_Button(m, p, w, pb_img, (160, w_height - 80))
    p_func = path_click_function()
    pb.set_function(p_func[0])

    cb_img = m.mlx_png_file_to_image(p, "Images/color_button.png")
    cb = MLX_Button(m, p, w, cb_img, (320, w_height - 80))
    c_func = color_click_function()
    cb.set_function(c_func[0])


    eb_img = m.mlx_png_file_to_image(p, "Images/exit_button.png")
    eb = MLX_Button(m, p, w, eb_img, (480, w_height - 80))
    eb.set_function(eb.mlx_close_window)

    data = [m, p, w, mlx_maze, [nb, pb, cb, eb], img_dict, p_func[1], c_func[1]]
    m.mlx_mouse_hook(w, mouse_click, data)

    mlx_update(data)
    m.mlx_loop(p)
    m.mlx_release(p)