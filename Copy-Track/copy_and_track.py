import os
from copy import deepcopy
import tkinter.messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from tkinter.ttk import Progressbar
import shutil

global size_obtained, copy_file_sizes
size_obtained = 0
my_copy_file = 0
my_copy_folder = 0

# app
app = Tk()

# geometry
# app.geometry("1920x1080")

# title
app.title("Copy and Track App")

app.minsize(1500, 800)

# loading pics
folder_image = PhotoImage(file="./src/folder.png").subsample(3, 3)
file_image = PhotoImage(file="./src/file.png").subsample(3, 3)
forward_image = PhotoImage(file="./src/forward.png").subsample(10, 10)
progress_image = PhotoImage(file="./src/progress_1.png").subsample(8, 8)
done = PhotoImage(file="./src/done_1.png").subsample(8, 8)

# boolean vars
file_source_is_not_empty = False
folder_source_is_not_empty = False
destination_is_not_empty = False


# ------ start of functions ------ #

#   start move files n folders function
#       move files function


def move_files():
    copy_files()
    for file in sources:
        os.remove(file)


# move folder function


def move_folder():
    copy_folders()
    os.remove(sources)


#   end move files n folders function

#   start of file and folder trackers
#       start of files tracker


def track_files():
    try:
        # directories
        dest_files = os.listdir(destination)
        # source_files = os.scandir(sources)
        # pages forgotten
        progress_label.place_forget()
        progress_title.place_forget()
        progress.place_forget()
        list_contents.place_forget()
        # frames
        global track_contents, success_content_scrolled_text, unsuccess_content_scrolled_text, table_header
        track_contents = Frame(canvas, width=1030, height=290, bg="white")
        table_header = Frame(track_contents, width=1030, height=25, bg="#ebe9e9")
        # text headers
        Label(table_header, text="Files Successful", bg="#ebe9e9").place(anchor="c", relx=0.25, rely=0.47)
        Label(table_header, text="Files Unsuccessful", bg="#ebe9e9").place(anchor="c", relx=0.7, rely=0.47)
        # canvas borders
        Canvas(track_contents, width=10, height=290).place(anchor="c", relx=0.0129, rely=0.58)
        Canvas(track_contents, width=10, height=290).place(anchor="c", relx=0.5, rely=0.58)
        Canvas(track_contents, width=10, height=290).place(anchor="c", relx=0.994, rely=0.58)
        # inner header
        inner_header = Frame(track_contents, width=485, height=35, bg="white")
        Label(inner_header, text="Name", bg="white").place(anchor="c", relx=0.1, rely=0.5)
        Label(inner_header, text="|", bg="white").place(anchor="c", relx=0.25, rely=0.5)
        Label(inner_header, text="Path", bg="white").place(anchor="c", relx=0.50, rely=0.5)
        Label(inner_header, text="|", bg="white").place(anchor="c", relx=0.74, rely=0.5)
        Label(inner_header, text="Size", bg="white").place(anchor="c", relx=0.88, rely=0.5)
        inner_header.place(anchor="c", relx=0.256, rely=0.19)
        Canvas(inner_header, width=490, height=0.5, bg="black").place(anchor="w", relx=0, rely=0.9)
        # copied inner header
        copy_inner_header = Frame(track_contents, width=490, height=35, bg="white")
        Label(copy_inner_header, text="Name", bg="white").place(anchor="c", relx=0.1, rely=0.5)
        Label(copy_inner_header, text="|", bg="white").place(anchor="c", relx=0.25, rely=0.5)
        Label(copy_inner_header, text="Path", bg="white").place(anchor="c", relx=0.50, rely=0.5)
        Label(copy_inner_header, text="|", bg="white").place(anchor="c", relx=0.74, rely=0.5)
        Label(copy_inner_header, text="Size", bg="white").place(anchor="c", relx=0.88, rely=0.5)
        Canvas(copy_inner_header, width=490, height=0.5, bg="black").place(anchor="w", relx=0, rely=0.9)
        copy_inner_header.place(anchor="c", relx=0.749, rely=0.19)
        # lists
        successful_list = {}
        unsuccessful_list = {}
        # get files
        if len(dest_files) != 0:
            for file in sources:
                if file.split("/")[-1] in os.listdir(destination):
                    successful_list[file.split("/")[-1]] = file
                else:
                    unsuccessful_list[file.split("/")[-1]] = file

        # success scrolled text widget
        success_content_scrolled_text = ScrolledText(track_contents, bg="white", width=58, height=12.2, bd=0)
        success_content_scrolled_text.place(anchor="c", relx=0.255, rely=0.6)
        for file in successful_list.keys():
            lb0 = Label(success_content_scrolled_text, text=f"{file}", bg="white", justify=LEFT,
                        wraplength=70, width=16)
            success_content_scrolled_text.window_create("end", window=lb0)

            lb1 = Label(success_content_scrolled_text, text=f"{successful_list[file]}", bg="white", justify=LEFT,
                        wraplength=200, width=34)
            success_content_scrolled_text.window_create("end", window=lb1)

            file_name = (successful_list[file]).split("/")[-1]
            size_of_file = os.path.getsize(destination + "/" + file_name)

            if size_of_file >= 1000000000:
                size_of_file = str(round((size_of_file / 1000000000), 1)) + " gb"
            elif 1000000 <= size_of_file < 1000000000:
                size_of_file = str(round((size_of_file / 1000000), 1)) + " mb"
            elif size_of_file >= 1000:
                size_of_file = str(round((size_of_file / 1000), 1)) + " kb"
            else:
                size_of_file = str(round(size_of_file, 1)) + " bytes"
            lb2 = Label(success_content_scrolled_text, text=size_of_file, bg="white", justify=LEFT, wraplength=60,
                        width=13)
            success_content_scrolled_text.window_create("end", window=lb2)

            canvas_separator = Canvas(success_content_scrolled_text, width=470, height=5)
            success_content_scrolled_text.window_create("end", window=canvas_separator)

        # unsuccessful scrolled text widget
        unsuccess_content_scrolled_text = ScrolledText(track_contents, bg="white", width=59, height=12.2, bd=0)
        unsuccess_content_scrolled_text.place(anchor="c", relx=0.75, rely=0.6)
        for file in unsuccessful_list.keys():
            lb0 = Label(unsuccess_content_scrolled_text, text=f"{file}", bg="white", justify=LEFT,
                        wraplength=70, width=16)
            success_content_scrolled_text.window_create("end", window=lb0)

            lb1 = Label(unsuccess_content_scrolled_text, text=f"{unsuccessful_list[file]}", bg="white", justify=LEFT,
                        wraplength=200, width=34)
            success_content_scrolled_text.window_create("end", window=lb1)

            file_name = (unsuccessful_list[file]).split("/")[-1]
            size_of_file = os.path.getsize(destination + "/" + file_name)

            if size_of_file >= 1000000000:
                size_of_file = str(round((size_of_file / 1000000000), 1)) + " gb"
            elif 1000000 <= size_of_file < 1000000000:
                size_of_file = str(round((size_of_file / 1000000), 1)) + " mb"
            elif size_of_file >= 1000:
                size_of_file = str(round((size_of_file / 1000), 1)) + " kb"
            else:
                size_of_file = str(round(size_of_file, 1)) + " bytes"

            lb2 = Label(unsuccess_content_scrolled_text, text=size_of_file, bg="white", justify=LEFT, wraplength=60,
                        width=13)
            success_content_scrolled_text.window_create("end", window=lb2)

        table_header.place(anchor="c", relx=0.5, rely=0.1)
        track_contents.place(anchor="c", relx=0.39, rely=0.8)
    except NameError:
        tkinter.messagebox.showinfo("Error Message", "No files copied")
    return 0


