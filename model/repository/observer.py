

class RepositoryObserver:

    def __init__(self):
        self.__listeners = []

    def add_on_data_changed_listener(self, listener):
        if listener.on_data_changed() is None:
            raise NotImplementedError('Listeners must implement the method on_data_changed().')

        self.__listeners.append(listener)

    def remove_on_data_changed_listener(self, listener):

        while listener in self.__listeners:
            self.__listeners.remove(listener)

    def _notify_on_data_changed_listeners(self):
        for a_listener in self.__listeners:
            a_listener.on_data_changed()
