from flask import Flask

app = Flask(__name__)
app.config.from_object('taskplanner.config.DevelopmentConfig')

import taskplanner.views.admin
import taskplanner.views.auth
import taskplanner.views.project