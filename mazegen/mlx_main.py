#!/usr/bin/python3
from mlx import Mlx  # type: ignore[import-untyped]
from typing import Any, Callable
from mazegen.maze import Maze
from mazegen.mlx_maze import MLX_Maze
from mazegen.mlx_button import MLX_Button
from mazegen.constants import MLX_BUTTON_IMGS, MLX_MAZE_SPRITES


def path_click_function() -> tuple[Callable[[], None], Callable[[], bool]]:
    """
    Creates a closure state machine to toggle the visible path overlay.

    Encapulates a local scope boolean flag that toggles back and forth
    between true and false every time the actionable button handler is run.

    Returns:
        tuple[Callable[[], None], Callable[[], bool]]:
            - Index 0: Callback action execution hook that flips the
                visibility state.
            - Index 1: Read-only evaluation hook to safely read the current
                visibility.
    """
    with_path: bool = True

    def path_click() -> None:
        nonlocal with_path
        with_path = not with_path

    def get_path_bool() -> bool:
        return with_path

    return (path_click, get_path_bool)


def color_click_function() -> tuple[Callable[[], None], Callable[[], int]]:
    """
    Creates a closure state machine to toggle between available visual style
    themes.

    Encapsulates an internal count index variable within local scope, shifting
    the active value back and forth between available indexes (0 and 1) to swap
    active color profiles dynamically.

    Returns:
        tuple[Callable[[], None], Callable[[], int]]:
            - Index 0: Callback action execution hook that shifts the index
                count.
            - Index 1: Read-only evaluation hook to retrieve the current
                texture index.
    """
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
    """
    Clears the target active framework window and re-renders the complete
    frame state.

    This refresh pipeline empties the active context buffer, polls status
    indicators from closure hooks to bind matching skin/path textures, draws
    the static labyrinth grid layout, projects the calculated solution route,
    and cycles through structural interactive button arrays to paint
    individual graphical elements.

    Args:
        data (Any): Multi-type data sequence storing the core context:
                    [0] Mlx core context, [1] Pointer,
                    [2] Window layout context,[3] MLX_Maze,
                    [4] List of buttons, [5] Theme map,
                    [6] Path boolean hook, [7] Color index hook.
    """
    data[0].mlx_clear_window(data[1], data[2])
    data[3].set_img_list(data[5][data[7]()])
    data[3].mlx_print_maze(data[3].get_maze_pos())
    data[3].mlx_print_path(data[3].get_maze_pos(), data[6]())
    for btn in data[4]:
        btn.print()


def mouse_click(button: int, x: int, y: int, data: Any) -> None:
    """
    Dispatches and processes screen click collision interactions.

    Loops across registered interactive interface boundaries to map mouse
    position coordinates against bounding targets. If collision checks pass,
    the registered action click trigger executes.
    A full layout context update is called automatically unless the close/exit
    window routine is requested.

    Args:
        button (int): Numerical identifier for the mouse button clicked.
        x (int): Horizontal mouse coordinate position recorded upon clicking.
        y (int): Vertical mouse coordinate position recorded upon clicking.
        data (Any): Structured data sequence holding active context pointers
            and buttons list.
    """
    for b in data[4]:
        if b.inside_button((x, y)):
            b.click()
            if b is data[4][3]:
                return
    mlx_update(data)


def mlx_main_func(conf_filepath: str) -> None:
    """
    Initializes window managers, loads textures, registers inputs, and opens
    the loop.

    Acts as the primary entry pipeline for the window layout layer. It
    extracts dimensions, calculates responsive layout alignment padding, sets
    up asset paths, builds button profiles, hooks interactions to mouse
    inputs, and relinquishes application thread flow control directly over
    to the underlying MiniLibX frame processing loop handler.

    Args:
        conf_filepath (str): Physical system directory path pointing to the
            active `.txt` configuration file asset.
    """
    maze = Maze.generate_maze_output(conf_filepath)
    # Mlx
    m = Mlx()
    p = m.mlx_init()
    w_width = (maze.get_width()*2+1)*16
    w_height = (maze.get_height()*2+1)*16 + 80
    maze_pos: tuple[int, int] = (0, 0)
    button_pos_x = 0
    if w_width <= 640:
        maze_pos = ((640-w_width)//2, 0)
        w_width = 640
    else:
        button_pos_x = (w_width//2 - 320)
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
    mlx_maze.set_maze_pos(maze_pos)

    nb_img = m.mlx_png_file_to_image(p, MLX_BUTTON_IMGS[0])
    nb = MLX_Button(m, p, w, nb_img, (button_pos_x + 0, w_height - 80))
    nb.set_function(mlx_maze.gen_new_maze)

    pb_img = m.mlx_png_file_to_image(p, MLX_BUTTON_IMGS[1])
    pb = MLX_Button(m, p, w, pb_img, (button_pos_x + 160, w_height - 80))
    p_func = path_click_function()
    pb.set_function(p_func[0])

    cb_img = m.mlx_png_file_to_image(p, MLX_BUTTON_IMGS[2])
    cb = MLX_Button(m, p, w, cb_img, (button_pos_x + 320, w_height - 80))
    c_func = color_click_function()
    cb.set_function(c_func[0])

    eb_img = m.mlx_png_file_to_image(p, MLX_BUTTON_IMGS[3])
    eb = MLX_Button(m, p, w, eb_img, (button_pos_x + 480, w_height - 80))
    eb.set_function(eb.mlx_close_window)

    data = [m, p, w, mlx_maze,
            [nb, pb, cb, eb], img_dict, p_func[1], c_func[1]]
    m.mlx_mouse_hook(w, mouse_click, data)

    mlx_update(data)
    m.mlx_loop(p)
    m.mlx_release(p)
