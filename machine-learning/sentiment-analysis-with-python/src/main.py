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
import warnings
warnings.filterwarnings("ignore")

# --------------------------------------------------
# Define global parameters
# --------------------------------------------------
# Inherit Light/Dark mode from system
customtkinter.set_appearance_mode("System")

# Dark-blue UI
customtkinter.set_default_color_theme("dark-blue")



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
                                               weight=self.font_body_weight)
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
        
        # Toplevel window
        self.toplevel_window = None

        # System Settings
        # --------------------------------------------------
        self.iconbitmap('digital_assets/favicon_code_white.ico') # Define favicon
        self.geometry(f"{1366}x{768}") # Define resolution
        self.title('Pablo Aguirre | Sentiment Analysis 1.0') # Define app title

        # UI Elements - Grid Layout (4x4)
        # --------------------------------------------------
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 1), weight=1)

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
                                                   command=self.open_help_prompt)
        
        self.help_prompt.grid(row=1, column=0, padx=20, pady=10)

        # About Button
        self.about_prompt = customtkinter.CTkButton(self.sidebar_frame,
                                                   text="About",
                                                   font=self.font_body,
                                                   command=self.open_about_prompt)
        
        self.about_prompt.grid(row=2, column=0, padx=20, pady=10)

        # Light / Dark Mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                            text="Appearance Mode",
                                                            anchor="w",
                                                            font=self.font_body)
        
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["System", "Light", "Dark"],
                                                                       corner_radius=0,
                                                                       command=self.change_appearance_mode_event,
                                                                       font=self.font_body,
                                                                       dropdown_font=self.font_body)
        
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                    text="UI Scaling",
                                                    anchor="w",
                                                    font=self.font_body)
        
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               corner_radius=0,
                                                               command=self.change_scaling_event,
                                                               font=self.font_body,
                                                               dropdown_font=self.font_body)
        
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # UI Elements - Text Box
        # --------------------------------------------------
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # UI Elements - Tab View
        # --------------------------------------------------
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # UI Elements - Radio Button
        # --------------------------------------------------
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # # UI Elements - Model Selector (VADER, RoBERTa)
        # # --------------------------------------------------
        # model_prompt = customtkinter.CTkLabel(self, text='Select a Model')
        # model_prompt_var = customtkinter.StringVar(value=resources.getParameters()['model'][0]) # Set initial value

        # def model_prompt_callback(model_choice):
        #     print(model_choice)
        #     return None

        # combobox = customtkinter.CTkOptionMenu(master=self,
        #                                        values=resources.getParameters()['model'],
        #                                        command=model_prompt_callback,
        #                                        variable=model_prompt_var)

        # # UI Elements - Mode Selector (Download / Run on Existing File)
        # # --------------------------------------------------
        # mode_prompt = customtkinter.CTkLabel(self, text='Select a Mode')
        # mode_prompt_var = customtkinter.StringVar(value=resources.getParameters()['input_method'][0]) # Set initial value

        # def mode_prompt_callback(mode_choice):
        #     print(mode_choice)
        #     return None

        # combobox = customtkinter.CTkOptionMenu(master=self,
        #                             values=resources.getParameters()['input_method'],
        #                             command=mode_prompt_callback,
        #                             variable=mode_prompt_var)

        # UI Elements - Absolute Source Path Specification
        # --------------------------------------------------
        self.entry = customtkinter.CTkEntry(self,
                                            placeholder_text="Database Absolute Path",
                                            corner_radius=0,
                                            font=self.font_body_pc,
                                            placeholder_text_color=self.text_placeholder_color)

        self.entry.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # UI Elements - Absolute Output Path Specification
        # --------------------------------------------------
        self.entry = customtkinter.CTkEntry(self,
                                            placeholder_text="Output Path",
                                            corner_radius=0,
                                            font=self.font_body_pc,
                                            placeholder_text_color=self.text_placeholder_color)

        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # UI Elements - Run Button
        # --------------------------------------------------
        self.main_button_1 = customtkinter.CTkButton(master=self,
                                                     text='Run Model',
                                                     fg_color="transparent",
                                                     border_width=1,
                                                     font=self.font_body,
                                                     text_color=("gray10", self.text_color),
                                                     corner_radius = 0,
                                                     command=self.button_event)
        
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
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

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def button_event(self):
        print('Run Model')

    def runModel(self):
        # Define the target dataset
        target_dataset = resources.getParameters()['dataset']
        rdir = resources.getParameters()['rdir']

        for target in target_dataset:
            # Create target path
            dataset = os.path.join(rdir, target)
            # Perform Sentiment Analysis
            df = resources.runSentimentModel(dataset)

        return None
        # return df

# Call main function
if __name__ == '__main__':
    app = sentimentAnalysisApp()
    app.mainloop()