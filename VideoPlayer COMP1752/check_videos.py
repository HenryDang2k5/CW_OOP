import tkinter as tk
import tkinter.scrolledtext as tkst

import video_library as lib
import font_manager as fonts

def set_text(text_area, content):
    """
    Set the content of a given text area widget.
    
    Parameters:
    text_area (tk.Widget): The text area widget where the content will be set.
    content (str): The content to set in the text area widget.
    """
    text_area.delete("1.0", tk.END)  # Clear the text area
    text_area.insert(1.0, content)   # Insert new content at the beginning

class CheckVideos:
    def __init__(self, window):
        """
        Initialize the CheckVideos GUI application.

        Parameters:
        window (tk.Tk): The main window of the application.
        """
        window.geometry("750x350")  # Set the window size
        window.title("Check Videos")  # Set the window title

        # Create and place the "List All Videos" button
        list_videos_btn = tk.Button(window, text="List All Videos", command=self.list_videos_clicked)
        list_videos_btn.grid(row=0, column=0, padx=10, pady=10)

        # Create and place the label for entering the video number
        enter_lbl = tk.Label(window, text="Enter Video Number")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)

        # Create and place the entry widget for the video number input
        self.input_txt = tk.Entry(window, width=3)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)

        # Create and place the "Check Video" button
        check_video_btn = tk.Button(window, text="Check Video", command=self.check_video_clicked)
        check_video_btn.grid(row=0, column=3, padx=10, pady=10)

        # Create and place the scrolled text area for listing videos
        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        # Create and place the text area for displaying video details
        self.video_txt = tk.Text(window, width=24, height=4, wrap="none")
        self.video_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10)

        # Create and place the status label
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        # Automatically list all videos when the application starts
        self.list_videos_clicked()

    def check_video_clicked(self):
        """
        Handle the "Check Video" button click event.
        """
        key = self.input_txt.get()  # Get the input video number
        name = lib.get_name(key)  # Get the name of the video
        if name is not None:
            # Get the video details
            director = lib.get_director(key)
            rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)
            video_details = f"{name}\n{director}\nrating: {rating}\nplays: {play_count}"
            set_text(self.video_txt, video_details)  # Display the video details
        else:
            set_text(self.video_txt, f"Video {key} not found")  # Display not found message
        self.status_lbl.configure(text="Check Video button was clicked!")  # Update status label

    def list_videos_clicked(self):
        """
        Handle the "List All Videos" button click event.
        """
        video_list = lib.list_all()  # Get the list of all videos
        set_text(self.list_txt, video_list)  # Display the list of videos
        self.status_lbl.configure(text="List Videos button was clicked!")  # Update status label

if __name__ == "__main__":
    window = tk.Tk()  # Create the main window object
    fonts.configure()  # Configure the fonts
    CheckVideos(window)  # Create and open the CheckVideos GUI
    window.mainloop()  # Run the main loop to react to events (button presses, etc.)