#       end of files tracker
#       start of folders tracker


def track_folder():
    try:
        # directories
        dest_files = os.listdir(destination)
        source_files = os.scandir(sources)
        # pages forgotten
        progress_label.place_forget()
        progress_title.place_forget()
        progress.place_forget()
        list_contents.place_forget()
        # frames
        global track_contents, success_content_scrolled_text, unsuccess_content_scrolled_text, table_header
        track_contents = Frame(canvas, width=1030, height=290, bg="white")
        table_header = Frame(track_contents, width=1030, height=25, bg="#ebe9e9")
        # text headers
        Label(table_header, text="Files Successful", bg="#ebe9e9").place(anchor="c", relx=0.25, rely=0.47)
        Label(table_header, text="Files Unsuccessful", bg="#ebe9e9").place(anchor="c", relx=0.7, rely=0.47)
        # canvas borders
        Canvas(track_contents, width=10, height=290).place(anchor="c", relx=0.0129, rely=0.58)
        Canvas(track_contents, width=10, height=290).place(anchor="c", relx=0.5, rely=0.58)
        Canvas(track_contents, width=10, height=290).place(anchor="c", relx=0.994, rely=0.58)
        # inner header
        inner_header = Frame(track_contents, width=485, height=35, bg="white")
        Label(inner_header, text="Name", bg="white").place(anchor="c", relx=0.1, rely=0.5)
        Label(inner_header, text="|", bg="white").place(anchor="c", relx=0.25, rely=0.5)
        Label(inner_header, text="Path", bg="white").place(anchor="c", relx=0.50, rely=0.5)
        Label(inner_header, text="|", bg="white").place(anchor="c", relx=0.74, rely=0.5)
        Label(inner_header, text="Size", bg="white").place(anchor="c", relx=0.88, rely=0.5)
        inner_header.place(anchor="c", relx=0.256, rely=0.19)
        Canvas(inner_header, width=490, height=0.5, bg="black").place(anchor="w", relx=0, rely=0.9)
        # copied inner header
        copy_inner_header = Frame(track_contents, width=490, height=35, bg="white")
        Label(copy_inner_header, text="Name", bg="white").place(anchor="c", relx=0.1, rely=0.5)
        Label(copy_inner_header, text="|", bg="white").place(anchor="c", relx=0.25, rely=0.5)
        Label(copy_inner_header, text="Path", bg="white").place(anchor="c", relx=0.50, rely=0.5)
        Label(copy_inner_header, text="|", bg="white").place(anchor="c", relx=0.74, rely=0.5)
        Label(copy_inner_header, text="Size", bg="white").place(anchor="c", relx=0.88, rely=0.5)
        Canvas(copy_inner_header, width=490, height=0.5, bg="black").place(anchor="w", relx=0, rely=0.9)
        copy_inner_header.place(anchor="c", relx=0.749, rely=0.19)
        # lists
        successful_list = {}
        unsuccessful_list = {}
        # get files
        if sources.split("/")[-1] in dest_files:
            for file in source_files:
                if file.name in os.listdir(destination + "/" + sources.split("/")[-1]):
                    successful_list[file.name] = file.path
                else:
                    unsuccessful_list[file.name] = file.path

        # success scrolled text widget
        success_content_scrolled_text = ScrolledText(track_contents, bg="white", width=58, height=12.2, bd=0)
        success_content_scrolled_text.place(anchor="c", relx=0.255, rely=0.6)
        for file in successful_list.keys():
            lb0 = Label(success_content_scrolled_text, text=f"{file}", bg="white", justify=LEFT,
                        wraplength=70, width=16)
            success_content_scrolled_text.window_create("end", window=lb0)

            # split file path
            successful_list_splitted = str(successful_list[file]).split("\\")
            reformatted_path = '/'.join(successful_list_splitted)

            lb1 = Label(success_content_scrolled_text, text=f"{reformatted_path}", bg="white", justify=LEFT,
                        wraplength=200, width=34)
            success_content_scrolled_text.window_create("end", window=lb1)

            file_name = (reformatted_path).split("/")[-1]
            size_of_file = os.path.getsize(destination + "/" + file_name)

            if size_of_file >= 1000000000:
                size_of_file = str(size_of_file / 1000000000) + " gb"
            elif 1000000 <= size_of_file < 1000000000:
                size_of_file = str(size_of_file / 1000000) + " mb"
            elif size_of_file >= 1000:
                size_of_file = str(size_of_file / 1000) + " kb"
            else:
                size_of_file = str(size_of_file) + " bytes"
            lb2 = Label(success_content_scrolled_text, text=size_of_file, bg="white", justify=LEFT, wraplength=60,
                        width=13)
            success_content_scrolled_text.window_create("end", window=lb2)

            canvas_separator = Canvas(success_content_scrolled_text, width=470, height=5)
            success_content_scrolled_text.window_create("end", window=canvas_separator)

        # unsuccessful scrolled text widget
        unsuccess_content_scrolled_text = ScrolledText(track_contents, bg="white", width=59, height=12.2, bd=0)
        unsuccess_content_scrolled_text.place(anchor="c", relx=0.75, rely=0.6)
        for file in unsuccessful_list.keys():
            lb0 = Label(unsuccess_content_scrolled_text, text=f"{file}", bg="white", justify=LEFT,
                        wraplength=70, width=16)
            success_content_scrolled_text.window_create("end", window=lb0)

            # split file path
            successful_list_splitted = str(successful_list[file]).split("\\")
            reformatted_path = '/'.join(successful_list_splitted)

            lb1 = Label(unsuccess_content_scrolled_text, text=f"{reformatted_path}", bg="white", justify=LEFT,
                        wraplength=200, width=34)
            success_content_scrolled_text.window_create("end", window=lb1)

            file_name = (reformatted_path).split("/")[-1]
            size_of_file = os.path.getsize(destination + "/" + file_name)

            if size_of_file >= 1000000000:
                size_of_file = str(size_of_file / 1000000000) + " gb"
            elif 1000000 <= size_of_file < 1000000000:
                size_of_file = str(size_of_file / 1000000) + " mb"
            elif size_of_file >= 1000:
                size_of_file = str(size_of_file / 1000) + " kb"
            else:
                size_of_file = str(size_of_file) + " bytes"

            lb2 = Label(unsuccess_content_scrolled_text, text=size_of_file, bg="white", justify=LEFT, wraplength=60,
                        width=13)
            success_content_scrolled_text.window_create("end", window=lb2)

        table_header.place(anchor="c", relx=0.5, rely=0.1)
        track_contents.place(anchor="c", relx=0.39, rely=0.8)
    except NameError:
        tkinter.messagebox.showinfo("Error Message", "No files copied")
    return 0


