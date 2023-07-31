from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import socket
import random
from threading import Thread
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import shutil
import json

sub_win_r = Tk()
sub_win_r.geometry("400x400")
sub_win_r.title("Port registration")
label_1 = Label(text="Enter your HOST :")
label_1.pack()
entry_1 = ttk.Entry()
entry_1.pack()
label_2 = Label(text="Enter your PORT :")
label_2.pack()
entry_2 = ttk.Entry()
entry_2.pack()

file_road = None


def up_select_win():
    global file_road

    def backer():
        global work_files
        global work_folder
        global work_dirs
        catalog = os.getcwd()
        catalog = os.path.dirname(catalog)
        for dirs, folder, files in os.walk(catalog):
            work_dirs = dirs
            work_folder = folder
            work_files = files
            break
        label["text"] = ("Текущая папка: " + work_dirs)
        list_var.delete(0, END)
        for new_files in work_files:
            list_var.insert(tk.END, new_files)
        for new_folders in work_folder:
            list_var.insert(tk.END, new_folders)

    def new_iteration(event):
        global work_files
        global work_folder
        global work_dirs
        catalog = os.getcwd()
        w = list_var.curselection()
        y = None
        if len(w) > 0:
            y = list_var.curselection()[0]
        if y is not None:
            for dirs, folder, files in os.walk(catalog):
                work_dirs = dirs
                work_folder = folder
                work_files = files
                break
            if list_var.get(y) not in work_files:
                if catalog[-1] != "\\":
                    catalog = catalog + "\\" + list_var.get(y)
                else:
                    catalog = catalog + list_var.get(y)
                for dirs, folder, files in os.walk(catalog):
                    work_dirs = dirs
                    work_folder = folder
                    work_files = files
                    break
                label["text"] = ("Текущая папка: " + work_dirs)
                list_var.delete(0, END)
                for new_files in work_files:
                    list_var.insert(tk.END, new_files)
                for new_folders in work_folder:
                    list_var.insert(tk.END, new_folders)

    def work_please(file_name_var, file_road_var):

        file_size = (os.stat(file_road_var)).st_size
        full_size = file_size // 1024
        other_size = file_size - (full_size * 1024)

        dialog_window.insert(END, name + ": " + file_name_var)

        if person not in groups:

            s.send(bytes(str(full_size) + "/file_name" + str(other_size) + "/file_name" + file_name_var
                         + "/file_name" + str(name), "utf8"))

            if os.path.exists("story\\" + str(name) + " " + str(person) + ".txt") is False:

                file = open("story\\" + str(name) + " " + str(person) + ".txt", "w")
                file.write(str(name) + ": " + file_name_var)
                file.close()

            else:

                file = open("story\\" + str(name) + " " + str(person) + ".txt", "a")
                file.write("\n" + str(name) + ": " + file_name_var)
                file.close()

        else:

            s.send(bytes(str(full_size) + "/file_group" + str(other_size) + "/file_group" + file_name_var
                         + "/file_group" + str(name) + "/file_group" + str(person), "utf8"))

            if os.path.exists("groups\\" + str(person) + ".txt") is False:

                file = open("groups\\" + str(person) + ".txt", "w")
                file.write(str(name) + ": " + file_name_var)
                file.close()

            else:

                file = open("groups\\" + str(person) + ".txt", "a")
                file.write("\n" + str(name) + ": " + file_name_var)
                file.close()

        f = open(file_road_var, "rb")

        l = f.read(1024)

        while (l):
            s.send(l)
            l = f.read(1024)

        f.close()

    def select():
        global file_road
        file_road = None
        cv = list_var.curselection()
        if len(cv) > 0:
            file_road = list_var.get(cv[0])
            file_name = file_road
            if work_dirs[-1] != "\\":
                file_road = work_dirs + "\\" + file_road
            else:
                file_road = work_dirs + file_road

            work_please(file_name, file_road)
            win.destroy()

    work_files = None
    work_folder = None
    work_dirs = None

    win = Tk()
    geo = win.geometry
    geo("400x400")
    win.title("Searcher")
    catalog = os.getcwd()
    list_var = tk.Listbox(win)
    for dirs, folder, files in os.walk(catalog):
        work_dirs = dirs
        work_folder = folder
        work_files = files
        break
    for new_files in work_files:
        list_var.insert(tk.END, new_files)
    for new_folders in work_folder:
        list_var.insert(tk.END, new_folders)
    list_var.grid(column=1, row=0)
    btn_1 = ttk.Button(win, text="<---", command=backer)
    btn_1.grid(column=1, row=8)
    label = Label(win, text="Текущая папка: " + work_dirs)
    label.grid(column=1, row=7)
    list_var.bind("<Double-Button-1>", new_iteration)
    btn_select = ttk.Button(win, text="Select", command=select)
    btn_select.grid(column=1, row=9)
    win.mainloop()
    return file_road


