

from app import app,db
from app.models import User,Post


@app.shell_context_processor #装饰器
def make_shell_context():
    return{'db':db,'User':User,'Post':Post}



if __name__ == '__main__':
    # print("git ok1")
    app.run(debug=True)

