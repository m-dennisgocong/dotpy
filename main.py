import tkinter as tk
from tkinter import ttk,filedialog
class TreeviewFrame(ttk.Frame):
    def __init__(self,container):
        super().__init__(container)
        self.columnconfigure(0, weight=3)
        self.rowconfigure(0,weight=3)
        self.tree = ttk.Treeview(container, show="tree")
        self.ybar = ttk.Scrollbar(container,orient = "vertical", command = self.tree.yview)
        style = ttk.Style()
        style.configure("Treeview",background="azure2",foreground="black",fieldbackground="azure2")
        self.tree.configure(yscroll = self.ybar.set)
    def select_folder(self):
        directory = filedialog.askdirectory()
        #print(directory)
        self.tree.heading("#0", text="Dir: "+directory,anchor="w")
        path=os.path.abspath(directory)
        node = self.tree.insert("","end",text=path,open=True,tag="top_dir")
        def traverse_dir(parent,path):
            for d in os.listdir(path):
                full_path=os.path.join(path,d)
                isdir = os.path.isdir(full_path)
                id=self.tree.insert(parent,'end',text=d,open=False,values=full_path)
                if isdir:
                    traverse_dir(id,full_path)
        traverse_dir(node,path)
        self.ybar.grid(row=0,column=1,sticky="nsw")
        self.tree.grid(column=0,sticky="NSWE",row=0,rowspan=2)
        def selectItem():
            print("work")
            try:
                curItem = self.tree.focus()
                sltpath = self.tree.item(curItem)["values"]
                file_selected = os.path.abspath(sltpath[0])
                name_of_file = self.tree.item(curItem)["text"]
                filename = os.path.basename(file_selected)
                isfile = os.path.isdir(file_selected)
                if not isfile:
                    with open(file_selected,"r") as file:
                        code = file.read()
                    create_file(code,filename,file_selected)
                else:
                    pass
            except:
                pass

        self.tree.bind("<Double-1>", selectItem())

class TextEdit(ttk.Frame):
    def __init__(self,container):
        super().__init__(container)
        self.columnconfigure(0,weight = 3)
        self.columnconfigure(0,weight = 1)
        self.__create_widgets()
    def __create_widgets(self):
        text_area = tk.Text(self)
        text_area.insert("1.0","")
        text_area.grid(column=0, row=0, sticky="NEWS")
class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        #File Bar
        file_bar = tk.Menu(self, tearoff=0) #tearoff for no line
        file_bar.add_command(label = "New File")
        file_bar.add_command(label = "Open File")
        file_bar.add_command(label = "Open Folder")
        file_bar.add_separator()
        file_bar.add_command(label = "Save")
        file_bar.add_command(label = "Save As..")
        file_bar.add_command(label = "Close Tab")
        file_bar.add_separator()
        file_bar.add_command(label = "Quit", command = self.quit)
        self.add_cascade(label = "File", menu = file_bar) # File bar
        #Edit Bar
        edit_bar = tk.Menu(self,tearoff=0)
        edit_bar.add_command(label = "Undo")
        edit_bar.add_separator()
        edit_bar.add_command(label = "Cut")
        edit_bar.add_command(label = "Copy")
        edit_bar.add_command(label = "Paste")
        edit_bar.add_separator()
        edit_bar.add_command(label = "Delete")
        edit_bar.add_command(label = "Select All")
        self.add_cascade(label = "Edit", menu = edit_bar)

        #Run Bar
        run_bar = tk.Menu(self,tearoff=0)
        run_bar.add_command(label = "Run")
        self.add_cascade(label = "Run", menu = run_bar)

    def quit(self):
        sys.exit(0)

class MainApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("dotpy")
        self.geometry("1000x650")
        self.__create_widgets()

        #Layout on the root
        self.columnconfigure(0,weight = 1)
        self.columnconfigure(1,weight = 5)

        menu_bar = MenuBar(self) #Menu bar for File,Edit and Run File
        self.config(menu = menu_bar)

    def __create_widgets(self):
        tree_view = TreeviewFrame(self)
        tree_view.grid(column = 0, row = 0)

        text_edit_area = TextEdit(self)
        tree_view.grid(column = 1, row = 0)

    def open_folder(self):
        t = TreeviewFrame.select_folder()

if __name__ == "__main__":
    main = MainApp()
    main.mainloop()
