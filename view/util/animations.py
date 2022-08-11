from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QPoint


class GoForwardAndReturnAnimation(QSequentialAnimationGroup):

    RIGHT_DIRECTION = 'right'
    LEFT_DIRECTION = 'left'
    UP_DIRECTION = 'up'
    DOWN_DIRECTION = 'down'

    def __init__(self, an_object, a_property: bytes, distance: int, direction: str, duration: int = 500):
        super().__init__()

        self.__an_object = an_object
        self.__a_property = a_property
        self.__distance = distance
        self.__direction = direction
        self.__duration = duration

    def __add_forward_movement_animation(self):
        move_forward_animation = QPropertyAnimation(self.__an_object, self.__a_property)
        move_forward_animation.setDuration(self.__duration)
        move_forward_animation.setStartValue(self.__an_object.pos())
        move_forward_animation.setEndValue(
            self.__get_end_position_of_forward_movement_depending_on_direction())
        self.addAnimation(move_forward_animation)

    def __get_end_position_of_forward_movement_depending_on_direction(self) -> QPoint:
        if self.__direction == self.RIGHT_DIRECTION:
            return self.__an_object.pos() + QPoint(self.__distance, 0)
        elif self.__direction == self.LEFT_DIRECTION:
            return self.__an_object.pos() - QPoint(self.__distance, 0)
        elif self.__direction == self.UP_DIRECTION:
            return self.__an_object.pos() - QPoint(0, self.__distance)
        else:
            return self.__an_object.pos() + QPoint(0, self.__distance)

    def __add_return_movement_animation(self):
        return_movement_animation = QPropertyAnimation(self.__an_object, self.__a_property)
        return_movement_animation.setDuration(self.__duration)
        # Este movimiento comienza a partir del la posición donde quedó el widget animado
        return_movement_animation.setStartValue(
            self.__get_end_position_of_forward_movement_depending_on_direction())
        # Se regresa al punto en el que se encontraba el widget antes de ser animado
        return_movement_animation.setEndValue(self.__an_object.pos())
        self.addAnimation(return_movement_animation)

    def start(self, policy=QSequentialAnimationGroup.KeepWhenStopped):
        self.clear()
        self.__add_forward_movement_animation()
        self.__add_return_movement_animation()
        super().start(policy)
