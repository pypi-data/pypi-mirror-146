from MzView import MzView

from flask import *

app = Flask('mzflaskfive')

app.add_url_rule('/', view_func=MzView.as_view('index'))
print(app.url_map)  # 输出所有路由


if __name__ == '__main__':
	app.run('0.0.0.0', 5000)