#       end of folders tracker
#   end of trackers

def callback_function(copied):
    tracker(copied)


def tracker(copied):
    global size_obtained
    if total_files == 1:
        if int(copied) < 1e3:
            current_size = str(round(int(copied), 1)) + " bytes"
        elif 1e3 <= int(copied) < 1e6:
            current_size = str(round((int(copied) / 1E3), 1)) + " KB"
        elif 1e6 <= int(copied) < 1e9:
            current_size = str(round((int(copied) / 1E6), 1)) + " MB"
        else:
            current_size = str(round((int(copied) / 1E9), 1)) + " GB"

        bars_files(current_size, copied)
    else:
        current_size = ''
        size_obtained = size_obtained + copied
        if int(size_obtained) < 1e3:
            current_size = str(round(int(size_obtained), 1)) + " bytes"
        elif 1e3 <= int(size_obtained) < 1e6:
            current_size = str(round((int(size_obtained) / 1E3), 1)) + " KB"
        elif 1e6 <= int(size_obtained) < 1e9:
            current_size = str(round(int(size_obtained) / 1E6, 1)) + " MB"
        else:
            current_size = str(round(int(size_obtained) / 1E9, 1)) + " GB"

        bars_files(current_size, copied)


def callback_function_folder(copied):
    tracker_folder(copied)


