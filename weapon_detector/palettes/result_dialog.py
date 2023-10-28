result_dialog_styles = """
*{
  color: #000;
}
QWidget {
  background-color: #F5F5F5;
}
QScrollBar:vertical {
  width: 20px;
  margin: 20px 0 20px 0;
  background-color: #C0C0C0;
}
QScrollBar::handle:vertical {
  min-height: 10px;
  border-radius: 10px;
  background-color: #A0A0A0;
}
QScrollBar::add-line:vertical {
  border-radius: 10px;
  height: 20px;
  subcontrol-position: bottom;
  subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
  border-radius: 10px;
  height: 20px;
  subcontrol-position: top;
  subcontrol-origin: margin;
}
QScrollBar::up-arrow:vertical { 
  height: 20px; 
  width: 20px 
}
QScrollBar::down-arrow:vertical {
  height: 20px; 
  width: 20px                              
}
"""
