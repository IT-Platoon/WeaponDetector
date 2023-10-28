main_window_styles = """
*{
  color: #000;
}
#load_button {
  border-radius: 150px;
}
#load_button:hover {
  background-color: #DCDCDC;
}
QTabWidget::pane {
  border: 1px solid lightgray;
  top:-1px;
  background-color: #F5F5F5;
}
QTabBar::tab {
  background-color: #DCDCDC;
  border: 1px solid lightgray;
  padding: 10px 20px;
}
QTabBar::tab:hover {
  background-color: #C0C0C0;
}
QTabBar::tab:selected {
  background-color: #F5F5F5;
  margin-bottom: -1px;
}
QPlainTextEdit, QWidget {
  background-color: #F5F5F5;
}
"""