def tracker_folder(copied):
    global size_obtained
    if total_files == 1:
        if int(copied) < 1e3:
            current_size = str(round(int(copied), 1)) + " bytes"
        elif 1e3 <= int(copied) < 1e6:
            current_size = str(round((int(copied) / 1E3), 1)) + " KB"
        elif 1e6 <= int(copied) < 1e9:
            current_size = str(round((int(copied) / 1E6), 1)) + " MB"
        else:
            current_size = str(round((int(copied) / 1E9), 1)) + " GB"

        bars_folder(current_size, copied)
    else:
        current_size = ''
        size_obtained = size_obtained + copied
        if int(size_obtained) < 1e3:
            current_size = str(round(int(size_obtained), 1)) + " bytes"
        elif 1e3 <= int(size_obtained) < 1e6:
            current_size = str(round((int(size_obtained) / 1E3), 1)) + " KB"
        elif 1e6 <= int(size_obtained) < 1e9:
            current_size = str(round(int(size_obtained) / 1E6, 1)) + " MB"
        else:
            current_size = str(round(int(size_obtained) / 1E9, 1)) + " GB"

        bars_folder(current_size, copied)


#   start of progress bar handler


def bars_files(current_size, copied):
    total = total_files
    current_i = 0
    i = 0
    if int(copied) >= file_sizes[0]:
        item = file_sizes.pop(0)
        current_i = copy_file_sizes.index(item)
        i = copy_file_sizes.index(item) + 1
    global my_copy_file
    current_percent = 0
    try:
        if total > 1:
            my_copy_file = my_copy_file + (copied * (100 / copy_file_sizes[current_i]))
            total_percent = 100 * total
            current_percent = (my_copy_file / total_percent) * 100
        else:
            new_copy = copied * (100 / copy_file_sizes[current_i])
            total_percent = 100 * total
            current_percent = (new_copy / total_percent) * 100
    except IndexError:
        pass

    files_total["text"] = "Total Files: " + str(i) + "/" + str(total)
    if int(FILE_SIZE) < 1E3:
        file_size_string = str(round(FILE_SIZE, 1)) + " bytes"
    elif 1E3 <= int(FILE_SIZE) < 1E6:
        file_size_string = str(round((FILE_SIZE / 1E3), 1)) + " KB"
    elif 1E6 <= int(FILE_SIZE) < 1E9:
        file_size_string = str(round((FILE_SIZE / 1E6), 1)) + " MB"
    else:
        file_size_string = str(round((FILE_SIZE / 1E9), 1)) + " GB"

    total_size["text"] = "Total Size: " + str(current_size) + "/" + str(file_size_string)
    percentage["text"] = "Percentages: " + str(round(current_percent)) + "/" + "100"
    if round(current_percent) == 100:
        progress_label["image"] = done
        app.update_idletasks()
    progress["value"] = current_percent
    app.update_idletasks()


def bars_folder(current_size, copied):
    total = total_files
    current_i = 0
    i = 0
    if int(copied) >= file_sizes[0]:
        item = file_sizes.pop(0)
        current_i = copy_file_sizes.index(item)
        i = copy_file_sizes.index(item) + 1
    global my_copy_folder
    current_percent = 0
    try:
        if total > 1:
            my_copy_folder = my_copy_folder + (copied * (100 / copy_file_sizes[current_i]))
            total_percent = 100 * total
            current_percent = (my_copy_folder / total_percent) * 100
        else:
            new_copy = copied * (100 / copy_file_sizes[current_i])
            total_percent = 100 * total
            current_percent = (new_copy / total_percent) * 100
    except IndexError:
        pass

    files_total["text"] = "Total Files: " + str(i) + "/" + str(total)
    if int(FILE_SIZE) < 1E3:
        file_size_string = str(round(FILE_SIZE, 1)) + " bytes"
    elif 1E3 <= int(FILE_SIZE) < 1E6:
        file_size_string = str(round((FILE_SIZE / 1E3), 1)) + " KB"
    elif 1E6 <= int(FILE_SIZE) < 1E9:
        file_size_string = str(round((FILE_SIZE / 1E6), 1)) + " MB"
    else:
        file_size_string = str(round((FILE_SIZE / 1E9), 1)) + " GB"

    total_size["text"] = "Total Size: " + str(current_size) + "/" + str(file_size_string)
    percentage["text"] = "Percentages: " + str(round(current_percent)) + "/" + "100"
    if round(current_percent) == 100:
        progress_label["image"] = done
        app.update_idletasks()
    progress["value"] = current_percent
    app.update_idletasks()


