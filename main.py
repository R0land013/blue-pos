from easy_mvp.application_manager import ApplicationManager
from easy_mvp.intent import Intent
from presenter.main import MainPresenter
from util.resources_path import resource_path


app = ApplicationManager(app_name='Blue POS',
                         window_icon_path=resource_path('view/ui/images/bluepos.png'))
intent = Intent(MainPresenter)
app.execute_app(intent)
