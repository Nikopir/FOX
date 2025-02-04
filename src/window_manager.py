class WindowManager:
    def __init__(self, screen):
        self.screen = screen
        self.windows = {
        }
        self.current_window = None

    def add_window(self, name, value):
        self.windows[name] = value

    def set_window(self, name):
        self.current_window = self.windows.get(name)

    def run(self):
        while self.current_window:
            self.current_window.run()