#   end of progress bar handler

#   start of copying function
#       start of copying files function


def copy_files():
    global FILE_SIZE, files_total, total_files, progress_label, progress, total_size, percentage, file_sizes, \
        copy_file_sizes
    src_text_widget.delete("0.0", "insert")
    dest_text_widget.delete("0.0", "insert")
    if file_source_is_not_empty and destination_is_not_empty:
        try:
            track_contents.place_forget()
            success_content_scrolled_text.place_forget()
            unsuccess_content_scrolled_text.place_forget()
            table_header.place_forget()
        except NameError:
            pass
        list_contents = Frame(canvas, width=1030, height=290, bg="#ebe9e9")
        progress_label = Label(list_contents, image=progress_image)
        progress_label.place(anchor="c", relx=0.5, rely=0.2)
        progress = Progressbar(list_contents, orient=HORIZONTAL, length=100,
                               mode='determinate')

        progress.place(anchor="c", relx=0.5, rely=0.45, width=150, height=30)
        files_total = Label(list_contents, text="Total Files: 0/0", bg="#ebe9e9")
        files_total.place(anchor="c", relx=0.5, rely=0.65)
        total_size = Label(list_contents, text="Total Size: 0/0", bg="#ebe9e9")
        total_size.place(anchor="c", relx=0.5, rely=0.74)
        percentage = Label(list_contents, text="Percentage: 0/100", bg="#ebe9e9")
        percentage.place(anchor="c", relx=0.5, rely=0.83)
        list_contents.place(anchor="c", relx=0.39, rely=0.8)
        progress_title = Label(app, text="Progress Bar", bg="white")
        progress_title.place(anchor="c", relx=0.10, rely=0.598)

        total_files = 0
        file_sizes = []
        i = 1
        for file in sources:
            total_files = total_files + 1
            file_sizes.append(int(os.path.getsize(file)))
        copy_file_sizes = deepcopy(file_sizes)
        FILE_SIZE = sum(file_sizes)
        try:
            for file in sources:
                shutil.copy(file, destination, callback_function)
        except shutil.SameFileError:
            pass


#       end of files copying function
#       start of folders copying function


def copy_folders():
    global files_total, total_files, progress_label, progress, total_size, percentage, file_sizes, copy_file_sizes, \
        FILE_SIZE
    src_text_widget.delete("0.0", "insert")
    dest_text_widget.delete("0.0", "insert")
    if folder_source_is_not_empty and destination_is_not_empty:
        try:
            track_contents.place_forget()
            success_content_scrolled_text.place_forget()
            unsuccess_content_scrolled_text.place_forget()
            table_header.place_forget()
        except NameError:
            pass
        list_contents = Frame(canvas, width=1030, height=290, bg="#ebe9e9")
        progress_label = Label(list_contents, image=progress_image)
        progress_label.place(anchor="c", relx=0.5, rely=0.2)
        progress = Progressbar(list_contents, orient=HORIZONTAL, length=100,
                               mode='determinate')

        progress.place(anchor="c", relx=0.5, rely=0.45, width=150, height=30)
        files_total = Label(list_contents, text="Total Files: 0/0", bg="#ebe9e9")
        files_total.place(anchor="c", relx=0.5, rely=0.65)
        total_size = Label(list_contents, text="Total Size: 0/0", bg="#ebe9e9")
        total_size.place(anchor="c", relx=0.5, rely=0.74)
        percentage = Label(list_contents, text="Percentage: 0/100", bg="#ebe9e9")
        percentage.place(anchor="c", relx=0.5, rely=0.83)
        list_contents.place(anchor="c", relx=0.39, rely=0.8)
        progress_title = Label(app, text="Progress Bar", bg="white")
        progress_title.place(anchor="c", relx=0.10, rely=0.598)

        file_list = os.scandir(sources)
        file_sizes = []
        total_files = 0
        for file in file_list:
            if file.is_dir():
                folder = os.listdir(file.path)
                for inner_file in folder:
                    inner_file = '/'.join(file.path.split('\\')) + '/' + inner_file
                    file_sizes.append(int(os.path.getsize(inner_file)))
                    total_files = total_files + 1

            elif file.is_file():
                file_sizes.append(int(os.path.getsize(file.path)))
                total_files = total_files + 1
        copy_file_sizes = deepcopy(file_sizes)
        FILE_SIZE = sum(file_sizes)
        try:
            shutil.copytree(sources, destination + "/" + sources.split("/")[-1], callback_function_folder)
        except FileExistsError:
            pass
        # for x in range(1, total_files + 1):
        #     time.sleep(1)
        #     bars_folder(x)


#       end of folder copying function
#   end of copying function

#   inserting into Texts
#       add text to folder source entry


