import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("dotpy")
        self.geometry("1000x650")

        menu_bar = tk.Menu(self) #Menu bar for File,Edit and Run File

        #File Bar
        file_bar = tk.Menu(menu_bar, tearoff=0) #tearoff for no line
        file_bar.add_command(label = "New File")
        file_bar.add_command(label = "Open File")
        file_bar.add_command(label = "Open Folder")
        file_bar.add_separator()
        file_bar.add_command(label = "Save")
        file_bar.add_command(label = "Save As..")
        file_bar.add_command(label = "Close Tab")
        file_bar.add_separator()
        file_bar.add_command(label = "Quit")
        menu_bar.add_cascade(label = "File", menu = file_bar) # File bar
        #Edit Bar
        edit_bar = tk.Menu(menu_bar,tearoff=0)
        edit_bar.add_command(label = "Undo")
        edit_bar.add_separator()
        edit_bar.add_command(label = "Cut")
        edit_bar.add_command(label = "Copy")
        edit_bar.add_command(label = "Paste")
        edit_bar.add_separator()
        edit_bar.add_command(label = "Delete")
        edit_bar.add_command(label = "Select All")
        menu_bar.add_cascade(label = "Edit", menu = edit_bar)

        #Run Bar
        run_bar = tk.Menu(menu_bar,tearoff=0)
        run_bar.add_command(label = "Run")
        menu_bar.add_cascade(label = "Run", menu = run_bar)

        self.config(menu = menu_bar)
if __name__ == "__main__":
    main = MainApp()
    main.mainloop()
