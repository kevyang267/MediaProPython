from customtkinter import *
from PIL import Image 
from tkinter import filedialog
from song import Song
import pygame
import tkinter as tk
from tags import Tags
from tkinter import ttk
from tkinter import colorchooser

class MediaPro:
    def __init__(self, master):
        pygame.mixer.init()

        self.master = master
        master.title("MediaPro")
        master.iconbitmap("MediaProPython\\images\\640px-Windows_Media_Player_simplified_logo.svg.ico")
        master.geometry("800x500")
        set_appearance_mode("dark")
        set_default_color_theme("blue")

        self.songs = []
        self.current_song = None
        self.paused = True 
        self.muted = False
        self.current_volume = 0.5
        self.played = False

        self.tags = []

        self.tabview = CTkTabview(master, width = 1200, height= 700, corner_radius=10, segmented_button_fg_color="black", segmented_button_unselected_color="black", anchor="w")
        self.tabview.pack(padx=20, pady = 20)

        self.tabview.add("Playing")
        self.tabview.add("Library")
        self.tabview.add("Queue")
        self.tabview.add("Rules")
        self.tabview.add("Tags")
        self.tabview.add("Settings")

        self.play_icon = tk.PhotoImage(file = "MediaProPython\\images\\play-button-arrowhead.png")
        self.scaled_play_icon = self.play_icon.subsample(25,25)

        self.label_1 = CTkButton(master=self.tabview.tab("Playing"), image=self.scaled_play_icon, command=self.play_music, text = "", fg_color="white", corner_radius=10)
        self.label_1.pack(padx=20, pady=20, side=tk.BOTTOM, anchor="s")

        self.pause_icon = tk.PhotoImage(file = "MediaProPython\\images\\pause.png")
        self.scaled_pause_icon = self.pause_icon.subsample(25,25)

        self.next_icon = tk.PhotoImage(file = "MediaProPython\\images\\forward.png")
        self.scaled_next_icon = self.next_icon.subsample(25,25)

        self.volume_slider = CTkSlider(master=self.tabview.tab("Playing"), from_ =0, to= 1, command=self.change_volume)
        self.volume_slider.set(self.current_volume)
        self.volume_slider.pack( anchor = "e", side= tk.BOTTOM)
        pygame.mixer.music.set_volume(self.current_volume)
        
        self.label_11 = CTkButton(master=self.tabview.tab("Playing"), image=self.scaled_next_icon, command=self.play_next_song, text = "", fg_color="black", corner_radius=10, anchor="s")
        self.label_11.pack(padx=20, pady=20, side=tk.BOTTOM, anchor="e")

        self.previous_icon = tk.PhotoImage(file = "MediaProPython\\images\\previous-track.png")
        self.scaled_previous_icon = self.previous_icon.subsample(25,25)
        
        self.label_11 = CTkButton(master=self.tabview.tab("Playing"), image=self.scaled_previous_icon, command=self.play_previous_song, text = "", fg_color="black", corner_radius=10, anchor="s")
        self.label_11.pack(side=tk.BOTTOM, anchor="w")

        self.label_12 = CTkLabel(master=self.tabview.tab("Playing"), text ="No playing song")
        self.label_12.pack(padx=20, pady=20, side = tk.BOTTOM, anchor="s")

        self.label_13 = CTkLabel(master=self.tabview.tab("Playing"), text ="No next song")
        self.label_13.pack(padx=20, pady=20, side = tk.BOTTOM, anchor="e")

        self.label_14 = CTkLabel(master=self.tabview.tab("Playing"), text ="No previous song")
        self.label_14.pack(padx=20, pady=20, side = tk.BOTTOM, anchor="w")

        self.label_2 = CTkLabel(master=self.tabview.tab("Library"), text="Library")
        self.label_2.pack(padx= 20, pady=20)

        self.label_3 = CTkLabel(master=self.tabview.tab("Queue"), text="Queue")
        self.label_3.pack(padx= 20, pady=20)

        self.label_4 = CTkLabel(master=self.tabview.tab("Rules"), text="Rules")
        self.label_4.pack(padx= 20, pady=20)

        self.label_6 = CTkButton(master=self.tabview.tab("Settings"), text="Select Folder with Music", corner_radius=20, fg_color="#1F1F1F", command=self.load_music)
        self.label_6.pack(padx= 20, pady=20)

        self.songList = tk.Listbox(master=self.tabview.tab("Library"), width = 1200, height = 700, background= "black", fg="white")
        self.songList.pack()

        self.queueList = tk.Listbox(master=self.tabview.tab("Queue"), width = 1200, height = 700, background= "black", fg="white")
        self.queueList.pack()

        self.addTag = CTkButton(master=self.tabview.tab("Tags"), text="Add tag", corner_radius = 20, fg_color="#1F1F1F", command=self.show_add_tag_popup)
        self.addTag.pack()

        self.deleteTag = CTkButton(master=self.tabview.tab("Tags"), text="Delete tag", corner_radius = 20, fg_color="#1F1F1F", command=self.delete_tag)
        self.deleteTag.pack(padx=100, pady=10)

        self.tagTree = ttk.Treeview(master=self.tabview.tab("Tags"), height=10)
        self.column_names = ("Tag Name", "Tag Color", "Enabled")
        self.tagTree.configure(columns=self.column_names)
        self.tagTree.heading("Tag Name", text="Tag Name")
        self.tagTree.heading("Tag Color", text="Tag Color")
        self.tagTree.heading("Enabled", text="Enabled")
        self.tagTree.pack(padx=20, pady=10)

    def delete_tag(self):
        item = self.tagTree.selection()[0]
        self.tagTree.delete(item)

    def show_add_tag_popup(self):
        popup = CTk()
        popup.title("Add Tag")

        label1 = CTkLabel(master=popup, text="Tag Name:")
        label1.pack(padx=5, pady=5, side=tk.LEFT)

        tag_name_entry = CTkEntry(master=popup)
        tag_name_entry.pack(padx=5, pady=5, side=tk.LEFT)

        label2 = CTkLabel(master=popup, text="Tag Color:")
        label2.pack(padx=5, pady=5, side=tk.LEFT)

        def choose_color():
            color = tk.colorchooser.askcolor()[1]  
            tag_color_entry.delete(0, tk.END)  
            tag_color_entry.insert(tk.END, color)  

        tag_color_entry = CTkEntry(master=popup)
        tag_color_entry.pack(padx=5, pady=5, side=tk.LEFT)

        color_button = CTkButton(master=popup, text="Choose Color", command=choose_color)
        color_button.pack(padx=5, pady=5, side=tk.LEFT)

        submit_button = CTkButton(master=popup, text="Add", corner_radius=5, command=lambda: self.submit_tag(popup, tag_name_entry.get(), tag_color_entry.get()))
        submit_button.pack(padx=5, pady=5, side=tk.LEFT)
        popup.mainloop()


    def submit_tag(self, popup, name, color):
        if name and color:
            # Assuming you have a Tags class to store tag information
            new_tag = Tags(name, color)
            self.tags.append(new_tag)
            # Add to the treeview
            checkbox_tag = self.tagTree.insert("", "end", text="", values=(name, color, "False",), tags=(color,))
            # Set the tag color for the background
            self.tagTree.tag_configure(color, background=color)
            popup.destroy()
        else:
            tk.messagebox.showwarning("Warning", "Please fill in both fields.")

    def change_volume(self, value):
        self.current_volume = value 
        if value == 0 and self.muted != True:
            self.muted = True
        elif value > 0 and self.muted == True:
            self.muted = False
        pygame.mixer.music.set_volume(value)

    # Ask for the file directory 
    def load_music(self): 
        self.master.directory = filedialog.askdirectory()
        for song in os.listdir(self.master.directory):
            name, ext = os.path.splitext(song)
            if ext == ".mp3":
                newSong = Song(song)
                self.songs.append(newSong)    
        
        for song in self.songs:
            self.songList.insert(END, song.get_song_name().replace(".mp3", ""))
            self.queueList.insert(END,song.get_song_name().replace(".mp3", ""))

        self.songList.selection_set(0)

        self.current_song = self.songs[0]
        self.next_song = self.songs[1]
        self.previous_song = None
        self.label_12.configure(text=self.current_song.get_song_name().replace(".mp3", ""))
        self.label_13.configure(text=self.next_song.get_song_name().replace(".mp3", "")) 

    def play_music(self):
        if self.paused and self.played == False:
            self.label_1.configure(image=self.scaled_pause_icon)
            pygame.mixer.music.load(os.path.join(self.master.directory, self.current_song.get_song_name()))
            pygame.mixer.music.play()
            self.paused = False
            self.played = True
        elif self.paused and self.played == True:
            self.label_1.configure(image=self.scaled_pause_icon)
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.pause()
            self.paused = True
            self.label_1.configure(image=self.scaled_play_icon)

    def update_songs(self):
        # update the current song 
        current_song_index = self.songs.index(self.current_song)
        self.label_12.configure(text=self.current_song.get_song_name())
        self.songList.selection_clear(0, END)
        self.songList.select_set(current_song_index)

        # update next song 
        if (current_song_index < len(self.songs) - 1):
            self.next_song = self.songs[current_song_index + 1]
            self.label_13.configure(text=self.next_song.get_song_name())
        else:
            self.next_song = None 
            self.label_13.configure(text="No next song")

        if (current_song_index > 0):
            self.previous_song = self.songs[current_song_index - 1]
            self.label_14.configure(text=self.previous_song.get_song_name())
        else:
            self.previous_song = None
            self.label_14.configure(text="No previous song")


    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True
        self.label_1.configure(image=self.scaled_pause_icon)

    def play_next_song(self):
        try:
            self.played = False
            self.current_song = self.songs[self.songs.index(self.current_song) + 1]
            self.update_songs()
            self.play_music()
        except:
            pass

    def play_previous_song(self):
        try:
            self.played = False
            if (self.songs.index(self.current_song) == 0):
                pass
            else:
                self.current_song = self.songs[self.songs.index(self.current_song) - 1]
                self.update_songs()
                self.play_music()
        except:
            pass

if __name__ == "__main__":
    root = CTk()
    app = MediaPro(root)
    root.mainloop()