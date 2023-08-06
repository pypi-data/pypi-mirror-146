import os, sys, re
import numpy as np

import datetime
from pathlib import Path

import tkinter as tk
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox
from tkinter import ttk

import json

import multiprocessing

# omicsone_src_dir = r"C:\Users\yhu39\Documents\GitHub\omicsone-dash"
# sys.path.append(omicsone_src_dir)

try:
    from .plugins.webapp import build_app
except:
    from plugins.webapp import build_app

try:
    from .plugins.layout import *
except:
    from omicsone.plugins.layout import *

import threading, webbrowser
from threading import Thread

from dash import dcc, html

def build_time_suffix():
    xnow = datetime.datetime.now()
    dt_string = xnow.strftime("%d%m%Y%H%M%S")
    return dt_string


def build_layout2(paths):
    return html.Div(
        id="app-container",
        children=[
            build_dcc_store_card(paths),
            # Input
            # build_input_card(),
            html.Br(),
            build_profile_card(),
            html.Br(),
            build_preprocess_card(),
            html.Br(),
            build_qc_card(),
            html.Br(),
            build_annotation_card(),
            html.Br(),
            # html.Button('Phenotype association Analysis', id='run-button', n_clicks=0,
            #             style={
            #                 'background-color': 'red',
            #                 'color': 'white',
            #             }),
            html.Br(),
            build_diff_card(),
            html.Br(),
            build_decomposition_card(),
            html.Br(),
            build_clustering_card(),
            html.Br(),
            build_association_card(),
            html.Br(),
            build_enrich_card(),
            # html.Br(),
            # # build_genz_card(),
            # html.Br(),
            # html.Br(),
            # html.Br(),
            # html.Br(),

        ]
    )


class OmicsOneGUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master
        self.param = {}

        self.omicsone_process = None

        # menubar = tk.Menu(self.master)
        #
        # # create a pulldown menu, and add it to the menu bar
        # wfmenu = tk.Menu(menubar, tearoff=0)
        # wfmenu.add_command(label="Open", command=self.hello)
        # wfmenu.add_command(label="Save", command=self.hello)
        # wfmenu.add_separator()
        # wfmenu.add_command(label="Exit", command=self.master.quit)
        # menubar.add_cascade(label="WorkFlow", menu=wfmenu)
        #
        # # create more pulldown menus
        # toolmenu = tk.Menu(menubar, tearoff=0)
        # toolmenu.add_command(label="ResultViewer", command=self.view_result)
        # toolmenu.add_command(label="Glycode", command=self.hello)
        # # editmenu.add_command(label="Paste", command=self.hello)
        # menubar.add_cascade(label="Tool", menu=toolmenu)
        #
        # helpmenu = tk.Menu(menubar, tearoff=0)
        # helpmenu.add_command(label="About", command=self.hello)
        # menubar.add_cascade(label="Help", menu=helpmenu)
        #
        # # display the menu
        # self.master.config(menu=menubar)

        self.init_dir = "/"

        nrow = 0
        # def setup(self):
        self.input_labelframe = tk.LabelFrame(self.master, text="Input Files")

        self.label_protein_file_name = tk.Label(self.input_labelframe,
                                                text='File Type')
        self.label_protein_file_name.grid(row=nrow, column=0, columnspan=2, padx=5, pady=2)

        # Combobox creation
        # n = tk.StringVar()
        self.file_type_select = ttk.Combobox(self.input_labelframe, width=27,
                                             # textvariable=n
                                             )
        # Adding combobox drop down list
        self.file_type_select['values'] = (' Meta',
                                           ' Methylation',
                                           ' RNA',
                                           ' Protein',
                                           ' Glycoform',
                                           ' Phosphopeptide',
                                           ' Other'
                                           )
        self.file_type_select.grid(row=nrow, column=2, columnspan=3, padx=5, pady=2)
        self.file_type_select.current(0)

        # button
        self.btn_protein = tk.Button(self.input_labelframe, text="Browse&Add",
                                     command=self.ask_open_matrix_path)
        self.btn_protein.grid(row=nrow, column=5, columnspan=4, padx=5, pady=2)

        # delete all
        self.btn_input_delall = tk.Button(self.input_labelframe, text="Delete All", command=self.input_del_all)
        self.btn_input_delall.grid(row=nrow, column=10, sticky='we', padx=5, pady=2)

        # delete one
        self.btn_input_delone = tk.Button(self.input_labelframe, text="Delete One", command=self.input_del_one)
        self.btn_input_delone.grid(row=nrow, column=12, sticky='we', padx=5, pady=2)

        # number of files
        self.strvar_input_files = tk.StringVar(self.input_labelframe, value="0")
        self.label_input_files = tk.Label(self.input_labelframe, textvariable=self.strvar_input_files)
        self.label_input_files.grid(row=nrow, column=20, padx=5, pady=2)
        self.input_labelframe.pack(fill="both", expand="yes")

        nrow += 1

        self.listbox_yScroll = tk.Scrollbar(self.input_labelframe, orient=tk.VERTICAL)

        self.listbox_xScroll = tk.Scrollbar(self.input_labelframe, orient=tk.HORIZONTAL)
        self.lbox_input_files = tk.Listbox(self.input_labelframe, selectmode="extended",
                                           xscrollcommand=self.listbox_xScroll.set,
                                           yscrollcommand=self.listbox_yScroll.set,
                                           width=105
                                           )
        self.lbox_input_files.grid(row=nrow, columnspan=20, sticky='we', padx=5, pady=2)
        self.listbox_yScroll.grid(row=nrow, column=20, sticky=tk.N + tk.S)

        nrow += 1
        self.listbox_xScroll.grid(row=nrow, columnspan=20, sticky=tk.E + tk.W)

        self.listbox_xScroll['command'] = self.lbox_input_files.xview
        self.listbox_yScroll['command'] = self.lbox_input_files.yview

        nrow += 1

        # output directory
        self.output_labelframe = tk.LabelFrame(self.master, text="Output Directory")
        self.strvar_output_dir = tk.StringVar(self.master, value="")

        nrow = 0
        self.strvar_output_dir.set("")
        self.entry_output_dir = tk.Entry(self.output_labelframe, text=self.strvar_output_dir, width=100, bd=5)
        self.entry_output_dir.grid(row=nrow, column=0, padx=5, pady=2)

        self.btn_output_dir = tk.Button(self.output_labelframe, text="Select", command=self.ask_open_out_dir)
        self.btn_output_dir.grid(row=nrow, column=1, padx=5, pady=2)
        self.output_labelframe.pack(fill="both", expand="yes")

        nrow = 0
        self.param_labelframe = tk.LabelFrame(self.master, text="Parameter File")
        self.strvar_param_file = tk.StringVar(self.master, value="")
        self.strvar_param_file.set("")
        self.entry_param_file = tk.Entry(self.param_labelframe, text=self.strvar_param_file, width=100, bd=5)

        self.entry_param_file.grid(row=nrow, column=0, padx=5, pady=2)
        self.btn_param_file = tk.Button(self.param_labelframe, text="Select", command=self.ask_open_param_file)
        self.btn_param_file.grid(row=nrow, column=1, padx=5, pady=2)
        self.param_labelframe.pack(fill="both", expand="yes")

        self.opt_labelframe = tk.LabelFrame(self.master, text="Operation")

        nrow = 0

        self.btn_use_sample1 = tk.Button(self.opt_labelframe, text="Sample HGSOC", width=30,
                                        command=self.use_sample1)
        self.btn_use_sample1.grid(row=nrow, column=0, sticky='we', padx=2, pady=2)

        self.btn_use_sample2 = tk.Button(self.opt_labelframe, text="Sample LSCC", width=30,
                                        command=self.use_sample2)
        self.btn_use_sample2.grid(row=nrow, column=1, sticky='we', padx=2, pady=2)

        self.btn_start_server = tk.Button(self.opt_labelframe, text="Start", width=15,
                                          command=self.start_omicsone_server)
        self.btn_start_server.grid(row=nrow, column=2, sticky='e', padx=2, pady=2)

        self.btn_stop_server = tk.Button(self.opt_labelframe, text="Stop", width=15,
                                         command=self.stop_omicsone_server)
        self.btn_stop_server.grid(row=nrow, column=3, sticky='e', padx=5, pady=2)

        self.opt_labelframe.pack(fill="both", expand="yes")

        # self.pbar_one = ttk.Progressbar(self.master, mode='indeterminate')
        # self.pbar_one.pack(fill="both", expand="yes")
        # self.pbar_all = ttk.Progressbar(self.master, mode='indeterminate')
        # self.pbar_all.pack(fill="both", expand="yes")

    def hello(self):
        print("Hello!")

    def view_result(self):
        pass

    def input_del_all(self):
        self.lbox_input_files.delete(0, tk.END)
        self.strvar_input_files.set(self.lbox_input_files.size())

    def input_del_one(self):
        self.lbox_input_files.delete(tk.ANCHOR)
        self.strvar_input_files.set(self.lbox_input_files.size())

    def use_sample1(self):
        # set up samples input files
        self.lbox_input_files.delete(0, tk.END)
        root_dir = Path(__file__).parent
        sample_dir = r'{}'.format(str(root_dir)) + os.sep + "samples"
        self.lbox_input_files.insert(0, "Meta=" + sample_dir + os.sep + "CPTAC_OVA_meta_info.txt")
        self.lbox_input_files.insert(1, "Protein=" + sample_dir + os.sep + "CPTAC_OVA_protein_log2r_20210811.txt")
        self.lbox_input_files.insert(2, "Glycoform=" + sample_dir + os.sep + "CPTAC_OVA_glycoform_log2r_20210811.txt")

        # set up out_dir
        out_dir = sample_dir + os.sep + "OmicsOne_Output_{0}".format(build_time_suffix())
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        self.strvar_output_dir.set(out_dir)

        # set up param_dir
        param_dir = out_dir + os.sep + "Parameters"
        if not os.path.exists(param_dir):
            os.mkdir(param_dir)
        self.entry_param_file.delete(0, tk.END)
        self.entry_param_file.insert(0, param_dir)

    def use_sample2(self):
        # set up samples input files
        self.lbox_input_files.delete(0, tk.END)
        root_dir = Path(__file__).parent
        sample_dir = r'{}'.format(str(root_dir)) + os.sep + "samples"
        self.lbox_input_files.insert(0, "Meta=" + sample_dir + os.sep + "CPTAC_LSCC_meta_info.xlsx")
        self.lbox_input_files.insert(1, "Protein=" + sample_dir + os.sep + "CPTAC_LSCC_proteome.xlsx")

        # set up out_dir
        out_dir = sample_dir + os.sep + "OmicsOne_Output_{0}".format(build_time_suffix())
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        self.strvar_output_dir.set(out_dir)

        # set up param_dir
        param_dir = out_dir + os.sep + "Parameters"
        if not os.path.exists(param_dir):
            os.mkdir(param_dir)
        self.entry_param_file.delete(0, tk.END)
        self.entry_param_file.insert(0, param_dir)



    def ask_open_out_dir(self):
        out_dir = tkFileDialog.askdirectory()
        if os.path.exists(out_dir):
            self.param['OutDir'] = {
                'PATH': out_dir
            }
            self.strvar_output_dir.set(str(out_dir))

    def ask_open_param_dir(self):
        param_dir = tkFileDialog.askdirectory()
        if os.path.exists(param_dir):
            self.param['ParamDir'] = {
                'PATH': param_dir
            }
            self.strvar_param_file.set(str(param_dir))

    def ask_open_param_file(self):
        param_file = tkFileDialog.askopenfilename(initialdir="/", title="Select Param File",
                                                  filetypes=(("param files", "*.json"), ("param files", "*.txt")))
        if os.path.exists(param_file):

            self.strvar_param_file.set(param_file)
            # x = json.load(open(param_file, "r"), "UTF-8")
            x = json.load(open(param_file, "r"))
            for i in x:
                self.param[i] = x[i]

    def ask_open_matrix_path(self):
        file_name = tkFileDialog.askopenfilename(initialdir=self.init_dir, title="Select file",
                                                 filetypes=(("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")))
        folder, bn = os.path.split(file_name)
        file_type = self.file_type_select.get()
        paths = self.lbox_input_files.get(0, tk.END)

        if os.path.exists(file_name) and file_type != "":
            path = str(file_type) + "=" + str(file_name)
            if path not in paths:
                self.lbox_input_files.insert(tk.END, path)
                self.init_dir = folder
                self.strvar_input_files.set(self.lbox_input_files.size())

    def start_omicsone_server(self):
        url = '127.0.0.1'
        port = '8051'
        paths = self.lbox_input_files.get(0, tk.END)
        paths = '\t'.join([i for i in paths])
        out_dir = self.entry_output_dir.get()
        paths += "\t" + r'OutDir={0}'.format(out_dir)
        param_dir = self.entry_param_file.get()
        paths += "\t" + r'ParamDir={0}'.format(param_dir)

        # start server
        self.omicsone_process = multiprocessing.Process(target=thread_server, name='omicsone', args=(url, port, paths))
        self.omicsone_process.start()

        # start client
        threading.Timer(3, lambda: webbrowser.open('http://' + url + ":" + port)).start()

        self.btn_start_server['state'] = 'disabled'

    def stop_omicsone_server(self):
        if self.omicsone_process is not None:
            self.omicsone_process.terminate()
            self.btn_start_server['state'] = 'normal'


def thread_server(url, port, paths):
    app = build_app(paths)
    app.layout = build_layout2(paths=paths)
    app.run_server(host=url, port=port)


def gui():
    root = tk.Tk()
    root.geometry('680x400')
    root.resizable(False, False)
    root.title("OmicsOne 1.0beta")
    g = OmicsOneGUI(root)
    root.mainloop()


if __name__ == "__main__":
    gui()
