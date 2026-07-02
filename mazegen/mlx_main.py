#!/usr/bin/python3
from mlx import Mlx  # type: ignore[import-untyped]
from typing import Any, Callable
from mazegen.maze import Maze
from mazegen.mlx_maze import MLX_Maze
from mazegen.mlx_button import MLX_Button
from mazegen.constants import MLX_BUTTON_IMGS, MLX_MAZE_SPRITES


def path_click_function() -> tuple[Callable[[], None], Callable[[], bool]]:
    with_path: bool = True

    def path_click() -> None:
        nonlocal with_path
        with_path = not with_path

    def get_path_bool() -> bool:
        return with_path

    return (path_click, get_path_bool)


def color_click_function() -> tuple[Callable[[], None], Callable[[], int]]:
    count: int = 0

    def color_click() -> None:
        nonlocal count
        count += 1
        if count > 1:
            count = 0

    def get_color_idx() -> int:
        return count

    return (color_click, get_color_idx)


def mlx_update(data: Any) -> None:
    data[0].mlx_clear_window(data[1], data[2])
    data[3].set_img_list(data[5][data[7]()])
    data[3].mlx_print_maze()
    if data[6]() is True:
        data[3].mlx_print_path()
    for btn in data[4]:
        btn.print()


def mouse_click(button: int, x: int, y: int, data: Any) -> None:
    for b in data[4]:
        if b.inside_button((x, y)):
            b.click()
            if b is data[4][3]:
                return
            mlx_update(data)


def mlx_main_func(conf_filepath: str) -> None:
    maze = Maze.generate_maze_output(conf_filepath)
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
        img_lst.append(m.mlx_png_file_to_image(p, MLX_MAZE_SPRITES[nbr][0]))
        img_lst.append(m.mlx_png_file_to_image(p, MLX_MAZE_SPRITES[nbr][1]))
        img_lst.append(m.mlx_png_file_to_image(p, MLX_MAZE_SPRITES[nbr][2]))
        img_lst.append(m.mlx_png_file_to_image(p, MLX_MAZE_SPRITES[nbr][3]))
        img_lst.append(m.mlx_png_file_to_image(p, MLX_MAZE_SPRITES[nbr][4]))
        img_lst.append(m.mlx_png_file_to_image(p, MLX_MAZE_SPRITES[nbr][5]))
        img_dict[nbr] = img_lst

    mlx_maze = MLX_Maze(m, p, w, maze, img_dict[1])
    mlx_maze.set_config_filepath(conf_filepath)

    nb_img = m.mlx_png_file_to_image(p, MLX_BUTTON_IMGS[0])
    nb = MLX_Button(m, p, w, nb_img, (0, w_height - 80))
    nb.set_function(mlx_maze.gen_new_maze)

    pb_img = m.mlx_png_file_to_image(p, MLX_BUTTON_IMGS[1])
    pb = MLX_Button(m, p, w, pb_img, (160, w_height - 80))
    p_func = path_click_function()
    pb.set_function(p_func[0])

    cb_img = m.mlx_png_file_to_image(p, MLX_BUTTON_IMGS[2])
    cb = MLX_Button(m, p, w, cb_img, (320, w_height - 80))
    c_func = color_click_function()
    cb.set_function(c_func[0])

    eb_img = m.mlx_png_file_to_image(p, MLX_BUTTON_IMGS[3])
    eb = MLX_Button(m, p, w, eb_img, (480, w_height - 80))
    eb.set_function(eb.mlx_close_window)

    data = [m, p, w, mlx_maze,
            [nb, pb, cb, eb], img_dict, p_func[1], c_func[1]]
    m.mlx_mouse_hook(w, mouse_click, data)

    mlx_update(data)
    m.mlx_loop(p)
    m.mlx_release(p)
