"""
Created on Thu Mar  2 19:30:38 2023

@author: Pablo Aguirre

GitHub: https://github.com/pabloagn
Website: https://pabloagn.com
Contact: https://pabloagn.com/contact

Part of Portfolio Project: sentiment-analysis-in-python
"""

# Third-party packages
import customtkinter
import matplotlib
import matplotlib.pyplot as plt
import tkinter

# Built-in packages
import os
import shutil
import time
import warnings
warnings.filterwarnings("ignore")

# Internal packages
import utils
import sentiment_analysis

# Global parameters class
class SetGlobalParams(utils.GetParameters):
    '''
    DOT (Data Transfer Object) Class:
    - Set global parameters for all ctinker objects.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set project path
        self.project_path = os.path.dirname(os.getcwd())

        # Get global config
        self.config_interface = self.getConfig()['interface']
        self.config_fonts = self.getConfig()['fonts']

        # Config interface
        self.color_theme = self.config_interface['color_theme']
        self.front_color = self.config_interface['front_color']
        self.background_color = self.config_interface['background_color']
        self.geometry_width = self.config_interface['geometry_width']
        self.geometry_height = self.config_interface['geometry_height']
        self.dot_sep = self.config_interface['dot_sep']
        self.radius = self.config_interface['radius']

        # Config fonts
        self.text_color = self.config_fonts['text_color']
        self.text_placeholder_color = self.config_fonts['text_placeholder_color']
        self.font_header_family = self.config_fonts['font_header_family']
        self.font_header_size = self.config_fonts['font_header_size']
        self.font_header_weight = self.config_fonts['font_header_weight']
        self.font_body_family = self.config_fonts['font_body_family']
        self.font_body_size = self.config_fonts['font_body_size']
        self.font_body_weight = self.config_fonts['font_body_weight']
        self.font_body_pc_family = self.config_fonts['font_body_pc_family']
        self.font_body_pc_size = self.config_fonts['font_body_pc_size']
        self.font_body_pc_weight = self.config_fonts['font_body_pc_weight']
        self.font_body_pc_style = self.config_fonts['font_body_pc_style']
        self.font_code_family = self.config_fonts['font_code_family']
        self.font_code_size = self.config_fonts['font_code_size']
        self.font_code_weight = self.config_fonts['font_code_weight']

        # Set global parameters
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme(self.color_theme)

        # Set font parameters
        self.font_header = customtkinter.CTkFont(family=self.font_header_family,
                                                 size=self.font_header_size,
                                                 weight=self.font_header_weight)

        self.font_body = customtkinter.CTkFont(family=self.font_body_family,
                                               size=self.font_body_size,
                                               weight=self.font_body_weight)

        self.font_body_pc = customtkinter.CTkFont(family=self.font_body_pc_family,
                                                  size=self.font_body_pc_size,
                                                  weight=self.font_body_pc_weight,
                                                  slant=self.font_body_pc_style)

        self.font_code = customtkinter.CTkFont(family=self.font_code_family,
                                               size=self.font_code_size,
                                               weight=self.font_code_weight
                                               )
        
        # Set global params for other classes
        self.threshold_top = 0.70
        self.threshold_bottom = -0.70

        # Define plot parameters
        # Remove cache in order to set font attributes successfully
        try:
            shutil.rmtree(matplotlib.get_cachedir())
        except FileNotFoundError:
            pass

        plt.style.use('ggplot')
        self.color_main = '#1a1a1a'
        self.text_padding = 18
        self.title_font_size = 17
        self.label_font_size = 14
        self.subptitle_y = 0.98

# Help prompt class
class HelpPrompt(SetGlobalParams,
                 customtkinter.CTkToplevel):
    '''
    HelpPrompt class:
        - Display Help prompt when required.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # UI Elements - General Parameters
        # --------------------------------------------------
        self.geometry("600x300")
        self.title("Sentiment Analysis 1.0 | Help")
        self.minsize(600, 300)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.help_prompt = customtkinter.CTkTextbox(master=self,
                                                    corner_radius=self.radius,
                                                    font=self.font_body
                                                    )
        
        self.help_prompt.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="nsew")

        with open(os.path.join(self.project_path, 'src', 'application', 'dialogues', 'help.txt'), 'r') as f:
            self.help_prompt.insert("0.0", text=f.read())

        self.help_prompt.configure(state='disabled')

        # Focus window
        self.focus()