def add_text_to_source():
    global folder_source_is_not_empty
    try:
        if sources == "":
            tkinter.messagebox.showinfo("Error Message", "No source directory specified")
        else:
            src_text_widget.delete("0.0", "insert")
            src_text_widget.insert("insert", sources)
        folder_source_is_not_empty = True
    except NameError:
        tkinter.messagebox.showinfo("Error Message", "No source directory specified")


#       add text to file text entry


def add_filenames_to_text():
    global file_source_is_not_empty
    try:
        if sources == ():
            tkinter.messagebox.showinfo("Error Message", "No source directory specified")
        else:
            for files in sources:
                file_name = files.split("/")[-1]
                src_text_widget.insert("insert", file_name)
                if sources[-1] == files:
                    pass
                else:
                    src_text_widget.insert("insert", ", ")
        file_source_is_not_empty = True
    except NameError:
        tkinter.messagebox.showinfo("Error Message", "No source directory specified")


#       add text to destination text entry


def add_text_to_dest():
    global destination_is_not_empty
    try:
        if destination == "":
            tkinter.messagebox.showinfo("Error Message", "No destination directory specified")
        else:
            dest_text_widget.delete("0.0", "insert")
            dest_text_widget.insert("insert", destination)
        destination_is_not_empty = True
    except NameError:
        tkinter.messagebox.showinfo("Error Message", "No destination directory specified")


#   end insert of text functions


#   getting source contents
#       get folders
def get_files_from_folder(src_or_dest):
    global sources, destination
    if src_or_dest == "src":
        file_names = filedialog.askdirectory()
        sources = file_names
        add_text_to_source()
    elif src_or_dest == "dest":
        file_names = filedialog.askdirectory()
        destination = file_names
        add_text_to_dest()


#       get files


def get_files(src_or_dest):
    global sources, destination
    if src_or_dest == "src":
        file_names = filedialog.askopenfilenames()
        sources = file_names
        add_filenames_to_text()

    elif src_or_dest == "dest":
        file_names = filedialog.askdirectory()
        destination = file_names
        add_text_to_dest()


# --- end of functions --- #


# --- app pages content starts --- #

# file transfer page


def file_transfer():
    global src_text_widget, dest_text_widget, canvas, progress_title, progress_label, list_contents

    # canvas body
    canvas = Canvas(app, width=1300, height=650, bg="#ffffff")

    # frame body
    canvas_body_frame = Frame(canvas, width=300, height=1350, bg="#d0cece")
    canvas_body_frame.place(anchor="c", relx=0.9, rely=0)

    Button(canvas_body_frame, text="COPY", width=30, height=3, bg="white", command=copy_files).place(anchor="c",
                                                                                                     relx=0.5,
                                                                                                     rely=0.6)
    Button(canvas_body_frame, text="MOVE", width=30, height=3, bg="white", command=move_files).place(anchor="c",
                                                                                                     relx=0.5,
                                                                                                     rely=0.65)
    Button(canvas_body_frame, text="TRACK", width=30, height=3, bg="white", command=track_files).place(anchor="c",
                                                                                                       relx=0.5,
                                                                                                       rely=0.7)
    Button(canvas_body_frame, text="Copy Folders instead", width=30, height=3, bg="white",
           command=directory_transfer).place(anchor="c", relx=0.5, rely=0.9)
    Label(canvas, bg="white", text="Copy and Track files from one location "
                                   "to another location").place(anchor="c",
                                                                relx=0.4,
                                                                rely=0.05)
    Label(canvas, bg="white", image=file_image).place(anchor="c", relx=0.26, rely=0.25)
    Label(canvas, bg="white", image=forward_image).place(anchor="c", relx=0.40, rely=0.25)
    Label(canvas, bg="white", image=folder_image).place(anchor="c", relx=0.53, rely=0.25)
    scrollbar_src = Scrollbar(canvas)
    scrollbar_src.place(anchor="c", relx=0.35, rely=0.41, height=70)
    src_text_widget = Text(canvas, bd=5, height=4, width=25, yscrollcommand=scrollbar_src.set)
    scrollbar_src.config(command=src_text_widget.yview)
    src_text_widget.place(anchor="c", relx=0.26, rely=0.41)
    scrollbar_dest = Scrollbar(canvas)
    scrollbar_dest.place(anchor="c", relx=0.62, rely=0.41, height=70)
    dest_text_widget = Text(canvas, bd=5, height=4, width=25, yscrollcommand=scrollbar_dest.set)
    dest_text_widget.place(anchor="c", relx=0.53, rely=0.41)
    scrollbar_dest.config(command=dest_text_widget.yview)
    Button(canvas, text="Open Source directory", command=lambda: get_files("src")).place(anchor="c", relx=0.26,
                                                                                         rely=0.5)
    Button(canvas, text="Open Destination directory", command=lambda: get_files("dest")).place(anchor="c", relx=0.53,
                                                                                               rely=0.5)
    list_contents = Frame(canvas, width=1030, height=290, bg="#ebe9e9")
    progress_label = Label(list_contents, image=progress_image)
    progress_label.place(anchor="c", relx=0.5, rely=0.2)
    progress = Progressbar(list_contents, orient=HORIZONTAL, length=100,
                           mode='determinate')

    progress.place(anchor="c", relx=0.5, rely=0.5, width=150, height=30)
    files_total = Label(list_contents, text="Total Files: 0/0", bg="#ebe9e9")
    files_total.place(anchor="c", relx=0.5, rely=0.65)
    total_size = Label(list_contents, text="Total Size: 0/0", bg="#ebe9e9")
    total_size.place(anchor="c", relx=0.5, rely=0.74)
    percentage = Label(list_contents, text="Percentage: 0/100", bg="#ebe9e9")
    percentage.place(anchor="c", relx=0.5, rely=0.83)
    list_contents.place(anchor="c", relx=0.39, rely=0.8)
    progress_title = Label(app, text="Progress Bar", bg="white")
    progress_title.place(anchor="c", relx=0.10, rely=0.598)
    canvas.place(anchor="w", relx=0.07, rely=0.55)

    # copyright label
    copyright_label = Label(app, text="Copyright 2021")
    copyright_label.place(anchor="c", relx=0.5, rely=0.97)


