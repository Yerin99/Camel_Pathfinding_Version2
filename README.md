#  camelPathFinding

  
Camel Path Finding Project


###  A* Algorithm

(TBA)

### How to use program
0. If you succeed in running the program, this screen will be displayed.

There is 5 buttons and 5 commands.

Each button functions as follows.
* Wall Button: 회색 벽을 만든다. 벽은 경로 생성 시 피하는 영역이 된다.
* Start Button: 시작 지점을 선택한다. 선택은 하나만 할 수 있으며 초록색으로 표시된다.
* Goal Button: 도착 지점을 선택한다. 선택은 하나만 할 수 있으며 빨간색으로 표시된다.
* AStar Button: 시작점에서 도착점까지의 최단 경로를 생성한다. 최종 경로는 분홍색으로, open list는 파란색, close list는 노란색으로 표시된다.
* Reset Button: 모든 선택 영역을 초기화 시킨다.

Each command functions as follows.
* Save + : 벽, 시작점, 도착점의 정보를  .npy 확장자로 저장한다. 
* Load + : Save를 통해 저장된 .npy 파일을 불러와 벽, 시작점, 도착점을 표시한다.
