import pyqt5ac

pyqt5ac.main(
    uicOptions='--from-imports',
    force=False,
    initPackage=True,
    ioPaths=[
        ['resources.qrc', '../forms/resources.py'],
        ['main_window.ui', '../forms/main_window.py'],
        ['result_dialog.ui', '../forms/result_dialog.py'],
        ['result_widget.ui', '../forms/result_widget.py'],
    ],
)
