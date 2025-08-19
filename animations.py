from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from config import getDuration, getType

animations = []
count = 0

def animatePanel(parent, window, show=True, sub_widget: list = None):
    from widgets import MessageBox

    global count

    start_height = parent.maximumHeight()
    end_height = window.size().height() if show else 0

    if sub_widget and show:
        for widget in sub_widget:
            widget.show()

    elif sub_widget and not show:
        for widget in sub_widget:
            widget.hide()

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
                # link=True
                link='https://doc.qt.io/qtforpython-6/PySide6/QtCore/QEasingCurve.html'

            )

            count += 1

    # group = QParallelAnimationGroup()

    # height_anim = QPropertyAnimation(parent, b"maximumHeight")
    # height_anim.setDuration(300)
    # height_anim.setStartValue(start_height)
    # height_anim.setEndValue(end_height)
    # height_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    # opacity_anim = QPropertyAnimation(parent, b"windowOpacity")
    # opacity_anim.setDuration(300)
    # opacity_anim.setStartValue(0.0)
    # opacity_anim.setEndValue(1.0)
    # opacity_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

    # group.addAnimation(height_anim)
    # group.addAnimation(opacity_anim)

    # animations.append(group)
    animations.append(anim)


    if not show:
        anim.finished.connect(parent.hide)
        # group.finished.connect(parent.hide)

    else:
        parent.show()

    # group.start()
    anim.start()