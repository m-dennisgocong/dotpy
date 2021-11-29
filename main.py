import os
import subprocess
import tkinter as tk
import save_load as sl
from tkinter import ttk,filedialog,messagebox
from tkinter.filedialog import asksaveasfilename,askopenfilename

# class for Editor Text and Result Text frame
class TextFrame:
    def __init__(self,main):
        self.textFrame = ttk.Frame(main).grid(row=0,column=1,sticky="NEWS")
        self.nb = ttk.Notebook(self.textFrame)
        self.nb.grid(column=1, row=0, sticky="NEWS")
        self.resultFrame = ttk.Frame(main).grid(row=1,column=1,sticky="NEWS")
        self.text_result = tk.Text(self.resultFrame)
        self.text_result.grid(column=1, row=1, sticky="NEWS")

# class for tree view frame
class TreeFrame:
    def __init__(self,main):
        self.treeFrame = ttk.Frame(main)
        self.treeFrame.grid(row=0,column=0,rowspan=2,sticky="WNES")
        self.tree = ttk.Treeview(self.treeFrame, show="tree")
        style = ttk.Style()
        style.configure("Treeview",background="azure2",foreground="black",fieldbackground="azure2")

# class for frame control
class FrameController(TextFrame, TreeFrame):
    def __init__(self, main):
        #super().__init__(main)
        TextFrame.__init__(self,main)
        TreeFrame.__init__(self,main)
        self.content_data = dict()

    #create text in nb
    def create_file(self,content = "",title="Untitled", filepath = ""):

        text_area = tk.Text(self.nb, wrap="none", undo=True)
        text_area.insert("1.0",content)
        self.nb.add(text_area, text=title)
        self.nb.select(text_area)
        self.content_data[str(text_area)] = [hash(content),self.nb.tab("current")["text"], filepath]

    #open file
    def open_file(self):
        path = askopenfilename(filetypes=[("Python Files","*.py")])
        filename = os.path.basename(path)
        #check if the file already open
        for tab in self.nb.tabs():
            #currenttab = main.nametowidget(tab)
            if filename == self.content_data[str(tab)][1] and path == self.content_data[str(tab)][2]:
                self.nb.select(tab)
                return
        with open(path, "r") as file:
            code = file.read()
        self.create_file(code,filename,path)

    # open folder
    def openfolder(self):
        directory = filedialog.askdirectory()
        if directory: #to avoid error when cancelation
            try:
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
                #self.tree.grid(column=0,sticky="NEWS",row=0,rowspan=2)
                self.tree.pack(expand=True,fill=tk.BOTH)

                    #self.frame_area.ybar.grid(row=0,column=0,rowspan=2,sticky="WNES")
            except FileNotFoundError as error:
                showerror(title='Error', message=error)

    # select from opened folder
    def select_file(self):
        try:
            curItem = self.tree.focus()
            sltpath = self.tree.item(curItem)["values"]# the value/path of the selected file []
            file_selected = os.path.abspath(sltpath[0])# get the path
            name_of_file = self.tree.item(curItem)["text"] #text name of file
            #filename = os.path.basename(file_selected)
            isfile = os.path.isdir(file_selected)
            if not isfile: # check if the selected file in treeview is not directory file
                for tab in self.nb.tabs(): #check if the file is already in the tab
                    #currenttab = main.nametowidget(tab)
                    if name_of_file == self.content_data[str(tab)][1] and file_selected == self.content_data[str(tab)][2]:
                        self.nb.select(tab) #bring the to the tab that already open
                        return
                with open(file_selected,"r") as file:
                    code = file.read()
                self.create_file(code,name_of_file,file_selected)
        except:
            pass

    # check the value of checkbutton
    def show_hide_files(self, checker):

        if checker.get():
            self.treeFrame.grid(column=0,sticky="NEWS",row=0,rowspan=2)
        else:
            self.treeFrame.grid_remove()

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

    #save as file
    def save_as(self):
        file_path = asksaveasfilename(filetypes=[("Python Files", "*.py")])

        try:
            filename = os.path.basename(file_path)
            text_code = self.select_nb_tab()
            content = text_code.get("1.0","end-1c")
            with open(file_path, "w") as file:
                file.write(content)

        except(AttributeError, FileNotFoundError, TypeError):
            #print("Save operation cancelled")
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

    #close the current selected tab
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
    # select all text area
        """
    def select_all(self):
        get_content_text = self.select_nb_tab()
        get_content_text.tag_add("start","1.0","end")
        #get_content_text.mark_set("INSERT", "1.0")
        #get_content_text.see("INSERT")
        get_content_text.tag_configure("start",background="black",foreground="white")
        return "break"
        """
    def select_all(self):
        get_content_text = self.select_nb_tab()
        get_content_text.tag_add("sel","1.0","end")
        #get_content_text.tag_configure("start",background="black",foreground="white")
        return "break"
    def delete_all_text(self):
        get_content_text = self.select_nb_tab()
        get_content_text.delete("1.0","end")

    # close all
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

    #run the code
    def run(self):
        slctedtab = self.select_nb_tab()
        filepath = self.content_data[str(slctedtab)][2]
        if filepath == "":
            self.save_as()
            return
        command = f"python3 {filepath}" #python3
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell= True)
        output, error = process.communicate()
        self.text_result.insert("end",output)
        self.text_result.insert("end", error)

