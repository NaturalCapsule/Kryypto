from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from config import getDuration, getType

animations = []
count = 0



def animatePanel(parent, window, inner_window, show=True, sub_widget: list = None, is_dock = True, different = False):
    def animatePanelHeight():
        from widgets import MessageBox


        if sub_widget and show:
            for widget in sub_widget:
                widget.show()
                widget.setMinimumHeight(25)

        elif sub_widget and not show:
            for widget in sub_widget:
                widget.setMinimumHeight(0)
                widget.hide()


        from widgets import MessageBox

        global count

        start_height = parent.maximumHeight()

        end_height = window.size().height() if show else 0

        anim = QPropertyAnimation(parent, b"maximumHeight", parent)

        anim.setDuration(getDuration())
        anim.setStartValue(start_height)
        anim.setEndValue(end_height)



        curve_name = getType()

        if hasattr(QEasingCurve.Type, curve_name):
            anim.setEasingCurve(getattr(QEasingCurve.Type, curve_name))
        else:
            anim.setEasingCurve(QEasingCurve.Type.BezierSpline)
            if count == 0:
                MessageBox(
                    f"'{getType()}' is not a valid animation, please check: "
                    "<a href='https://doc.qt.io/qtforpython-6/PySide6/QtCore/QEasingCurve.html'>Qt Docs</a>",
                    link='https://doc.qt.io/qtforpython-6/PySide6/QtCore/QEasingCurve.html'

                )

                count += 1

        animations.append(anim)


        if not show:
            anim.finished.connect(parent.hide)
        else:
            parent.show()

        anim.start()

        if sub_widget and show:
            for widget in sub_widget:
                widget.setMinimumHeight(0)



    def animatePanelWidth():
        if sub_widget and show:
            for widget in sub_widget:
                widget.show()
                widget.setMinimumWidth(300)


        elif sub_widget and not show:
            for widget in sub_widget:
                widget.setMinimumWidth(0)
                widget.hide()
                
        from widgets import MessageBox

        global count

        start_width = parent.maximumWidth()
        # start_width = parent.width()

        end_width = window.size().width() if show else 0

        anim = QPropertyAnimation(parent, b"maximumWidth", parent)

        anim.setDuration(getDuration())
        anim.setStartValue(start_width)
        anim.setEndValue(end_width)



        curve_name = getType()

        if hasattr(QEasingCurve.Type, curve_name):
            anim.setEasingCurve(getattr(QEasingCurve.Type, curve_name))
        else:
            anim.setEasingCurve(QEasingCurve.Type.BezierSpline)
            if count == 0:
                MessageBox(
                    f"'{getType()}' is not a valid animation, please check: "
                    "<a href='https://doc.qt.io/qtforpython-6/PySide6/QtCore/QEasingCurve.html'>Qt Docs</a>",
                    # link=True
                    link='https://doc.qt.io/qtforpython-6/PySide6/QtCore/QEasingCurve.html'

                )

                count += 1

        animations.append(anim)


        if not show:
            anim.finished.connect(parent.hide)

        else:
            parent.show()

        anim.start()

        if sub_widget and show:
            for widget in sub_widget:
                widget.setMinimumWidth(0)


    if is_dock is False:
        animatePanelHeight()
        # return
    else:

        dock_area = inner_window.dockWidgetArea(parent)
        if dock_area in [Qt.DockWidgetArea.LeftDockWidgetArea, Qt.DockWidgetArea.RightDockWidgetArea]:
            animatePanelWidth()
            parent.setMaximumHeight(16777215)
        else:
            animatePanelHeight()
            parent.setMaximumWidth(16777215)
            # parent.setMinimumHeight(1000)

def locate_dock_widget(parent, inner_window):
    dock_area = inner_window.dockWidgetArea(parent)
    if dock_area in [Qt.DockWidgetArea.BottomDockWidgetArea, Qt.DockWidgetArea.TopDockWidgetArea]:
        return "height"
    else:
        return 'width'