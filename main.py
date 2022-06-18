import sys
from typing import Union, Optional
from operator import add, sub, mul, truediv

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase

from calc_design import Ui_MainWindow


operations = {
    '+': add,
    '-': sub,
    'x': mul,
    '/': truediv
}

error_zero_div = 'Division by zero'
error_undefined = 'Result is undefined'

class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.le_entry = self.ui.lineEdit
        self.lbl_temp = self.ui.label
        self.entry_max_len = self.le_entry.maxLength()

        QFontDatabase.addApplicationFont("fonts/Rubik-Regular.ttf")

        # digits
        self.ui.btn_0.clicked.connect(self.add_digit)
        self.ui.btn_1.clicked.connect(self.add_digit)
        self.ui.btn_2.clicked.connect(self.add_digit)
        self.ui.btn_3.clicked.connect(self.add_digit)
        self.ui.btn_4.clicked.connect(self.add_digit)
        self.ui.btn_5.clicked.connect(self.add_digit)
        self.ui.btn_6.clicked.connect(self.add_digit)
        self.ui.btn_7.clicked.connect(self.add_digit)
        self.ui.btn_8.clicked.connect(self.add_digit)
        self.ui.btn_9.clicked.connect(self.add_digit)

        # actions
        self.ui.btn_c.clicked.connect(self.clear_all)
        self.ui.btn_ce.clicked.connect(self.clear_entry)
        self.ui.btn_dot.clicked.connect(self.add_point)
        self.ui.btn_neg.clicked.connect(self.negate)
        self.ui.btn_backspace.clicked.connect(self.backspace)


        #math
        self.ui.btn_equal.clicked.connect(self.calculate)
        self.ui.btn_add.clicked.connect(self.math_operation)
        self.ui.btn_sub.clicked.connect(self.math_operation)
        self.ui.btn_mul.clicked.connect(self.math_operation)
        self.ui.btn_div.clicked.connect(self.math_operation)

    def add_digit(self):
        self.remove_error()
        btn = self.sender()
        digit_buttons = ('btn_0', 'btn_1', 'btn_2', 'btn_3', 'btn_4',
                         'btn_5', 'btn_6', 'btn_7', 'btn_8', 'btn_9')
        if btn.objectName() in digit_buttons:
            if self.le_entry.text() == '0': #не забываем убирать лишний ui.
                self.le_entry.setText(btn.text())
            else:
                self.le_entry.setText(self.le_entry.text() + btn.text())

    def clear_all(self) -> None:
        self.remove_error()
        self.le_entry.setText('0')
        self.lbl_temp.clear() #не забываем убирать лишний ui.

    def clear_entry(self) -> None:
        self.remove_error()
        self.le_entry.setText('0')

    def add_point(self) -> None:
        if '.' not in self.le_entry.text():
            self.le_entry.setText(self.le_entry.text() + '.')

    def negate(self) -> None:
        entry = self.le_entry.text()
        if '-' not in entry:
            if entry != '0':
                entry = '-' + entry
        else:
            entry = entry[1:]

        if len(entry) == self.entry_max_len + 1 and '-' in entry:
            self.le_entry.setMaxLength(self.entry_max_len + 1)
        else:
            self.le_entry.setMaxLength(self.entry_max_len)

        self.le_entry.setText(entry)
    def backspace(self) -> None:
        self.remove_error()
        entry = self.le_entry.text()

        if len(entry) != 1:
            if len(entry) == 2 and '-' in entry:
                self.le_entry.setText('0')
            else:
                self.le_entry.setText(entry[:-1])
        else:
            self.le_entry.setText('0')

    def add_temp(self) -> None:
        btn = self.sender()
        entry = self.remove_trailing_zeros(self.le_entry.text())

        if not self.lbl_temp.text() or self.get_math_sign() == '=':
            self.lbl_temp.setText(entry + f' {btn.text()} ')
            self.le_entry.setText('0')

    @staticmethod
    def remove_trailing_zeros(num: str) -> str:
        n = str(float(num))
        return n[:-2] if n[-2:] == '.0' else n

    def get_entry_num(self) -> int | float:
        entry = self.le_entry.text().strip('.')
        return float(entry) if '.' in entry else int(entry)

    def get_temp_num(self) -> Union[int, float, None]:
        if self.lbl_temp.text():
            temp = self.lbl_temp.text().strip('.').split()[0]
            return float(temp) if '.' in temp else int(temp)

    def get_math_sign(self) -> Optional[str]:
        if self.lbl_temp.text():
            return self.lbl_temp.text().strip('.').split()[-1]

    def calculate(self) -> Optional[str]:
        entry = self.le_entry.text()
        temp = self.lbl_temp.text()

        if temp:
            try:
                result = self.remove_trailing_zeros(
                    str(operations[self.get_math_sign()](self.get_temp_num(), self.get_entry_num())))
                self.lbl_temp.setText(temp + self.remove_trailing_zeros(entry) + ' =')
                self.le_entry.setText(result)
                return result
            except KeyError:
                pass

            except ZeroDivisionError:
                if self.get_temp_num() == 0:
                    self.show_error(error_undefined)
                else:
                    self.show_error(error_zero_div)

    def math_operation(self) -> None:
        temp = self.lbl_temp.text()
        btn = self.sender()

        if not temp:
            self.add_temp()
        else:
            if self.get_math_sign() != btn.text():
                if self.get_math_sign() == '=':
                    self.add_temp()
                else:
                    self.lbl_temp.setText(temp[:-2] + f'{btn.text()} ')
            else:
                try:
                    self.lbl_temp.setText(self.calculate() + f' {btn.text()}')
                except TypeError:
                    pass



    def clear_temp_if_equality(self) -> None:
        if self.get_math_sign() == '=':
            self.lbl_temp.clear()

    def show_error(self, text: str) -> None:
        self.le_entry.setMaxLength(len(text))
        self.le_entry.setText(text)
        self.disable_buttons(True)

    def remove_error(self) -> None:
        if self.le_entry.text() in (error_undefined, error_zero_div):
            self.le_entry.setMaxLength(self.entry_max_len)
            self.le_entry.setText('0')
            self.disable_buttons(False)

    def disable_buttons(self, disable: bool) -> None:
        self.ui.btn_c.setDisabled(disable)
        self.ui.btn_add.setDisabled(disable)
        self.ui.btn_sub.setDisabled(disable)
        self.ui.btn_mul.setDisabled(disable)
        self.ui.btn_div.setDisabled(disable)
        self.ui.btn_neg.setDisabled(disable)
        self.ui.btn_dot.setDisabled(disable)

        color = 'color: #888;' if disable else 'color: white;'
        self.change_buttons_color(color)

    def change_buttons_color(self, css_color: str) -> None:
        self.ui.btn_c.setStyleSheet(css_color)
        self.ui.btn_add.setStyleSheet(css_color)
        self.ui.btn_sub.setStyleSheet(css_color)
        self.ui.btn_mul.setStyleSheet(css_color)
        self.ui.btn_div.setStyleSheet(css_color)
        self.ui.btn_neg.setStyleSheet(css_color)
        self.ui.btn_dot.setStyleSheet(css_color)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()

    sys.exit(app.exec())