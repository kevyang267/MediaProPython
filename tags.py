class Tags():
    def __init__(self, tag_name, tag_color):
        self.tag_name = tag_name 
        self.tag_color = tag_color 
        self.enabled = False

    def set_color(self, new_color):
        self.tag_color = new_color 

    def set_name (self, new_name):
        self.tag_name = new_name 

    def change_enabled(self):
        self.enabled = not self.enabled
    
    def set_enabled(self, state):
        self.enabled = state

    def get_name(self):
        return self.tag_name 
    
    def get_color(self):
        return self.tag_color