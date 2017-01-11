# import os
# import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from flask.ext.script import Manager, Server, Command, Option
# from flix.flix import app
# from models import database, Media, Show, File, Directory, List


# manager = Manager(app)

# manager.add_command("runserver", Server(
#    use_debugger=True,
#    use_reloader=True,
#    host='0.0.0.0',
#    port=5000))


# if __name__ == '__main__':
#     database.create_tables([Media, Show, File, Directory, List], safe=True)
#     manager.run()

from flix.flix import app
from flix.models import database, Media, File, Directory
from flix.utils import create_directory
from flix.settings import DB_PATH
from werkzeug.serving import run_simple


if __name__ == '__main__':
    create_directory(DB_PATH)
    database.create_tables([Media, File, Directory], safe=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG'] = True
    run_simple('127.0.0.1', 5000, app, use_reloader=True)

