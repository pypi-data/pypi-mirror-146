from flask.views import MethodView
from flask import *
from mzflaskfive.MzChess import MzChess

# 网页视图类
class MzView(MethodView):
	def get(self):
		return render_template('index.html')
	def post(self):
		chessboardstr = request.form['chessboardstr']
		mzChess = MzChess(chessboardstr)         # 实例化棋盘对象
		choice = mzChess.choice()                 # 获取ai决策 return:[x, y]
		return choice
