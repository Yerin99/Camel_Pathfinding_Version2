#  camelPathFinding

  
Camel Path Finding Project


###  A* Algorithm

(TBA)

### How to use program
0. If you succeed in running the program, this screen will be displayed.


![image](https://user-images.githubusercontent.com/63496777/151313283-54ab35b8-28c8-40fe-901e-279fb09e4efd.png)

There is 5 buttons and 5 commands.

Each button functions as follows.
* Wall Button: 회색 벽을 만든다. 벽은 경로 생성 시 피하는 영역이 된다.
* Start Button: 시작 지점을 선택한다. 선택은 하나만 할 수 있으며 초록색으로 표시된다.
* Goal Button: 도착 지점을 선택한다. 선택은 하나만 할 수 있으며 빨간색으로 표시된다.
* AStar Button: 시작점에서 도착점까지의 최단 경로를 생성한다. 최종 경로는 분홍색으로, open list는 파란색, close list는 노란색으로 표시된다.
* Reset Button: 모든 선택 영역을 초기화 시킨다.

Each command functions as follows. 
> {fileName}은 확장자를 제외한 당신이 실제로 사용할 파일의 이름을 뜻합니다. 

* save + {fileName}: 벽, 시작점, 도착점의 정보를  {fileName}.npy 확장자로 저장한다. 
* load + {fileName}: Save를 통해 저장된 {fileName}.npy 파일을 불러와 벽, 시작점, 도착점을 표시한다.
* setbg + {fileName}: {fileName}, {fileName}.txt 파일이 있다면 그것 또한 불러와 좌표들이 설정된다.
* help: command들에 대한 설명을 볼 수 있다. help + {command}를 치면 해당 커맨드에 대한 자세한 설명을 볼 수 있다.  
* clear: 현재 떠있는 터미널 로그를 전부 삭제한다. 

1. It's not written yet.
