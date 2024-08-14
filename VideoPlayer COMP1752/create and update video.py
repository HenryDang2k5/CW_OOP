import tkinter as tk
from tkinter import Label, Entry, Button, Listbox, Frame, StringVar, Scrollbar, messagebox
import webbrowser
import csv
import os


class VideoManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Manager")
        self.root.geometry("700x500")
        self.root.configure(bg="#333333")

        # Header
        self.header = Frame(self.root, bg="#444444", pady=10)
        self.header.pack(fill=tk.X)

        self.title_label = Label(self.header, text="Video Manager", font=("Arial", 24, "bold"), fg="#FFFFFF", bg="#444444")
        self.title_label.pack()

        # Navigation Buttons
        self.nav_frame = Frame(self.root, bg="#333333", pady=10)
        self.nav_frame.pack(fill=tk.X)

        self.create_button = Button(self.nav_frame, text="Create Video List", font=("Arial", 12), bg="#555555", fg="#FFFFFF", command=self.show_create_video_list)
        self.create_button.pack(side=tk.LEFT, padx=10)

        self.update_button = Button(self.nav_frame, text="Update Videos", font=("Arial", 12), bg="#555555", fg="#FFFFFF", command=self.show_update_videos)
        self.update_button.pack(side=tk.LEFT, padx=10)

        # Main Content Frame
        self.main_frame = Frame(self.root, bg="#333333", pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Search and Listbox Frame
        self.search_listbox_frame = Frame(self.main_frame, bg="#333333")
        self.search_listbox_frame.pack(fill=tk.BOTH, expand=True)

        # Search Functionality
        search_frame = Frame(self.search_listbox_frame, bg="#333333")
        search_frame.pack(fill=tk.X)

        Label(search_frame, text="Search:", font=("Arial", 12), bg="#333333", fg="#FFFFFF").pack(side=tk.LEFT, padx=5)

        self.search_var = StringVar()
        self.search_entry = Entry(search_frame, textvariable=self.search_var, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.search_button = Button(search_frame, text="Search Local", font=("Arial", 12), bg="#555555", fg="#FFFFFF", command=self.perform_search)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.youtube_search_button = Button(search_frame, text="Search on YouTube", font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", command=self.search_youtube)
        self.youtube_search_button.pack(side=tk.LEFT, padx=5)

        # Listbox to display videos
        self.video_listbox = Listbox(self.search_listbox_frame, font=("Arial", 12), bg="#444444", fg="#FFFFFF", selectbackground="#666666")
        self.video_listbox.pack(fill=tk.BOTH, expand=True, pady=10)

        scrollbar = Scrollbar(self.video_listbox)
        self.video_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.video_listbox.yview)

        # Load video data from CSV file
        self.video_file = "videos.csv"
        self.videos = self.load_videos_from_csv()
        self.populate_listbox(self.videos)

        # Placeholder frames for Create and Update
        self.create_video_list_frame = None
        self.update_videos_frame = None

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
        self.clear_main_frame()

        self.create_video_list_frame = Frame(self.main_frame, bg="#333333")
        self.create_video_list_frame.pack(fill=tk.BOTH, expand=True)

        Label(self.create_video_list_frame, text="Create Video List", font=("Arial", 18, "bold"), fg="#FFFFFF", bg="#333333").grid(row=0, columnspan=2, pady=10)

        self.create_form_row(self.create_video_list_frame, "Video Number:", 1)
        self.create_form_row(self.create_video_list_frame, "Video Name:", 2)
        self.create_form_row(self.create_video_list_frame, "Director Name:", 3)
        self.create_form_row(self.create_video_list_frame, "Rating:", 4)

        self.save_button = Button(self.create_video_list_frame, text="Save Video", font=("Arial", 12), bg="#28a745", fg="#FFFFFF", command=self.save_video)
        self.save_button.grid(row=5, columnspan=2, pady=10, sticky="ew")

    def create_form_row(self, frame, label_text, row):
        Label(frame, text=label_text, font=("Arial", 12), fg="#FFFFFF", bg="#333333").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = Entry(frame, font=("Arial", 12))
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        if label_text == "Video Number:":
            self.number_entry = entry
        elif label_text == "Video Name:":
            self.name_entry = entry
        elif label_text == "Director Name:":
            self.director_entry = entry
        elif label_text == "Rating:":
            self.rating_entry = entry

    def save_video(self):
        new_video = {
            'number': self.number_entry.get(),
            'name': self.name_entry.get(),
            'director': self.director_entry.get(),
            'rating': self.rating_entry.get(),
            'play_count': '0'  # Initialize play count to 0
        }
        if self.validate_video(new_video):
            self.videos.append(new_video)
            self.save_videos_to_csv()
            self.populate_listbox(self.videos)
            messagebox.showinfo("Success", "Video saved successfully!")
        else:
            messagebox.showwarning("Validation Error", "Please fill in all fields.")

    def validate_video(self, video):
        return all(video.values())

    def show_update_videos(self):
        self.clear_main_frame()

        self.update_videos_frame = Frame(self.main_frame, bg="#333333")
        self.update_videos_frame.pack(fill=tk.BOTH, expand=True)

        Label(self.update_videos_frame, text="Update Videos", font=("Arial", 18, "bold"), fg="#FFFFFF", bg="#333333").grid(row=0, columnspan=2, pady=10)

        self.edit_button = Button(self.update_videos_frame, text="Edit Selected Video", font=("Arial", 12), bg="#17a2b8", fg="#FFFFFF", command=self.edit_selected_video)
        self.edit_button.grid(row=1, columnspan=2, pady=10)

        # Fields to edit the selected video details
        self.create_form_row(self.update_videos_frame, "Video Name:", 2)
        self.create_form_row(self.update_videos_frame, "Director Name:", 3)
        self.create_form_row(self.update_videos_frame, "Rating:", 4)
        self.create_form_row(self.update_videos_frame, "Play Count:", 5)

        self.save_changes_button = Button(self.update_videos_frame, text="Save Changes", font=("Arial", 12), bg="#28a745", fg="#FFFFFF", command=self.save_changes)
        self.save_changes_button.grid(row=6, columnspan=2, pady=10, sticky="ew")

    def clear_main_frame(self):
        if self.create_video_list_frame:
            self.create_video_list_frame.pack_forget()
        if self.update_videos_frame:
            self.update_videos_frame.pack_forget()

    def populate_listbox(self, videos):
        self.video_listbox.delete(0, tk.END)
        for video in videos:
            display_text = f"{video['number']}: {video['name']} (Director: {video['director']}, Rating: {video['rating']}, Play Count: {video['play_count']})"
            self.video_listbox.insert(tk.END, display_text)

    def edit_selected_video(self):
        selected_index = self.video_listbox.curselection()
        if selected_index:
            selected_video = self.videos[selected_index[0]]
            self.populate_edit_fields(selected_video)

    def populate_edit_fields(self, video):
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, video['name'])

        self.director_entry.delete(0, tk.END)
        self.director_entry.insert(0, video['director'])

        self.rating_entry.delete(0, tk.END)
        self.rating_entry.insert(0, video['rating'])

        self.number_entry.delete(0, tk.END)
        self.number_entry.insert(0, video['play_count'])

    def save_changes(self):
        selected_index = self.video_listbox.curselection()
        if selected_index:
            self.videos[selected_index[0]]['name'] = self.name_entry.get()
            self.videos[selected_index[0]]['director'] = self.director_entry.get()
            self.videos[selected_index[0]]['rating'] = self.rating_entry.get()
            self.videos[selected_index[0]]['play_count'] = self.number_entry.get()
            self.save_videos_to_csv()
            self.populate_listbox(self.videos)
            messagebox.showinfo("Success", "Changes saved successfully!")

    def perform_search(self):
        search_term = self.search_var.get().lower()
        filtered_videos = [video for video in self.videos if search_term in video['name'].lower()]
        self.populate_listbox(filtered_videos)

    def search_youtube(self):
        search_term = self.search_var.get()
        if search_term:
            query = search_term.replace(' ', '+')
            youtube_search_url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(youtube_search_url)
        else:
            messagebox.showwarning("Input Error", "Please enter a search term.")


# Run the application
root = tk.Tk()
app = VideoManagerApp(root)
root.mainloop()
