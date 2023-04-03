from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QKeyEvent, QTextCursor
from PyQt5.QtCore import Qt, QEvent
from typing import Callable
from PyQt5.QtWidgets import QApplication


class PlainTextEdit(QPlainTextEdit):

    __MAX_LENGTH = 3000
    __NOT_RESTRICTED_KEYS = [
        Qt.Key.Key_Up,
        Qt.Key.Key_Down,
        Qt.Key.Key_Left,
        Qt.Key.Key_Right,
        Qt.Key.Key_Backspace,
    ]

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.__max_length = self.__MAX_LENGTH

    def set_maximum_length(self, value):
        self.__max_length = value

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.__handle_length_greater_than_maximum(event, super().keyPressEvent)
    
    def __handle_length_greater_than_maximum(self,
                                             event: QKeyEvent,
                                             normal_key_processing: Callable[[QKeyEvent], None]):
        
        if self.__is_ctrl_v_event(event) and event.type() == QEvent.Type.KeyRelease:
            self.__paste_text_from_clipboard()
            event.ignore()

        elif self.__can_key_event_be_accepted(event):
            normal_key_processing(event)
        
        else:
            event.ignore()

    def __is_ctrl_v_event(self, event: QKeyEvent):
        return event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_V

    def __paste_text_from_clipboard(self):
        current_text = self.document().toPlainText()
        clipboard_text = QApplication.clipboard().text()
        text_cursor = self.textCursor()
        selected_text_start_index = text_cursor.selectionStart()
        selected_text_end_index = text_cursor.selectionEnd()
        
        # Replace the selected text with the clipboard text
        new_text = current_text[ : selected_text_start_index] + clipboard_text + current_text[selected_text_end_index : ]
        
        # Limit the paste to the maximum length
        self.setPlainText(new_text[ : self.__max_length])

        
        # Set the cursor on the same position that it was before pasting. When calling
        # setPlainText the cursor is set on position 0 by default
        new_cursor_position = selected_text_start_index + len(clipboard_text)
        if new_cursor_position > self.__max_length:
            new_cursor_position = self.__max_length
        
        new_cursor = QTextCursor(text_cursor)
        new_cursor.setPosition(new_cursor_position)
        self.setTextCursor(new_cursor)


    def __can_key_event_be_accepted(self, event: QKeyEvent):
        
        # Allow ctrl + C, ctrl + X  and ctrl + Z
        if (event.modifiers() == Qt.KeyboardModifier.ControlModifier and (event.key() == Qt.Key.Key_C or event.key() == Qt.Key.Key_X or event.key() == Qt.Key.Key_Z)):
            return True
        
        # Forbid pasting text(ctrl + V), this must be handled by other method due to length restriction
        if (event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_V):
            return False
        
        current_length = len(self.document().toPlainText())
        return ((current_length >= self.__max_length and event.key() in self.__NOT_RESTRICTED_KEYS) or
                current_length < self.__max_length)

    def keyReleaseEvent(self, event:QKeyEvent) -> None:
        self.__handle_length_greater_than_maximum(event, super().keyReleaseEvent)