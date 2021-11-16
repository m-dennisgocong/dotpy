import os
import subprocess
import tkinter as tk
import save_load as sl
from tkinter import ttk,filedialog,messagebox
from tkinter.filedialog import asksaveasfilename,askopenfilename

class MainFrame(tk.Frame):
    def __init__(self,container):
        super().__init__(container)
        self.tree = ttk.Treeview(container, show="tree")
        # store {key notebook [content/code, filename, filepath]}
        self.content_data = dict()

        #self.ybar = ttk.Scrollbar(container,orient = "vertical", command = self.tree.yview)
        style = ttk.Style()
        style.configure("Treeview",background="azure2",foreground="black",fieldbackground="azure2")

        self.nb = ttk.Notebook(container)

        """
        welcome_text = tk.StringVar()
        self.welcome_title = tk.Label(self.nb, textvariable=welcome_text,justify="center", height="25", width="25")
        welcome_text.set("Welcome \nto \ndotpy")
        """
        #need to get back here after done on save method
        #text_area = tk.Text(self.nb, wrap = "none")
        #self.nb.add(text_area)
        self.nb.grid(column=1, row=0, sticky="WNES")

        text_result = tk.Text(container)
        text_result.grid(column=1, row=1, sticky="WNES")
        self.grid(column=0, row=0,sticky="NEWS")