# folder transfer page


def directory_transfer():
    global src_text_widget, dest_text_widget, canvas, progress_title, progress_label, list_contents

    # canvas body
    canvas = Canvas(app, width=1300, height=650, bg="#ffffff")

    # frame body
    canvas_body_frame = Frame(canvas, width=300, height=1350, bg="#d0cece")
    canvas_body_frame.place(anchor="c", relx=0.9, rely=0)

    Button(canvas_body_frame, text="COPY", width=30, height=3, bg="white", command=copy_folders).place(anchor="c",
                                                                                                       relx=0.5,
                                                                                                       rely=0.6)
    Button(canvas_body_frame, text="MOVE", width=30, height=3, bg="white", command=move_folder).place(anchor="c",
                                                                                                        relx=0.5,
                                                                                                        rely=0.65)
    Button(canvas_body_frame, text="TRACK", width=30, height=3, bg="white", command=track_folder).place(anchor="c",
                                                                                                        relx=0.5,
                                                                                                        rely=0.7)
    Button(canvas_body_frame, text="Copy Files instead", width=30, height=3, bg="white",
           command=file_transfer).place(anchor="c", relx=0.5, rely=0.9)
    Label(canvas, bg="white", text="Copy and Track files from one location "
                                   "to another location").place(anchor="c",
                                                                relx=0.4,
                                                                rely=0.05)
    Label(canvas, bg="white", image=folder_image).place(anchor="c", relx=0.26, rely=0.25)
    Label(canvas, bg="white", image=forward_image).place(anchor="c", relx=0.40, rely=0.25)
    Label(canvas, bg="white", image=folder_image).place(anchor="c", relx=0.53, rely=0.25)
    scrollbar_src = Scrollbar(canvas)
    scrollbar_src.place(anchor="c", relx=0.35, rely=0.41, height=70)
    src_text_widget = Text(canvas, bd=5, height=4, width=25, yscrollcommand=scrollbar_src.set)
    scrollbar_src.config(command=src_text_widget.yview)
    src_text_widget.place(anchor="c", relx=0.26, rely=0.41)
    scrollbar_dest = Scrollbar(canvas)
    scrollbar_dest.place(anchor="c", relx=0.62, rely=0.41, height=70)
    dest_text_widget = Text(canvas, bd=5, height=4, width=25, yscrollcommand=scrollbar_dest.set)
    dest_text_widget.place(anchor="c", relx=0.53, rely=0.41)
    scrollbar_dest.config(command=dest_text_widget.yview)
    Button(canvas, text="Open Source directory", command=lambda: get_files_from_folder("src")).place(anchor="c",
                                                                                                     relx=0.26,
                                                                                                     rely=0.5)
    Button(canvas, text="Open Destination directory", command=lambda: get_files_from_folder("dest")).place(anchor="c",
                                                                                                           relx=0.53,
                                                                                                           rely=0.5)
    list_contents = Frame(canvas, width=1030, height=290, bg="#ebe9e9")
    progress_label = Label(list_contents, image=progress_image)
    progress_label.place(anchor="c", relx=0.5, rely=0.2)
    progress = Progressbar(list_contents, orient=HORIZONTAL, length=100,
                           mode='determinate')

    progress.place(anchor="c", relx=0.5, rely=0.45, width=150, height=30)
    files_total = Label(list_contents, text="Total Files: 0/0", bg="#ebe9e9")
    files_total.place(anchor="c", relx=0.5, rely=0.65)
    total_size = Label(list_contents, text="Total Size: 0/0", bg="#ebe9e9")
    total_size.place(anchor="c", relx=0.5, rely=0.74)
    percentage = Label(list_contents, text="Percentage: 0/100", bg="#ebe9e9")
    percentage.place(anchor="c", relx=0.5, rely=0.83)
    list_contents.place(anchor="c", relx=0.39, rely=0.8)
    progress_title = Label(app, text="Progress Bar", bg="white")
    progress_title.place(anchor="c", relx=0.10, rely=0.598)
    canvas.place(anchor="w", relx=0.07, rely=0.55)

    # copyright label
    copyright_label = Label(app, text="Copyright 2021")
    copyright_label.place(anchor="c", relx=0.5, rely=0.97)