# About prompt class
class AboutPrompt(SetGlobalParams,
                  customtkinter.CTkToplevel):
    '''
    AboutPrompt class:
        - Display About prompt when required.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # UI Elements - General Parameters
        # --------------------------------------------------
        self.geometry("600x300")
        self.title("Sentiment Analysis 1.0 | About")
        self.minsize(600, 300)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.about_info = customtkinter.CTkTextbox(master=self,
                                                   corner_radius=self.radius,
                                                   font=self.font_body)
        
        self.about_info.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="nsew")
        with open(os.path.join(self.project_path, 'src', 'application', 'dialogues', 'about.txt'), 'r') as f:
            self.about_info.insert("0.0", text = f.read())

        self.about_info.configure(state='disabled')

        # Focus window
        self.focus()

# Main application class
class MainApplication(SetGlobalParams,
                      customtkinter.CTk,
                      sentiment_analysis.SentimentAnalysis):
    '''
    MainApplication class:
        - Main GUI for SentimentAnalysis Application
    '''
    def __init__(self):
        super().__init__()

        # Local params
        self.toplevel_window = None
        self.progress_bar_height = 20
        self.option_box_width = 200

        # Printing Formatting Settings
        self.measure_title = ''
        self.value_title = ''
        self.print_position = '0.0'

        # Initial Variables - User-modifiable
        self.params_directories = self.getParams()['directories']
        self.config_operation = self.getParams()['operation']
        self.params_columns = self.getParams()['columns']

        self.var_rdir = tkinter.StringVar(value=self.params_directories['rdir'])
        self.var_wdir =  tkinter.StringVar(value=self.params_directories['wdir'])
        self.var_source_url = tkinter.StringVar(value=self.params_directories['sourceurl'])

        self.var_operation = tkinter.StringVar(value=self.config_operation['input_method'][0])
        self.var_model =  tkinter.StringVar(value=self.config_operation['model'][0])
        self.var_analysis = tkinter.StringVar(value=self.config_operation['analysis'][0])
        self.var_chart_transparency = tkinter.StringVar(value=self.config_operation['chart_background'][0])
        self.var_plot_colorscheme = tkinter.StringVar(value=self.config_operation['plot_color_scheme'][0])
        self.var_wait_time = tkinter.StringVar(value=self.config_operation['wait_time'][2])
        self.var_top_words = tkinter.StringVar(value=self.config_operation['top_words'][2])
        self.var_nltk_threshold = tkinter.DoubleVar(value=self.config_operation['nltk_threshold'][6])

        self.var_target_id_col = tkinter.StringVar(value=self.params_columns['target_id_col'])
        self.var_col1 = tkinter.StringVar(value=self.params_columns['agg_cols'][0])
        self.var_col2 = tkinter.StringVar(value=self.params_columns['agg_cols'][1])
        self.var_col3 = tkinter.StringVar(value=self.params_columns['agg_cols'][2])
        self.var_col4 = tkinter.StringVar(value=self.params_columns['agg_cols'][3])
        self.var_rating_col = tkinter.StringVar(value=self.params_columns['rating_col'])
        self.var_target_col = tkinter.StringVar(value=self.params_columns['target_col'])

        # Initial Variables - Non-user-modifiable
        self.var_sourceurl = tkinter.StringVar(value=self.params_directories['sourceurl'])

        # Window settings
        self.iconbitmap('digital_assets/favicon_code_white.ico')
        self.geometry(f"{self.geometry_width}x{self.geometry_height}")
        self.title('Pablo Aguirre | Sentiment Analysis 1.0')

        # UI Elements - Grid Layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # UI Elements - Sidebar with Widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=self.radius)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                 text="Sentiment Analysis 1.0",
                                                 font=self.font_header)
        
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.help_prompt = customtkinter.CTkButton(self.sidebar_frame,
                                                   text="Help",
                                                   font=self.font_body,
                                                   command=self.openHelpPrompt,
                                                   corner_radius=self.radius)
        
        self.help_prompt.grid(row=1, column=0, padx=20, pady=10)

        self.about_prompt = customtkinter.CTkButton(self.sidebar_frame,
                                                   text="About",
                                                   font=self.font_body,
                                                   command=self.openAboutPrompt,
                                                   corner_radius=self.radius)
        
        self.about_prompt.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                            text="Appearance Mode",
                                                            anchor="w",
                                                            font=self.font_body)
        
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                        values=["System", "Light", "Dark"],
                                                                        corner_radius=self.radius,
                                                                        command=self.changeAppearanceMode,
                                                                        font=self.font_body,
                                                                        dropdown_font=self.font_body)

        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 40))

        # UI Elements - Execution Parameters (Tab View) & Operation Mode (Option Menus)
        self.parameters_operation = customtkinter.CTkFrame(self)
        self.parameters_operation.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.parameters_operation.grid_columnconfigure(1, weight=1)
        self.parameters_operation.grid_rowconfigure(0, weight=1)

        self.parameters = customtkinter.CTkTabview(self.parameters_operation)
        self.parameters._segmented_button.configure(font=self.font_body)
        self.parameters.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.parameters.add('Model')
        self.parameters.add('Analysis')
        self.parameters.add('Advanced')
        self.parameters.tab("Model").grid_columnconfigure(0, weight=1)
        self.parameters.tab("Analysis").grid_columnconfigure(0, weight=1)
        self.parameters.tab("Advanced").grid_columnconfigure(0, weight=1)

        # Model Tab
        self.label_model_name = customtkinter.CTkLabel(master=self.parameters.tab("Model"),
                                                       text="NLP Model",
                                                       font=self.font_body
                                                       )
        
        self.label_model_name.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.model_name = customtkinter.CTkOptionMenu(self.parameters.tab("Model"),
                                                        dynamic_resizing=False,
                                                        values=self.getParams()['operation']['model'],
                                                        corner_radius=self.radius,
                                                        font=self.font_body,
                                                        dropdown_font=self.font_body,
                                                        width=self.option_box_width,
                                                        variable=self.var_model
                                                        )

        self.model_name.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Analysis Tab
        self.label_analysis_type = customtkinter.CTkLabel(master=self.parameters.tab("Analysis"),
                                                          text="Analysis Type",
                                                          font=self.font_body
                                                          )
        
        self.label_analysis_type.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.analysis_type = customtkinter.CTkOptionMenu(self.parameters.tab("Analysis"),
                                                         dynamic_resizing=False,
                                                         values=self.getParams()['operation']['analysis'],
                                                         corner_radius=self.radius,
                                                         font=self.font_body,
                                                         dropdown_font=self.font_body,
                                                         width=self.option_box_width,
                                                         variable=self.var_analysis
                                                         )

        self.analysis_type.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.label_chart_transparency = customtkinter.CTkLabel(master=self.parameters.tab("Analysis"),
                                                               text="Chart Background",
                                                               font=self.font_body
                                                               )
        
        self.label_chart_transparency.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")


        self.chart_transparency = customtkinter.CTkOptionMenu(self.parameters.tab("Analysis"),
                                                              dynamic_resizing=False,
                                                              values=self.getParams()['operation']['chart_background'],
                                                              corner_radius=self.radius,
                                                              font=self.font_body,
                                                              dropdown_font=self.font_body,
                                                              width=self.option_box_width,
                                                              variable=self.var_chart_transparency
                                                             )

        self.chart_transparency.grid(row=3, column=0, padx=20, pady=(10, 10))

        self.label_plot_colors = customtkinter.CTkLabel(master=self.parameters.tab("Analysis"),
                                                        text="Plot Color Scheme",
                                                        font=self.font_body
                                                        )
        
        self.label_plot_colors.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")


        self.plot_colors = customtkinter.CTkOptionMenu(self.parameters.tab("Analysis"),
                                                              dynamic_resizing=False,
                                                              values=self.getParams()['operation']['plot_color_scheme'],
                                                              corner_radius=self.radius,
                                                              font=self.font_body,
                                                              dropdown_font=self.font_body,
                                                              width=self.option_box_width,
                                                              variable=self.var_plot_colorscheme
                                                             )

        self.plot_colors.grid(row=5, column=0, padx=20, pady=(10, 10))

        # Operation Mode
        self.operation_mode_frame = customtkinter.CTkFrame(self.parameters_operation)
        self.operation_mode_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.operation_mode_frame.grid_columnconfigure(0, weight=1)
        self.operation_mode_frame.grid_rowconfigure(5, weight=1)

        self.label_operation_params = customtkinter.CTkLabel(master=self.operation_mode_frame,
                                                             text="Operation Parameters",
                                                             font=self.font_body
                                                             )
        
        self.label_operation_params.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


        self.label_operation_mode = customtkinter.CTkLabel(master=self.operation_mode_frame,
                                                           text="Operation Mode",
                                                           font=self.font_body
                                                           )
        
        self.label_operation_mode.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.operation_mode = customtkinter.CTkOptionMenu(master=self.operation_mode_frame,
                                                          dynamic_resizing=False,
                                                          values=self.getParams()['operation']['input_method'],
                                                          corner_radius=self.radius,
                                                          font=self.font_body,
                                                          dropdown_font=self.font_body,
                                                          width=self.option_box_width,
                                                          variable=self.var_operation
                                                          )

        self.operation_mode.grid(row=2, column=0, padx=20, pady=(10, 10))

        # Operation Time
        self.label_operation_time = customtkinter.CTkLabel(master=self.operation_mode_frame,
                                                    text="Operation Time [s]",
                                                    font=self.font_body
                                                    )
        
        self.label_operation_time.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")


        self.operation_time = customtkinter.CTkOptionMenu(master=self.operation_mode_frame,
                                                          dynamic_resizing=False,
                                                          values=self.getParams()['operation']['wait_time'],
                                                          corner_radius=self.radius,
                                                          font=self.font_body,
                                                          dropdown_font=self.font_body,
                                                          width=self.option_box_width,
                                                          variable=self.var_wait_time
                                                          )

        self.operation_time.grid(row=4, column=0, padx=20, pady=(10, 10))

       # Advanced Tab
        self.label_top_words = customtkinter.CTkLabel(master=self.parameters.tab("Advanced"),
                                                       text="Top N Words",
                                                       font=self.font_body
                                                       )
        
        self.label_top_words.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.top_words = customtkinter.CTkOptionMenu(self.parameters.tab("Advanced"),
                                                      dynamic_resizing=False,
                                                      values=self.getParams()['operation']['top_words'],
                                                      corner_radius=self.radius,
                                                      font=self.font_body,
                                                      dropdown_font=self.font_body,
                                                      width=self.option_box_width,
                                                      variable=self.var_top_words
                                                      )

        self.top_words.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.label_nltk_threshold = customtkinter.CTkLabel(master=self.parameters.tab("Advanced"),
                                                           text="NLTK Analysis Threshold",
                                                           font=self.font_body
                                                           )
        
        self.label_nltk_threshold.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.nltk_threshold = customtkinter.CTkSlider(master=self.parameters.tab("Advanced"),
                                                      from_=0,
                                                      to=1,
                                                      variable = self.var_nltk_threshold,
                                                      command = self.returnThresholdVal
                                                      )

        self.nltk_threshold.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        # UI Elements - Column Selector
        self.column_entry = customtkinter.CTkFrame(self)
        self.column_entry.grid(row=1, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.column_entry.grid_columnconfigure(3, weight=1)
        self.column_entry.grid_rowconfigure(2, weight=1)

        self.label_column_entry = customtkinter.CTkLabel(master=self.column_entry,
                                                         text="Column Selection",
                                                         font=self.font_body
                                                         )
        
        self.label_column_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.col_entry_1 = customtkinter.CTkEntry(self.column_entry,
                                                  placeholder_text="Column 1",
                                                  corner_radius=self.radius,
                                                  font=self.font_body_pc,
                                                  placeholder_text_color=self.text_placeholder_color,
                                                  textvariable=self.var_col1
                                                  )

        self.col_entry_1.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="new")

        self.col_entry_2 = customtkinter.CTkEntry(self.column_entry,
                                                  placeholder_text="Column 2",
                                                  corner_radius=self.radius,
                                                  font=self.font_body_pc,
                                                  placeholder_text_color=self.text_placeholder_color,
                                                  textvariable=self.var_col2
                                                  )

        self.col_entry_2.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="new")

        self.col_entry_3 = customtkinter.CTkEntry(self.column_entry,
                                                  placeholder_text="Column 3",
                                                  corner_radius=self.radius,
                                                  font=self.font_body_pc,
                                                  placeholder_text_color=self.text_placeholder_color,
                                                  textvariable=self.var_col3
                                                  )

        self.col_entry_3.grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="new")

        self.col_entry_4 = customtkinter.CTkEntry(self.column_entry,
                                                  placeholder_text="Column 4",
                                                  corner_radius=self.radius,
                                                  font=self.font_body_pc,
                                                  placeholder_text_color=self.text_placeholder_color,
                                                  textvariable=self.var_col4
                                                  )

        self.col_entry_4.grid(row=1, column=3, padx=(10, 10), pady=(10, 10), sticky="new")

        self.col_target = customtkinter.CTkEntry(self.column_entry,
                                                 placeholder_text="Target Column",
                                                 corner_radius=self.radius,
                                                 font=self.font_body_pc,
                                                 placeholder_text_color=self.text_placeholder_color,
                                                 textvariable=self.var_target_col
                                                 )

        self.col_target.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="new")

        self.col_id = customtkinter.CTkEntry(self.column_entry,
                                             placeholder_text="ID Column",
                                             corner_radius=self.radius,
                                             font=self.font_body_pc,
                                             placeholder_text_color=self.text_placeholder_color,
                                             textvariable=self.var_target_id_col
                                             )

        self.col_id.grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="new")

        self.col_rating = customtkinter.CTkEntry(self.column_entry,
                                                 placeholder_text="Rating Column",
                                                 corner_radius=self.radius,
                                                 font=self.font_body_pc,
                                                 placeholder_text_color=self.text_placeholder_color,
                                                 textvariable=self.var_rating_col
                                                 )

        self.col_rating.grid(row=2, column=3, padx=(10, 10), pady=(10, 10), sticky="new")

        # UI Elements - Status Box
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
        self.progress_frame = customtkinter.CTkFrame(self)
        self.progress_frame.grid(row=1, column=2, rowspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid_rowconfigure(5, weight=1)

        self.progressbar_1_tag =  customtkinter.CTkLabel(master=self.progress_frame,
                                                         text="Download/Load Progress",
                                                         font=self.font_body
                                                         )

        self.progressbar_1_tag.grid(row=0, column=0, padx=10, pady=10, sticky="new")

        self.progressbar_1 = customtkinter.CTkProgressBar(self.progress_frame,
                                                            mode='determinate',
                                                            height=self.progress_bar_height,
                                                            corner_radius=self.radius)

        self.progressbar_1.grid(row=1, column=0, padx=(20, 20), pady=(10, 10), sticky="new")
        self.progressbar_1.set(0) # Set to 0, since by default, it will be set to 0.5

        self.progressbar_2_tag =  customtkinter.CTkLabel(master=self.progress_frame,
                                                         text="Model Execution Progress",
                                                         font=self.font_body
                                                         )

        self.progressbar_2_tag.grid(row=2, column=0, padx=10, pady=10, sticky="new")

        self.progressbar_2 = customtkinter.CTkProgressBar(self.progress_frame,
                                                          mode='determinate',
                                                          height=self.progress_bar_height,
                                                          corner_radius=self.radius)
        
        self.progressbar_2.grid(row=3, column=0, padx=(20, 20), pady=(10, 10), sticky="new")
        self.progressbar_2.set(0) # Set to 0, since by default, it will be set to 0.5

        # Progress Generate Analysis
        self.progressbar_3_tag =  customtkinter.CTkLabel(master=self.progress_frame,
                                                         text="Analysis Progress",
                                                         font=self.font_body
                                                         )

        self.progressbar_3_tag.grid(row=4, column=0, padx=10, pady=10, sticky="new")

        self.progressbar_3 = customtkinter.CTkProgressBar(self.progress_frame,
                                                          mode='determinate',
                                                          height=self.progress_bar_height,
                                                          corner_radius=self.radius)
        
        self.progressbar_3.grid(row=5, column=0, padx=(20, 20), pady=(10, 10), sticky="new")
        self.progressbar_3.set(0) # Set to 0, since by default, it will be set to 0.5

        # UI Elements - Path Specification
        self.path_entry = customtkinter.CTkFrame(self)
        self.path_entry.grid(row=2, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.path_entry.grid_columnconfigure(1, weight=1)
        self.path_entry.grid_rowconfigure(2, weight=1)

        self.label_column_entry = customtkinter.CTkLabel(master=self.path_entry,
                                                         text="Path Selection",
                                                         font=self.font_body
                                                         )
        
        self.label_column_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="")


        self.entry = customtkinter.CTkEntry(self.path_entry,
                                            placeholder_text="Database Absolute Path",
                                            corner_radius=self.radius,
                                            font=self.font_body_pc,
                                            placeholder_text_color=self.text_placeholder_color,
                                            textvariable=self.var_rdir
                                            )

        self.entry.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.entry = customtkinter.CTkEntry(self.path_entry,
                                            placeholder_text="Output Path",
                                            corner_radius=self.radius,
                                            font=self.font_body_pc,
                                            placeholder_text_color=self.text_placeholder_color,
                                            textvariable=self.var_wdir
                                            )

        self.entry.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # UI Elements - Run Button
        self.main_button_1 = customtkinter.CTkButton(master=self.path_entry,
                                                     text='Run Model',
                                                     fg_color="transparent",
                                                     border_width=1,
                                                     font=self.font_body,
                                                     text_color=("gray10", self.text_color),
                                                     corner_radius=self.radius,
                                                     command=self.runModel)
        
        self.main_button_1.grid(row=2, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def openHelpPrompt(self):
        '''
        Event: Open Help prompt.
        '''
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = HelpPrompt(self)
        else:
            self.toplevel_window.focus()
    
    def openAboutPrompt(self):
        '''
        Event: Open About prompt.
        '''
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AboutPrompt(self)
        else:
            self.toplevel_window.focus()  # if window exists focus it

    # Return Threshold value to user
    def returnThresholdVal(self, value):
        '''
        Event: Get threshold values and print to text log.
        '''
        self.threshold_value_bottom_curr = self.padStr('THRESHOLD TOP', f'+{round(value, 4)}')
        self.threshold_value_top_curr = self.padStr('THRESHOLD BOTTOM', round(-value, 4))
        self.insertLog(f"{self.threshold_value_top_curr}\n",
                        f"{self.threshold_value_bottom_curr}\n",
                        clear=True)

    def changeAppearanceMode(self, new_appearance_mode: str):
        '''
        Event: Change application appearance.
        '''
        customtkinter.set_appearance_mode(new_appearance_mode)

    def runModel(self):
        '''
        Event: Performs initial input exception handling.
        Event: Runs model using SentimentAnalysis inherited module.
        '''
        if self.var_col1.get() == '':
            self.insertLog("PLEASE SELECT AT LEAST ONE AGGREGATION COLUMN IN COL1",
                           clear=True)
            
        elif self.var_target_col.get() == '':
            self.insertLog("PLEASE SELECT A TARGET COLUMN TO ANALYZE",
                           clear=True)
            
        elif self.var_target_id_col.get() == '':
            self.insertLog("PLEASE SELECT AN ID COLUMN",
                           clear=True)
            
        elif self.var_rdir.get() == '':
            self.insertLog("PLEASE SELECT AN INPUT DIRECTORY",
                           clear=True)
            
        elif self.var_wdir.get() == '':
            self.insertLog("PLEASE SELECT AN OUTPUT DIRECTORY",
                           clear=True)
            
        else:
            # Define text variables to print to textlog
            self.textvar_confirm = 'CONFIRMING VARIABLES'
            self.textvar_model = self.padStr('MODEL:', self.var_model.get())
            self.textvar_analysis = self.padStr('ANALYSIS:', self.var_analysis.get())
            self.textvar_operation = self.padStr('OPERATION:', self.var_operation.get())
            self.textvar_col1 = self.padStr('COL1:', self.var_col1.get())
            self.textvar_col2 = self.padStr('COL2:', self.var_col2.get())
            self.textvar_col3 = self.padStr('COL3:', self.var_col3.get())
            self.textvar_col4 = self.padStr('COL4:', self.var_col4.get())
            self.textvar_coltarget = self.padStr('TARGET:', self.var_target_col.get())
            self.textvar_colid = self.padStr('ID:', self.var_target_id_col.get())
            self.textvar_colrating = self.padStr('RATING:', self.var_rating_col.get())
            self.textvar_rdir = self.padStr('INPUT DIR:', self.var_rdir.get())
            self.textvar_wdir = self.padStr('OUTPUT DIR:', self.var_wdir.get())
            self.textvar_start = self.padStr('STARTING ANALYSIS IN', f'{float(self.var_wait_time.get())}s')
            self.textvar_stop = self.padStr('CONCLUDED ANALYSIS', 'ALL OK')

            # Confirm selected params to user
            self.insertLog(f"{self.textvar_confirm}\n",
                           f"{self.textvar_model}\n\n",
                           f"{self.textvar_analysis}\n",
                           f"{self.textvar_operation}\n",
                           f"{self.textvar_col1}\n",
                           f"{self.textvar_col2}\n",
                           f"{self.textvar_col3}\n",
                           f"{self.textvar_col4}\n",
                           f"{self.textvar_coltarget}\n",
                           f"{self.textvar_colid}\n",
                           f"{self.textvar_colrating}\n",
                           f"{self.textvar_rdir}\n",
                           f"{self.textvar_wdir}\n",
                           f"{self.textvar_start}\n\n")

            # Wait 5 seconds (for user to see params)
            time.sleep(float(self.var_wait_time.get()))

            # Run analysis
            self.executeModel()

            # Conclude analysis
            self.insertLog(f"{self.textvar_stop}\n\n")
            
        return None

# Call main function
if __name__ == '__main__':
    main() # type: ignore