def host_port_e(event):
    host_port()


def host_port():
    HOST = str(entry_1.get())
    PORT = int(entry_2.get())
    data = {
        "SERVER_HOST": HOST,
        "SERVER_PORT": PORT
    }
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile)
    sub_win_r.destroy()


btn = ttk.Button(text="OK", command=host_port)
btn.pack()
sub_win_r.bind("<Return>", host_port_e)
sub_win_r.mainloop()
with open('config.json') as f:
    templates = json.load(f)
SERVER_HOST = templates["SERVER_HOST"]
SERVER_PORT = templates["SERVER_PORT"]
s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))
client_list = []
group_mode = False
msg = s.recv(1024).decode("utf8")
split_msg = msg.split(" ")
time_client_list = split_msg[1].split(",")
print(time_client_list)
person = None
if os.path.exists("story") is False:
    os.mkdir("story")
if os.path.exists("groups") is False:
    os.mkdir("groups")
if os.path.exists("send_files") is False:
    os.mkdir("send_files")
if os.path.exists("sent") is False:
    os.mkdir("sent")
groups = []


# получатель
def receive():
    Ben = True
    full_number = None
    other_number = None
    f = None
    global client_list
    while True:
        try:
            if Ben is True:
                msg = s.recv(1024).decode("utf8")
                print(msg)
                if "/new_client_list " in msg:
                    split_msg = msg.split(" ")
                    client_list = split_msg[1].split(",")
                    person_list.delete(0, END)
                    if name in client_list:
                        client_list.remove(str(name))
                    for i in client_list:
                        person_list.insert(0, i)
                elif "/create_new_group " in msg:
                    msg = msg.split(" ")[1]
                    msg = msg.split(",")
                    name_of_group = msg.pop(0)
                    file_group = open("groups\\" + name_of_group + ".txt", "w")
                    file_group.write(",".join(msg))
                    file_group.close()
                    groups.append(name_of_group)
                    person_list.insert(0, name_of_group)
                elif "mes_group" in msg:
                    msg = msg.split("mes_group")
                    work_group = msg[0]
                    msg = msg[1]
                    file_group = open("groups\\" + work_group + ".txt", "a")
                    file_group.write("\n" + msg)
                    file_group.close()
                    if work_group == person:
                        dialog_window.insert(END, msg)
                elif "/abpers" in msg:
                    msg = msg.split("/abpers")[1]
                    msg_from = msg.split(":")[0]
                    if msg_from == person or msg_from == name:
                        dialog_window.insert(END, msg)
                    if msg_from != name and msg_from != person:
                        if os.path.exists("story\\" + str(name) + " " + str(msg_from) + ".txt") is False:
                            file = open("story\\" + str(name) + " " + str(msg_from) + ".txt", "w")
                            file.write(msg)
                            file.close()
                        else:
                            file = open("story\\" + str(name) + " " + str(msg_from) + ".txt", "a")
                            file.write("\n" + msg)
                            file.close()
                    else:
                        if os.path.exists("story\\" + str(name) + " " + str(person) + ".txt") is False:
                            file = open("story\\" + str(name) + " " + str(person) + ".txt", "w")
                            file.write(msg)
                            file.close()
                        else:
                            file = open("story\\" + str(name) + " " + str(person) + ".txt", "a")
                            file.write("\n" + msg)
                            file.close()

                elif "/file_name" in msg:
                    msg = msg.split("/file_name")
                    full_number = int(msg[0])
                    other_number = int(msg[1])
                    file_from = str(msg[3])
                    if file_from == person:
                        dialog_window.insert(END, str(file_from) + ": " + msg[2])
                    if os.path.exists("story\\" + str(name) + " " + str(file_from) + ".txt") is False:

                        file = open("story\\" + str(name) + " " + str(file_from) + ".txt", "w")
                        file.write(str(file_from) + ": " + msg[2])
                        file.close()

                    else:

                        file = open("story\\" + str(name) + " " + str(file_from) + ".txt", "a")
                        file.write("\n" + str(file_from) + ": " + msg[2])
                        file.close()

                    f = open('sent/' + msg[2], 'wb')
                    Ben = False

                elif "/file_group" in msg:

                    msg = msg.split("/file_group")

                    f = open('sent/' + msg[2], 'wb')
                    full_number = int(msg[0])
                    other_number = int(msg[1])
                    file_from_name = str(msg[3])
                    file_from_group = str(msg[4])
                    file = open("groups\\" + file_from_group + ".txt", "a")
                    file.write("\n" + str(file_from_name) + ": " + msg[2])
                    file.close()

                    f = open('sent/' + msg[2], 'wb')
                    Ben = False

            else:

                while full_number != 0:
                    msg = s.recv(1024)
                    f.write(msg)
                    full_number -= 1

                if other_number != 0:
                    msg = s.recv(int(other_number))
                    f.write(msg)

                f.close()
                Ben = True

        except OSError:
            break