# home page


def homepage():
    # top menu frame
    top_menu_frame = Frame(app, width=1920, height=60)

    # file menu button
    file_menu_btn = Menubutton(top_menu_frame, text="File", relief=RAISED, bd=0,
                               activeforeground="white", activebackground="blue")
    # file menu
    file_menu = Menu(file_menu_btn, tearoff=0)
    file_menu_btn["menu"] = file_menu
    file_menu.add_command(label="New")
    file_menu.add_command(label="Save")
    file_menu.add_command(label="Save As")
    file_menu.add_command(label="Exit")
    file_menu_btn.place(anchor="c", relx=0.01, rely=0.745)

    # edit menu button
    edit_menu_btn = Menubutton(top_menu_frame, text="Edit", relief=RAISED, bd=0,
                               activeforeground="white", activebackground="blue")
    edit_menu_btn.place(anchor="c", relx=0.026, rely=0.745)
    # edit menu
    edit_menu = Menu(edit_menu_btn, tearoff=0)
    edit_menu_btn["menu"] = edit_menu
    edit_menu.add_command(label="Find")
    edit_menu.add_command(label="Replace")

    # view menu button
    view_menu_btn = Menubutton(top_menu_frame, text="View", relief=RAISED, bd=0,
                               activeforeground="white", activebackground="blue")
    # view menu
    view_menu = Menu(view_menu_btn, tearoff=0)
    view_menu_btn["menu"] = view_menu
    view_menu.add_command(label="Themes")
    view_menu.add_command(label="Preferences")
    view_menu_btn.place(anchor="c", relx=0.044, rely=0.745)

    # help menu button
    help_menu_btn = Menubutton(top_menu_frame, text="Help", relief=RAISED, bd=0,
                               activeforeground="white", activebackground="blue")
    # help menu
    help_menu = Menu(help_menu_btn, tearoff=0)
    help_menu_btn["menu"] = help_menu
    help_menu.add_command(label="About")
    help_menu.add_command(label="Update")
    help_menu_btn.place(anchor="c", relx=0.063, rely=0.745)

    top_menu_frame.place(anchor="w", relx=0, rely=0)

    # canvas separator
    canvas = Canvas(app, width=1920, height=0.5, bg="#d0cece")
    canvas.create_line(50, 50, 100, 100)
    canvas.place(anchor="w", relx=0, rely=0.035)

    # Tutorials label
    tuts_label = Button(app, text="Tutorials", bd=0)
    tuts_label.place(anchor="c", relx=0.02, rely=0.05)

    # Vertical label
    vertical_label = Button(app, text="     |     ", bd=0)
    vertical_label.place(anchor="c", relx=0.05, rely=0.05)

    # Docs label
    docs_label = Button(app, text="Docs", bd=0)
    docs_label.place(anchor="c", relx=0.07, rely=0.05)

    # canvas separator
    canvas = Canvas(app, width=1920, height=0.5, bg="#d0cece")
    canvas.create_line(50, 50, 100, 100)
    canvas.place(anchor="w", relx=0, rely=0.065)

    # canvas title
    canvas = Canvas(app, width=1220, height=55, bg="#ffffff")
    Label(canvas, text="COPY AND TRACK FILES VERSION 1.0", fg="blue", bg="white").place(
        anchor="c", relx=0.5, rely=0.5)
    canvas.place(anchor="w", relx=0.1, rely=0.12)

    # canvas body
    canvas = Canvas(app, width=1300, height=650, bg="#ffffff")

    Label(canvas, bg="white", text="Copy and Track Folders and Files from one location "
                                   "to another location").place(anchor="c",
                                                                relx=0.5,
                                                                rely=0.05)
    Label(canvas, bg="white", image=folder_image).place(anchor="c", relx=0.36, rely=0.25)
    Label(canvas, bg="white", image=forward_image).place(anchor="c", relx=0.50, rely=0.25)
    Label(canvas, bg="white", image=folder_image).place(anchor="c", relx=0.63, rely=0.25)
    Button(canvas, text="Transfer & Track Folders", width=50, height=3, bg="white",
           command=directory_transfer, bd=3).place(anchor="c", relx=0.5, rely=0.45)
    Label(canvas, bg="white", image=file_image).place(anchor="c", relx=0.36, rely=0.65)
    Label(canvas, bg="white", image=forward_image).place(anchor="c", relx=0.50, rely=0.65)
    Label(canvas, bg="white", image=folder_image).place(anchor="c", relx=0.63, rely=0.65)
    Button(canvas, text="Transfer & Track Files", width=50, height=3, bg="white", command=file_transfer,
           bd=3).place(anchor="c", relx=0.5, rely=0.85)
    canvas.place(anchor="w", relx=0.07, rely=0.55)


# --- app content ends --- #


homepage()

# keep app alive
app.mainloop()
