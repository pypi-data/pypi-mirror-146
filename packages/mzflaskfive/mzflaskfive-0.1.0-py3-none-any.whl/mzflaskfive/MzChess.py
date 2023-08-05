import time
import json
import random
import math
#################################################
# @下棋决策类
# 预计使用博弈树的策略进行搜索
# 以_开头的方法都是私有
# 
# 关键方法：
# _search方法用于搜索
# _grade方法用于给盘面打分

class MzChess():
	
	# 内部类，棋盘类，用作搜索节点
	class Chessboard():
		def __init__(self, board=None, whoami=1, who=1, floor=1, floorMax=3):
			# 初始化参数
			if board == None:
				self.board = [[0 for i in range(15)] for j in range(15)]    # 当前盘面
			else:
				self.board = board    # 当前盘面 可以直接通过棋盘数组创建
			self.who = who             # 当前是谁的回合
			self.whoami = whoami       # ai使用的棋子颜色(当前未使用)
			self.floor = floor         # 当前层数
			self.floorMax = floorMax   # 最大层数
			self.childList = []        # 子节点列表
			self.score = None          # 分值
			# 实例化时如果没有board参数，一定要调用init开头的函数去“初始化Board”才能正常使用
		
		# 从格式化串创建棋盘
		# *用于和前端对接的时候
		def initFromStr(self, _str):
			_count_black = 0
			_count_white = 0
			for i in range(15):
				for j in range(15):
					self.board[i][j] = int(_str[i*15+j])
					if self.board[i][j] == 1:
						_count_black += 1
					elif self.board[i][j] == 2:
						_count_white += 1
						
			if _count_black > _count_white:
				self.who = 2                 # 下一个应该是白
				
				
		# 这个方式是为了后续存储做准备的
		def board2str(self, board):
			pass
			
		# 遍历增加子节点
		def bornChild(self):
			# 遍历所有可以走的位置
			for i in range(15):
				for j in range(15):
					if self.board[i][j] == 0:
						# 剪枝
						# 如果周围2格内都没有棋子直接continue
						_exist = False
						for _ in range(-2,3):
							for __ in range(-2, 3):
								if (i+_)>=0 and (i+_)<15 and \
									(j+__)>=0 and (j+__)<15:
									if self.board[i+_][j+__] != 0:
										_exist = True
										break
							if _exist == True:
								break

						if _exist == False:
							continue     # 剪枝
						
						_tmpBoard = self.copyBoard(self.board)    # 创建棋盘副本
						_tmpBoard[i][j] = self.who   # 模拟下棋后的棋盘
						# 切换新棋盘下的棋子
						if self.who == 1:
							_tmpWho = 2
						elif self.who == 2:
							_tmpWho = 1
						# self.greatOutput(board=_tmpBoard)
						_tmp = self.__class__(
							board=_tmpBoard, 
							floor=self.floor+1, 
							who=_tmpWho
							)   # 创建新棋盘(递归创建自身的实例),层数+1，棋子颜色反转
						self.childList.append(_tmp)
		
		# 深拷贝棋盘
		# 直接创建副本还是会出问题
		def copyBoard(self, _board):
			board = [[0 for i in range(15)] for j in range(15)]
			for i in range(15):
				for j in range(15):
					board[i][j] = _board[i][j]
			return board
			
			
		# 优雅的输出棋盘
		def greatOutput(self, board=None):
			if board == None:
				board = self.board
			print('> now:')
			for i in board:
				print('  ',end='')
				print(i)
				
		# 设置盘面分值
		def setScore(self, score):
			self.score = score
			
		# 返回棋盘数组
		def getBoard(self):
			return self.board
		
		# 返回该盘面下的下一个走棋的人
		def getWho(self):
			return self.who

	# 初始化
	def __init__(self, chessboardstr):
		self.chessboard = self.Chessboard()
		self.chessboard.initFromStr(chessboardstr)  # 棋盘格式串
		self.whoami = self.chessboard.getWho()    # 下一个走棋的人，即我(AI)应该是黑还是白   # 此处为重要参数，要作为对比使用
		self.rootHighest = -100000    # 记录根节点的最大值，用于剪枝
		# 输出调试信息
		print(f'next: {self.whoami}')
		
		
	# 对比两个棋盘给出走的位置
	# return [x,y]
	def _getChoiceFromBoard(self, board):
		_board = self.chessboard.getBoard()
		# 对比给出的盘面和自身盘面
		for i in range(15):
			for j in range(15):
				if board[i][j] != _board[i][j]:
					return [j, i]  # x,y与i,j相反
		
		
	# 打分函数
	# 参数为盘面
	# 给局面进行打分返回int
	# ------------------------
	#  这里是Mz1自创的五子棋小妙招
	#  提出一个叫做"逼点"的概念: 即这个点如果你/对方走了，下一步对方就必须来堵你
	#  如果一个点是两组以上棋子造成的逼点（双逼点），则这个点有机会绝杀对方，因为他有可能需要堵2个位置
	#     特殊情况：如果对方堵了一个位置造成了逼走，则可能无效。
	#  针对盘面打分的系统提出"逼走"的概念，属于逼点的特殊情况，如果一个点对方下一步不走就可以击杀对方，则此步为"逼走"。
	#     即如果我方走了逼点，则对方盘面就会出现逼走。
	#  综上：打分的原则是出现尽可能多的逼走/逼点/双逼点
	#     双逼点的分值应该最高
	#  ----
	#  逼点的情况判定(x代表这个点，1代表己方棋子，0代表无子)：
	#  1. 空点x
	#  2. 周围存在2连(0x110)(0x1010)(01x10)         -> 弱逼点
	#  3. 周围存在3连(0x1112)(1x011)(10x11)  -> 强逼点
	#  4. 周围存在4连(x1111)(1x111)(11x11) -> 逼走
	#  ---
	#  打分过程(废弃)
	#  逐个遍历空白的点：
	#      判断是否是逼点/逼走
	#         一个弱逼点加15分
	#         一个强逼点加30分
	#         一个双逼点加100分
	#         一个逼走加20分
	#  --
	#  棋型(根据1进行判断)(*后面的是分值)：
	#  2连：(0110*15)(01010*10)(010010*5)
	#  3连：(01110*50)(001112*20)(211100*20)(10011*16)(11001*16) 
	#       (010110*20)(210110*16)(011010*20)(211010*16)(010112*16)(011012*16)
	#  4连：(011110*999)(011112*100)(211110*100)(11011*100)(11101*100)(10111*100)
	#  5连: (11111*10000    游戏结束)
	#  注意：还需要考虑在墙边的情况！(尚未考虑，需要修改_checkChessStruct函数)
	#  --
	#  之后考虑通过棋型进行建模
	#  建立通过棋型进行运算的函数
	def _grade(self, board, floor):
		# self.whoami 用于标识我是什么棋子
		# floor 用于标识这是极大层还是极小层，奇数
		score = 0   # 初始化分值
		me = self.whoami
		if me == 1:
			enemy = 2
		elif me == 2:
			enemy = 1
		
		# 我方棋子向中心的聚拢程度
		# 这个参数值要尽可能的小，只是用来控制最开始的一步要往中间走的
		for i in range(15):
			for j in range(15):
				if board[i][j] == self.whoami:
					# score += 1/(math.sqrt((i-7)*(i-7)+(j-7)*(j-7))+10)
					score += int(10/(math.sqrt((i-7)*(i-7)+(j-7)*(j-7))+1))   # 避免浮点数计算
					
		# 棋型评估
		# 方向: 右，右下，下，左下
		# 根据层数设定参数
		if floor % 2 == 0:   # 偶数层就是自己的视角（参见算法描述图）
			_view = 0
		else:
			_view = -1       # 奇数层就是敌人的视角，需要翻转参数
		# print(f'_view={_view}')
		# 遍历评估
		for i in range(15):
			for j in range(15):

				# 评估己方棋型(分数参数前面的是己方评分，后面的是敌方评分，这样写是为了反转视角, 因为第二层敌人思考的时候会需要翻转)
				if board[i][j] == me:
					# 5连检测
					score += self._checkChessStruct(board, i, j, '11111') * (10000, 9000)[_view]
					# 2连检测
					score += self._checkChessStruct(board, i, j, '0110') * (15, 15)[_view]
					score += self._checkChessStruct(board, i, j, '01010') * (10, 10)[_view]
					score += self._checkChessStruct(board, i, j, '010010') * (5, 5)[_view]
					# 3连检测
					score += self._checkChessStruct(board, i, j, '01110') * (50, 600)[_view]
					score += self._checkChessStruct(board, i, j, '001112') * (20, 20)[_view]
					score += self._checkChessStruct(board, i, j, '211100') * (20, 20)[_view]
					score += self._checkChessStruct(board, i, j, '10011') * (16, 16)[_view]
					score += self._checkChessStruct(board, i, j, '11001') * (16, 16)[_view]

					score += self._checkChessStruct(board, i, j, '011010') * (20, 600)[_view]
					score += self._checkChessStruct(board, i, j, '010110') * (20, 600)[_view]
					score += self._checkChessStruct(board, i, j, '210110') * (16, 16)[_view]
					score += self._checkChessStruct(board, i, j, '211010') * (16, 16)[_view]
					score += self._checkChessStruct(board, i, j, '010112') * (16, 16)[_view]
					score += self._checkChessStruct(board, i, j, '011012') * (16, 16)[_view]
					# 4连检测
					score += self._checkChessStruct(board, i, j, '011110') * (900, 1500)[_view]
					score += self._checkChessStruct(board, i, j, '011112') * (110, 1000)[_view]
					score += self._checkChessStruct(board, i, j, '211110') * (110, 1000)[_view]
					score += self._checkChessStruct(board, i, j, '11011') * (100, 1000)[_view]
					score += self._checkChessStruct(board, i, j, '11101') * (100, 1000)[_view]
					score += self._checkChessStruct(board, i, j, '10111') * (100, 1000)[_view]
					'''
					# 这部分是之前的判定代码，已经被self._checkChessStruct代替
					### 5连-游戏结束
					## 右
					if (j+4)<15 and \
						board[i][j+1] == me and \
						board[i][j+2] == me and \
						board[i][j+3] == me and \
						board[i][j+4] == me:
						score += 10000
						break
					## 右下
					elif (j+4)<15 and (i+4)<15 and \
						board[i+1][j+1] == me and \
						board[i+2][j+2] == me and \
						board[i+3][j+3] == me and \
						board[i+4][j+4] == me:
						score += 10000
						break
					## 下
					elif (i+4)<15 and \
						board[i+1][j] == me and \
						board[i+2][j] == me and \
						board[i+3][j] == me and \
						board[i+4][j] == me:
						score += 10000
						break
					## 左下
					elif (j-4)>=0 and (i+4)<15 and \
						board[i+1][j-1] == me and \
						board[i+2][j-2] == me and \
						board[i+3][j-3] == me and \
						board[i+4][j-4] == me:
						score += 10000
						break

					### 2连
					## 右
					# 0110
					if (j+2)<15 and (j-1)>=0 and \
						board[i][j-1] == 0 and \
						board[i][j+1] == me and \
						board[i][j+2] == 0:
						score += 15
					# 01010
					elif (j+3)<15 and (j-1)>=0 and \
						board[i][j-1] == 0 and \
						board[i][j+1] == 0 and \
						board[i][j+2] == me and \
						board[i][j+3] == 0:
						score += 10
					# 010010
					elif (j+4)<15 and (j-1)>=0 and \
						board[i][j-1] == 0 and \
						board[i][j+1] == 0 and \
						board[i][j+2] == 0 and \
						board[i][j+3] == me and \
						board[i][j+4] == 0:
						score += 5
					## 右下
					# 0110
					if (i-1)>=0 and (j-1)>=0 and (i+2)<15 and (j+2)<15 and \
						board[i-1][j-1] == 0 and \
						board[i+1][j+1] == me and \
						board[i+2][j+2] == 0:
						score += 15
					# 01010
					elif (i-1)>=0 and (j-1)>=0 and (i+3)<15 and (j+3)<15 and \
						board[i-1][j-1] == 0 and \
						board[i+1][j+1] == 0 and \
						board[i+2][j+2] == me and \
						board[i+3][j+3] == 0:
						score += 10
					# 010010
					elif (i-1)>=0 and (j-1)>=0 and (i+4)<15 and (j+4)<15 and \
						board[i-1][j-1] == 0 and \
						board[i+1][j+1] == 0 and \
						board[i+2][j+2] == 0 and \
						board[i+3][j+3] == me and \
						board[i+4][j+4] == 0:
						score += 5
					## 下
					# 0110
					if (i+2)<15 and (i-1)>=0 and \
						board[i-1][j] == 0 and \
						board[i+1][j] == me and \
						board[i+2][j] == 0:
						score += 15
					# 01010
					elif (i+3)<15 and (i-1)>=0 and \
						board[i-1][j] == 0 and \
						board[i+1][j] == 0 and \
						board[i+2][j] == me and \
						board[i+3][j] == 0:
						score += 10
					# 010010
					elif (i+4)<15 and (i-1)>=0 and \
						board[i-1][j] == 0 and \
						board[i+1][j] == 0 and \
						board[i+2][j] == 0 and \
						board[i+3][j] == me and \
						board[i+4][j] == 0:
						score += 5
					## 左下
					# 0110
					if (i-1)>=0 and (j-2)>=0 and (i+2)<15 and (j+1)<15 and \
						board[i-1][j+1] == 0 and \
						board[i+1][j-1] == me and \
						board[i+2][j-2] == 0:
						score += 15
					# 01010
					elif (i-1)>=0 and (j-3)>=0 and (i+3)<15 and (j+1)<15 and \
						board[i-1][j+1] == 0 and \
						board[i+1][j-1] == 0 and \
						board[i+2][j-2] == me and \
						board[i+3][j-3] == 0:
						score += 10
					# 010010
					elif (i-1)>=0 and (j-4)>=0 and (i+4)<15 and (j+1)<15 and \
						board[i-1][j+1] == 0 and \
						board[i+1][j-1] == 0 and \
						board[i+2][j-2] == 0 and \
						board[i+3][j-3] == me and \
						board[i+4][j-4] == 0:
						score += 5
					
					###3连
					## 右
					# 01110
					if (j+3)<15 and (j-1)>=0 and \
						board[i][j-1] == 0 and \
						board[i][j+1] == me and \
						board[i][j+2] == me and \
						board[i][j+3] == 0:
						score += 50
					# 01112
					elif (j+3)<15 and (j-1)>=0 and \
						board[i][j-1] == 0 and \
						board[i][j+1] == me and \
						board[i][j+2] == me and \
						board[i][j+3] == enemy:
						score += 20
					# 21110
					elif (j+3)<15 and (j-1)>=0 and \
						board[i][j-1] == enemy and \
						board[i][j+1] == me and \
						board[i][j+2] == me and \
						board[i][j+3] == 0:
						score += 20
					# 10011
					# 11001
					
					## 右下
					# 01110
					if (i-1)>=0 and (j-1)>=0 and (i+3)<15 and (j+3)<15 and \
						board[i-1][j-1] == 0 and \
						board[i+1][j+1] == me and \
						board[i+2][j+2] == me and \
						board[i+3][j+3] == 0:
						score += 50
					# 01112
					elif (i-1)>=0 and (j-1)>=0 and (i+3)<15 and (j+3)<15 and \
						board[i-1][j-1] == 0 and \
						board[i+1][j+1] == me and \
						board[i+2][j+2] == me and \
						board[i+3][j+3] == enemy:
						score += 20
					# 21110
					elif (i-1)>=0 and (j-1)>=0 and (i+3)<15 and (j+3)<15 and \
						board[i-1][j-1] == enemy and \
						board[i+1][j+1] == me and \
						board[i+2][j+2] == me and \
						board[i+3][j+3] == 0:
						score += 20
					# 10011
					# 11001
					## 下
					# 01110
					if (i+3)<15 and (i-1)>=0 and \
						board[i-1][j] == 0 and \
						board[i+1][j] == me and \
						board[i+2][j] == me and \
						board[i+3][j] == 0:
						score += 50
					# 01112
					elif (i+3)<15 and (i-1)>=0 and \
						board[i-1][j] == 0 and \
						board[i+1][j] == me and \
						board[i+2][j] == me and \
						board[i+3][j] == enemy:
						score += 20
					# 21110
					elif (i+3)<15 and (i-1)>=0 and \
						board[i-1][j] == enemy and \
						board[i+1][j] == me and \
						board[i+2][j] == me and \
						board[i+3][j] == 0:
						score += 20
					# 10011
					# 11001
					## 左下
					# 01110
					if (i-1)>=0 and (j-3)>=0 and (i+3)<15 and (j+1)<15 and \
						board[i-1][j+1] == 0 and \
						board[i+1][j-1] == me and \
						board[i+2][j-2] == me and \
						board[i+3][j-3] == 0:
						score += 50
					# 01112
					elif (i-1)>=0 and (j-3)>=0 and (i+3)<15 and (j+1)<15 and \
						board[i-1][j+1] == 0 and \
						board[i+1][j-1] == me and \
						board[i+2][j-2] == me and \
						board[i+3][j-3] == enemy:
						score += 20
					# 21110
					elif (i-1)>=0 and (j-3)>=0 and (i+3)<15 and (j+1)<15 and \
						board[i-1][j+1] == enemy and \
						board[i+1][j-1] == me and \
						board[i+2][j-2] == me and \
						board[i+3][j-3] == 0:
						score += 20
					# 10011
					# 11001
					
					### 4连
					## 右
					# 011110
					if (j+4)<15 and (j-1)>=0 and \
						board[i][j-1] == 0 and \
						board[i][j+1] == me and \
						board[i][j+2] == me and \
						board[i][j+3] == me and \
						board[i][j+4] == 0:
						score += 5000     # 成杀
					# 011112
					elif (j+3)<15 and (j-1)>=0 and \
						board[i][j-1] == 0 and \
						board[i][j+1] == me and \
						board[i][j+2] == me and \
						board[i][j+3] == me and \
						board[i][j+3] == enemy:
						score += 100
					# 211110
					elif (j+4)<15 and (j-1)>=0 and \
						board[i][j-1] == enemy and \
						board[i][j+1] == me and \
						board[i][j+2] == me and \
						board[i][j+3] == me and \
						board[i][j+4] == 0:
						score += 100
					# 11011
					elif (j+4)<15 and \
						board[i][j+1] == me and \
						board[i][j+2] == 0 and \
						board[i][j+3] == me and \
						board[i][j+4] == me:
						score += 100
					## 右下
					# 011110
					if (i-1)>=0 and (j-1)>=0 and (i+4)<15 and (j+4)<15 and \
						board[i-1][j-1] == 0 and \
						board[i+1][j+1] == me and \
						board[i+2][j+2] == me and \
						board[i+3][j+3] == me and \
						board[i+4][j+4] == 0:
						score += 5000
					# 011112
					elif (i-1)>=0 and (j-1)>=0 and (i+4)<15 and (j+4)<15 and \
						board[i-1][j-1] == 0 and \
						board[i+1][j+1] == me and \
						board[i+2][j+2] == me and \
						board[i+3][j+3] == me and \
						board[i+4][j+4] == enemy:
						score += 100
					# 211110
					elif (i-1)>=0 and (j-1)>=0 and (i+4)<15 and (j+4)<15 and \
						board[i-1][j-1] == enemy and \
						board[i+1][j+1] == me and \
						board[i+2][j+2] == me and \
						board[i+3][j+3] == me and \
						board[i+4][j+4] == 0:
						score += 100
					# 11011
					elif (j+4)<15 and (i+4)<15 and \
						board[i+1][j+1] == me and \
						board[i+2][j+2] == 0 and \
						board[i+3][j+3] == me and \
						board[i+4][j+4] == me:
						score += 100
					## 下
					# 011110
					if (i+4)<15 and (i-1)>=0 and \
						board[i-1][j] == 0 and \
						board[i+1][j] == me and \
						board[i+2][j] == me and \
						board[i+3][j] == me and \
						board[i+4][j] == 0:
						score += 5000
					# 011112
					elif (i+4)<15 and (i-1)>=0 and \
						board[i-1][j] == 0 and \
						board[i+1][j] == me and \
						board[i+2][j] == me and \
						board[i+3][j] == me and \
						board[i+4][j] == enemy:
						score += 100
					# 211110
					elif (i+4)<15 and (i-1)>=0 and \
						board[i-1][j] == enemy and \
						board[i+1][j] == me and \
						board[i+2][j] == me and \
						board[i+3][j] == me and \
						board[i+4][j] == 0:
						score += 100
					# 11011
					elif (i+4)<15 and \
						board[i+1][j] == me and \
						board[i+2][j] == 0 and \
						board[i+3][j] == me and \
						board[i+4][j] == me:
						score += 100
					## 左下
					# 011110
					if (i-1)>=0 and (j-4)>=0 and (i+4)<15 and (j+1)<15 and \
						board[i-1][j+1] == 0 and \
						board[i+1][j-1] == me and \
						board[i+2][j-2] == me and \
						board[i+3][j-3] == me and \
						board[i+4][j-4] == 0:
						score += 5000
					# 011112
					elif (i-1)>=0 and (j-4)>=0 and (i+4)<15 and (j+1)<15 and \
						board[i-1][j+1] == 0 and \
						board[i+1][j-1] == me and \
						board[i+2][j-2] == me and \
						board[i+3][j-3] == me and \
						board[i+4][j-4] == enemy:
						score += 100
					# 211110
					elif (i-1)>=0 and (j-4)>=0 and (i+4)<15 and (j+1)<15 and \
						board[i-1][j+1] == enemy and \
						board[i+1][j-1] == me and \
						board[i+2][j-2] == me and \
						board[i+3][j-3] == me and \
						board[i+4][j-4] == 0:
						score += 100
					# 11011
					elif (j-4)>=0 and (i+4)<15 and \
						board[i+1][j-1] == me and \
						board[i+2][j-2] == 0 and \
						board[i+3][j-3] == me and \
						board[i+4][j-4] == me:
						score += 100
					'''
				# 评估敌方棋型(扣分)
				if board[i][j] == enemy:
					# 5连检测
					score -= self._checkChessStruct(board, i, j, '11111') * (10000, 9000)[1+_view]
					# 2连检测
					score -= self._checkChessStruct(board, i, j, '0110') * (15, 15)[1+_view]
					score -= self._checkChessStruct(board, i, j, '01010') * (10, 10)[1+_view]
					score -= self._checkChessStruct(board, i, j, '010010') * (5, 5)[1+_view]
					# 3连检测
					score -= self._checkChessStruct(board, i, j, '01110') * (50, 600)[1+_view]
					score -= self._checkChessStruct(board, i, j, '001112') * (20, 20)[1+_view]
					score -= self._checkChessStruct(board, i, j, '211100') * (20, 20)[1+_view]
					score -= self._checkChessStruct(board, i, j, '10011') * (16, 16)[1+_view]
					score -= self._checkChessStruct(board, i, j, '11001') * (16, 16)[1+_view]

					score -= self._checkChessStruct(board, i, j, '011010') * (20, 600)[1+_view]
					score -= self._checkChessStruct(board, i, j, '010110') * (20, 600)[1+_view]
					score -= self._checkChessStruct(board, i, j, '210110') * (16, 16)[1+_view]
					score -= self._checkChessStruct(board, i, j, '211010') * (16, 16)[1+_view]
					score -= self._checkChessStruct(board, i, j, '010112') * (16, 16)[1+_view]
					score -= self._checkChessStruct(board, i, j, '011012') * (16, 16)[1+_view]
					# 4连检测
					score -= self._checkChessStruct(board, i, j, '011110') * (900, 1500)[1+_view]
					score -= self._checkChessStruct(board, i, j, '011112') * (110, 1000)[1+_view]
					score -= self._checkChessStruct(board, i, j, '211110') * (110, 1000)[1+_view]
					score -= self._checkChessStruct(board, i, j, '11011') * (100, 1000)[1+_view]
					score -= self._checkChessStruct(board, i, j, '11101') * (100, 1000)[1+_view]
					score -= self._checkChessStruct(board, i, j, '10111') * (100, 1000)[1+_view]
		return score
	
	# 该函数用于辅助判分
	# 判断该棋子[i][j]周围是否存在struct棋型:struct为格式串('21110')第一个1代表当前棋子的位置
	# 同时要考虑墙和对方
	def _checkChessStruct(self, board, i, j, struct):
		me = board[i][j]  # 获取当前判定的棋子
		if me == 1:
			enemy = 2
		elif me == 2:
			enemy = 1
		# 初始化(1代表存在，0代表不存在)
		rightExist = 1
		rightdownExist = 1
		downExist = 1
		leftdownExist = 1
		# 依次判定右、右下、下、左下，避免出现重复
		pos = struct.index('1')   # 获取当前棋子在格式中的位置 2也可以判定为墙
		# print(f'\n    > enemy={enemy} me={me}')
		for index in range(len(struct)):
			# print(f'\n     > 正在判定{struct}的第{index}位:{struct[index]}')
			# 右判定
			if rightExist == 1:
				# print(f'     > 右判断: 第{index}个:{board[i][j+index-pos]} struct[index]={struct[index]}')
				if (j+index-pos)>=15 or (j+index-pos)<0:    # 超越边界
					rightExist = 0
				elif int(struct[index]) == 2 and board[i][j+index-pos] != enemy:
					rightExist = 0
				elif int(struct[index]) == 1 and board[i][j+index-pos] != me:
					rightExist = 0
				elif int(struct[index]) == 0 and board[i][j+index-pos] != 0:
					rightExist = 0
			# 右下判定
			if rightdownExist == 1:
				# print(f'     > 右下判断: 第{index}个:{board[i+index-pos][j+index-pos]} struct[index]={struct[index]}')
				if (j+index-pos) >= 15 or (j+index-pos)<0 or (i+index-pos)>=15 or (i+index-pos)<0:
					rightdownExist = 0
				elif int(struct[index]) == 2 and board[i+index-pos][j+index-pos] != enemy:
					rightdownExist = 0
				elif int(struct[index]) == 1 and board[i+index-pos][j+index-pos] != me:
					rightdownExist = 0
				elif int(struct[index]) == 0 and board[i+index-pos][j+index-pos] != 0:
					rightdownExist = 0			
			# 下判定
			if downExist == 1:
				# print(f'     > 下判断: 第{index}个:{board[i+index-pos][j]} struct[index]={struct[index]}')
				if (i+index-pos)>=15 or (i+index-pos)<0:    # 超越边界
					downExist = 0
				elif int(struct[index]) == 2 and board[i+index-pos][j] != enemy:
					downExist = 0
				elif int(struct[index]) == 1 and board[i+index-pos][j] != me:
					downExist = 0
				elif int(struct[index]) == 0 and board[i+index-pos][j] != 0:
					downExist = 0
			# 左下判定
			if leftdownExist == 1:
				# print(f'     > 左下判断: 第{index}个:{board[i+index-pos][j-index+pos]} struct[index]={struct[index]}')
				if (j-index+pos) >= 15 or (j-index+pos)<0 or (i+index-pos)>=15 or (i+index-pos)<0:
					leftdownExist = 0
				elif int(struct[index]) == 2 and board[i+index-pos][j-index+pos] != enemy:
					leftdownExist = 0
				elif int(struct[index]) == 1 and board[i+index-pos][j-index+pos] != me:
					leftdownExist = 0
				elif int(struct[index]) == 0 and board[i+index-pos][j-index+pos] != 0:
					leftdownExist = 0
			if rightExist+rightdownExist+downExist+leftdownExist == 0:   # 判定全部不存在直接返回
				return 0
		# print(f'> struct={struct},r={rightExist},rd={rightdownExist},d={downExist},ld={leftdownExist}') # 调试输出
		return rightExist+rightdownExist+downExist+leftdownExist   # 累计倍数
		
	# 搜索函数，用于探索可能的结果
	# 参数为棋盘节点(内部类)
	def _search(self, chessboard):
		# 判断自身是否是叶子节点
		if chessboard.floor == chessboard.floorMax:
			# 达到最大层数
			# print('  > 已是子节点, 开始判分')
			_score = self._grade(chessboard.getBoard(), chessboard.floor)   # 对当前局势判分(只有最终的子节点需要通过判分函数打分)
			# print(f'  > 分数:{_score}')
			chessboard.setScore(_score)   # 设置节点分值
			return 0                      # 返回
		else:
			chessboard.bornChild()  # 遍历获取子节点
			print(f'> 当前节点一共{len(chessboard.childList)}个子节点')
			# dfs
			highest = -99999   # 子节点中的最高分
			lowest = 99999     # 子节点中的最低分
			for child in chessboard.childList:
				self._search(child)    # 深度优先搜索
				# 记录最高最低分
				if child.score > highest:
					highest = child.score
					highestBoard = child.getBoard()
				if child.score < lowest:
					lowest = child.score
					lowestBoard = child.getBoard()
					
				# 如果是顶层，则记录子节点分数并进行剪枝
				if chessboard.floor == 1:
					# highest 为当前时刻的最高分
					# 将当前的highest复制到全局变量用于剪枝
					#   如果在alpha层碰到小于这个的分数，就直接剪掉
					self.rootHighest = highest
					
				# alpha层(第二层)，选取子节点的最小值
				elif chessboard.floor == 2:
					if lowest <= self.rootHighest:
						# 因为这层肯定是要选最小值，而我要在这层中选取最大值，已经小于我现在能走的最大值的话就可以直接剪掉了
						chessboard.setScore(lowest)   # 设置分值
						print(f'  > 敌方选择最优局面，分值:{lowest}，剪枝，当前rootHighest={self.rootHighest}')
						return 0                      # 直接不搜了返回
					

			
			print(f'> 当前节点的子节点最高分:{highest}')
			print(f'> 当前节点的子节点最低分:{lowest}')
			
			# 判断是alpha还是beta(取最大值还是最小值)
			if chessboard.floor % 2 != 0:   # 当前为奇数层，子节点为偶数层(alpha) 分值越大越好
				chessboard.setScore(highest)
				print('> 我方最优局面:')
				# chessboard.greatOutput(highestBoard)
				print(f'> 当前节点分值: {chessboard.score}')
				# 判断是不是顶层，如果是顶层，则返回坐标
				if chessboard.floor == 1:
					pos = self._getChoiceFromBoard(highestBoard)
					return pos   # 返回最优坐标[x,y]
			elif chessboard.floor % 2 == 0:   # 子节点为奇数层(beta) 取最小值
				chessboard.setScore(lowest)
				print('> 敌方最优局面:')
				# chessboard.greatOutput(lowestBoard)
				print(f'> 当前节点分值: {chessboard.score}\n')
				

	# 返回下一步的决策
	def choice(self):
		t1 = time.time()
		pos = self._search(self.chessboard)   # 搜索最优策略
		print(f'最优解: {pos}')
		t2 = time.time()
		print(f'用时: {t2-t1}s')
		
		return json.dumps(pos)
