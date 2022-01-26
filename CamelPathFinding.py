from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import Image, ImageDraw, ImageTk
from matplotlib.pyplot import grid, text
import numpy as np
import time

from pyparsing import White
# Define useful parameters
imagewidth = 1400
width = 1700
imageheight=600;
height = 700;
horizontalStepCount = 100
verticalStepCount = imageheight//(imagewidth//horizontalStepCount)
length = imagewidth//horizontalStepCount
print(verticalStepCount)
Color = {0: "none", 1: "white", 2: "green", 3: "red"}  # 열린목록 닫힌목록 길 등은 나중에 추가


class AStarPathFinding:
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("AStarPathFinding")
        self.pnu= ImageTk.PhotoImage(Image.open("Logo/pnu_logo.png"))
        self.camel= ImageTk.PhotoImage(Image.open("Logo/camel_logo.png"))
        self.canvas = Canvas(self.window, width=width, height=height, background="white")
        self.canvas.pack()
        self.reset()
        self.command = Entry(self.window, width=35, borderwidth=3)
        self.command.place(x=1420, y=565)
        self.command.bind("<Return>",self.commandfunc)
        self.frame=Frame(self.window, relief="ridge", width=260, height=540)
        self.frame.place(x=1420, y=15)
        self.scrollbar=Scrollbar(self.frame)
        self.scrollbar.pack(side="right",fill="y")
        self.cmdwindow=Text(self.frame, width=34, height=41, background="white", relief="groove", yscrollcommand=self.scrollbar.set, wrap="word")
        self.cmdwindow.config(state="disabled")
        self.scrollbar.config(command=self.cmdwindow.yview)
        self.cmdwindow.pack()
        self.guide=Label(self.window, width=39, height=6, anchor=NW, justify="left", background="white")
        self.guide.place(x=1420, y=600)
        self.guide.config(text= "save : save custom grid map to npy file\n"+
                                "load : load your npy file into grip map\n"+
                                "setbg : set background image and coordinates\n"+
                                "help : show details of commands\n"+
                                "clear : clean up the terminal log\n")
        self.window.bind("<Button-1>", self.click)
        Button(self.window, text="none", font=36, fg="black", background="white", height = 2, width = 6,
               command=self.BTnone).place(x=400, y=630)
        Button(self.window, text="wall", font=36, fg="black", background="white", height = 2, width = 6,
               command=self.BTwall).place(x=520, y=630)
        Button(self.window, text="start", font=36, fg="black", background="white", height = 2, width = 6,
               command=self.BTstart).place(x=640, y=630)
        Button(self.window, text="goal", font=36, fg="black", background="white", height = 2, width = 6,
               command=self.BTgoal).place(x=760, y=630)
        Button(self.window, text="reset", font=36, fg="black", background="white", height = 2, width = 6,
               command=self.reset).place(x=880, y=630)
        Button(self.window, text="astar", font=36, fg="black", background="white", height = 2, width = 6,
               command=self.BTastar).place(x=1000, y=630)

    
    # initialize the board matrix to 0
    def boardZero(self):
        self.board = []
        self.board = np.zeros(shape=(verticalStepCount, horizontalStepCount))

    # fill board regard to matrix and create line
    def initialize_board(self):
        for i in range(verticalStepCount):
            for j in range(horizontalStepCount):
                tagname = "rect"+self.convertRecNum(j)+self.convertRecNum(i)
                if(self.board[i][j] == 0):  # none #fixed
                    self.canvas.create_rectangle(
                        j*length, i*length, (j+1)*length, (i+1)*length ,tag=tagname)
                elif(self.board[i][j] == 1):  # wall #fixed
                    self.canvas.create_rectangle(
                        j*length, i*length, (j+1)*length, (i+1)*length, tag=tagname, fill="white" ,outline="black")
                elif(self.board[i][j] == 2):  # start #fixed
                    self.canvas.create_rectangle(
                        j*length, i*length, (j+1)*length, (i+1)*length, tag=tagname, fill="green")
                elif(self.board[i][j] == 3):  # goal #fixed
                    self.canvas.create_rectangle(
                        j*length, i*length, (j+1)*length, (i+1)*length, tag=tagname, fill="red")

    # reset board
    def reset(self):
        self.boardZero()
        self.canvas.create_image(180, 648, image=self.pnu)
        self.canvas.create_image(1240, 650, image=self.camel)
        # self.canvas.create_image(700, 290, image=self.photo)
        # self.initialize_board()
        self.modenumber = 0
        self.startcount = 0
        self.goalcount = 0

    def mainloop(self):
        self.window.mainloop()

    # ---------------------------------------------------------
    # Button Command function
    # ---------------------------------------------------------
    def BTnone(self):
        self.modenumber = 0

    def BTwall(self):
        self.modenumber = 1
        self.initialize_board()

    def BTstart(self):
        self.modenumber = 2

    def BTgoal(self):
        self.modenumber = 3

    def BTastar(self):
        startflag = np.any(self.board == 2)
        goalflag = np.any(self.board == 3)

        if not (startflag and goalflag):
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

        def aStar(maze, start, end):
            startNode = Node(None, start)
            endNode = Node(None, end)

            # openList, closedList 초기화
            openList = []
            closedList = []

            # openList에 시작 노드 추가
            openList.append(startNode)

            # endNode를 찾을 때까지 실행
            while openList:
                # 현재 노드 지정
                currentNode = openList[0]
                currentIdx = 0

                # 이미 같은 노드가 openList에 있고, f 값이 더 크면
                # currentNode를 openList안에 있는 값으로 교체
                for index, item in enumerate(openList):
                    if item.f < currentNode.f:
                        currentNode = item
                        currentIdx = index
                # openList에서 제거하고 closedList에 추가
                openList.pop(currentIdx)
                closedList.append(currentNode)
                def drawnode(currentNode):
                    self.canvas.create_rectangle(
                        (currentNode.position[1])*length, (currentNode.position[0])*length, (currentNode.position[1]+1)*length, (currentNode.position[0]+1)*length, fill="lawn green")
                    self.window.update()  
                                       
                self.window.update()
                self.window.after(10,drawnode(currentNode))
                # 현재 노드가 목적지면 current.position 추가하고
                # current의 부모로 이동
                def findpath(cell):
                        if cells.index(cell) == 0:
                            self.canvas.create_rectangle(
                                (cell[1])*length, (cell[0])*length, (cell[1]+1)*length, (cell[0]+1)*length, fill="green")
                        elif cells.index(cell) == (len(cells) - 1):
                            self.canvas.create_rectangle(
                                (cell[1])*length, (cell[0])*length, (cell[1]+1)*length, (cell[0]+1)*length, fill="red")
                        else:
                            self.canvas.create_rectangle(
                                (cell[1])*length, (cell[0])*length, (cell[1]+1)*length, (cell[0]+1)*length, fill="yellow")
                        self.window.update()
                if currentNode.position == endNode.position:
                    path = []
                    current = currentNode
                    while current is not None:
                        path.append(current.position)
                        current = current.parent
                    cells = path[::-1]
                    for cell in cells:
                        self.window.update()
                        self.window.after(10,findpath(cell))
                    return

                children = []
                # 인접한 xy좌표 전부
                for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

                    # 노드 위치 업데이트
                    nodePosition = (
                        currentNode.position[0] + newPosition[0],  # X
                        currentNode.position[1] + newPosition[1])  # Y

                    # 미로 maze index 범위 안에 있어야함
                    within_range_criteria = [
                        nodePosition[0] > (len(maze) - 1),
                        nodePosition[0] < 0,
                        nodePosition[1] > (len(maze[len(maze) - 1]) - 1),
                        nodePosition[1] < 0,
                    ]

                    if any(within_range_criteria):  # 하나라도 true면 범위 밖임
                        continue

                    # 장애물이 있으면 다른 위치 불러오기
                    if maze[nodePosition[0]][nodePosition[1]] == 1:
                        continue

                    new_node = Node(currentNode, nodePosition)
                    children.append(new_node)

                # 자식들 모두 loop
                for child in children:

                    # 자식이 closedList에 있으면 continue
                    if child in closedList:
                        continue

                    # f, g, h값 업데이트
                    child.g = currentNode.g + 1
                    child.h = ((child.position[0] - endNode.position[0]) **
                               2) + ((child.position[1] - endNode.position[1]) ** 2)
                    child.f = child.g + child.h

                    # 자식이 openList에 있으고, g값이 더 크면 continue
                    if len([openNode for openNode in openList
                            if child == openNode and child.g > openNode.g]) > 0:
                        continue
                    
                    def drawlist(child):
                        self.canvas.create_rectangle(
                        (child.position[1])*length, (child.position[0])*length, (child.position[1]+1)*length, (child.position[0]+1)*length, fill="dodger blue")
                        self.window.update()
                    self.window.update()
                    self.window.after(10,drawlist(child))
                    openList.append(child)
                    # time.sleep(0.5)

        start = (np.where(self.board == 2)[0].tolist()[0],
                 np.where(self.board == 2)[1].tolist()[0])
        end = (np.where(self.board == 3)[0].tolist()[0],
               np.where(self.board == 3)[1].tolist()[0])
        aStar(self.board, start, end)


    def filesave(self):
        np.save("GridMap/"+self.filename+".npy", self.board, 'x')
        messagebox.showinfo("Notion", "save completed")


    def fileload(self):
        self.board = np.load("GridMap/"+self.filename+".npy")
        messagebox.showinfo("Notion", "load completed")
        self.canvas.delete("all")
        self.canvas.create_image(700, 290, image=self.photo)
        self.canvas.create_image(180, 648, image=self.pnu)
        self.canvas.create_image(1240, 650, image=self.camel)
        self.initialize_board()
        self.loadcount()

    def setbg(self):
        imgpath = "Images/"+self.filename+".png"
        img = Image.open(imgpath)
        if img.size[0] > img.size[1]: # 가로로 김 
            if img.size[0] > 1400:
                img_resize=img.resize((1400,int(img.size[1]*(1400/img.size[0]))))
            else :
                img_resize=img
        else : # 세로로 김
            if img.size[1] > 600:
                img_resize=img.resize((int(img.size[0]*(600/img.size[1])),600))
            else :
                img_reize=img
        self.photo = ImageTk.PhotoImage(img_resize)
        self.canvas.create_image(700, 300, image=self.photo)
        self.initialize_board()
        messagebox.showinfo("Notion", "setbg completed")
    def loadcount(self):
        startflag = np.any(self.board == 2)
        goalflag = np.any(self.board == 3)
        if startflag:
            self.startcount = 1
        else:
            self.startcount = 0
        if goalflag:
            self.goalcount = 1
        else:
            self.goalcount = 0
    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def drawRec(self, logical_position):
        logical_position = np.array(logical_position)
        x = int(logical_position[0])
        y = int(logical_position[1])
        tagname = "rect"+self.convertRecNum(x)+self.convertRecNum(y)
        if not self.modenumber == 0:
            self.canvas.create_rectangle(
                x*length, y*length, (x+1)*length, (y+1)*length, tag=tagname, fill=Color[self.modenumber])
            self.board[logical_position[1]][logical_position[0]
                                            ] = self.modenumber  # fixed

    def deleteRec(self, logical_position):
        if not self.modenumber == 0:
            x = int(logical_position[0])
            y = int(logical_position[1])
            tagname = "rect"+self.convertRecNum(x)+self.convertRecNum(y)
            self.canvas.delete(tagname)
            self.board[logical_position[1]][logical_position[0]] = 0  # fixed

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------
    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (imagewidth / horizontalStepCount) * logical_position + imagewidth / (horizontalStepCount*2)

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (imagewidth / horizontalStepCount), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board[logical_position[1]][logical_position[0]] == 0:  # fixed
            return False
        else:
            return True

    # to make number 3 digit ex) 1 -> 001, 13 -> 013
    def convertRecNum(self, num):
        if(num//100 != 0):
            return str(num)
        elif(num//10 != 0):
            return "0"+str(num)
        else:
            return "00"+str(num)

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        # 버튼 눌렀을 때 사각형이 클릭되었다고 인식하지않기 위해
        if logical_position[0] < horizontalStepCount and logical_position[1] <verticalStepCount :
            if logical_position[0] > 4 or logical_position[1] > 3:
                if not self.is_grid_occupied(logical_position):
                    if self.modenumber == 2:
                        if self.startcount == 0:
                            self.drawRec(logical_position)
                            self.startcount += 1
                    elif self.modenumber == 3:
                        if self.goalcount == 0:
                            self.drawRec(logical_position)
                            self.goalcount += 1
                    else:
                        self.drawRec(logical_position)
                else:
                    # fixed
                    if self.modenumber == self.board[logical_position[1]][logical_position[0]]:
                        if self.modenumber == 2:
                            if self.startcount == 1:
                                self.deleteRec(logical_position)
                                self.startcount -= 1
                        elif self.modenumber == 3:
                            if self.goalcount == 1:
                                self.deleteRec(logical_position)
                                self.goalcount -= 1
                        else:
                            self.deleteRec(logical_position)

    def writeMessage(self, string):
        self.cmdwindow.config(state="normal")
        self.cmdwindow.insert(INSERT,string+"\n\n")
        self.cmdwindow.config(state="disable")
        self.cmdwindow.see(END)

    def commandfunc(self, event):
        command=str(self.command.get())
        self.command.delete(0,len(command))
        self.cmdwindow.config(state="normal")
        self.cmdwindow.insert(INSERT,">> "+command+"\n")
        self.cmdwindow.config(state="disable")
        commandList=command.split(" ")
        if commandList[0] == "save" :
            self.filename=commandList[1]
            self.filesave()
        elif commandList[0] =="load" :
            self.filename=commandList[1]
            self.fileload()
        elif commandList[0] =="setbg":
            self.filename=commandList[1]
            self.setbg()
        elif commandList[0] =="clear":
            self.cmdwindow.config(state="normal")
            self.cmdwindow.delete(1.0,END)
            self.cmdwindow.config(state="disable")
        elif commandList[0] =="help":
            self.writeMessage("may i help you?")
        else :
            self.writeMessage("command not found...")
        self.cmdwindow.see(END)
game_instance = AStarPathFinding()
game_instance = mainloop()
