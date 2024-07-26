import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
import json

class FileCopierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Save File Backup")

        self.source_dir = ""
        self.destination_dir = ""

        # Load profiles from JSON file
        self.profiles = self.load_profiles()
        self.selected_profile = tk.StringVar(self.root)
        self.selected_profile.set("Select Profile")

        self.create_widgets()

    def create_widgets(self):
        # Profile selection
        self.profile_label = tk.Label(self.root, text="Select Profile:")
        self.profile_label.pack()

        self.profile_menu = tk.OptionMenu(self.root, self.selected_profile, *list(self.profiles.keys()), command=self.update_directories)
        self.profile_menu.pack()

        # Source directory
        self.source_label = tk.Label(self.root, text="Source Directory:")
        self.source_label.pack()

        self.source_entry = tk.Entry(self.root, width=90)
        self.source_entry.pack()

        self.source_button = tk.Button(self.root, text="Browse", command=self.browse_source)
        self.source_button.pack()

        # Destination directory
        self.destination_label = tk.Label(self.root, text="Destination Directory:")
        self.destination_label.pack()

        self.destination_entry = tk.Entry(self.root, width=90)
        self.destination_entry.pack()

        self.destination_button = tk.Button(self.root, text="Browse", command=self.browse_destination)
        self.destination_button.pack()

        # New folder name entry
        self.folder_name_label = tk.Label(self.root, text="New Folder Name:")
        self.folder_name_label.pack()

        self.folder_name_entry = tk.Entry(self.root, width=90)
        self.folder_name_entry.pack()

        # Profile name entry
        self.profile_name_label = tk.Label(self.root, text="New Profile Name:")
        self.profile_name_label.pack()

        self.profile_name_entry = tk.Entry(self.root, width=90)
        self.profile_name_entry.pack()

        # Save profile button
        self.save_profile_button = tk.Button(self.root, text="Save Profile", command=self.save_profile)
        self.save_profile_button.pack()

        # Copy button
        self.copy_button = tk.Button(self.root, text="Copy Files", command=self.copy_files)
        self.copy_button.pack()

        # Reverse copy button
        self.reverse_copy_button = tk.Button(self.root, text="Reverse Copy Files", command=self.reverse_copy_files)
        self.reverse_copy_button.pack()

    def browse_source(self):
        self.source_dir = filedialog.askdirectory()
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, self.source_dir)

    def browse_destination(self):
        self.destination_dir = filedialog.askdirectory()
        self.destination_entry.delete(0, tk.END)
        self.destination_entry.insert(0, self.destination_dir)

    def update_directories(self, profile):
        self.source_dir = self.profiles[profile]["source"]
        self.destination_dir = self.profiles[profile]["destination"]
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, self.source_dir)
        self.destination_entry.delete(0, tk.END)
        self.destination_entry.insert(0, self.destination_dir)

    def save_profile(self):
        profile_name = self.profile_name_entry.get()
        if not profile_name:
            messagebox.showerror("Error", "Please enter a profile name.")
            return

        if not self.source_dir or not self.destination_dir:
            messagebox.showerror("Error", "Please select both source and destination directories.")
            return

        self.profiles[profile_name] = {"source": self.source_dir, "destination": self.destination_dir}
        self.update_profile_menu()

        # Save profiles to JSON file
        self.save_profiles()
        messagebox.showinfo("Success", f"Profile '{profile_name}' saved successfully!")

    def update_profile_menu(self):
        menu = self.profile_menu['menu']
        menu.delete(0, 'end')
        for profile in self.profiles.keys():
            menu.add_command(label=profile, command=lambda p=profile: self.selected_profile.set(p))
        self.selected_profile.set("Select Profile")

    def copy_files(self):
        if not self.source_dir or not self.destination_dir:
            messagebox.showerror("Error", "Please select both source and destination directories.")
            return

        folder_name = self.folder_name_entry.get()
        if not folder_name:
            messagebox.showerror("Error", "Please enter a name for the new folder.")
            return

        new_folder_path = os.path.join(self.destination_dir, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        try:
            for item in os.listdir(self.source_dir):
                source_item = os.path.join(self.source_dir, item)
                destination_item = os.path.join(new_folder_path, item)

                if os.path.isdir(source_item):
                    shutil.copytree(source_item, destination_item)
                else:
                    shutil.copy2(source_item, destination_item)

            messagebox.showinfo("Success", "Files copied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def reverse_copy_files(self):
        if not self.source_dir or not self.destination_dir:
            messagebox.showerror("Error", "Please select both source and destination directories.")
            return

        destination_dir = self.destination_entry.get()

        try:
            for item in os.listdir(destination_dir):
                source_item = os.path.join(destination_dir, item)
                destination_item = os.path.join(self.source_dir, item)

                if os.path.isdir(source_item):
                    shutil.copytree(source_item, destination_item)
                else:
                    shutil.copy2(source_item, destination_item)

            messagebox.showinfo("Success", "Files copied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def load_profiles(self):
        try:
            with open("profiles.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def save_profiles(self):
        with open("profiles.json", "w") as file:
            json.dump(self.profiles, file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCopierApp(root)
    root.mainloop()