class FrameController(MainFrame):
    def __init__(self, main):
        super().__init__(main)
    #create text in nb
    def create_file(self,content = "",title="Untitled", filepath = ""):
        text_area = tk.Text(self.nb, wrap="none")
        text_area.insert("1.0",content)
        self.nb.add(text_area, text=title)
        self.content_data[str(text_area)] = [hash(content),self.nb.tab("current")["text"], filepath]
        self.nb.select(text_area)

    #open file
    def open_file(self):
        path = askopenfilename(filetypes=[("Python Files", "*.py")])
        filename = os.path.basename(path)

        #check if the file already open
        for tab in self.nb.tabs():
            currenttab = self.nb.nametowidget(tab)
            if filename == self.content_data[str(currenttab)][1] and path == self.content_data[str(currenttab)][2]:
                self.nb.select(currenttab)

        with open(path, "r") as file:
            code = file.read()
        self.create_file(code,filename,path)

    # open folder
    def openfolder(self):
        try:
            directory = filedialog.askdirectory()
            path=os.path.abspath(directory)
            folder_name = path.split("/")
            self.tree.heading("#0", text="Dir: "+directory,anchor="w")
            node = self.tree.insert("","end",text=folder_name[-1],open=True,tag="top_dir")
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

    # select from opened folder
    def select_file(self):
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
                self.create_file(code,filename,file_selected)
            else:
                pass
        except:
            pass

    # get the selected tab in notebook
    def select_nb_tab(self):
        selected_nb = main.nametowidget(self.nb.select())
        return selected_nb

    #checker for changes
    def change_checker(self):
        current = self.select_nb_tab()
        content = current.get("1.0","end-1c")
        name = self.nb.tab("current")["text"]
        if hash(content) != self.content_data[str(current)][0]:
            if name[-1] != "*":
                self.nb.tab("current", text = name + "*")
        else:
            self.nb.tab("current",text=name[:-1])

    def save_as(self):
        file_path = asksaveasfilename(filetypes=[("Python Files", "*.py")])
        try:
            filename = os.path.basename(file_path)
            text_code = self.select_nb_tab()
            content = text_code.get("1.0","end-1c")
            with open(file_path, "w") as file:
                file.write(content)

        except(AttributeError, FileNotFoundError, TypeError):
            print("Save operation cancelled")
            return

        self.nb.tab("current",text=filename)
        self.content_data[str(text_code)] = [hash(content),self.nb.tab("current")["text"],file_path]

    #save current file
    def save_file(self):
        current_tab = self.select_nb_tab()
        name = self.nb.tab("current")["text"]

        #check if not yet save
        if self.content_data[str(current_tab)][2] != "":
            content = current_tab.get("1.0","end-1c")
            filepath = self.content_data[str(current_tab)][2]
            with open(filepath, "w") as file:
                file.write(content)
            self.content_data[str(current_tab)][0] = hash(content)
        else:
            self.save_as()
        #self.check_for_changes()

    def close_current_tab(self):
        current = self.select_nb_tab()
        if self.current_tab_nsave() and not self.confirm_close():
            return
        if len(self.nb.tabs()) == 1:#create notebook if close all tab
            self.create_file()
        self.nb.forget(current)

    #check if current tab not save
    def current_tab_nsave(self):
        get_content_text = self.select_nb_tab()
        content = get_content_text.get("1.0","end-1c")
        return hash(content) != self.content_data[str(get_content_text)][0] #return true if tab is not save_as

    #check confim to close
    def confirm_close(self):
        return messagebox.askyesno(
            message="Your changes will be lost if you close without saving. Are you sure you want to close?",
            icon="question",
            title="Unsave changes"
        )

    #Close All
    def confirm_quit(self, root):
        savetabs = list() # save the notebook/tabs
        unsave = False
        unsavetabs = list() #unsave notebook/tabs

        #check all notebook
        for tab in self.nb.tabs():
            currenttab = main.nametowidget(tab)
            content = currenttab.get("1.0","end-1c")
            if hash(content) != self.content_data[str(currenttab)][0]: #check the unsave file
                unsave = True
                unsavetabs.append(self.content_data[str(currenttab)][1]) #stored to unsavetabs

            savetabs.append(self.content_data[str(currenttab)][2]) #store to savetabs

        #confirmation for quiting
        if unsave:
            tabsname = ""
            for x in unsavetabs:
                tabsname = tabsname + x + ", "
            confirm = messagebox.askyesno(
                message = "{} has changes. Are you sure you want to quit without saving?".format(tabsname),
                icon = "question",
                title = "Confirm Quit"
            )
            #save_load data/ save the tabs
            if not confirm :
                return
        with open("save_load.py","w") as f:
            f.write("listtabs =" + str(savetabs))
        return True


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

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("dotpy")
        self.geometry("850x650")
        #self.resizable(False, False)

        # layout on the root/main
        self.columnconfigure(0,weight = 1)
        # create instance object inherit from FrameController(MainFrame)
        self.frame_control = FrameController(self)

        # create instance object inherit from MenuBar
        self.menu_bar = MenuBar(self)
        self.config(menu = self.menu_bar)

        # file bar command
        self.menu_bar.file_bar.entryconfig(0, command=self.creat_f , accelerator = "Ctrl+N")
        self.menu_bar.file_bar.entryconfig(1, command=self.open_f , accelerator = "Ctrl+O")
        self.menu_bar.file_bar.entryconfig(2, command=self.openfolder , accelerator = "Ctrl+Shift+O")
        self.menu_bar.file_bar.entryconfig(4, command=self.save_f , accelerator = "Ctrl+S")
        self.menu_bar.file_bar.entryconfig(5, command=self.save_as , accelerator = "Crt+Shift+S")
        self.menu_bar.file_bar.entryconfig(6, command=self.close_tab , accelerator = "Crt+W")
        self.menu_bar.file_bar.entryconfig(8, command=self.quit , accelerator = "Crt+Q")
        # edit bar command
        self.menu_bar.edit_bar.entryconfig(0, command=self.creat_f , accelerator = "Ctrl+Z")
        self.menu_bar.edit_bar.entryconfig(2, command=self.creat_f , accelerator = "Ctrl+C")
        self.menu_bar.edit_bar.entryconfig(3, command=self.creat_f , accelerator = "Ctrl+V")
        #self.menu_bar.edit_bar.entryconfig(5, commdand=self.creat_t)
        self.menu_bar.edit_bar.entryconfig(6, command=self.creat_f , accelerator = "Ctrl+A")

        self.menu_bar.run_bar.entryconfig(0, command=self.creat_f, accelerator = "Ctrl+Shift+B")

        self.frame_control.tree.bind("<Double-1>", lambda e: self.frame_control.select_file())
        self.bind("<KeyPress>", lambda e: self.frame_control.change_checker())
        self.bind("<Control-w>", lambda e: self.frame_control.close_current_tab())
        self.protocol("WM_DELETE_WINDOW",self.quit)

    def open_f(self):
        self.frame_control.open_file()
    def openfolder(self):
        self.frame_control.openfolder()
    def creat_f(self):
        self.frame_control.create_file()
    def save_f(self):
        self.frame_control.save_file()
    def save_as(self):
        self.frame_control.save_as()
    def close_tab(self):
        self.frame_control.close_current_tab()
    def quit(self):
        if self.frame_control.confirm_quit(self) is True:
            self.destroy()

if __name__ == "__main__":
    main = MainApp()
    main.mainloop()
