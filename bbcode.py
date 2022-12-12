# Import the necessary modules
from tkinter import *
import webbrowser

# Create the main window
root = Tk()
root.title("osu! BBCode editor")

# Create a text editor widget
editor = Text(root)
editor.pack()

icon = PhotoImage(file="icons/osu! bbcode editor.png")
# Set the icon of the root window
root.iconphoto(False, icon)

editor.configure(width=106)
editor.configure(wrap="none")
editor.configure(insertbackground="white")
editor.config(bg="#333333", fg="white")
editor.config(padx=5, pady=5)

index = editor.index(INSERT)
editor.insert(index, "# to scroll in this editor use scroll wheel for up/down\n# and shift + scroll wheel for left/right\n# help: ")

# Create a tag for the hyperlink
editor.tag_configure("hyperlink", foreground="#05c0eb", underline=True)

# Define a function that opens the link in a web browser
def open_link(event):
    webbrowser.open_new(event.widget.get("3.8", "3.end"))

# Bind the function to the "hyperlink" tag
editor.tag_bind("hyperlink", "<Control-Button-1>", open_link)

# Add the hyperlink to the text
index = editor.index("3.28")
editor.insert(index, "https://osu.ppy.sh/wiki/en/BBCode\n\n", "hyperlink")

# Define functions for applying bbcode formatting to selected text
def bold():
    index = editor.index(INSERT)
    editor.insert(index, "[b] [/b]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[b]")))  # move cursor up one line
def italic():
    index = editor.index(INSERT)
    editor.insert(index, "[i] [/i]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[i]")))  # move cursor up one line
def underline():
    index = editor.index(INSERT)
    editor.insert(index, "[u] [/u]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[u]")))  # move cursor up one line
def strikethrough():
    index = editor.index(INSERT)
    editor.insert(index, "[strike] [/strike]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[strike]")))  # move cursor up one line
def colour():
    index = editor.index(INSERT)
    editor.insert(index, "[color=HEXCODE] [/color]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[color=HEXCODE]")))  # move cursor up one line
def font_size():
    index = editor.index(INSERT)
    editor.insert(index, "[size=NUMBER (50,85,100,150)] [/size]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[size=NUMBER (50,85,100,150)]")))  # move cursor up one line
def spoiler():
    index = editor.index(INSERT)
    editor.insert(index, "[spoiler] [/spoiler]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[spoiler]")))  # move cursor up one line
def box():
    index = editor.index(INSERT)
    editor.insert(index, "[box=NAME]\n\n[/box]")
    editor.mark_set("insert", "%d.0" % (int(index.split(".")[0]) + 1))  # move cursor up one line
def spoilerbox():
    index = editor.index(INSERT)
    editor.insert(index, "[spoilerbox] [/spoilerbox]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[spoilerbox]")))  # move cursor up one line
def quote():
    index = editor.index(INSERT)
    editor.insert(index, "[quote=\"NAME\"]\n\n[/quote]")
    editor.mark_set("insert", "%d.0" % (int(index.split(".")[0]) + 1))  # move cursor up one line
def code():
    index = editor.index(INSERT)
    editor.insert(index, "[code]\n\n[/code]")
    editor.mark_set("insert", "%d.0" % (int(index.split(".")[0]) + 1))  # move cursor up one line
def centre():
    index = editor.index(INSERT)
    editor.insert(index, "[centre] [/centre]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[centre]")))  # move cursor up one line
def url():
    index = editor.index(INSERT)
    editor.insert(index, "[url=LINK] [/url]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[url]")))  # move cursor up one line
def profile():
    index = editor.index(INSERT)
    editor.insert(index, "[profile=USERID] username [/profile]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[profile=USERID]")))  # move cursor up one line
def list():
    index = editor.index(INSERT)
    editor.insert(index, "[list=TYPE]\n[*]\n[*]\n[/list]")
    editor.mark_set("insert", "%d.0" % (int(index.split(".")[0]) + 1))  # move cursor up one line
    current_line = editor.index("insert linestart")
    editor.mark_set("insert", f"{current_line} lineend")
def email():
    index = editor.index(INSERT)
    editor.insert(index, "[email=ADDRESS] [/email]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[email=ADDRESS]")))  # move cursor up one line
def images():
    index = editor.index(INSERT)
    editor.insert(index, "[img] ADDRESS [/img]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[img]")))  # move cursor up one line
def youtube():
    index = editor.index(INSERT)
    editor.insert(index, "[youtube] VIDEO_ID [/youtube]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[youtube]")))  # move cursor up one line
def audio():
    index = editor.index(INSERT)
    editor.insert(index, "[audio] URL [/audio]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[audio]")))  # move cursor up one line
def heading():
    index = editor.index(INSERT)
    editor.insert(index, "[heading] [/heading]")
    editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len("[heading]")))  # move cursor up one line
def notice():
    index = editor.index(INSERT)
    editor.insert(index, "[notice]\n\n[/notice]")
    editor.mark_set("insert", "%d.0" % (int(index.split(".")[0]) + 1))  # move cursor up one line

