from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import pandas as pd

# Define useful parameters
IMAGE_WIDTH = 1400
WIDTH = 1700
IMAGE_HEIGHT = 602
HEIGHT = 700
LENGTH = 14

COLORS = {0: "none", 1: "white", 2: "green", 3: "red"}  # 열린 목록 닫힌 목록 길 등은 나중에 추가


class CamelPathFinding:
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.coordinates = pd.DataFrame()
        self.x_coordinates = []
        self.y_coordinates = []
        self.mapSE = None
        self.mapSW = None
        self.mapNE = None
        self.mapNW = None
        self.file_name = None
        self.board = None
        self.img_canvas = None
        self.photo = None
        self.img_frame = None
        self.horizontal_step_count = 100
        self.vertical_step_count = IMAGE_HEIGHT // (IMAGE_WIDTH // self.horizontal_step_count)
        self.left = 0
        self.right = 1400
        self.up = 0
        self.down = 602
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("AStarPathFinding")
        self.pnu_logo = Image.open("Logo/pnu_logo.png")
        self.pnu_resize = self.pnu_logo.resize((338, 85))
        self.pnu = ImageTk.PhotoImage(self.pnu_resize)
        self.camel_logo = Image.open("Logo/camel_logo.png")
        self.camel_resize = self.camel_logo.resize((285, 90))
        self.camel = ImageTk.PhotoImage(self.camel_resize)
        self.canvas = Canvas(self.window, width=WIDTH, height=HEIGHT, background="white")
        self.canvas.pack()
        self.canvas.create_image(180, 648, image=self.pnu)
        self.canvas.create_image(1240, 650, image=self.camel)
        self.mode_number = 0
        self.start_count = 0
        self.goal_count = 0
        self.board_on = False
        self.command = Entry(self.window, width=35, borderwidth=3)
        self.command.place(x=1420, y=565)
        self.command.bind("<Return>", self.do_command)
        self.frame = Frame(self.window, relief="ridge", width=260, height=540)
        self.frame.place(x=1420, y=15)
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side="right", fill="y")
        self.cmd_window = Text(self.frame, width=34, height=41, background="white", relief="groove",
                               yscrollcommand=self.scrollbar.set, wrap="word")
        self.cmd_window.config(state="disabled")
        self.scrollbar.config(command=self.cmd_window.yview)
        self.cmd_window.pack()
        self.guide = Label(self.window, width=39, height=6, anchor=NW, justify="left", background="white")
        self.guide.place(x=1420, y=600)
        self.guide.config(text="save : save custom grid map to npy file\n" +
                               "load : load your npy file into grip map\n" +
                               "setbg : set background image and coordinates\n" +
                               "coor : save coordinates as file clicked with coord \n"  
                               "help : show details of commands\n" +
                               "clear : clean up the terminal log\n")
        Button(self.window, text="coord", font=36, fg="black", background="white", height=2, width=6,
               command=self.click_button_none).place(x=400, y=630)
        Button(self.window, text="wall", font=36, fg="black", background="white", height=2, width=6,
               command=self.click_button_wall).place(x=520, y=630)
        Button(self.window, text="start", font=36, fg="black", background="white", height=2, width=6,
               command=self.click_button_start).place(x=640, y=630)
        Button(self.window, text="goal", font=36, fg="black", background="white", height=2, width=6,
               command=self.click_button_goal).place(x=760, y=630)
        Button(self.window, text="reset", font=36, fg="black", background="white", height=2, width=6,
               command=self.reset).place(x=880, y=630)
        Button(self.window, text="astar", font=36, fg="black", background="white", height=2, width=6,
               command=self.click_button_astar).place(x=1000, y=630)

    # initialize the board matrix to 0
    def board_zero(self):
        vertical_step_count = (self.down - self.up) // 14
        horizontal_step_count = (self.right - self.left) // 14

        self.board = np.zeros(shape=(vertical_step_count, horizontal_step_count))

        for i in range(vertical_step_count):
            for j in range(horizontal_step_count):
                self.img_canvas.create_rectangle(
                    j * LENGTH, i * LENGTH, (j + 1) * LENGTH, (i + 1) * LENGTH)

    # fill board regard to matrix and create line
    def initialize_board(self):
        for i in range(self.vertical_step_count):
            for j in range(self.horizontal_step_count):
                tag_name = "rect" + self.convert_rectangle_num(j) + self.convert_rectangle_num(i)
                target_grid = self.board[i][j]
                if target_grid == 0:  # none #fixed
                    self.img_canvas.create_rectangle(
                        j * LENGTH, i * LENGTH, (j + 1) * LENGTH, (i + 1) * LENGTH, tag=tag_name)
                elif target_grid == 1:  # wall #fixed
                    self.img_canvas.create_rectangle(
                        j * LENGTH, i * LENGTH, (j + 1) * LENGTH, (i + 1) * LENGTH, tag=tag_name, fill="white")
                elif target_grid == 2:  # start #fixed
                    self.img_canvas.create_rectangle(
                        j * LENGTH, i * LENGTH, (j + 1) * LENGTH, (i + 1) * LENGTH, tag=tag_name, fill="green")
                elif target_grid == 3:  # goal #fixed
                    self.img_canvas.create_rectangle(
                        j * LENGTH, +i * LENGTH, (j + 1) * LENGTH, (i + 1) * LENGTH, tag=tag_name, fill="red")

    # reset board
    def reset(self):
        if self.board_on:
            self.img_canvas.delete("all")
            self.img_canvas.create_image(0, 0, anchor=NW, image=self.photo)
            self.board_zero()
            self.mode_number = 0
            self.start_count = 0
            self.goal_count = 0

    def mainloop(self):
        self.window.mainloop()

    # ---------------------------------------------------------
    # Button Command function
    # ---------------------------------------------------------
    def click_button_none(self):
        if self.board_on:
            self.mode_number = 0

    def click_button_wall(self):
        if self.board_on:
            self.mode_number = 1

    def click_button_start(self):
        if self.board_on:
            self.mode_number = 2

    def click_button_goal(self):
        if self.board_on:
            self.mode_number = 3

    def click_button_astar(self):
        if self.board_on:
            start_flag = np.any(self.board == 2)
            goal_flag = np.any(self.board == 3)

            if not (start_flag and goal_flag):
                messagebox.showinfo("Notice", "Please select start and goal point")

            class Node:
                def __init__(self, parent=None, position=None):
                    self.parent = parent
                    self.position = position

                    self.g = 0
                    self.h = 0
                    self.f = 0

                def __eq__(self, other):
                    return self.position == other.position

            def astar(maze, s, e):
                start_node = Node(None, s)
                end_node = Node(None, e)

                # open_list, closed_list 초기화
                open_list = []
                closed_list = []

                # open list 에 시작 노드 추가
                open_list.append(start_node)

                # end node 를 찾을 때까지 실행
                while open_list:
                    # 현재 노드 지정
                    current_node = open_list[0]
                    current_index = 0

                    # 이미 같은 노드가 open list 에 있고, f 값이 더 크면
                    # current node 를 open list 안에 있는 값으로 교체
                    for index, item in enumerate(open_list):
                        if item.f < current_node.f:
                            current_node = item
                            current_index = index

                    # open list 에서 제거 하고 closed list 에 추가
                    open_list.pop(current_index)
                    closed_list.append(current_node)

                    def draw_node(cur_node):
                        self.img_canvas.create_rectangle(
                            (cur_node.position[1]) * LENGTH, (cur_node.position[0]) * LENGTH,
                            (cur_node.position[1] + 1) * LENGTH, (cur_node.position[0] + 1) * LENGTH,
                            fill="lawn green")
                        self.window.update()

                    self.window.update()
                    self.window.after(10, draw_node(current_node))

                    # 현재 노드가 목적지면 current.position 추가 하고
                    # current의 부모로 이동

                    def find_path(_cell):
                        if cells.index(_cell) == 0:
                            self.img_canvas.create_rectangle(
                                (_cell[1]) * LENGTH, (_cell[0]) * LENGTH, (_cell[1] + 1) * LENGTH, (_cell[0] + 1) * LENGTH,
                                fill="green")
                        elif cells.index(_cell) == (len(cells) - 1):
                            self.img_canvas.create_rectangle(
                                (_cell[1]) * LENGTH, (_cell[0]) * LENGTH, (_cell[1] + 1) * LENGTH, (_cell[0] + 1) * LENGTH,
                                fill="red")
                        else:
                            self.img_canvas.create_rectangle(
                                (_cell[1]) * LENGTH, (_cell[0]) * LENGTH, (_cell[1] + 1) * LENGTH, (_cell[0] + 1) * LENGTH,
                                fill="yellow")
                        self.window.update()

                    if current_node.position == end_node.position:
                        path = []
                        current = current_node
                        while current is not None:
                            path.append(current.position)
                            current = current.parent
                        cells = path[::-1]
                        for cell in cells:
                            self.window.update()
                            self.window.after(10, find_path(cell))
                        return

                    children = []
                    # 인접한 (x, y) 좌표 전부
                    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

                        # 노드 위치 업데이트
                        node_position = (
                            current_node.position[0] + new_position[0],  # X
                            current_node.position[1] + new_position[1])  # Y

                        # 미로 maze index 범위 안에 있어야함
                        within_range_criteria = [
                            node_position[0] > (len(maze) - 1),
                            node_position[0] < 0,
                            node_position[1] > (len(maze[len(maze) - 1]) - 1),
                            node_position[1] < 0,
                        ]

                        if any(within_range_criteria):  # 하나라도 true 면 범위 밖임
                            continue

                        # 장애물이 있으면 다른 위치 불러오기
                        if maze[node_position[0]][node_position[1]] == 1:
                            continue

                        new_node = Node(current_node, node_position)
                        children.append(new_node)

                    # 자식들 모두 loop
                    for child in children:

                        # 자식이 closed list에 있으면 continue
                        if child in closed_list:
                            continue

                        # f, g, h값 업데이트
                        child.g = current_node.g + 1
                        child.h = ((child.position[0] - end_node.position[0]) **
                                   2) + ((child.position[1] - end_node.position[1]) ** 2)
                        child.f = child.g + child.h

                        # 자식이 open list에 있으고, g값이 더 크면 continue
                        if len([openNode for openNode in open_list
                                if child == openNode and child.g > openNode.g]) > 0:
                            continue

                        def draw_list(_child):
                            self.img_canvas.create_rectangle(
                                (_child.position[1]) * LENGTH, (_child.position[0]) * LENGTH,
                                (_child.position[1] + 1) * LENGTH, (_child.position[0] + 1) * LENGTH, fill="dodger blue")
                            self.window.update()

                        self.window.update()
                        self.window.after(10, draw_list(child))
                        open_list.append(child)
                        # time.sleep(0.5)

            start = (np.where(self.board == 2)[0].tolist()[0],
                     np.where(self.board == 2)[1].tolist()[0])
            end = (np.where(self.board == 3)[0].tolist()[0],
                   np.where(self.board == 3)[1].tolist()[0])
            astar(self.board, start, end)

    def save_file(self):
        np.save("GridMap/" + self.file_name + ".npy", self.board)
        messagebox.showinfo("Notion", "save completed")

    def load_file(self):
        self.board = np.load("GridMap/" + self.file_name + ".npy")
        messagebox.showinfo("Notion", "load completed")
        self.img_canvas.delete("all")
        self.img_canvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.initialize_board()
        self.load_count()

    def set_background(self):
        if self.board_on:
            self.img_frame.destroy()
        self.canvas.delete("all")
        self.canvas.create_image(180, 648, image=self.pnu)
        self.canvas.create_image(1240, 650, image=self.camel)
        img_path = "Images/" + self.file_name + ".png"
        try:
            img = Image.open(img_path)
        except IOError:
            self.write_message("There is no image")
            return
        try:
            coord_file = open("Coordinates/" + self.file_name + ".txt")
            self.mapNW = coord_file.readline().split(",")
            self.mapNE = coord_file.readline().split(",")
            self.mapSW = coord_file.readline().split(",")
            self.mapSE = coord_file.readline().split(",")
        except IOError:
            self.write_message("There is no coordinate file")
        if img.size[0] > img.size[1]:  # 가로로 김
            img_resize = img.resize((1400, int(img.size[1] * (1400 / img.size[0]))))
            if img_resize.size[1] % 14 != 0:
                img_resize = img_resize.resize((1400, int(img_resize.size[1] + (14 - img_resize.size[1] % 14))))
        else:  # 세로로 김
            img_resize = img.resize((int(img.size[0] * (602 / img.size[1])), 602))
            if img_resize.size[0] % 14 != 0:
                img_resize = img_resize.resize((int(img_resize.size[0] + (14 - img_resize.size[0] % 14)), 602))
        self.photo = ImageTk.PhotoImage(img_resize)
        self.left = 700 - img_resize.size[0] // 2
        self.right = 700 + img_resize.size[0] // 2
        self.up = 301 - img_resize.size[1] // 2
        self.down = 301 + img_resize.size[1] // 2
        self.img_frame = Frame(self.window, width=int(img_resize.size[0]), height=int(img_resize.size[1]),
                               background="white")
        self.img_frame.place(x=self.left, y=self.up)
        self.img_canvas = Canvas(self.img_frame, width=int(img_resize.size[0]), height=int(img_resize.size[1]),
                                 background="white")
        self.img_canvas.pack()
        self.img_canvas.bind("<Button-1>", self.click)
        self.img_canvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.board_zero()
        messagebox.showinfo("Notion", "setbg completed")
        self.board_on = True

    def load_count(self):
        start_flag = np.any(self.board == 2)
        goal_flag = np.any(self.board == 3)
        if start_flag:
            self.start_count = 1
        else:
            self.start_count = 0
        if goal_flag:
            self.goal_count = 1
        else:
            self.goal_count = 0

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_rectangle(self, logical_position):
        logical_position = np.array(logical_position)
        x = int(logical_position[0])
        y = int(logical_position[1])
        tag_name = "rect" + self.convert_rectangle_num(x) + self.convert_rectangle_num(y)
        if not self.mode_number == 0:
            self.img_canvas.create_rectangle(
                x * LENGTH, y * LENGTH, (x + 1) * LENGTH, (y + 1) * LENGTH, tag=tag_name, fill=COLORS[self.mode_number])
            self.board[logical_position[1]][logical_position[0]] = self.mode_number  # fixed

    def delete_rectangle(self, logical_position):
        if not self.mode_number == 0:
            x = int(logical_position[0])
            y = int(logical_position[1])
            tag_name = "rect" + self.convert_rectangle_num(x) + self.convert_rectangle_num(y)
            self.img_canvas.delete(tag_name)
            self.board[logical_position[1]][logical_position[0]] = 0  # fixed

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------
    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (IMAGE_WIDTH / self.horizontal_step_count) * logical_position + IMAGE_WIDTH / (self.horizontal_step_count * 2)

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (IMAGE_WIDTH / self.horizontal_step_count), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board[logical_position[1]][logical_position[0]] == 0:  # fixed
            return False
        else:
            return True

    # to make number 3 digit ex) 1 -> 001, 13 -> 013
    def convert_rectangle_num(self, num):
        if num // 100 != 0:
            return str(num)
        elif num // 10 != 0:
            return "0" + str(num)
        else:
            return "00" + str(num)

    def get_coordinates(self, x, y):
        each_x = (float(self.mapNE[0]) - float(self.mapNW[0])) / self.horizontal_step_count
        each_y = (float(self.mapSW[1]) - float(self.mapNW[1])) / self.vertical_step_count
        x_coordinate = str(float(self.mapNW[0]) + each_x * x)
        y_coordinate = str(float(self.mapNW[1]) + each_y * y)
        self.x_coordinates.append(x_coordinate)
        self.y_coordinates.append(y_coordinate)
        self.write_message(x_coordinate + ", " + y_coordinate)

    def save_coordinates(self):
        self.coordinates["x 좌표"] = self.x_coordinates
        self.coordinates["y 좌표"] = self.y_coordinates
        self.coordinates.to_csv("Coordinates/" + self.file_name + ".csv", encoding="utf-8-sig", index=False)
        self.coordinates.to_excel("Coordinates/" + self.file_name + ".xlsx", index=False)
        messagebox.showinfo("Notion", "save completed")

    def click(self, event):
        if self.board_on:
            grid_position = [event.x, event.y]
            logical_position = self.convert_grid_to_logical_position(grid_position)
            # 버튼 눌렀을 때 사각형이 클릭 되었다고 인식 하지 않기 위해
            if not self.is_grid_occupied(logical_position):
                if self.mode_number == 0:
                    self.get_coordinates(logical_position[0], logical_position[1])
                elif self.mode_number == 2:
                    if self.start_count == 0:
                        self.draw_rectangle(logical_position)
                        self.start_count += 1
                elif self.mode_number == 3:
                    if self.goal_count == 0:
                        self.draw_rectangle(logical_position)
                        self.goal_count += 1
                else:
                    self.draw_rectangle(logical_position)
            else:
                # fixed
                if self.mode_number == self.board[logical_position[1]][logical_position[0]]:
                    if self.mode_number == 2:
                        if self.start_count == 1:
                            self.delete_rectangle(logical_position)
                            self.start_count -= 1
                    elif self.mode_number == 3:
                        if self.goal_count == 1:
                            self.delete_rectangle(logical_position)
                            self.goal_count -= 1
                    else:
                        self.delete_rectangle(logical_position)

    def write_message(self, string):
        self.cmd_window.config(state="normal")
        self.cmd_window.insert(INSERT, string + "\n\n")
        self.cmd_window.config(state="disabled")
        self.cmd_window.see(END)

    def do_command(self, event):  # Don't remove event
        command = str(self.command.get())
        self.command.delete(0, len(command))
        self.cmd_window.config(state="normal")
        self.cmd_window.insert(INSERT, ">> " + command + "\n")
        self.cmd_window.config(state="disabled")
        command_list = command.split(" ")
        if command_list[0] == "save":
            self.file_name = command_list[1]
            self.save_file()
        elif command_list[0] == "load":
            self.file_name = command_list[1]
            self.load_file()
        elif command_list[0] == "setbg":
            self.file_name = command_list[1]
            self.set_background()
        elif command_list[0] == "coor":
            self.file_name = command_list[1]
            self.save_coordinates()
        elif command_list[0] == "clear":
            self.cmd_window.config(state="normal")
            self.cmd_window.delete(1.0, END)
            self.cmd_window.config(state="disabled")
        elif command_list[0] == "help":
            self.write_message("{fileName}은 확장자를 제외한 당신이 실제로 사용할 파일의 이름을 뜻합니다.")
            self.write_message("- save + {fileName}: 벽, 시작점, 도착점의 정보를 {fileName}.npy 확장자로 저장한다.")
            self.write_message("- load + {fileName}: save를 통해 저장됐었던 {fileName}.npy 파일을 불러와 벽, 시작점, 도착점을 보여준다.")
            self.write_message(
                "- setbg + {fileName}: {fileName}.png가 background 사진으로 깔리고, 만약 {fileName}.txt가 있다면 불러와 좌표를 설정한다.")
            self.write_message("- coor + {fileName}: coord 클릭을 통해 얻었던 좌표들을 {fileName}.csv & {fileName}.xlsx에 저장한다.")
            self.write_message("- help: command들에 대한 자세한 설명을 볼 수 있다.")
            self.write_message("- clear: 현재 떠있는 터미널 로그를 전부 삭제한다.")
        else:
            self.write_message("command not found...")
        self.cmd_window.see(END)


CamelPathFinding()
mainloop()
