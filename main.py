from easy_mvp.application_manager import ApplicationManager
from easy_mvp.intent import Intent

from presenter.main import MainPresenter

app = ApplicationManager(app_name='Blue POS',
                         window_icon_path='./view/ui/images/bluepos.png')
intent = Intent(MainPresenter)
app.execute_app(intent)
