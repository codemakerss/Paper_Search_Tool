import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import back_end as be
import pandas as pd
from tksheet import Sheet
from multiprocessing import Process
import threading
import webview
import webbrowser
from tkinter import filedialog
import shutil
import requests
import os

ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Connect With All Papers - Infinite Insights Papers")
        self.geometry(f"{1375}x{700}")

        self.layout_design()
        self.left_side_bar_design()
        self.right_side_bar_design()
        # self.middle_side_bar_design()
        # self.bind("<Configure>", self.on_resize)

        # self.style = ttk.Style(self)
        # self.configure_styles()

    def layout_design(self):
        """
        configure layout over here
        """
        # Configure grid layout for a 3x3 grid
        self.grid_columnconfigure(0, weight=1, minsize=150)  # Column 0 with fixed width of 170
        self.grid_columnconfigure(1, weight=0, minsize=850)  # Column 1 with fixed width of 830
        self.grid_columnconfigure(2, weight=1, minsize=375)  # Column 2 with fixed width of 375

        self.grid_rowconfigure(0, weight=0)  # Rows 0, 1, and 2 to expand equally       
        self.grid_rowconfigure((1,2), weight=1)
    def right_side_bar_design(self):
        """
        provide papers related information for users to look up with
        """
        # configure grid layout (3x3)
        # self.grid_columnconfigure((0,1,2), weight=1)
        # self.grid_rowconfigure((0,1,2), weight=1)

        # create sidebar frame with widgets
        # set corner to be a litte bit in round lookings 
        
        # self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=10)
        # self.sidebar_frame.grid(row=0, column=2, rowspan=3, sticky="nsew")

        #self.sidebar_frame.grid_columnconfigure(2, weight=1)
        #self.sidebar_frame.grid_rowconfigure(3, weight=1)

        # set the side bar logo name as search papers
        """
        +-----+------+-----+-----+
        |     |      |     |     |  <- Row 0 (weight=1)
        +-----+------+-----+-----+
        |     |      |     |     |  <- Row 1 (weight=1)
        +-----+------+-----+-----+
        |     |      |     |     |  <- Row 2 (weight=1)
        +-----+------+-----+-----+
        |     |      |     |     |  <- Row 3 (not configured, weight=0 by default)
        +-----+------+-----+-----+
          ^      ^      ^     ^
          |      |      |     |
        Col 0  Col 1  Col 2 Col 3
        (weight=0) (weight=1) (weight=0)
        """
        # add scrollable_frame at here
        self.search_engine_frame()

    # remove message when user click the textbox
    def on_focus_in(self, event):
        textbox = self.get_textbox_from_event(event)
        if textbox and textbox.get('1.0', 'end-1c') == textbox.placeholder:
            textbox.delete('1.0', 'end')
            textbox.configure(font=('Arial', 15, 'normal'))

    # show message when user click the textbox
    def on_focus_out(self, event):
        textbox = self.get_textbox_from_event(event)
        if textbox and not textbox.get('1.0', 'end-1c').strip():
            textbox.insert('1.0', textbox.placeholder)
            textbox.configure(font=('Arial', 15, 'italic'))

    # retrieve the placeholder names
    def get_textbox_from_event(self, event):
        # Check if the widget that triggered the event is a Text widget inside a CTkTextbox
        if isinstance(event.widget.master, ctk.CTkTextbox):
            return event.widget.master  
        return None  

    def reset_arxiv_controls(self):
        # reset all switches in the arXiv and scholar
        # arXiv
        for switch in self.search_parameters_switches:
            switch.deselect()
            self.switch.bind('<ButtonClose-1>', reset_arxiv_controls)

    def reset_scholar_controals(self):
        # reset all switches in the arXiv and scholar
        # scholar
        for switch in self.search2_parameters_switches:
            switch.deselect()  
            self.switch.bind('<ButtonClose-1>', reset_scholar_controals)

        # # Reset all values in option menus
        # # Assuming you have a list of all option menus like self.all_option_menus
        # for option_menu in self.all_option_menus:
        #     option_menu.set("default_value")  # Replace "default_value" with your actual default value


    def search_engine_frame(self):
        """
        switch with different search engines
        """
        # self.static_frame = tk.Frame(self, bd=2, relief="groove")
        # self.static_frame.grid(row=0, column=2, padx=(5, 0), pady=(0, 60), sticky="ew")
        # create scrollable frame
        self.search_engine_frame = ctk.CTkFrame(self, height = 100, border_width=2)
        self.search_engine_frame.grid(row=0, column=2, sticky="nsew")

        #self.scrollable_frame.grid(row=1, column=2, padx=(20, 0s), pady=(0, 30), sticky="nsew")

        self.search_engine_frame.grid_columnconfigure(0, weight=1)
        #self.scrollable_frame_switches = []

        self.right_bar_label = ctk.CTkLabel(self.search_engine_frame, text="Search Papers", font=ctk.CTkFont(size=20, weight="bold"),anchor="center")
        self.right_bar_label.grid(row=0, column=0, padx=80, pady=(20, 10))

        # integrate switches in the  search engine frames 
        # switch constrains goes here 
        def switch_x_callback(*args):
            if self.switch_x.get() == 1:  # If switch_x is turned on
                self.switch_g.deselect() # Turn off switch_g
                self.tabview.set("arXiv")  # Set the arXiv tab to be visible
                # set other tabs cannot be accessed 
                # self.tabview.tab("Google Scholar Search", state='disabled')
                # self.tabview.tab("InfiniteInsights", state='disabled')

                # reset scholar
                # self.reset_scholar_controals()
                for switch in self.search_parameters_switches:
                    switch.deselect()
                    # print(switch.get())

                # reset scholar values 
                self.display_language_optionmenu.set("en-English")
                self.display_at_year_optionmenu.set("2023")
                self.display_until_year_optionmenu.set("2023")
                self.max_results2_textbox.delete('1.0', 'end')

                self.max_results2_textbox.insert('1.0', "Enter integer numbers here")

                # clear query context
                self.tk_textbox.delete('1.0', 'end')
                self.tk_textbox.insert('1.0', "Please provide your query message here.")

            else:
                self.tabview.set("InfiniteInsights Papers")

                # self.reset_arxiv_controls(self)
                for switch in self.search2_parameters_switches:
                    switch.deselect()  

                # reset arxiv search values 
                self.search_by_optionmenu.set("None")
                self.category_taxonomy_optionmenu.set("None")
                self.id_list_textbox.delete('1.0', 'end')
                self.max_results_textbox.delete('1.0', 'end')

                self.id_list_textbox.insert('1.0', "Enter id list here")
                self.max_results_textbox.insert('1.0', "Enter integer numbers here")

                # clear query context
                self.tk_textbox.delete('1.0', 'end')
                self.tk_textbox.insert('1.0', "Please provide your query message here.")
                #self.tk_textbox.configure(font=('Arial', 18, 'italic'), text_color="black")

        def switch_g_callback(*args):
            if self.switch_g.get() == 1:  # If switch_g is turned on
                self.switch_x.deselect()  # Turn off switch_x
                self.tabview.set("scholar")  # Set the scholar tab to be visible
                # set other tabs cannot be accessed 
                # self.tabview.tab("ArXiv Search", state='disabled')
                # self.tabview.tab("InfiniteInsights", state='disabled')

                # reset arxiv
                # self.reset_arxiv_controls(self)
                for switch in self.search2_parameters_switches:
                    switch.deselect()  
                    # print(switch.get())

                # reset arxiv search values 
                self.search_by_optionmenu.set("None")
                self.category_taxonomy_optionmenu.set("None")
                self.id_list_textbox.delete('1.0', 'end')
                self.max_results_textbox.delete('1.0', 'end')

                self.id_list_textbox.insert('1.0', "Enter id list here")
                self.max_results_textbox.insert('1.0', "Enter integer numbers here")

                # clear query context
                self.tk_textbox.delete('1.0', 'end')
                self.tk_textbox.insert('1.0', "Please provide your query message here.")

            else:
                self.tabview.set("InfiniteInsights Papers")

                # self.reset_scholar_controals()
                for switch in self.search_parameters_switches:
                    switch.deselect()

                # reset scholar values 
                self.display_language_optionmenu.set("en-English")
                self.display_at_year_optionmenu.set("2023")
                self.display_until_year_optionmenu.set("2023")
                self.max_results2_textbox.delete('1.0', 'end')

                self.max_results2_textbox.insert('1.0', "Enter integer numbers here")

                # clear query context
                self.tk_textbox.delete('1.0', 'end')
                self.tk_textbox.insert('1.0', "Please provide your query message here.")
                #self.tk_textbox.configure(font=('Arial', 18, 'italic'), text_color="black")

        self.search_engine_frame_switches = []
        # create switch for arXiv
        self.switch_x = ctk.CTkSwitch(master=self.search_engine_frame, text=f"ArXiv Search")
        self.switch_x.grid(row=1, column=0, padx=20, pady=(0, 20), sticky='w')
        self.search_engine_frame_switches.append(self.switch_x)
        self.switch_x.bind('<ButtonRelease-1>', switch_x_callback)  # Bind callback to switch_x

        # create switch for Google Scholar
        self.switch_g = ctk.CTkSwitch(master=self.search_engine_frame, text=f"Google Scholar Search")
        self.switch_g.grid(row=2, column=0, padx=20, pady=(0, 20), sticky='w')
        self.search_engine_frame_switches.append(self.switch_g)
        #self.switch_g.bind('<ButtonRelease-1>', switch_g_callback)  # Bind callback to switch_g
        self.switch_g.deselect() # save for future usage

        # create text box for query search 
        self.tk_textbox = ctk.CTkTextbox(master=self.search_engine_frame, activate_scrollbars=False, height = 50)
        self.tk_textbox.grid(row=3, column=0, padx = 10, pady = (0, 20), sticky="ew")
        self.tk_textbox.insert("1.0", "Please provide your query message here.")
        if (self.appearance_mode_optionemenu.get() == "Dark"):
            print("test Dark")
            self.tk_textbox.configure(font=('Arial', 15, 'italic'), text_color="white")
        else:
            self.tk_textbox.configure(font=('Arial', 15, 'italic'), text_color="black")

        self.tk_textbox.placeholder = "Please provide your query message here."

        # Bind the focus in and focus out events
        self.tk_textbox.bind('<FocusIn>', self.on_focus_in)
        self.tk_textbox.bind('<FocusOut>', self.on_focus_out)
        
        # # create CTk scrollbar
        # ctk_textbox_scrollbar = ctk.CTkScrollbar(master=self.search_engine_frame, command=self.tk_textbox.xview, orientation='horizontal')
        # ctk_textbox_scrollbar.grid(row=4, column=0, sticky="ew")

        # # connect textbox scroll event to CTk scrollbar
        # self.tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

        # text box only for Google Scholar API
        # create text box for query search 
        self.scholar_textbox = ctk.CTkTextbox(master=self.search_engine_frame, activate_scrollbars=False, height = 30)
        self.scholar_textbox.grid(row=4, column=0, padx = 10, pady = (0, 20), sticky="ew")
        self.scholar_textbox.insert("1.0", "Google Serp Webscraping API goes here.")
        self.scholar_textbox.configure(font=('Arial', 15, 'italic'), text_color="gray")

        self.scholar_textbox.placeholder = "Google Serp Webscraping API goes here."

        # self.x = ctk.CTkTextbox(master=self.search_engine_frame, activate_scrollbars=False, height = 30)
        # self.x.grid(row=7, column=0, padx = 10, sticky="nsew")
        # Bind the focus in and focus out events
        self.scholar_textbox.bind('<FocusIn>', self.on_focus_in)
        self.scholar_textbox.bind('<FocusOut>', self.on_focus_out)

        self.search_query_frame()

    def get_serach_query_value(self):
        # retrieve serach query if exist
        return self.tk_textbox.get('1.0', 'end-1c')
        # if (self.tk_textbox.get('1.0', 'end-1c') != "Please provide your query message here." and self.tk_textbox.get('1.0', 'end-1c') != ""):
        #         return self.tk_textbox.get('1.0', 'end-1c')
        # else:
        #     # show error message on no query text provided 
        #     messagebox.showerror("Error", "Please include query values when searching papers.")
        #     return 0

    def search_query_frame(self):
        """
        search query frame design by using parameters from arXiv and scholar functions
        """
        # create main entry and button
        self.scroll_query_frame = ctk.CTkScrollableFrame(self, label_text="Search Parameters", height = 400, label_font=ctk.CTkFont(size=20, weight="bold"), border_width=2)
        self.scroll_query_frame.grid(row=1, column=2, rowspan=2, sticky="nsew")
        self.scroll_query_frame.scrollbar_width = 0
        self.scroll_query_frame.scrollbar_hover = False

        # create tabview
        # set tab view initially not able to be switched by users
        self.tabview = ctk.CTkTabview(master = self.scroll_query_frame, width=330, state = "disabled") 
        self.tabview.grid(row=0, padx=15, sticky="nsew")
        self.tabview.add("InfiniteInsights Papers")
        self.tabview.add("arXiv")
        self.tabview.add("scholar")
        self.tabview.tab("InfiniteInsights Papers").grid_columnconfigure(0, weight=1)
        self.tabview.tab("arXiv").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("scholar").grid_columnconfigure(0, weight=1)

        self.logo_tab_view()
        self.arxiv_tab_view()
        self.scholar_tab_view()

    def logo_tab_view(self):
        # frame a logo for the app in the tab view 
        # light_image_path = os.path.abspath("IIF_200x200.png")
        # dark_image_path = os.path.abspath("IIF_200x200.png")
        light_image_path = os.path.join(os.path.dirname(__file__), "IIF_200x200.png")
        dark_image_path = os.path.join(os.path.dirname(__file__), "IIF_200x200.png")

        open_image_1 = Image.open(light_image_path)
        open_image_2 = Image.open(dark_image_path)

        # # resize the logo 
        # resized_image_1 = open_image_1.resize((200, 204), Image.Resampling.LANCZOS) 
        # resized_image_2 = open_image_2.resize((200, 204), Image.Resampling.LANCZOS)

        self.logo = ctk.CTkImage(light_image=open_image_1,
                                  dark_image=open_image_2,
                                  size=(271, 200))

        self.image_label = ctk.CTkLabel(self.tabview.tab("InfiniteInsights Papers"), image = self.logo, text="")  # display image with a CTkLabel
        self.image_label.grid(row=1, column=0, padx = 5, pady = 50)

    def arxiv_tab_view(self): 
        # all switches for arxiv
        self.search_parameters_switches = []

        # arXiv search parameters
        # search by parameter
        self.switch_search_by = ctk.CTkSwitch(self.tabview.tab("arXiv"), text=f"Search by")
        self.switch_search_by.grid(row=0, column=0, padx=5, pady=(50, 20),sticky='w')
        self.search_parameters_switches.append(self.switch_search_by)

        self.search_by_optionmenu = ctk.CTkOptionMenu(self.tabview.tab("arXiv"), dynamic_resizing=False,
                                                        values=["Title", "Abstract", "Category (Taxonomy)"], height=30, width=150, anchor="center")
        self.search_by_optionmenu.grid(row=0, column=1, pady=(50, 20), sticky="ew")
        self.search_by_optionmenu.set("None")
        
        # self.scholar_textbox = ctk.CTkTextbox(master=self.tabview.tab("arXiv"), activate_scrollbars=False,height=10, width=170)
        # self.scholar_textbox.grid(row=0, column=1, pady=(0, 20), sticky="ew")

        # taxonomy parameter
        self.switch_category_taxonomy = ctk.CTkSwitch(self.tabview.tab("arXiv"), text=f"Taxonomy")
        self.switch_category_taxonomy.grid(row=1, column=0, padx=5, pady=(0, 20),sticky='w')
        self.search_parameters_switches.append(self.switch_category_taxonomy)

        # self.category_taxonomy_optionmenu = ctk.CTkOptionMenu(self.tabview.tab("arXiv"), dynamic_resizing=False,
        #                                                 values=["q-fin.CP", "q-fin.EC", "q-fin.GN", "q-fin.MF", "q-fin.PM", "q-fin.PR", "q-fin.RM", "q-fin.ST", "q-fin.TR"], height=30, width=170, anchor="center")
        self.category_taxonomy_optionmenu = ctk.CTkOptionMenu(self.tabview.tab("arXiv"), dynamic_resizing=False,
                                                        values=["q-fin.CP", "q-fin.EC", "q-fin.GN", "q-fin.MF", "q-fin.PM", "q-fin.PR", "q-fin.RM", "q-fin.ST", "q-fin.TR", 
                                                        "cs.AI", "cs.AR", "cs.CC", "cs.CE", "cs.CG", "cs.CL", "cs.CR", "cs.CV", "cs.CY", "cs.DB", "cs.DC", "cs.DL", "cs.DM", "cs.DS", "cs.ET", "cs.FL", "cs.GL", "cs.GR", "cs.GT", "cs.HC", "cs.IR", "cs.IT", "cs.LG", "cs.LO", "cs.MA", "cs.MM", "cs.MS", "cs.NA", "cs.NE", "cs.NI", "cs.OH", "cs.OS", "cs.PF", "cs.PL", "cs.RO", "cs.SC", "cs.SD", "cs.SE", "cs.SI", "cs.SY",
                                                        "econ.EM", "econ.GN", "econ.TH",
                                                        "eess.AS", "eess.IV", "eess.SP", "eess.SY",
                                                        "math.AC", "math.AG", "math.AP", "math.AT", "math.CA", "math.CO", "math.CT", "math.CV", "math.DG", "math.DS", "math.FA", "math.GM", "math.GN", "math.GR", "math.GT", "math.HO", "math.IT", "math.KT", "math.LO", "math.MG", "math.MP", "math.NA", "math.NT", "math.OA", "math.OC", "math.PR", "math.QA", "math.RA", "math.RT", "math.SG", "math.SP", "math.ST",
                                                        "stat.AP", "stat.CO", "stat.ME", "stat.ML", "stat.OT", "stat.TH"], height=30, width=170, anchor="center")
        self.category_taxonomy_optionmenu.grid(row=1, column=1, pady=(0, 20), sticky="ew")
        self.category_taxonomy_optionmenu.set("None")

        # self.scholar_textbox = ctk.CTkTextbox(master=self.tabview.tab("arXiv"), activate_scrollbars=False,height=10, width=170)
        # self.scholar_textbox.grid(row=1, column=1, pady=(0, 20), sticky="ew")

        # id list parameter
        self.switch_id_list = ctk.CTkSwitch(self.tabview.tab("arXiv"), text=f"Id list")
        self.switch_id_list.grid(row=2, column=0, padx=5, pady=(0, 20),sticky='w')
        self.search_parameters_switches.append(self.switch_id_list)

        self.id_list_textbox = ctk.CTkTextbox(master=self.tabview.tab("arXiv"), activate_scrollbars=False,height=10, width=170)
        self.id_list_textbox.grid(row=2, column=1, pady=(0, 20), sticky="ew")
        self.id_list_textbox.insert('1.0', "Enter id list here")
        self.id_list_textbox.configure(font=('Arial', 15, 'italic'), text_color="gray")


        # show message when not typing
        self.id_list_textbox.placeholder = "Enter id list here"
        self.id_list_textbox.bind('<FocusIn>', self.on_focus_in)
        self.id_list_textbox.bind('<FocusOut>', self.on_focus_out)

        # max results
        self.switch_max_results = ctk.CTkSwitch(self.tabview.tab("arXiv"), text=f"Max results")
        self.switch_max_results.grid(row=3, column=0, padx=5, pady=(0, 20),sticky='w')
        self.search_parameters_switches.append(self.switch_max_results)

        self.max_results_textbox = ctk.CTkTextbox(master=self.tabview.tab("arXiv"), activate_scrollbars=False,height=10, width=170)
        self.max_results_textbox.grid(row=3, column=1, pady=(0, 20), sticky="ew")
        self.max_results_textbox.insert('1.0', "Enter integer numbers here")
        self.max_results_textbox.configure(font=('Arial', 15, 'italic'), text_color="gray")

        # show message when not typing
        self.max_results_textbox.placeholder = "Enter integer numbers here"
        self.max_results_textbox.bind('<FocusIn>', self.on_focus_in)
        self.max_results_textbox.bind('<FocusOut>', self.on_focus_out)

        # run arXiv paper searches here 
        # def button_event():
        #     #self.sheet.delete_sheet_format(clear_values = True)
        #     #self.sheet.delete_all_formatting(clear_values = True)

        #     # self.update()

        #     temp_query = self.get_serach_query_value()
        #     # temp_arxiv_search_by = self.get_arxiv_search_by_optionmenu()
        #     temp_arxiv_id_list = self.get_arxiv_id_list_textbox()

        #     if (temp_query != 0):
        #         test1 = be.arxiv_search_without_constrains(temp_query, int(self.get_arxiv_max_results()))
        #         #print(test1)
        
        #         #self.middle_side_bar_design(1,0, test1)
        #         self.middle_side_bar_design(0,1, test1)

        #     elif (temp_arxiv_id_list != 0):
        #         test2 = be.arxiv_search_only_id_list(temp_arxiv_id_list, int(self.get_arxiv_max_results()))
        #         self.middle_side_bar_design(0,1, test2)
          
            # temp_arxiv_category = self.get_arxiv_category_taxonomy_optionmenu()
            # temp_arxiv_id_list = self.get_arxiv_id_list_textbox()
            # temp_arxiv_max_results = self.get_arxiv_max_results
        def button_event():

            temp_query = self.get_serach_query_value()
            temp_arxiv_id_list = self.get_arxiv_id_list_textbox()
            temp_search_by = self.get_arxiv_search_by_optionmenu()
            temp_arxiv_category = self.get_arxiv_category_taxonomy_optionmenu()

            #print("teststs : ", temp_arxiv_category)

            if temp_query != "Please provide your query message here.":
                # "Title", "Abstract", "Category (Taxonomy)"

                if (temp_search_by == "Title"):
                    print("query title only")
                    # check if category is on
                    if (temp_arxiv_category or temp_arxiv_category == 0):
                        # show errors for category under title
                        messagebox.showerror("Error", "Please deselect Taxonomy switch when using Title as search.")
                    elif (temp_arxiv_id_list or temp_arxiv_id_list == 0):
                        # show errors for id list under title 
                        messagebox.showerror("Error", "Please deselect Id list switch when using Title as search.")
                    else:
                        test3 = be.arxiv_search_only_title(temp_search_by, int(self.get_arxiv_max_results()))
                        self.middle_side_bar_design(0, 1, test3)

                elif(temp_search_by == "Abstract"):
                    print("query abstract only")
                    # check if category is on
                    if (temp_arxiv_category or temp_arxiv_category == 0):
                        # show errors for category under abstract 
                        messagebox.showerror("Error", "Please deselect Taxonomy switch when using Abstract as search.")
                    elif (temp_arxiv_id_list or temp_arxiv_id_list == 0):
                        # show errors for id list under abstract
                        messagebox.showerror("Error", "Please deselect Taxonomy switch when using Abstract as search.")
                    else:
                        test4 = be.arxiv_search_only_abstract(temp_search_by, int(self.get_arxiv_max_results()))
                        self.middle_side_bar_design(0, 1, test4)

                elif(temp_search_by == "Category (Taxonomy)"):
                    print("query category only")
                    # temp_arxiv_category = self.get_arxiv_category_taxonomy_optionmenu()
                    # check if id list turn on first
                    if (temp_arxiv_id_list or temp_arxiv_id_list == 0):
                        # show errors for id list under abstract
                        messagebox.showerror("Error", "Please deselect Id List switch when using Category (Taxonomy) as search.")
                    else:
                        # without id list issue 
                        if (temp_arxiv_category != 0 and temp_arxiv_category != None): # normal category search by with its value 
                            print("test :", temp_arxiv_category)
                            print("Test Category")
                            # print(temp_arxiv_category == "None")
                            # print(temp_arxiv_category == None)
                            test5 = be.arxiv_search_only_category(temp_search_by, temp_arxiv_category, int(self.get_arxiv_max_results()))
                            self.middle_side_bar_design(0, 1, test5)
                        else:
                            # needs a category value and its switch on
                            messagebox.showerror("Error", "Please turn Taxonomy switch and select a taxonomy value when using Category (Taxonomy) as search.")
                # check all switches and values to be off
                elif (self.switch_search_by.get() == 0 and self.search_by_optionmenu.get() == "None" and self.switch_category_taxonomy.get() == 0 and self.category_taxonomy_optionmenu.get() == "None" and self.switch_id_list.get() == 0 and self.id_list_textbox.get('1.0', 'end-1c') == "Enter id list here"):
                    # simple only query search
                    test1 = be.arxiv_search_without_constrains(temp_query, int(self.get_arxiv_max_results()))
                    self.middle_side_bar_design(0, 1, test1)   
                # all errors here
                else:
                    # show errors for both simple search or swtich on without values or values without turning on switches 
                    messagebox.showerror("Error", "Please check all switches with its value has been selected or do simple query search without selecting any parameters.")              
            else:
                # only id list search 
                if (self.switch_search_by.get() == 0 and self.search_by_optionmenu.get() == "None" and self.switch_category_taxonomy.get() == 0 and self.category_taxonomy_optionmenu.get() == "None"):
                    if (self.switch_id_list.get() == 1 and self.id_list_textbox.get('1.0', 'end-1c') != "Enter id list here"):
                        test2 = be.arxiv_search_only_id_list(temp_arxiv_id_list)
                        self.middle_side_bar_design(0, 1, test2)
                    # else: 
                    #     messagebox.showerror("Error", "Please turn on either Id List switch or enter id list values to search by id list.")

                # no query message and no switches and values
                if (self.switch_search_by.get() == 0 and self.search_by_optionmenu.get() == "None" and self.switch_category_taxonomy.get() == 0 and self.category_taxonomy_optionmenu.get() == "None" and self.switch_id_list.get() == 0 and self.id_list_textbox.get('1.0', 'end-1c') == "Enter id list here"):
                    messagebox.showerror("Error", "Please include search query before searching.")

                # no query message and switches or values on
                if (self.switch_search_by.get() == 1 or self.search_by_optionmenu.get() != "None" or self.switch_category_taxonomy.get() == 1 or self.category_taxonomy_optionmenu.get() != "None"):
                    messagebox.showerror("Error", "Please include search query before searching.")



                # if any switches on without query, report errors
                # if (temp_arxiv_id_list == 0):
                #     messagebox.showerror("Error", "Please include search query before turning Id List switch on.")
                
                # if (temp_search_by == 0):
                #     messagebox.showerror("Error", "Please include search query before turning Search By switch on.")
                
                # if (temp_arxiv_category == 0):
                #     messagebox.showerror("Error", "Please include search query before turning Taxonomy switch on.")


            # elif temp_arxiv_id_list != 0:
            #     test2 = be.arxiv_search_only_id_list(temp_arxiv_id_list)
            #     self.middle_side_bar_design(0, 1, test2)

            # elif temp_search_by and temp_search_by != "None":
            #     test3 = be.arxiv_search_only_title(temp_search_by, int(self.get_arxiv_max_results()))
            #     self.middle_side_bar_design(0, 1, test3)

            # else:
            #     # show error message only when the search query is empty or has the default message
            #     if not temp_query or temp_query == "Please provide your query message here.":
            #         messagebox.showerror("Error", "Please include either query values or any other parameters when searching papers.")



        self.arxiv_button = ctk.CTkButton(master=self.tabview.tab("arXiv"), text="Get Papers!", width = 250,command=button_event)
        self.arxiv_button.grid(row=5, column=0, columnspan=2, padx=5, pady=(0, 20),sticky='ew')

        def button_event_2(): # clear all data 
             self.middle_side_bar_design(1, 0, {})

        self.arxiv_button_clear = ctk.CTkButton(master=self.tabview.tab("arXiv"), text="Clear Data", width = 250,command=button_event_2)
        self.arxiv_button_clear.grid(row=6, column=0, columnspan=2, padx=5, pady=(0, 20),sticky='ew')

    def get_arxiv_search_by_optionmenu(self):
        # retrieve arxiv search by values
        if (self.search_by_optionmenu.get() != "None"):
            if (self.switch_search_by.get() == 1):
                return self.search_by_optionmenu.get()
            else:
                messagebox.showerror("Error", "Please turn on Search by switch on to use search by parameter.")
                return 0
        else:
            if (self.switch_search_by.get() == 1):  
                messagebox.showerror("Error", "Please select a search by parameter values when turn on Search by switch.")
                return 0          
            # nothing ...

        # if (self.switch_search_by.get() == 1):
            # if (self.search_by_optionmenu.get() != "None"):
            #     return self.search_by_optionmenu.get()
            # else:
            #     # show error message of turn switch on without select search by values
            #     messagebox.showerror("Error", "Please select a search by parameter values when turn on Search by switch.")
            #     return 0
        #     return self.search_by_optionmenu.get()
        # else:
        #     messagebox.showerror("Error", "Please turn on Search by switch on to use search by parameter.")
        #     return 0

    def get_arxiv_category_taxonomy_optionmenu(self):
        # retrieve arxiv category taxonomy values

        # if (self.switch_category_taxonomy.get() == 1):
        #     if (self.category_taxonomy_optionmenu.get() != "None"):
        #         return self.category_taxonomy_optionmenu.get()
        #     else:
        #         # show error message of turn switch on without select category taxonomy values
        #         messagebox.showerror("Error", "Please select a category taxonomy parameter values when turn on Category Taxonomy switch.")
        #         return 0     
        # else:
        #     messagebox.showerror("Error", "Please turn on Category Taxonomy switch on to use category taxonomy parameter.")
        #     return 0              

        if (self.category_taxonomy_optionmenu.get() != "None"): # if has taxonomy value 
            if (self.switch_category_taxonomy.get() == 1): # if switch is on
                # double check if "Category (Taxonomy)" is on
                if (self.get_arxiv_search_by_optionmenu()):
                    return self.category_taxonomy_optionmenu.get()
                else:
                    messagebox.showerror("Error", "Please select the category taxonomy parameter values and turn on Category Taxonomy switch.")
                    return 0

        else:
            if (self.switch_category_taxonomy.get() == 1): # if has no taxonomy value, but switch is on
                messagebox.showerror("Error", "Please turn on Category Taxonomy switch on to use category taxonomy parameter.")
                return 0


    def get_arxiv_id_list_textbox(self): 
        # retrieve arxiv id list if exist
        if (self.id_list_textbox.get('1.0', 'end-1c') != "Enter id list here"):
            if (self.switch_id_list.get() == 1):
                return self.id_list_textbox.get('1.0', 'end-1c')
            else:
                messagebox.showerror("Error", "Please turn on Id List switch on to use id list parameter.")
                return 0
        else:
            if (self.switch_id_list.get() == 1):
                messagebox.showerror("Error", "Please include id list values when turn on Id List switch.")
                return 0

        # if (self.switch_id_list.get() == 1):
        #     if (self.id_list_textbox.get('1.0', 'end-1c') != "Enter id list here"):
        #         return self.id_list_textbox.get('1.0', 'end-1c')
        #     else:
        #         # show error message of turn switch on without input values
        #         messagebox.showerror("Error", "Please include id list values when turn on Id List switch.")
        #         return 0
        # else:
        #     messagebox.showerror("Error", "Please turn on Id List switch on to use id list parameter.")
        #     return 0

    def get_arxiv_max_results(self):
        # retrieve arxiv max results if exist
        if (self.max_results_textbox.get('1.0', 'end-1c') != "Enter integer numbers here"):
            if (self.switch_max_results.get() == 1):
                return self.max_results_textbox.get('1.0', 'end-1c')
            else:
                messagebox.showerror("Error", "Please turn on Max Result switch on to use max results parameter.")
                return 0  
        else:
            if (self.switch_max_results.get() == 1):
                # show error message of turn switch on without input values
                messagebox.showerror("Error", "Please include max results values when turn on Max Result switch.")
                return 0 
            else:
                return 0




        # if (self.switch_max_results.get() == 1):
            
        #     if (self.max_results_textbox.get('1.0', 'end-1c') != "Enter integer numbers here"):
        #         return self.max_results_textbox.get('1.0', 'end-1c')
        #     else:
        #         # show error message of turn switch on without input values
        #         messagebox.showerror("Error", "Please include max results values when turn on Max Result switch.")
        #         return 0   
        # else:
        #     messagebox.showerror("Error", "Please turn on Max Result switch on to use max results parameter.")
        #     return 0                        

    def scholar_tab_view(self): 
        # all switches for scholar
        self.search2_parameters_switches = []

        # result language display 
        self.switch_display_language = ctk.CTkSwitch(self.tabview.tab("scholar"), text=f"Language")
        self.switch_display_language.grid(row=0, column=0, padx=5, pady=(50, 20),sticky='w')
        self.search2_parameters_switches.append(self.switch_display_language)      

        self.display_language_optionmenu = ctk.CTkOptionMenu(self.tabview.tab("scholar"), dynamic_resizing=False,
                                                        values=["en-English", "it-Italian", "zh-CN-Chinese"], height=30, width=170, anchor="center")
        self.display_language_optionmenu.grid(row=0, column=1, pady=(50, 20), sticky="ew")
        self.display_language_optionmenu.set("None") 

        # at this year data
        self.switch_display_at_year = ctk.CTkSwitch(self.tabview.tab("scholar"), text=f"At year")
        self.switch_display_at_year.grid(row=1, column=0, padx=5, pady=(0, 20),sticky='w')
        self.search2_parameters_switches.append(self.switch_display_at_year)  

        years = ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992', '1991', '1990', '1989', '1988', '1987', '1986', '1985', '1984', '1983', '1982', '1981', '1980', '1979', '1978', '1977', '1976', '1975', '1974']
        self.display_at_year_optionmenu = ctk.CTkOptionMenu(self.tabview.tab("scholar"), dynamic_resizing=False,
                                                        values=years, height=30, width=170, anchor="center") # back 50 years
        self.display_at_year_optionmenu.grid(row=1, column=1, pady=(0, 20), sticky="ew")
        self.display_at_year_optionmenu.set("None") 

        # until this year data
        self.switch_display_until_year = ctk.CTkSwitch(self.tabview.tab("scholar"), text=f"Until year")
        self.switch_display_until_year.grid(row=2, column=0, padx=5, pady=(0, 20),sticky='w')
        self.search2_parameters_switches.append(self.switch_display_until_year)  
 
        years = ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992', '1991', '1990', '1989', '1988', '1987', '1986', '1985', '1984', '1983', '1982', '1981', '1980', '1979', '1978', '1977', '1976', '1975', '1974']
        self.display_until_year_optionmenu = ctk.CTkOptionMenu(self.tabview.tab("scholar"), dynamic_resizing=False,
                                                        values=years, height=30, width=170, anchor="center") # back 50 years
        self.display_until_year_optionmenu.grid(row=2, column=1, pady=(0, 20), sticky="ew")
        self.display_until_year_optionmenu.set("None") 

        # number of results
        self.switch_num_results = ctk.CTkSwitch(self.tabview.tab("scholar"), text=f"Max results")
        self.switch_num_results.grid(row=3, column=0, padx=5, pady=(0, 20),sticky='w')
        self.search2_parameters_switches.append(self.switch_num_results)   

        self.max_results2_textbox = ctk.CTkTextbox(master=self.tabview.tab("scholar"), activate_scrollbars=False,height=10, width=170)
        self.max_results2_textbox.grid(row=3, column=1, pady=(0, 20), sticky="ew")
        self.max_results2_textbox.insert('1.0', "Enter integer numbers here")
        self.max_results2_textbox.configure(font=('Arial', 15, 'italic'), text_color="gray")

        # show message when not typing
        self.max_results2_textbox.placeholder = "Enter integer numbers here"
        self.max_results2_textbox.bind('<FocusIn>', self.on_focus_in)
        self.max_results2_textbox.bind('<FocusOut>', self.on_focus_out)

        # run scholar paper searches here 
        def button_event():
            print("button pressed")

        self.scholar_button = ctk.CTkButton(master=self.tabview.tab("scholar"), text="Get Papers!", width = 250,command=button_event)
        self.scholar_button.grid(row=5, column=0, columnspan=2, padx=5, pady=(0, 20),sticky='ew')

    def get_scholar_display_language(self):
        # retrieve language display values
        if (self.switch_display_language.get() == 0):
            if (self.display_language_optionmenu.get() != "None"):
                return self.display_language_optionmenu.get()
            else:
                # show error message of turn switch on without select language values
                messagebox.showerror("Error", "Please select a display language parameter values when turn on Display Language switch.")
                return 0     
        else:
            messagebox.showerror("Error", "Please turn on Display Language switch on to use display language parameter.")
            return 0  
 
 
    def get_scholar_display_at_year(self):
        # retrieve display at years values
        if (self.switch_display_at_year.get() == 0):
            if (self.display_at_year_optionmenu.get() != "None"):
                return self.display_at_year_optionmenu.get()
            else:
                # show error message of turn switch on without select display at year values
                messagebox.showerror("Error", "Please select a display at year parameter values when turn on At Year switch.")
                return 0     
        else:
            messagebox.showerror("Error", "Please turn on At Year switch on to use display at year parameter.")
            return 0 

    def get_scholar_display_until_year(self):
        # retrieve display until years values
        if (self.switch_display_until_year.get() == 0):
            if (self.display_until_year_optionmenu.get() != "None"):
                return self.display_until_year_optionmenu.get()
            else:
                # show error message of turn switch on without select display until year values
                messagebox.showerror("Error", "Please select a display until year parameter values when turn on Until Year switch.")
                return 0     
        else:
            messagebox.showerror("Error", "Please turn on Until Year switch on to use display until year parameter.")
            return 0 

    def get_scholar_max_results(self):
        # retrieve arxiv max results if exist
        if (self.switch_num_results.get() == 0):
            if (self.max_results2_textbox.get('1.0', 'end-1c') != "Enter integer numbers here"):
                return self.max_results2_textbox.get('1.0', 'end-1c')
            else:
                # show error message of turn switch on without input values
                messagebox.showerror("Error", "Please include max results values when turn on Max Result switch.")
                return 0   
        else:
            messagebox.showerror("Error", "Please turn on Max Result switch on to use max results parameter.")
            return 0   

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

        if (new_appearance_mode == "Dark"):
            self.tk_textbox.configure(font=('Arial', 15, 'italic'), text_color="white")
            self.update()
        else:
            self.tk_textbox.configure(font=('Arial', 15, 'italic'), text_color="black")
            self.update()

        theme_background_colors = {
            "System": "black",  
            "Light": "white",
            "Dark": "black"  
        }

        # light blue, light green, dark, dark blue and dark green
        if (new_appearance_mode == "Dark"):
            self.sheet.change_theme(theme = "dark blue")
            self.update()
        else:
            self.sheet.change_theme(theme = "light blue")
            self.update()

       
        

        # # Redraw/update the widgets if necessary
        # self.configure_styles()
        # self.update_idletasks()

    def left_side_bar_design(self):
        """
        design with customization side bar for users to switch themes and other functions
        """
        # set corner to be a litte bit in round lookings 
        self.sidebar_frame = ctk.CTkFrame(self, width=170, corner_radius=10, border_width=2)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")

        #self.log_history()
        # self.scroll_log_frame = ctk.CTkScrollableFrame(master = self.sidebar_frame, label_text="Logs", width = 200, height = 100, border_width=2, label_font=ctk.CTkFont(size=20, weight="bold"))
        # self.scroll_log_frame.grid(row=2,column=0,sticky="nsew")

        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        # change theme mode for users
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(15, 0), sticky="ew")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(20, 20), sticky="ew")

        self.sidebar_frame.grid_columnconfigure(0, weight=1)
    
    def sidebar_button_event(self):
        # some weird code here
        print("sidebar_button click")
    
    def wrap_text(self, text, max_line_length):
        """
        This function inserts newline characters to simulate text wrapping
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 > max_line_length:  # +1 for the space
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
            else:
                current_line.append(word)
                current_length += len(word) + 1
        lines.append(' '.join(current_line))  # add the last line

        return '\n'.join(lines)

    def middle_side_bar_design(self, clean, add, paper_search_data):
        # self.data = {
        #     'date published': ['2023-07-31T16:40:06Z', '2023-07-31T16:40:06Z', '2023-07-31T16:40:06Z', '2023-07-31T16:40:06Z'],
        #     'paper tile': ["Alpha-GPT: Human-AI Interactive Alpha Mining for Quantitative Investment", "Alpha-GPT: Human-AI Interactive Alpha Mining for Quantitative Investment", "Alpha-GPT: Human-AI Interactive Alpha Mining for Quantitative Investment", "Alpha-GPT: Human-AI Interactive Alpha Mining for Quantitative Investment"],
        #     'paper summary': ["One of the most important tasks in quantitative investment research is mining new alphas (effective trading signals or factors). Traditional alpha mining methods, either hand-crafted factor synthesizing or algorithmic factor mining (e.g., search with genetic programming), have inherent limitations, especially in implementing the ideas of quants. In this work, we propose a new alpha mining paradigm by introducing human-AI interaction, and a novel prompt engineering algorithmic framework to implement this paradigm by leveraging the power of large language models. Moreover, we develop Alpha-GPT, a new interactive alpha mining system framework that provides a heuristic way to ``understand'' the ideas of quant researchers and outputs creative, insightful, and effective alphas. We demonstrate the effectiveness and advantage of Alpha-GPT via a number of alpha mining experiments.", 
        #     "One of the most important tasks in quantitative investment research is mining new alphas (effective trading signals or factors). Traditional alpha mining methods, either hand-crafted factor synthesizing or algorithmic factor mining (e.g., search with genetic programming), have inherent limitations, especially in implementing the ideas of quants. In this work, we propose a new alpha mining paradigm by introducing human-AI interaction, and a novel prompt engineering algorithmic framework to implement this paradigm by leveraging the power of large language models. Moreover, we develop Alpha-GPT, a new interactive alpha mining system framework that provides a heuristic way to ``understand'' the ideas of quant researchers and outputs creative, insightful, and effective alphas. We demonstrate the effectiveness and advantage of Alpha-GPT via a number of alpha mining experiments.", 
        #     "One of the most important tasks in quantitative investment research is mining new alphas (effective trading signals or factors). Traditional alpha mining methods, either hand-crafted factor synthesizing or algorithmic factor mining (e.g., search with genetic programming), have inherent limitations, especially in implementing the ideas of quants. In this work, we propose a new alpha mining paradigm by introducing human-AI interaction, and a novel prompt engineering algorithmic framework to implement this paradigm by leveraging the power of large language models. Moreover, we develop Alpha-GPT, a new interactive alpha mining system framework that provides a heuristic way to ``understand'' the ideas of quant researchers and outputs creative, insightful, and effective alphas. We demonstrate the effectiveness and advantage of Alpha-GPT via a number of alpha mining experiments.", 
        #     "One of the most important tasks in quantitative investment research is mining new alphas (effective trading signals or factors). Traditional alpha mining methods, either hand-crafted factor synthesizing or algorithmic factor mining (e.g., search with genetic programming), have inherent limitations, especially in implementing the ideas of quants. In this work, we propose a new alpha mining paradigm by introducing human-AI interaction, and a novel prompt engineering algorithmic framework to implement this paradigm by leveraging the power of large language models. Moreover, we develop Alpha-GPT, a new interactive alpha mining system framework that provides a heuristic way to ``understand'' the ideas of quant researchers and outputs creative, insightful, and effective alphas. We demonstrate the effectiveness and advantage of Alpha-GPT via a number of alpha mining experiments."],
        #     'download link': ["http://arxiv.org/pdf/2308.00016v1", "http://arxiv.org/pdf/2308.00016v1", "http://arxiv.org/pdf/2308.00016v1", "http://arxiv.org/pdf/2308.00016v1"],
        # }

        #paper_search_data = {'date_published': ['2023-09-28T06:17:15Z', '2023-09-19T23:50:45Z', '2023-09-18T19:24:21Z', '2023-09-16T06:25:06Z', '2023-09-08T09:58:25Z', '2023-09-06T17:18:55Z', '2023-09-01T13:58:24Z', '2023-08-22T11:10:58Z', '2023-08-19T03:01:45Z', '2023-08-02T04:06:16Z'], 'paper_tile': ['Intergenerational Equity in Models of Climate Change Mitigation:\n  Stochastic Interest Rates introduce Adverse Effects, but (Non-linear) Funding\n  Costs can Improve Intergenerational Equity', 'Bell Correlations as Selection Artefacts', 'Reasoning about the Unseen for Efficient Outdoor Object Navigation', 'Charged spherically symmetric black holes in scalar-tensor Gauss-Bonnet\n  gravity', 'Interband scattering- and nematicity-induced quantum oscillation\n  frequency in FeSe', 'GPT-InvestAR: Enhancing Stock Investment Strategies through Annual\n  Report Analysis with Large Language Models', 'On the flow of perfect energy tensors', 'Transmission of optical communication signals through ring core fiber\n  using perfect vortex beams', 'Inductive-bias Learning: Generating Code Models with Large Language\n  Model', 'QUANT: A Minimalist Interval Method for Time Series Classification'], 'paper_summary': ['  Assessing the costs of climate change is essential to finding efficient pathways for the transition to a net-zero emissions economy, which is necessary to stabilise global temperatures at any level. In evaluating the benefits and costs of climate change mitigation, the discount rate converting future damages and costs into net-present values influences the timing of mitigation.   Here, we amend the DICE model with a stochastic interest rate model to consider the uncertainty of discount rates in the future. Since abatement reduces future damages, changing interest rates renders abatement investments more or less beneficial. Stochastic interest rates will hence lead to a stochastic abatement strategy.   We introduce a simple stochastic abatement model and show that this can increase intergenerational inequality concerning cost and risk.   Analysing the sensitivities of the model calibration analytically and numerically exhibits that intergenerational inequality is a consequence of the DICE model calibration (and maybe that of IAMs in general).   We then show that introducing funding of abatement costs reduces the variation of future cash-flows, which occur at different times but are off-setting in their net-present value. This effect can be interpreted as improving intergenerational effort sharing, which might be neglected in classical optimisation. This mechanism is amplified, including dependence of the interest rate risk on the amount of debt to be financed, i.e. considering the limited capacity of funding sources. As an alternative policy optimisation method, we propose limiting the total cost of damages and abatement below a fixed level relative to GDP - this modification induces equality between generations compared to their respective economic welfare, inducing early and fast mitigation of climate change to keep the total cost of climate change below 3% of global GDP. ', '  We propose an explanation of the correlations characteristic of Bell experiments, showing how they may arise as a special sort of selection artefact. This explanation accounts for the phenomena that have been taken to imply nonlocality, without recourse to any direct spacelike causality or influence. If correct, the proposal offers a novel way to reconcile nonlocality with relativity. The present paper updates an earlier version of the proposal (arXiv:2101.05370v4 [quant-ph], arXiv:2212.06986 [quant-ph]) in two main respects: (i) in demonstrating its application in a real Bell experiment; and (ii) in avoiding the need for an explicit postulate of retrocausality. ', '  Robots should exist anywhere humans do: indoors, outdoors, and even unmapped environments. In contrast, the focus of recent advancements in Object Goal Navigation(OGN) has targeted navigating in indoor environments by leveraging spatial and semantic cues that do not generalize outdoors. While these contributions provide valuable insights into indoor scenarios, the broader spectrum of real-world robotic applications often extends to outdoor settings. As we transition to the vast and complex terrains of outdoor environments, new challenges emerge. Unlike the structured layouts found indoors, outdoor environments lack clear spatial delineations and are riddled with inherent semantic ambiguities. Despite this, humans navigate with ease because we can reason about the unseen. We introduce a new task OUTDOOR, a new mechanism for Large Language Models (LLMs) to accurately hallucinate possible futures, and a new computationally aware success metric for pushing research forward in this more complex domain. Additionally, we show impressive results on both a simulated drone and physical quadruped in outdoor environments. Our agent has no premapping and our formalism outperforms naive LLM-based approaches ', '  We derive a novel class of four-dimensional black hole solutions in Gauss-Bonnet gravity coupled with a scalar field in presence of Maxwell electrodynamics. In order to derive such solutions, we assume the ansatz $ g_{tt}\\neq g_{rr}{}^{-1}$ for metric potentials. Due to the ansatz for the metric, the Reissner Nordstr\\"om gauge potential cannot be recovered because of the presence of higher-order terms ${\\cal O}\\left(\\frac{1}{r}\\right)$ which are not allowed to be vanishing. Moreover, the scalar field is not allowed to vanish. If it vanishes, a function of the solution results undefined. For this reason, the solution cannot be reduced to a Reissner Nordstr\\"om space-time in any limit. Furthermore, it is possible to show that the electric field is of higher-order in the monopole expansion: this fact explicitly comes from the contribution of the scalar field. Therefore, we can conclude that the Gauss-Bonnet scalar field acts as non-linear electrodynamics creating monopoles, quadrupoles, etc. in the metric potentials. We compute the invariants associated with the black holes and show that, when compared to Schwarzschild or Reissner-Nordstr\\"om space-times, they have a soft singularity. Also, it is possible to demonstrate that these black holes give rise to three horizons in AdS space-time and two horizons in dS space-time. Finally, thermodynamic quantities can be derived and we show that the solution can be stable or unstable depending on a critical value of the temperature. ', '  Understanding the nematic phase observed in the iron-chalcogenide materials is crucial for describing their superconducting pairing. Experiments on FeSe$_{1-x}$S$_x$ showed that one of the slow Shubnikov--de Haas quantum oscillation frequencies disappears when tuning the material out of the nematic phase via chemical substitution or pressure, which has been interpreted as a Lifshitz transition [Coldea et al., npj Quant Mater 4, 2 (2019), Reiss et al., Nat. Phys. 16, 89-94 (2020)]. Here, we present a generic, alternative scenario for a nematicity-induced sharp quantum oscillation frequency which disappears in the tetragonal phase and is not connected to an underlying Fermi surface pocket. We show that different microscopic interband scattering mechanisms - for example, orbital-selective scattering - in conjunction with nematic order can give rise to this quantum oscillation frequency beyond the standard Onsager relation. We discuss implications for iron-chalcogenides and the interpretation of quantum oscillations in other correlated materials. ', '  Annual Reports of publicly listed companies contain vital information about their financial health which can help assess the potential impact on Stock price of the firm. These reports are comprehensive in nature, going up to, and sometimes exceeding, 100 pages. Analysing these reports is cumbersome even for a single firm, let alone the whole universe of firms that exist. Over the years, financial experts have become proficient in extracting valuable information from these documents relatively quickly. However, this requires years of practice and experience. This paper aims to simplify the process of assessing Annual Reports of all the firms by leveraging the capabilities of Large Language Models (LLMs). The insights generated by the LLM are compiled in a Quant styled dataset and augmented by historical stock price data. A Machine Learning model is then trained with LLM outputs as features. The walkforward test results show promising outperformance wrt S&P500 returns. This paper intends to provide a framework for future work in this direction. To facilitate this, the code has been released as open source. ', '  The necessary and sufficient conditions are obtained for a unit time-like vector field $u$ to be the unit velocity of a divergence-free perfect fluid energy tensor. This plainly kinematic description of a conservative perfect fluid requires considering eighteen classes defined by differential concomitants of $u$. For each of these classes, we get the additional constraints that label the flow of a conservative energy tensor, and we obtain the pairs of functions $\\{\\rho,p\\}$, energy density and pressure, which complete a solution to the conservation equations. ', '  Orbital angular momentum can be used to implement high capacity data transmission systems that can be applied for classical and quantum communications. Here we experimentally study the generation and transmission properties of the so-called perfect vortex beams and the Laguerre-Gaussian beams in ring-core optical fibers. Our results show that when using a single preparation stage, the perfect vortex beams present less ring-radius variation that allows coupling of higher optical power into a ring core fiber. These results lead to lower power requirements to establish fiber-based communications links using orbital angular momentum and set the stage for future implementations of high-dimensional quantum communication over space division multiplexing fibers. ', "  Large Language Models(LLMs) have been attracting attention due to a ability called in-context learning(ICL). ICL, without updating the parameters of a LLM, it is possible to achieve highly accurate inference based on rules ``in the context'' by merely inputting a training data into the prompt. Although ICL is a developing field with many unanswered questions, LLMs themselves serves as a inference model, seemingly realizing inference without explicitly indicate ``inductive bias''. On the other hand, a code generation is also a highlighted application of LLMs. The accuracy of code generation has dramatically improved, enabling even non-engineers to generate code to perform the desired tasks by crafting appropriate prompts. In this paper, we propose a novel ``learning'' method called an ``Inductive-Bias Learning (IBL)'', which combines the techniques of ICL and code generation. An idea of IBL is straightforward. Like ICL, IBL inputs a training data into the prompt and outputs a code with a necessary structure for inference (we referred to as ``Code Model'') from a ``contextual understanding''. Despite being a seemingly simple approach, IBL encompasses both a ``property of inference without explicit inductive bias'' inherent in ICL and a ``readability and explainability'' of the code generation. Surprisingly, generated Code Models have been found to achieve predictive accuracy comparable to, and in some cases surpassing, ICL and representative machine learning models. Our IBL code is open source: https://github.com/fuyu-quant/IBLM ", "  We show that it is possible to achieve the same accuracy, on average, as the most accurate existing interval methods for time series classification on a standard set of benchmark datasets using a single type of feature (quantiles), fixed intervals, and an 'off the shelf' classifier. This distillation of interval-based approaches represents a fast and accurate method for time series classification, achieving state-of-the-art accuracy on the expanded set of 142 datasets in the UCR archive with a total compute time (training and inference) of less than 15 minutes using a single CPU core. "], 'paper_download_link': ['http://arxiv.org/pdf/2309.16186v2', 'http://arxiv.org/pdf/2309.10969v1', 'http://arxiv.org/pdf/2309.10103v1', 'http://arxiv.org/pdf/2309.08894v1', 'http://arxiv.org/pdf/2309.04237v1', 'http://arxiv.org/pdf/2309.03079v1', 'http://arxiv.org/pdf/2309.00463v2', 'http://arxiv.org/pdf/2308.11354v2', 'http://arxiv.org/pdf/2308.09890v1', 'http://arxiv.org/pdf/2308.00928v1']}
        #print(paper_search_data['date published'])

        # convert data to dictionary lists
        # paper_search_data = paper_search_data.to_dict(orient='list')
        # paper_search_data.pop('paper_fields')

        # print(paper_search_data)

        # save for future usage
        # delete all rows here
        def delete_rows():
            num_rows = self.sheet.get_total_rows(include_index = False)
            print("rows number :", num_rows)

            if (num_rows != 0):
                for i in range(num_rows):
                    # print(i)
                    self.sheet.delete_row(idx = 0, deselect_all = False, redraw = True)

        # add rows to the tksheet
        def add_rows(data):
            data.pop('paper_fields')
            rows_data = list(zip(*data.values()))
            for row in rows_data:
                self.sheet.insert_row(values=list(row))

        # save for future usage
        # if (add == 1): # check add command here
        #     add_rows(paper_search_data.to_dict(orient='list'))

        # check paper_search_data empty - clear data
        if (len(paper_search_data) == 0):
            if (clean == 1): # check clean command here
                delete_rows()
        else:
            # check theme compatible with app
            # light blue, light green, dark, dark blue and dark green
            theme_color = "light blue"
            if (self.appearance_mode_optionemenu.get() == "Dark"):
                theme_color = "dark blue"

            # Convert your data to a list of lists for tksheet
            headers = ['date_published', 'paper_tile', 'paper_summary', 'paper_download_link']
            self.data_list = [[paper_search_data[col][row] for col in headers] for row in range(len(paper_search_data['date_published']))]

            # Wrap text for each cell in data
            max_line_length = 31  # Adjust based on your desired width
            for row in self.data_list:
                for i, cell in enumerate(row):
                    row[i] = self.wrap_text(str(cell), max_line_length)  # Ensure the cell content is string

            # Create the tksheet widget within the self
            self.sheet = Sheet(self,
                               data=self.data_list,  # your data here
                               headers=headers,
                               total_rows=len(self.data_list), 
                               total_columns=len(headers),
                               show_x_scrollbar=False,
                               show_top_left=True,
                               # auto_resize_columns=True,
                               # total_columns=4,
                               empty_horizontal = 0,
                               empty_vertical =10,
                               display_selected_fg_over_highlights=True,
                               theme = theme_color
                               )

            # set up unique width for each column
            self.sheet.column_width(column = 0, width = 200, only_set_if_too_small = False, redraw = True)
            self.sheet.column_width(column = 1, width = 200, only_set_if_too_small = False, redraw = True)
            self.sheet.column_width(column = 2, width = 200, only_set_if_too_small = False, redraw = True)
            self.sheet.column_width(column = 3, width = 200, only_set_if_too_small = False, redraw = True)  

            # enable column and row resizing
            self.sheet.enable_bindings("copy", "single_select", "ctrl_click_select","select_all", "right_click_popup_menu", "rc_select", "rc_delete_row")  # enables cell editing

            # grid the sheet in the frame
            self.sheet.grid(row=0, column=1, rowspan=3, sticky="nsew")

            # auto adjust rows 
            self.sheet.set_all_row_heights(height=None)

            # for i in range(4):
            #     print(f"Width of column {i}: {self.sheet.column_width(column=i)}")

            # print("number of columns :", self.sheet.get_total_columns(include_header = False))


            #self.sheet.popup_menu_add_command("View Paper", self.new_right_click_button1_view_paper)
            self.sheet.popup_menu_add_command("Download Paper", self.new_right_click_button2_download_paper)

            self.update()
 

    # def new_right_click_button1_view_paper(self, event = None):
    #     """
    #     right click menu with view paper function
    #     """
    #     self.currently_selected = self.sheet.get_currently_selected()
    #     if self.currently_selected:
    #         row = self.currently_selected.row
    #         column = 3
    #         type_ = self.currently_selected.type_

    #         self.cell_value = self.sheet.get_cell_data(row, column)

    #         self.open_webview(self.cell_value, "View Paper " + str(row + 1))
    #     else:
    #         # show error message of turn switch on without select display until year values
    #         messagebox.showerror("Error", "No value to be found in the selected cell.")
    #         return 0    

    # def open_webview(self, link, title):
    #     """
    #     multi-thread to view papers
    #     """
    #     self.after(0, self.iconify) # minimize main screen

    #     # start webview in a new process
    #     p = Process(target=start_webview, args=(link, title))
    #     p.start()
        
    def new_right_click_button2_download_paper(self, event = None):
        """
        right click menu with download paper function
        """     
        self.currently_selected2 = self.sheet.get_currently_selected()
        if self.currently_selected2:
            row = self.currently_selected2.row
            column = 3
            type_ = self.currently_selected2.type_

            self.cell_value2 = self.sheet.get_cell_data(row, column)

            pdf_id2 = self.cell_value2.split("/")[-1]

          # ask user to select save path
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=f"{pdf_id2}.pdf")

            if file_path:  # ensure a file path was selected
                # perform downloading process
                response = requests.get(self.cell_value2, stream=True)

                if response.status_code == 200: # success
                    with open(file_path, 'wb') as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)

                    messagebox.showinfo("Success", "PDF" + pdf_id2 +"has been downloaded successfully.")
                else:
                    messagebox.showerror("Error", f"Failed to download PDF {pdf_id2}. Status code: {response.status_code}")
            else:
                messagebox.showerror("Error", "No path selected for saving the PDF" + pdf_id2 + ".")
        else:
            # Show error message if no cell is selected
            messagebox.showerror("Error", "No value to be found in the selected cell.")
            return 0

    # self.update_idletasks()



# def start_webview(link, title):
#     """
#     view papers in the current window
#     """
#     # Create a webview window
#     pdf_id = link.split("/")[-1]

#     webview.create_window(title, "http://arxiv.org/pdf/" + pdf_id)
#     webview.start()

#     #self.deiconify()
       
       

if __name__ == "__main__":
    app = App()
    app.mainloop()



