def on_key_released(event):
    # check if the first two lines are present in the editor
    if editor.get("1.0", "1.end") != "# to scroll in this editor use scroll wheel for up/down\n" \
            or editor.get("2.0", "2.end") != "# and shift + scroll wheel for left/right\n"\
            or editor.get("3.0", "3.end") != "# help: https://osu.ppy.sh/wiki/en/BBCode":
        # add the first two lines back to the editor
        editor.delete("1.0", "4.0")
        editor.insert("1.0", "# to scroll in this editor use scroll wheel for up/down\n# and shift + scroll wheel for left/right\n# help: ")
        index = editor.index("3.28")
        editor.insert(index, "https://osu.ppy.sh/wiki/en/BBCode\n", "hyperlink")

# Bind the <KeyRelease> event to the callback function
editor.bind("<KeyRelease>", on_key_released)

def highlight_brackets(event):
    index = editor.index("1.0")  # start at the beginning of the text
    while True:
        index = editor.search("[", index, stopindex="end")  # search for a "["
        if not index:  # if no more "[" are found, break out of the loop
            break
        end_index = editor.search("]", index, stopindex="end")  # search for the corresponding "]"
        if not end_index:  # if no corresponding "]" is found, break out of the loop
            break

        # Highlight the entire bracketed text
        start = f"{index}"
        end = f"{end_index}+1c"
        editor.tag_add("bracket", start, end)

        index = end_index  # move to the end of the current bracket pair

        # Search for the next "]" character
        end_index = editor.search("]", index, stopindex="end")
        if not end_index:  # if no more "]" are found, break out of the loop
            break
        editor.tag_add("bracket", index, end_index)  # add a tag to highlight the bracket
        index = end_index  # move to the end of the current bracket

editor.tag_configure("bracket", foreground="red")

# Bind the highlight_brackets function to the "<Key>" event
editor.bind("<Key>", highlight_brackets)
editor.bind("<Button>", highlight_brackets)

# Create buttons for applying function formatting
bold_button = Button(root, text="Bold", command=bold, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
italic_button = Button(root, text="Italic", command=italic, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
underline_button = Button(root, text="Underline", command=underline, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
strikethrough_button = Button(root, text="Strike", command=strikethrough, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
color_button = Button(root, text="Colour", command=colour, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
font_size_button = Button(root, text="Font Size", command=font_size, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
spoiler_button = Button(root, text="Spoiler", command=spoiler, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
box_button = Button(root, text="Box", command=box, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
spoilerbox_button = Button(root, text="Spoilerbox", command=spoilerbox, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
quote_button = Button(root, text="Quote", command=quote, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
code_block_button = Button(root, text="Code", command=code, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
center_button = Button(root, text="Center", command=centre, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
url_button = Button(root, text="URL", command=url, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
profile_button = Button(root, text="Profile", command=profile, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
list_button = Button(root, text="List", command=list, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
email_button = Button(root, text="Email", command=email, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
images_button = Button(root, text="Images", command=images, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
youtube_button = Button(root, text="YouTube", command=youtube, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
audio_button = Button(root, text="Audio", command=audio, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
heading_button = Button(root, text="Heading", command=heading, bg="#333", fg="#eee", font=("Arial", 12, "bold"))
notice_button = Button(root, text="Notice", command=notice, bg="#333", fg="#eee", font=("Arial", 12, "bold"))

# pack the buttons into a grid
editor.grid(row=0, column=0, columnspan=7)
bold_button.grid(row=1, column=0)
italic_button.grid(row=1, column=1)
underline_button.grid(row=1, column=2)
strikethrough_button.grid(row=1, column=3)
color_button.grid(row=1, column=4)
font_size_button.grid(row=1, column=5)
spoiler_button.grid(row=1, column=6)
box_button.grid(row=2, column=0)
spoilerbox_button.grid(row=2, column=1)
quote_button.grid(row=2, column=2)
code_block_button.grid(row=2, column=3)
center_button.grid(row=2, column=4)
url_button.grid(row=2, column=5)
profile_button.grid(row=2, column=6)
list_button.grid(row=3, column=0)
email_button.grid(row=3, column=1)
images_button.grid(row=3, column=2)
youtube_button.grid(row=3, column=3)
audio_button.grid(row=3, column=4)
heading_button.grid(row=3, column=5)
notice_button.grid(row=3, column=6)

# set the size of the buttons

size = 11

bold_button.config(width=size, bd=5)
italic_button.config(width=size, bd=5)
underline_button.config(width=size, bd=5)
strikethrough_button.config(width=size, bd=5)
color_button.config(width=size, bd=5)
font_size_button.config(width=size, bd=5)
spoiler_button.config(width=size, bd=5)
box_button.config(width=size, bd=5)
spoilerbox_button.config(width=size, bd=5)
quote_button.config(width=size, bd=5)
code_block_button.config(width=size, bd=5)
center_button.config(width=size, bd=5)
url_button.config(width=size, bd=5)
profile_button.config(width=size, bd=5)
list_button.config(width=size, bd=5)
email_button.config(width=size, bd=5)
images_button.config(width=size, bd=5)
youtube_button.config(width=size, bd=5)
audio_button.config(width=size, bd=5)
heading_button.config(width=size, bd=5)
notice_button.config(width=size, bd=5)

# Start the main event loop
root.mainloop()
