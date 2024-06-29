from pathlib import Path
from utils import Utils
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     engine = QQmlApplicationEngine()
    
#     file = Path(__file__).resolve().parent / "Test.qml"
#     engine.load(file)


#     if not engine.rootObjects():
#         sys.exit(-1)
#     sys.exit(app.exec())

file_path = r'E:\\_BrainLab\\SampleRecords\\testowy_bardzo_krotki.csv'
icp = Utils.read_data(file_path, 'icp[mmHg]')