# class for menu
class MenuBar(tk.Menu):
    def __init__(self, main):
        super().__init__(main)

        # file bar list
        file_list = ["New File", "Open File", "Open Folder", "Save", "Save As..",
        "Close Tab", "Quit"]

        # create file bar menu button
        self.file_bar = tk.Menu(main, tearoff=0) # tearoff for no line

        # add the file_list to the file_bar menu
        for i in file_list:
            self.file_bar.add_command(label = i,compound=tk.LEFT)

        # add the file menu button to the menubar
        self.add_cascade(label = "File", menu = self.file_bar)

        # create separator
        self.file_bar.insert_separator(3)
        self.file_bar.insert_separator(7)

        # edit bar list
        edit_list = ["Undo","Redo","Cut","Copy","Paste","Delete","Select All"]

        # create edit bar
        self.edit_bar = tk.Menu(self,tearoff=0)
        for i in edit_list:
            self.edit_bar.add_command(label = i)

        # create separator
        self.edit_bar.insert_separator(2)
        self.edit_bar.insert_separator(6)
        self.add_cascade(label = "Edit", menu = self.edit_bar)

        #Run Bar
        self.run_bar = tk.Menu(self,tearoff=0)
        self.run_bar.add_command(label = "Run")
        self.add_cascade(label = "Run", menu = self.run_bar)

        #View tree Bar
        self.view_bar = tk.Menu(self,tearoff=0)
        self.view_bar.add_checkbutton(label = "Folder")
        self.add_cascade(label = "View", menu = self.view_bar)

# main class
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("dotpy")
        self.geometry("850x650")
        #self.resizable(False, False)

        # layout on the root/main
        self.grid_columnconfigure(0,weight = 1)
        self.grid_columnconfigure(1,weight = 5)

        # create instance object inherit from FrameController
        self.frame_control = FrameController(self)

        #use the listtabs of save_load module
        store = sl.listtabs #get list of tabs to be load
        for filepath in sl.listtabs:
            if filepath == "": #create an emty text editor tab if the listtabs is empty
                self.frame_control.create_file()
            else:
                filename = os.path.basename(filepath) #get the filename
                with open(filepath, "r") as file: #read inside of the file
                    code = file.read()
                self.frame_control.create_file(code,filename,filepath) #create the tab

        # create MenuBar
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
        self.menu_bar.edit_bar.entryconfig(0, command=self.undo , accelerator = "Ctrl+Z")
        self.menu_bar.edit_bar.entryconfig(1, command=self.redo , accelerator = "Ctrl+Shift+Z")
        self.menu_bar.edit_bar.entryconfig(3, command=self.cut , accelerator = "Ctrl+X")
        self.menu_bar.edit_bar.entryconfig(4, command=self.copy , accelerator = "Ctrl+C")
        self.menu_bar.edit_bar.entryconfig(5, command=self.paste , accelerator = "Ctrl+V")
        self.menu_bar.edit_bar.entryconfig(7, command= self.delete_all)
        self.menu_bar.edit_bar.entryconfig(8, command= self.select_all, accelerator = "Ctrl+A")
        #ran bar command
        self.menu_bar.run_bar.entryconfig(0, command=self.run_file, accelerator = "Ctrl+r")

        #self.frame_control.tree.bind("<Double-1>", lambda e: self.frame_control.select_file())

        self.bind("<Control-n>", lambda e: self.creat_f())
        self.bind("<KeyPress>", lambda e: self.frame_control.change_checker())
        self.bind("<Control-w>", lambda e: self.close_tab())
        self.bind("<Control-r>", lambda e: self.run_file())
        self.bind("<Control-a>", lambda e: self.select_all())

        #result code
        self.frame_control.text_result.bind("<Key>", lambda e: "break")
        self.frame_control.text_result.bind("<Button -1>", lambda e: "break")

        #create variable for add_checkbutton
        self.checkVar = tk.BooleanVar()
        self.checkVar.set(True) #set the check button to true
        self.menu_bar.view_bar.entryconfig(0, command=self.show_or_hide, var=self.checkVar)

        self.protocol("WM_DELETE_WINDOW",self.quit)

    # file bar method
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

    # edit bar method
    def undo(self):
        self.frame_control.nb.focus_get().event_generate("<<Undo>>")
    def redo(self):
        self.frame_control.nb.focus_get().event_generate("<<Redo>>")
    def cut(self):
        self.frame_control.nb.focus_get().event_generate("<<Cut>>")
    def copy(self):
        self.frame_control.nb.focus_get().event_generate("<<Copy>>")
    def paste(self):
        self.frame_control.nb.focus_get().event_generate("<<Paste>>")
    def select_all(self):
        self.frame_control.select_all()
    def delete_all(self):
        self.frame_control.delete_all_text()

    # run bar method
    def run_file(self):
        self.frame_control.run()

    # view bar method
    def show_or_hide(self):
        self.frame_control.show_hide_files(self.checkVar)


if __name__ == "__main__":
    main = MainApp()
    main.mainloop()
