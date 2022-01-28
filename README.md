# Camel_PathFinding_Version2

  
Project making Camel Path Finding Program


####  A* Algorithm

(TBA)

## How to use program
### 0. If you succeed in running the program, this screen will be displayed.


![image](https://user-images.githubusercontent.com/63496777/151313283-54ab35b8-28c8-40fe-901e-279fb09e4efd.png)

There is 5 buttons and 5 commands.

Each button functions as follows.
* Wall Button: 회색 벽을 만든다. 벽은 경로 생성 시 피하는 영역이 된다.
* Start Button: 시작 지점을 선택한다. 선택은 하나만 할 수 있으며 초록색으로 표시된다.
* Goal Button: 도착 지점을 선택한다. 선택은 하나만 할 수 있으며 빨간색으로 표시된다.
* AStar Button: 시작점에서 도착점까지의 최단 경로를 생성한다. 
* 최종 경로는 yellow로, open list는 dodge blue, close list는 lawn green으로 표시된다.
* Reset Button: 모든 선택 영역을 초기화 시킨다.

Each command functions as follows. 
> {fileName}은 확장자를 제외한 당신이 실제로 사용할 파일의 이름을 뜻합니다. 


* save + {fileName}: 벽, 시작점, 도착점의 정보를 {fileName}.npy 확장자로 저장한다.
* load + {fileName}: save를 통해 저장됐었던 {fileName}.npy 파일을 불러와 벽, 시작점, 도착점을 보여준다.
* setbg + {fileName}: {fileName}.png가 background 사진으로 깔리고, 만약 {fileName}.txt가 있다면 불러와 좌표를 설정한다.
* help: command들에 대한 자세한 설명을 볼 수 있다. 
* clear: 현재 떠있는 터미널 로그를 전부 삭제한다.


### 1.  And then follow this desription.


#### [step 1] Set background picture with typing 'setbg + {fileName}' on the console.  
  ** 'fileName' mentioned here is the name of the png picture. ** 
  And it should be stored in the Images folder.  
  If you want to know the coordinate values for each grid, create a txt file with the same name as the picture.
  And store it in the Coordinates folder.  
  
![image](https://user-images.githubusercontent.com/63496777/151462784-a6e2762f-6e8e-4140-9749-419e3112c84c.png)


#### [step 2] Make numpy file with buttons and "save" it so that you can use it through "load" next time.  
  Using wall, start, goal buttons, make your own numpy file which has grid map information.  
  If you finish, type 'save + {fileName}' on the console.   
  The file will be saved as {fileName}.npy.  
  Next time, you don't have to make your own numpy file using buttons, you just need to load it.  
  If you're sure you have the file, just type "load + {fileName}" on the console.
    
![image](https://user-images.githubusercontent.com/63496777/151463741-f37608d2-f115-4e0b-8277-536eaab17118.png)

#### [step 3] Press astar button and see what program can do.    
![image](https://user-images.githubusercontent.com/63496777/151463970-6ef3783d-d82d-458e-86de-9f2eab05900e.png)


### 2. Actual use case: Finding the shortest route from building 207 to building 201.
![ezgif com-gif-maker](https://user-images.githubusercontent.com/63496777/151465180-d51bf4ce-59e2-41c7-bafe-ba75e98c0bcf.gif)


