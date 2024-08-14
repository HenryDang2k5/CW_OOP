import tkinter as tk
from tkinter import Label, Entry, Button, Listbox, Frame, StringVar, Scrollbar
import csv
import os

class VideoManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Manager")
        
        self.main_frame = Frame(root)
        self.main_frame.pack()

        # Buttons to navigate between Create and Update functionalities
        self.create_button = Button(self.main_frame, text="Create Video List", command=self.show_create_video_list)
        self.create_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.update_button = Button(self.main_frame, text="Update Videos", command=self.show_update_videos)
        self.update_button.grid(row=0, column=1, padx=10, pady=10)

        self.create_video_list_frame = None
        self.update_videos_frame = None

        # Search functionality
        Label(self.main_frame, text="Search:").grid(row=1, column=0, padx=10, pady=10)
        self.search_var = StringVar()
        self.search_entry = Entry(self.main_frame, textvariable=self.search_var)
        self.search_entry.grid(row=1, column=1, padx=10, pady=10)

        # Search button
        self.search_button = Button(self.main_frame, text="Search", command=self.perform_search)
        self.search_button.grid(row=1, column=2, padx=10, pady=10)

        # Listbox to display videos
        self.video_listbox = Listbox(self.main_frame)
        self.video_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        scrollbar = Scrollbar(self.main_frame)
        scrollbar.grid(row=2, column=3, sticky="ns")

        self.video_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.video_listbox.yview)

        # Load video data from CSV file
        self.video_file = "videos.csv"
        self.videos = self.load_videos_from_csv()
        self.populate_listbox(self.videos)

    def load_videos_from_csv(self):
        videos = []
        if os.path.exists(self.video_file):
            with open(self.video_file, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    videos.append(row)
        return videos

    def save_videos_to_csv(self):
        with open(self.video_file, mode='w', newline='') as file:
            fieldnames = ['number', 'name', 'director', 'rating', 'play_count']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for video in self.videos:
                writer.writerow(video)

    def show_create_video_list(self):
        if self.update_videos_frame:
            self.update_videos_frame.pack_forget()
        
        if not self.create_video_list_frame:
            self.create_video_list_frame = Frame(self.root)
            
            Label(self.create_video_list_frame, text="Create Video List", font=("Arial", 14)).grid(row=0, columnspan=2, padx=10, pady=10)
            
            Label(self.create_video_list_frame, text="Video Number:").grid(row=1, column=0, padx=10, pady=10)
            self.number_entry = Entry(self.create_video_list_frame)
            self.number_entry.grid(row=1, column=1, padx=10, pady=10)
            
            Label(self.create_video_list_frame, text="Video Name:").grid(row=2, column=0, padx=10, pady=10)
            self.name_entry = Entry(self.create_video_list_frame)
            self.name_entry.grid(row=2, column=1, padx=10, pady=10)
            
            Label(self.create_video_list_frame, text="Director Name:").grid(row=3, column=0, padx=10, pady=10)
            self.director_entry = Entry(self.create_video_list_frame)
            self.director_entry.grid(row=3, column=1, padx=10, pady=10)
            
            Label(self.create_video_list_frame, text="Rating:").grid(row=4, column=0, padx=10, pady=10)
            self.rating_entry = Entry(self.create_video_list_frame)
            self.rating_entry.grid(row=4, column=1, padx=10, pady=10)
            
            self.save_button = Button(self.create_video_list_frame, text="Save Video", command=self.save_video)
            self.save_button.grid(row=5, columnspan=2, padx=10, pady=10)
        
        self.create_video_list_frame.pack()

    def save_video(self):
        new_video = {
            'number': self.number_entry.get(),
            'name': self.name_entry.get(),
            'director': self.director_entry.get(),
            'rating': self.rating_entry.get(),
            'play_count': '0'  # Initialize play count to 0
        }
        self.videos.append(new_video)
        self.save_videos_to_csv()
        self.populate_listbox(self.videos)
        print(f"Video '{new_video['name']}' by {new_video['director']} with rating {new_video['rating']} saved.")

    def show_update_videos(self):
        if self.create_video_list_frame:
            self.create_video_list_frame.pack_forget()

        if not self.update_videos_frame:
            self.update_videos_frame = Frame(self.root)
            
            Label(self.update_videos_frame, text="Update Videos", font=("Arial", 14)).grid(row=0, columnspan=2, padx=10, pady=10)

            self.populate_listbox(self.videos)

            self.update_button = Button(self.update_videos_frame, text="Edit Selected Video", command=self.edit_selected_video)
            self.update_button.grid(row=2, columnspan=2, padx=10, pady=10)

            # Fields to edit the selected video details
            Label(self.update_videos_frame, text="Video Name:").grid(row=3, column=0, padx=10, pady=10)
            self.edit_name_entry = Entry(self.update_videos_frame)
            self.edit_name_entry.grid(row=3, column=1, padx=10, pady=10)

            Label(self.update_videos_frame, text="Director Name:").grid(row=4, column=0, padx=10, pady=10)
            self.edit_director_entry = Entry(self.update_videos_frame)
            self.edit_director_entry.grid(row=4, column=1, padx=10, pady=10)

            Label(self.update_videos_frame, text="Rating:").grid(row=5, column=0, padx=10, pady=10)
            self.edit_rating_entry = Entry(self.update_videos_frame)
            self.edit_rating_entry.grid(row=5, column=1, padx=10, pady=10)

            Label(self.update_videos_frame, text="Play Count:").grid(row=6, column=0, padx=10, pady=10)
            self.edit_play_count_entry = Entry(self.update_videos_frame)
            self.edit_play_count_entry.grid(row=6, column=1, padx=10, pady=10)

            self.save_changes_button = Button(self.update_videos_frame, text="Save Changes", command=self.save_changes)
            self.save_changes_button.grid(row=7, columnspan=2, padx=10, pady=10)

        self.update_videos_frame.pack()

    def populate_listbox(self, videos):
        self.video_listbox.delete(0, tk.END)
        for video in videos:
            display_text = f"{video['number']}: {video['name']} (Director: {video['director']}, Rating: {video['rating']}, Play Count: {video['play_count']})"
            self.video_listbox.insert(tk.END, display_text)

    def edit_selected_video(self):
        selected_index = self.video_listbox.curselection()
        if selected_index:
            selected_video = self.videos[selected_index[0]]
            self.edit_name_entry.delete(0, tk.END)
            self.edit_name_entry.insert(0, selected_video['name'])
            self.edit_director_entry.delete(0, tk.END)
            self.edit_director_entry.insert(0, selected_video['director'])
            self.edit_rating_entry.delete(0, tk.END)
            self.edit_rating_entry.insert(0, selected_video['rating'])
            self.edit_play_count_entry.delete(0, tk.END)
            self.edit_play_count_entry.insert(0, selected_video['play_count'])

            self.selected_video_index = selected_index[0]  # Store the index of the selected video

    def save_changes(self):
        if hasattr(self, 'selected_video_index'):
            updated_video = {
                'number': self.videos[self.selected_video_index]['number'],  # Preserve the original number
                'name': self.edit_name_entry.get(),
                'director': self.edit_director_entry.get(),
                'rating': self.edit_rating_entry.get(),
                'play_count': self.edit_play_count_entry.get()
            }
            self.videos[self.selected_video_index] = updated_video
            self.save_videos_to_csv()
            self.populate_listbox(self.videos)
            print(f"Video '{updated_video['name']}' updated. Director: {updated_video['director']}, Rating: {updated_video['rating']}, Play Count: {updated_video['play_count']}")

    def search_videos(self, search_term):
        search_term = search_term.lower()
        filtered_videos = [
            video for video in self.videos
            if search_term in video['number'].lower() or
               search_term in video['name'].lower() or
               search_term in video['director'].lower()
        ]
        self.populate_listbox(filtered_videos)

    def perform_search(self):
        search_term = self.search_var.get()
        self.search_videos(search_term)

    def on_key_release(self, event):
        search_term = self.search_var.get()
        self.search_videos(search_term)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoManagerApp(root)
    root.mainloop()
