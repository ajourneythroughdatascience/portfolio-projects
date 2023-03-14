# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 19:30:38 2023

@author: pablo

GitHub: https://github.com/pabloagn
Website: https://pabloagn.com
Contact: https://pabloagn.com/contact

Part of Portfolio Project: sentiment-analysis-in-python
"""

# --------------------------------------------------
# Import Modules
# --------------------------------------------------
import tkinter
import customtkinter
import resources
import os
import time
import warnings
warnings.filterwarnings("ignore")

# --------------------------------------------------
# Define global parameters
# --------------------------------------------------
# Inherit Light/Dark mode from system
customtkinter.set_appearance_mode("System")

# Dark-blue UI
customtkinter.set_default_color_theme("blue")



# --------------------------------------------------
# Define helpPrompt Class
# --------------------------------------------------
class helpPrompt(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Global Variables
        # --------------------------------------------------
        # Color palette
        self.text_color = '#f2f2f2'
        self.background_color = '#1a1a1a'

        # Header Font Parameters
        self.font_header_family = 'Tw Cen MT'
        self.font_header_size = 20
        self.font_header_weight = 'bold'

        # Header Font Object
        self.font_header = customtkinter.CTkFont(family=self.font_header_family,
                                                 size=self.font_header_size,
                                                 weight=self.font_header_weight)

        # Body Font Parameters
        self.font_body_family = 'Tw Cen MT'
        self.font_body_size = 16
        self.font_body_weight = 'normal'

        # Body Font Object
        self.font_body = customtkinter.CTkFont(family=self.font_body_family,
                                               size=self.font_body_size,
                                               weight=self.font_body_weight)
        
        # UI Elements - General Parameters
        # --------------------------------------------------
        self.geometry("600x300")
        self.title("Sentiment Analysis 1.0 | Help")
        self.minsize(600, 300)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.help_prompt = customtkinter.CTkTextbox(master=self,
                                                corner_radius=0,
                                                font=self.font_body)
        
        self.help_prompt.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="nsew")

        with open('dialogues/help.txt', 'r') as f:
            self.help_prompt.insert("0.0", text=f.read())

        self.help_prompt.configure(state='disabled')

        # Focus window
        self.focus()

# --------------------------------------------------
# Define aboutInfo Class
# --------------------------------------------------
class aboutInfo(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Global Variables
        # --------------------------------------------------
        # Color palette
        self.text_color = '#f2f2f2'
        self.background_color = '#1a1a1a'

        # Header Font Parameters
        self.font_header_family = 'Tw Cen MT'
        self.font_header_size = 20
        self.font_header_weight = 'bold'

        # Header Font Object
        self.font_header = customtkinter.CTkFont(family=self.font_header_family,
                                                 size=self.font_header_size,
                                                 weight=self.font_header_weight)

        # Body Font Parameters
        self.font_body_family = 'Tw Cen MT'
        self.font_body_size = 16
        self.font_body_weight = 'normal'

        # Body Font Object
        self.font_body = customtkinter.CTkFont(family=self.font_body_family,
                                               size=self.font_body_size,
                                               weight=self.font_body_weight
                                               )
        
        # Code Font Parameters
        self.font_code_family = 'Fira Code Retina'
        self.font_code_size = 14
        self.font_code_weight = 'normal'

        # Body Font Object
        self.font_code = customtkinter.CTkFont(family=self.font_code_family,
                                               size=self.font_code_size,
                                               weight=self.font_code_weight
                                               )
        
        # UI Elements - General Parameters
        # --------------------------------------------------
        self.geometry("600x300")
        self.title("Sentiment Analysis 1.0 | About")
        self.minsize(600, 300)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.about_info = customtkinter.CTkTextbox(master=self,
                                                   corner_radius=0,
                                                   font=self.font_body)
        
        self.about_info.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="nsew")

        with open('dialogues/about.txt', 'r') as f:
            self.about_info.insert("0.0", text=f.read())

        self.about_info.configure(state='disabled')

        # Focus window
        self.focus()

# --------------------------------------------------
# Define sentimentAnalysisApp Class
# --------------------------------------------------
class sentimentAnalysisApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Global Variables
        # --------------------------------------------------
        # Color palette
        self.text_color = '#f2f2f2'
        self.background_color = '#1a1a1a'
        self.text_placeholder_color = '#7f7f7f'

        # Header Font Parameters
        self.font_header_family = 'Tw Cen MT'
        self.font_header_size = 20
        self.font_header_weight = 'bold'

        # Header Font Object
        self.font_header = customtkinter.CTkFont(family=self.font_header_family,
                                                 size=self.font_header_size,
                                                 weight=self.font_header_weight)

        # Body Font Parameters
        self.font_body_family = 'Tw Cen MT'
        self.font_body_size = 16
        self.font_body_weight = 'normal'

        # Body Font Object
        self.font_body = customtkinter.CTkFont(family=self.font_body_family,
                                               size=self.font_body_size,
                                               weight=self.font_body_weight)

        # Body Placeholder Font Parameters
        self.font_body_pc_family = 'Tw Cen MT'
        self.font_body_pc_size = 16
        self.font_body_pc_weight = 'normal'
        self.slant_pc = 'italic'

        # Body Placeholder Font Object
        self.font_body_pc = customtkinter.CTkFont(family=self.font_body_pc_family,
                                                  size=self.font_body_pc_size,
                                                  weight=self.font_body_pc_weight,
                                                  slant=self.slant_pc)

        # Code Font Parameters
        self.font_code_family = 'Fira Code Retina'
        self.font_code_size = 14
        self.font_code_weight = 'normal'

        # Body Font Object
        self.font_code = customtkinter.CTkFont(family=self.font_code_family,
                                               size=self.font_code_size,
                                               weight=self.font_code_weight
                                               )

        # Toplevel window
        self.toplevel_window = None

        # Progress Bar Height
        self.progress_bar_height = 20

        # Option Box Width
        self.option_box_width = 200

        # System Settings
        # --------------------------------------------------
        self.iconbitmap('digital_assets/favicon_code_white.ico') # Define favicon
        self.geometry(f"{1416}x{768}") # Define resolution
        self.title('Pablo Aguirre | Sentiment Analysis 1.0') # Define app title

        # Printing Formatting Settings
        # --------------------------------------------------
        self.dot_sep = 25
        self.measure_title = ''
        self.value_title = ''

        # Initial Variables
        # --------------------------------------------------
        self.var_model = customtkinter.StringVar(value=resources.getParameters()['model'][0])
        self.var_analysis = customtkinter.StringVar(value=resources.getParameters()['analysis'][0])
        self.var_operation = customtkinter.StringVar(value=resources.getParameters()['input_method'][0])
        self.var_col1 = customtkinter.StringVar(value=resources.getParameters()['agg_cols'][0])
        self.var_col2 = customtkinter.StringVar(value=resources.getParameters()['agg_cols'][1])
        self.var_col3 = customtkinter.StringVar(value=resources.getParameters()['agg_cols'][2])
        self.var_col4 = customtkinter.StringVar(value=resources.getParameters()['agg_cols'][3])
        self.var_coltarget = customtkinter.StringVar(value=resources.getParameters()['text_col'])
        self.var_colid = customtkinter.StringVar(value=resources.getParameters()['target_id_col'])
        self.var_colrating = customtkinter.StringVar(value=resources.getParameters()['rating_col'])
        self.var_rdir = customtkinter.StringVar(value=resources.getParameters()['rdir'])
        self.var_wdir = customtkinter.StringVar(value=resources.getParameters()['wdir'])

        # UI Elements - Grid Layout (3x4) (3Rows, 4 Cols)
        # --------------------------------------------------
        self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((0, 2), weight=0)
        # self.grid_rowconfigure((0, 1, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # UI Elements - Sidebar with Widgets
        # --------------------------------------------------
        # Structure
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Project Title
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                 text="Sentiment Analysis 1.0",
                                                 font=self.font_header)
        
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Help Button
        self.help_prompt = customtkinter.CTkButton(self.sidebar_frame,
                                                   text="Help",
                                                   font=self.font_body,
                                                   command=self.open_help_prompt,
                                                   corner_radius=0)
        
        self.help_prompt.grid(row=1, column=0, padx=20, pady=10)

        # About Button
        self.about_prompt = customtkinter.CTkButton(self.sidebar_frame,
                                                   text="About",
                                                   font=self.font_body,
                                                   command=self.open_about_prompt,
                                                   corner_radius=0)
        
        self.about_prompt.grid(row=2, column=0, padx=20, pady=10)

        # Light / Dark Mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                            text="Appearance Mode",
                                                            anchor="w",
                                                            font=self.font_body)
        
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["System", "Light", "Dark"],
                                                                       corner_radius=0,
                                                                       command=self.change_appearance_mode_event,
                                                                       font=self.font_body,
                                                                       dropdown_font=self.font_body)
        
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 40))

        # UI Elements - Execution Parameters (Tab View) & Operation Mode (Radio Button)
        # --------------------------------------------------
        self.parameters_operation = customtkinter.CTkFrame(self)
        self.parameters_operation.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.parameters_operation.grid_columnconfigure(1, weight=1)
        self.parameters_operation.grid_rowconfigure(0, weight=1)

        # Execution Parameters (Tab View)
        self.parameters = customtkinter.CTkTabview(self.parameters_operation)
        # Illegally change tab font family (indirect method)
        self.parameters._segmented_button.configure(font=self.font_body)
        # Configure tab view grid & add tab objects
        self.parameters.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.parameters.add('Model')
        self.parameters.add('Analysis')

        # Configure grid of individual tabs
        self.parameters.tab("Model").grid_columnconfigure(0, weight=1)
        self.parameters.tab("Analysis").grid_columnconfigure(0, weight=1)

        # Tab 1 Elements
        self.model_name = customtkinter.CTkOptionMenu(self.parameters.tab("Model"),
                                                      dynamic_resizing=False,
                                                      values=resources.getParameters()['model'],
                                                      corner_radius=0,
                                                      font=self.font_body,
                                                      dropdown_font=self.font_body,
                                                      width=self.option_box_width,
                                                      variable=self.var_model
                                                      )    

        self.model_name.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Tab 2 Elements
        self.analysis_type = customtkinter.CTkOptionMenu(self.parameters.tab("Analysis"),
                                                         dynamic_resizing=False,
                                                         values=resources.getParameters()['analysis'],
                                                         corner_radius=0,
                                                         font=self.font_body,
                                                         dropdown_font=self.font_body,
                                                         width=self.option_box_width,
                                                         variable=self.var_analysis
                                                         )

        self.analysis_type.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Operation Mode
        self.operation_mode_frame = customtkinter.CTkFrame(self.parameters_operation)
        self.operation_mode_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.operation_mode_frame.grid_columnconfigure(0, weight=1)
        self.operation_mode_frame.grid_rowconfigure(2, weight=1)

        self.label_operation_mode = customtkinter.CTkLabel(master=self.operation_mode_frame,
                                                           text="Operation Mode",
                                                           font=self.font_body
                                                           )
        
        self.label_operation_mode.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Download Mode
        self.operation_mode_1 = customtkinter.CTkRadioButton(master=self.operation_mode_frame,
                                                             variable=self.var_operation,
                                                             value=resources.getParameters()['input_method'][0],
                                                             text=resources.getParameters()['input_method'][0],
                                                             font=self.font_body)
        
        # Justify North-West
        self.operation_mode_1.grid(row=1, column=0, pady=10, padx=20, sticky="nw")

        # Load Mode
        self.operation_mode_2 = customtkinter.CTkRadioButton(master=self.operation_mode_frame,
                                                           variable=self.var_operation,
                                                           value=resources.getParameters()['input_method'][1],
                                                           text=resources.getParameters()['input_method'][1],
                                                           font=self.font_body)
        # Justify North-West
        self.operation_mode_2.grid(row=2, column=0, pady=10, padx=20, sticky="nw")

        # UI Elements - Column Selector
        # --------------------------------------------------
        self.column_entry = customtkinter.CTkFrame(self)
        self.column_entry.grid(row=1, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.column_entry.grid_columnconfigure(3, weight=1)
        self.column_entry.grid_rowconfigure(2, weight=1)

        # Column Entry Title
        self.label_column_entry = customtkinter.CTkLabel(master=self.column_entry,
                                                         text="Column Selection",
                                                         font=self.font_body
                                                         )
        
        self.label_column_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Segmentation Columns
        # Row 1 - Column 1
        self.col_entry_1 = customtkinter.CTkEntry(self.column_entry,
                                                  placeholder_text="Column 1",
                                                  corner_radius=0,
                                                  font=self.font_body_pc,
                                                  placeholder_text_color=self.text_placeholder_color,
                                                  textvariable=self.var_col1
                                                  )

        self.col_entry_1.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="new")

        # Row 1 - Column 2
        self.col_entry_2 = customtkinter.CTkEntry(self.column_entry,
                                                  placeholder_text="Column 2",
                                                  corner_radius=0,
                                                  font=self.font_body_pc,
                                                  placeholder_text_color=self.text_placeholder_color,
                                                  textvariable=self.var_col2
                                                  )

        self.col_entry_2.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="new")

        # Row 1 - Column 3
        self.col_entry_3 = customtkinter.CTkEntry(self.column_entry,
                                                  placeholder_text="Column 3",
                                                  corner_radius=0,
                                                  font=self.font_body_pc,
                                                  placeholder_text_color=self.text_placeholder_color,
                                                  textvariable=self.var_col3
                                                  )

        self.col_entry_3.grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="new")

        # Row 1 - Column 4
        self.col_entry_4 = customtkinter.CTkEntry(self.column_entry,
                                                  placeholder_text="Column 4",
                                                  corner_radius=0,
                                                  font=self.font_body_pc,
                                                  placeholder_text_color=self.text_placeholder_color,
                                                  textvariable=self.var_col4
                                                  )

        self.col_entry_4.grid(row=1, column=3, padx=(10, 10), pady=(10, 10), sticky="new")

        # Target Columns
        # Target Column
        self.col_target = customtkinter.CTkEntry(self.column_entry,
                                                 placeholder_text="Target Column",
                                                 corner_radius=0,
                                                 font=self.font_body_pc,
                                                 placeholder_text_color=self.text_placeholder_color,
                                                 textvariable=self.var_coltarget
                                                 )

        self.col_target.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="new")

        # Col ID
        self.col_id = customtkinter.CTkEntry(self.column_entry,
                                             placeholder_text="ID Column",
                                             corner_radius=0,
                                             font=self.font_body_pc,
                                             placeholder_text_color=self.text_placeholder_color,
                                             textvariable=self.var_colid
                                             )

        self.col_id.grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="new")

        # Rating Column
        self.col_rating = customtkinter.CTkEntry(self.column_entry,
                                                 placeholder_text="Rating Column",
                                                 corner_radius=0,
                                                 font=self.font_body_pc,
                                                 placeholder_text_color=self.text_placeholder_color,
                                                 textvariable=self.var_colrating)

        self.col_rating.grid(row=2, column=3, padx=(10, 10), pady=(10, 10), sticky="new")

        # UI Elements - Status Box
        # --------------------------------------------------
        self.textbox_frame = customtkinter.CTkFrame(self)
        self.textbox_frame.grid(row=0,
                                column=2,
                                padx=(20, 20),
                                pady=(20, 20),
                                sticky="nsew")
        
        self.textbox_frame.grid_columnconfigure(0, weight=1)
        self.textbox_frame.grid_rowconfigure(0, weight=1)

        self.textlog = customtkinter.CTkTextbox(self.textbox_frame,
                                                width=450,
                                                wrap='word',
                                                font=self.font_code
                                                )
        
        self.textlog.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # UI Elements - Progress Bars
        # --------------------------------------------------
        self.progress_frame = customtkinter.CTkFrame(self)
        self.progress_frame.grid(row=1, column=2, rowspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid_rowconfigure(5, weight=1)

        # Progress Load or Download
        self.progressbar_1_tag =  customtkinter.CTkLabel(master=self.progress_frame,
                                                         text="Download/Load Progress",
                                                         font=self.font_body
                                                         )

        self.progressbar_1_tag.grid(row=0, column=0, padx=10, pady=10, sticky="new")

        self.progressbar_1 = customtkinter.CTkProgressBar(self.progress_frame,
                                                          mode='determinate',
                                                          height=self.progress_bar_height,
                                                          corner_radius=0)
        
        self.progressbar_1.grid(row=1, column=0, padx=(20, 20), pady=(10, 10), sticky="new")
        # Set to 0, since by default, it will be set to 0.5
        self.progressbar_1.set(0)

        # Progress Run Model
        self.progressbar_2_tag =  customtkinter.CTkLabel(master=self.progress_frame,
                                                         text="Model Execution Progress",
                                                         font=self.font_body
                                                         )

        self.progressbar_2_tag.grid(row=2, column=0, padx=10, pady=10, sticky="new")

        self.progressbar_2 = customtkinter.CTkProgressBar(self.progress_frame,
                                                          mode='determinate',
                                                          height=self.progress_bar_height,
                                                          corner_radius=0)
        
        self.progressbar_2.grid(row=3, column=0, padx=(20, 20), pady=(10, 10), sticky="new")
        # Set to 0, since by default, it will be set to 0.5
        self.progressbar_2.set(0)

        # Progress Generate Analysis
        self.progressbar_3_tag =  customtkinter.CTkLabel(master=self.progress_frame,
                                                         text="Analysis Progress",
                                                         font=self.font_body
                                                         )

        self.progressbar_3_tag.grid(row=4, column=0, padx=10, pady=10, sticky="new")

        self.progressbar_3 = customtkinter.CTkProgressBar(self.progress_frame,
                                                          mode='determinate',
                                                          height=self.progress_bar_height,
                                                          corner_radius=0)
        
        self.progressbar_3.grid(row=5, column=0, padx=(20, 20), pady=(10, 10), sticky="new")
        # Set to 0, since by default, it will be set to 0.5
        self.progressbar_3.set(0)

        # UI Elements - Path Specification
        # --------------------------------------------------
        # Absolute Source Path Specification
        self.path_entry = customtkinter.CTkFrame(self)
        self.path_entry.grid(row=2, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.path_entry.grid_columnconfigure(1, weight=1)
        self.path_entry.grid_rowconfigure(2, weight=1)

        # Column Entry Title
        self.label_column_entry = customtkinter.CTkLabel(master=self.path_entry,
                                                          text="Path Selection",
                                                          font=self.font_body
                                                          )
        
        self.label_column_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="")


        self.entry = customtkinter.CTkEntry(self.path_entry,
                                            placeholder_text="Database Absolute Path",
                                            corner_radius=0,
                                            font=self.font_body_pc,
                                            placeholder_text_color=self.text_placeholder_color,
                                            textvariable=self.var_rdir
                                            )

        self.entry.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Absolute Output Path Specification
        self.entry = customtkinter.CTkEntry(self.path_entry,
                                            placeholder_text="Output Path",
                                            corner_radius=0,
                                            font=self.font_body_pc,
                                            placeholder_text_color=self.text_placeholder_color,
                                            textvariable=self.var_wdir
                                            )

        self.entry.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # UI Elements - Run Button
        # --------------------------------------------------
        self.main_button_1 = customtkinter.CTkButton(master=self.path_entry,
                                                     text='Run Model',
                                                     fg_color="transparent",
                                                     border_width=1,
                                                     font=self.font_body,
                                                     text_color=("gray10", self.text_color),
                                                     corner_radius = 0,
                                                     command=self.runModel)
        
        self.main_button_1.grid(row=2, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
    # UI Elements - Events
    # --------------------------------------------------

    # Open help toplevel_window
    def open_help_prompt(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = helpPrompt(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
    
    # Open about toplevel_window
    def open_about_prompt(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = aboutInfo(self) # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)



    # Run Model
    def runModel(self):

        # Function to print padded strings
        def padStr(self, measure_title, value_title):
            measure_title += ' '
            self.padded_str = measure_title + '.'*(self.dot_sep - len(measure_title))
            self.padded_str = ('%s %s' % ( self.padded_str, value_title))
            return self.padded_str

        # Create initial input exception handling
        if self.var_col1.get() == '':
            # Unlock textbox
            self.textlog.configure(state="normal")
            # Clear textlog from line 0 character 0 to end
            self.textlog.delete("0.0", "end")
            # Insert log at end
            self.textlog.insert("end", "PLEASE SELECT AT LEAST ONE AGGREGATION COLUMN IN COL1")
            # Lock textbox
            self.textlog.configure(state="disabled")
        elif self.var_coltarget.get() == '':
            self.textlog.configure(state="normal")
            self.textlog.delete("0.0", "end")
            self.textlog.insert("end", "PLEASE SELECT A TARGET COLUMN TO ANALYZE")
            self.textlog.configure(state="disabled")
        elif self.var_colid.get() == '':
            self.textlog.configure(state="normal")
            self.textlog.delete("0.0", "end")
            self.textlog.insert("end", "PLEASE SELECT AN ID COLUMN")
            self.textlog.configure(state="disabled")
        elif self.var_rdir.get() == '':
            self.textlog.configure(state="normal")
            self.textlog.delete("0.0", "end")
            self.textlog.insert("end", "PLEASE SELECT AN INPUT DIRECTORY")
            self.textlog.configure(state="disabled")
            print('PLEASE SELECT AN INPUT DIRECTORY')
        elif self.var_wdir.get() == '':
            self.textlog.configure(state="normal")
            self.textlog.delete("0.0", "end")
            self.textlog.insert("end", "PLEASE SELECT AN OUTPUT DIRECTORY")
            self.textlog.configure(state="disabled")
        else:
            self.textlog.configure(state="normal")
            self.textlog.delete("0.0", "end")

            textvar_confirm = padStr(self, 'CONFIRMING VARIABLES', '')
            textvar_model = padStr(self, 'MODEL:', self.var_model.get())
            textvar_analysis = padStr(self, 'ANALYSIS:', self.var_analysis.get())
            textvar_operation = padStr(self, 'OPERATION:', self.var_operation.get())
            textvar_col1 = padStr(self, 'COL1:', self.var_col1.get())
            textvar_col2 = padStr(self, 'COL2:', self.var_col2.get())
            textvar_col3 = padStr(self, 'COL3:', self.var_col3.get())
            textvar_col4 = padStr(self, 'COL4:', self.var_col4.get())
            textvar_coltarget = padStr(self, 'TARGET:', self.var_coltarget.get())
            textvar_colid = padStr(self, 'ID:', self.var_colid.get())
            textvar_colrating = padStr(self, 'RATING:', self.var_colrating.get())
            textvar_rdir = padStr(self, 'INPUT DIR:', self.var_rdir.get())
            textvar_wdir = padStr(self, 'OUTPUT DIR:', self.var_wdir.get())
            textvar_start = padStr(self, 'STARTING ANALYSIS IN', '5s')
            textvar_stop = padStr(self, 'CONCLUDED ANALYSIS', '')

            self.textlog.insert("end", f"{textvar_confirm}\n\n")
            self.textlog.insert("end", f"{textvar_model}\n")
            self.textlog.insert("end", f"{textvar_analysis}\n")
            self.textlog.insert("end", f"{textvar_operation}\n")
            self.textlog.insert("end", f"{textvar_col1}\n")
            self.textlog.insert("end", f"{textvar_col2}\n")
            self.textlog.insert("end", f"{textvar_col3}\n")
            self.textlog.insert("end", f"{textvar_col4}\n")
            self.textlog.insert("end", f"{textvar_coltarget}\n")
            self.textlog.insert("end", f"{textvar_colid}\n")
            self.textlog.insert("end", f"{textvar_colrating}\n")
            self.textlog.insert("end", f"{textvar_rdir}\n")
            self.textlog.insert("end", f"{textvar_wdir}\n\n")
            self.textlog.insert("end", f"{textvar_start}\n\n")

            self.textlog.configure(state="disabled")
            self.update_idletasks()
            time.sleep(5)
            self.textlog.configure(state="normal")

            # Start analysis
            n = 5000
            iter_step = 1/n
            progress_step = iter_step
            self.textlog.insert("0.0", "\n")
            self.progressbar_1.start()
            for i in range(n):
                self.progressbar_1.set(progress_step)
                textvar_progress = padStr(self, 'ENTRY', round(progress_step, 4))
                self.textlog.insert("0.0", f"{textvar_progress}\n")
                progress_step += iter_step
                self.update_idletasks()
            self.progressbar_1.stop()

            # Conclude analysis
            self.textlog.insert("0.0", "\n")
            self.textlog.insert("end", f"{textvar_stop}\n\n")

            # Disable textlog
            self.textlog.configure(state="disabled")

        # # Define the target dataset
        # target_dataset = resources.getParameters()['dataset']
        # rdir = resources.getParameters()['rdir']

        # for target in target_dataset:
        #     # Create target path
        #     dataset = os.path.join(rdir, target)
        #     # Perform Sentiment Analysis
        #     df = resources.runSentimentModel(dataset)

        return None

# Call main function
if __name__ == '__main__':
    app = sentimentAnalysisApp()
    app.mainloop()