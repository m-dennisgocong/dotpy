import os
import tkinter as tk
from tkinter import ttk,filedialog
from tkinter.filedialog import asksaveasfilename,askopenfilename

class MainFrame(tk.Frame):
    def __init__(self,container):
        super().__init__(container)
        self.tree = ttk.Treeview(container, show="tree")
        #self.ybar = ttk.Scrollbar(container,orient = "vertical", command = self.tree.yview)
        style = ttk.Style()
        style.configure("Treeview",background="azure2",foreground="black",fieldbackground="azure2")

        #text_area = tk.Text(container)
        #text_area.insert("1.0","")
    #    text_area.grid(column=2, row=0, sticky="WNES")
        self.nb = ttk.Notebook(container)
        self.nb.grid(column=1, row=0, sticky="WNES")


        text_result = tk.Text(container)
        text_result.grid(column=1, row=1, sticky="WNES")
        self.grid(column=0, row=0,sticky="NEWS")

class FrameController(MainFrame):
    def __init__(self, main):
        super().__init__(main)

    def openfolder(self):
        try:

            directory = filedialog.askdirectory()
            path=os.path.abspath(directory)
            file_names = path.split("/")
            #self.frame_area.tree.heading("#0", text=path,anchor="w")
            node = self.tree.insert("","end",text=file_names[-1],open=True,tag="top_dir")
            def traverse_dir(parent,path):
                for d in os.listdir(path):
                    full_path=os.path.join(path,d)
                    isdir = os.path.isdir(full_path)
                    id=self.tree.insert(parent,'end',text=d,open=False,values=full_path)
                    if isdir:
                        traverse_dir(id,full_path)
            traverse_dir(node,path)
                #self.frame_area.tree.configure(yscroll = self.frame_area.ybar.set)
            self.tree.grid(column=0,sticky="NEWS",row=0,rowspan=2)

                #self.frame_area.ybar.grid(row=0,column=0,rowspan=2,sticky="WNES")
        except FileNotFoundError as error:
            showerror(title='Error', message=error)

    def create_file(self,content = "",title="Untitled", filepath = ""):
        text_area = tk.Text(self.nb, wrap="none")
        self.nb.add(text_area)

class MenuBar(tk.Menu):
    def __init__(self, main):
        super().__init__(main)

        # file bar list
        file_list = ["New File", "Open File", "Open Folder", "Save", "Save As..",
        "Close Tab", "Quit"]

        # create file bar menu
        self.file_bar = tk.Menu(main, tearoff=0) # tearoff for no line

        # add the file_list to the file_bar menu
        for i in file_list:
            self.file_bar.add_command(label = i)

        # add the file menu to the menubar
        self.add_cascade(label = "File", menu = self.file_bar)

        # create separator
        self.file_bar.insert_separator(3)
        self.file_bar.insert_separator(7)

        # edit bar list
        edit_list = ["Undo","Copy","Paste","Delete","Select All"]

        # create edit bar
        self.edit_bar = tk.Menu(self,tearoff=0)
        for i in edit_list:
            self.edit_bar.add_command(label = i)

        # create separator
        self.edit_bar.insert_separator(1)
        self.edit_bar.insert_separator(4)
        self.add_cascade(label = "Edit", menu = self.edit_bar)

        #Run Bar
        self.run_bar = tk.Menu(self,tearoff=0)
        self.run_bar.add_command(label = "Run")
        self.add_cascade(label = "Run", menu = self.run_bar)

    def quit(self):
        sys.exit(0)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("dotpy")
        self.geometry("850x650")
        #self.resizable(False, False)

        # layout on the root/main
        self.columnconfigure(0,weight = 1) #For Scroll Bar
        self.columnconfigure(1,weight = 5) #For Tree View
        #self.columnconfigure(2,weight = 5) #For text edit and result

        # FrameController(MainFrame)
        self.frame_control = FrameController(self)

        # create a Menubar
        self.menu_bar = MenuBar(self)
        self.config(menu = self.menu_bar)

        # file bar fucntions call
        self.menu_bar.file_bar.entryconfig(0, command=self.creat_t , accelerator = "Ctrl+N")
        self.menu_bar.file_bar.entryconfig(1, command=self.creat_t , accelerator = "Ctrl+O")
        self.menu_bar.file_bar.entryconfig(2, command=self.creat_t , accelerator = "Ctrl+Shift+O")
        self.menu_bar.file_bar.entryconfig(4, command=self.creat_t , accelerator = "Ctrl+S")
        self.menu_bar.file_bar.entryconfig(5, command=self.creat_t , accelerator = "Crt+Shift+S")
        self.menu_bar.file_bar.entryconfig(6, command=self.creat_t , accelerator = "Crt+W")
        self.menu_bar.file_bar.entryconfig(8, command=self.creat_t , accelerator = "Crt+Q")
        # edit bar function call
        self.menu_bar.edit_bar.entryconfig(0, command=self.creat_t , accelerator = "Ctrl+Z")
        self.menu_bar.edit_bar.entryconfig(2, command=self.creat_t , accelerator = "Ctrl+C")
        self.menu_bar.edit_bar.entryconfig(3, command=self.creat_t , accelerator = "Ctrl+V")
        self.menu_bar.edit_bar.entryconfig(5, command=self.creat_t)
        self.menu_bar.edit_bar.entryconfig(6, command=self.creat_t , accelerator = "Ctrl+A")

        # run bar function call
        self.menu_bar.run_bar.entryconfig(0, command=self.creat_t, accelerator = "Ctrl+Shift+B")
    def etry(self):
        self.frame_control.openfolder()
    def creat_t(self):
        self.frame_control.create_file()

if __name__ == "__main__":
    main = MainApp()
    main.mainloop()
