import tkinter as tk
from tkinter import ttk

class LibraryItem:
    def __init__(self, name, director, rating):
        self.name = name
        self.director = director
        self.rating = rating
        self.play_count = 0

    def info(self):
        return f"{self.name} directed by {self.director}, rating: {self.rating}, play count: {self.play_count}"

# Initialize the library dictionary
library = {
    "01": LibraryItem("Tom and Jerry", "Fred Quimby", 4),
    "02": LibraryItem("Breakfast at Tiffany's", "Blake Edwards", 5),
    "03": LibraryItem("Casablanca", "Michael Curtiz", 2),
    "04": LibraryItem("The Sound of Music", "Robert Wise", 1),
    "05": LibraryItem("Gone with the Wind", "Victor Fleming", 3),
}

class UpdateVideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Update Video")

        self.create_widgets()

    def create_widgets(self):
        # Frame for the update form
        self.update_frame = ttk.Frame(self.root)
        self.update_frame.pack(padx=10, pady=10)

        # Video ID
        self.id_label = ttk.Label(self.update_frame, text="Video ID:")
        self.id_label.grid(row=0, column=0, padx=5, pady=5)
        self.id_entry = ttk.Entry(self.update_frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Video Name
        self.name_label = ttk.Label(self.update_frame, text="Name:")
        self.name_label.grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.update_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Director
        self.director_label = ttk.Label(self.update_frame, text="Director:")
        self.director_label.grid(row=2, column=0, padx=5, pady=5)
        self.director_entry = ttk.Entry(self.update_frame)
        self.director_entry.grid(row=2, column=1, padx=5, pady=5)

        # Rating
        self.rating_label = ttk.Label(self.update_frame, text="Rating:")
        self.rating_label.grid(row=3, column=0, padx=5, pady=5)
        self.rating_entry = ttk.Entry(self.update_frame)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # Update button
        self.update_button = ttk.Button(self.update_frame, text="Update", command=self.update_video)
        self.update_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Close button
        self.close_button = ttk.Button(self.root, text="Close", command=self.root.quit)
        self.close_button.pack(pady=10)

    def update_video(self):
        video_id = self.id_entry.get()
        if video_id in library:
            name = self.name_entry.get()
            director = self.director_entry.get()
            try:
                rating = int(self.rating_entry.get())
            except ValueError:
                print("Invalid rating. Please enter a number.")
                return
            
            library[video_id].name = name
            library[video_id].director = director
            library[video_id].rating = rating

            print(f"Updated {video_id}: {library[video_id].info()}")
        else:
            print("Video ID not found in the library.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateVideoApp(root)
    root.mainloop()
