from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
# animations = {}
animations = []

def animatePanel(parent, window, show=True, sub_widget: list = None):
    start_height = parent.maximumHeight()
    end_height = window.size().height() if show else 0

    if sub_widget and show:
        for widget in sub_widget:
            widget.show()

    elif sub_widget and not show:
        for widget in sub_widget:
            widget.hide()


    # anim = QPropertyAnimation(parent, b"maximumHeight")
    # anim.setDuration(300)
    # anim.setStartValue(start_height)
    # anim.setEndValue(end_height)
    # anim.setEasingCurve(QEasingCurve.Type.InOutQuad)


    # animations[parent] = anim  

    # anim.finished.connect(lambda: animations.pop(parent, None))

    # anim.start()

    anim = QPropertyAnimation(parent, b"maximumHeight", parent)
    anim.setDuration(300)
    anim.setStartValue(start_height)
    anim.setEndValue(end_height)
    # anim.setEasingCurve(QEasingCurve.Type.SineCurve)
    anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

    animations.append(anim)


    if not show:
        # if sub_widget:
        #     for widget in sub_widget:
        #         anim.finished.connect(widget.hide)
        anim.finished.connect(parent.hide)  # hide only when collapse finishes
    else:

        # if sub_widget:
        #     for widget in sub_widget:
                # anim.finished.connect(widget.show)
        parent.show()  # make it visible before expand starts

    anim.start()