list_of_group = []


def new_dialog(event):
    global person
    global list_of_group
    global group_mode
    if group_mode is False and person_list.get(person_list.curselection()[0]) not in groups and person_list.get(
            person_list.curselection()[0]) != person:
        dialog_window.delete(0, END)
        person = person_list.get(person_list.curselection()[0])
        user_now["text"] = "Talk with: " + person
        s.send(bytes(name + "/talk_person" + person, "utf8"))
        if os.path.exists("story\\" + str(name) + " " + str(person) + ".txt"):
            file = open("story\\" + str(name) + " " + str(person) + ".txt", "r")
            old_string = file.readlines()
            for i in old_string:
                dialog_window.insert(END, i)

        def send_e(event):
            send()

        def send():
            mes = entry_send.get()
            if mes is not None and mes != "" and person is not None and person != "":
                s.send(bytes(str(name + "abpers" + mes + "abpers" + person), "utf8"))
                entry_send.delete(0, END)

        def send_file():
            s.send(bytes(name + "/talk_person" + person, "utf8"))
            up_select_win()
            # f = open(str(var_file_road), "rb")
            # l = f.read(1024)
            # while (l):
            # s.send(l)
            # l = f.read(1024)
            # f.close()

        btn_send = ttk.Button(text="Send", command=send)
        main_win.bind("<Return>", send_e)
        btn_send.grid(column=4, row=4)
        btn_send_file = ttk.Button(text="Send file", command=send_file)
        btn_send_file.grid(column=4, row=5)
        entry_send = ttk.Entry()
        entry_send.grid(column=3, row=4)
    elif person_list.get(person_list.curselection()[0]) in groups and group_mode is False and person_list.get(
            person_list.curselection()[0]) != person:
        dialog_window.delete(0, END)
        person = person_list.get(person_list.curselection()[0])
        user_now["text"] = "Group: " + person
        file = open("groups\\" + person + ".txt", "r")
        old_string = file.readlines()
        old_string.pop(0)
        for i in old_string:
            dialog_window.insert(END, i)

        def send_e_g(event):
            send_g()

        def send_g():
            mes = entry_send.get()
            if mes is not None and mes != "" and person is not None and person != "":
                with open("groups\\" + person + ".txt", "r") as f:
                    lines = f.readlines()
                    persons = lines[0]
                s.send(bytes(str(person + "mes_group" + persons + "mes_group" + str(name) + ": " + mes), "utf8"))
            entry_send.delete(0, END)

        def send_file_group():

            with open("groups\\" + person + ".txt", "r") as f:
                lines = f.readlines()
                persons = lines[0]
            s.send(bytes(name + "/talk_group" + person + "/talk_group" + persons, "utf8"))

            up_select_win()

        btn_send_g = ttk.Button(text="Send", command=send_g)
        main_win.bind("<Return>", send_e_g)
        btn_send_g.grid(column=4, row=4)
        btn_send_file_group = ttk.Button(text="Send file", command=send_file_group)
        btn_send_file_group.grid(column=4, row=5)
        entry_send = ttk.Entry()
        entry_send.grid(column=3, row=4)
    else:
        if group_mode is True:
            if dialog_window.get(0) != "Your group: ":
                dialog_window.delete(0, END)
                dialog_window.insert(0, "Your group: ")
            group_person = person_list.get(person_list.curselection()[0])
            if group_person not in list_of_group:
                list_of_group.append(group_person)
                dialog_window.insert(END, group_person)

            def create_group():
                win_name_group = Toplevel()
                win_name_group.geometry('200x150')
                Label(win_name_group, text="Enter name of your group: ").pack()
                group_name = Entry(win_name_group)
                group_name.pack()

                def create_new_group():
                    global group_mode
                    global list_of_group
                    if group_name.get() not in groups:
                        group_name_var = group_name.get()
                        groups.append(group_name_var)
                        g_file = open("groups\\" + group_name_var + ".txt", "w")
                        g_file.write(name + "," + ",".join(list_of_group))
                        g_file.close()
                        person_list.insert(0, group_name_var)
                        dialog_window.delete(0, END)
                        group_mode = False
                        s.send(
                            bytes(
                                "/create_new_group " + group_name_var + "," + str(name) + "," + ",".join(list_of_group),
                                "utf8"))
                        list_of_group = []
                        btn_send.destroy()
                        win_name_group.destroy()

                Button(win_name_group, text="OK", command=create_new_group).pack()

            if len(list_of_group) >= 2:
                btn_send = ttk.Button(text="Create", command=create_group)
                btn_send.grid(column=3, row=5)


