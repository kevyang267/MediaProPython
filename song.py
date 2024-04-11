class Song:
    def __init__(self, song_name):
        self.song_name = song_name 
        self.tags = []

    def create_tag(self, tag_name):
        self.tags.append(tag_name)

    def get_all_tags(self):
        return self.tags    

    def get_song_name(self):
        return self.song_name 