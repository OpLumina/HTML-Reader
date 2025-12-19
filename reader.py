import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QFileDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

# 1. The "Firewall" class
class OfflineInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        url = info.requestUrl()
        # Only allow local file requests (file://)
        if not url.isLocalFile():
            print(f"🚫 Blocked external request to: {url.toString()}")
            info.block(True)

class LocalReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Private Offline HTML Reader")
        self.resize(1000, 750)

        # Container setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # UI Buttons
        self.btn_open = QPushButton("📂 Open Local HTML File")
        self.btn_open.clicked.connect(self.select_file)
        
        self.btn_refresh = QPushButton("🔄 Refresh (Reload from Disk)")
        self.btn_refresh.clicked.connect(self.refresh_page)

        # 2. Setup the Offline Profile
        self.view = QWebEngineView()
        self.interceptor = OfflineInterceptor()
        
        # Apply the interceptor to the default profile
        profile = QWebEngineProfile.defaultProfile()
        profile.setUrlRequestInterceptor(self.interceptor)
        # Disable cache to ensure nothing is stored/fetched from previous sessions
        profile.setHttpCacheType(QWebEngineProfile.NoCache)

        self.layout.addWidget(self.btn_open)
        self.layout.addWidget(self.btn_refresh)
        self.layout.addWidget(self.view)

        self.current_url = None

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open HTML", "", "HTML Files (*.html *.htm)")
        if file_path:
            self.current_url = QUrl.fromLocalFile(os.path.abspath(file_path))
            self.view.load(self.current_url)

    def refresh_page(self):
        if self.current_url:
            self.view.reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LocalReader()
    window.show()
    sys.exit(app.exec_())