def new_group():
    global group_mode
    group_mode = True


def sub_close_e(event):
    sub_close()


def sub_close():
    global name
    name = entry.get()
    if name != "" and name not in time_client_list and " " not in name:
        s.send(bytes(name, "utf8"))
        sub_win.destroy()
    elif name in time_client_list:
        Label(sub_win, text="login already exists").pack()
    elif " " in name or "," in name:
        Label(sub_win, text="wrong character").pack()


name = None
sub_win = Tk()
sub_win.geometry("400x400")
sub_win.title("Registration")
label = Label(text="Enter your login :")
label.pack()
entry = ttk.Entry()
entry.pack()
btn = ttk.Button(text="OK", command=sub_close)
btn.pack()
sub_win.bind("<Return>", sub_close_e)
sub_win.mainloop()
main_win = Tk()
main_win.geometry("400x400")
main_win.title("Chats")
log_name = Label(text="Profile: " + str(name))
log_name.grid(column=0, row=0, padx=0, pady=0)
person_names = Label(text="Users :")
person_names.grid()
person_names.grid(column=0, row=1, padx=0, pady=0)
person_list = tk.Listbox(main_win)
person_list.grid(column=0, row=2, padx=0, pady=0)
dialog_window = tk.Listbox(main_win)
dialog_window.grid(column=3, row=2)
person_list.bind("<Double-Button-1>", new_dialog)
btn_group = ttk.Button(text="+New group", command=new_group)
btn_group.grid(column=0, row=4)
user_now = Label(text="Talk with: ")
user_now.grid(column=3, row=1)

receive_thread = Thread(target=receive)
receive_thread.start()
if name is not None or name != "":
    def user_exit():
        s.send(bytes("/user_exit " + str(name), "utf8"))


    main_win.protocol("WM_EXIT", user_exit)
    main_win.mainloop()

s.close()
