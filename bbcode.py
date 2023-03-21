# Import the necessary modules
import re
from tkinter import *
import os
import io
import webbrowser
from threading import Timer

# Create the main window
root = Tk()
root.title("osu! BBCode editor")
root.keepclipboard = True

# Create a text editor widget
editor = Text(root)
editor.pack()

icon = PhotoImage(file="osu! bbcode editor.png")
# Set the icon of the root window
root.iconphoto(False, icon)

editor.config(width=106, wrap="none", insertbackground="white", bg="#333333", fg="white", padx=5, pady=5, font=("Vayu Sans", 11))

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
def insert_bbcode(tag, has_option=False, multiline=False):
    index = editor.index(INSERT)
    option = f"={tag.upper()}" if has_option else ""
    content = f"\n\n" if multiline else " "
    editor.insert(index, f"[{tag}{option}]{content}[/{tag}]")
    if multiline:
        editor.mark_set("insert", "%d.0" % (int(index.split(".")[0]) + 1))
    else:
        editor.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len(f"[{tag}{option}]")))


bold = lambda: insert_bbcode("b")
italic = lambda: insert_bbcode("i")
underline = lambda: insert_bbcode("u")
strikethrough = lambda: insert_bbcode("strike")
colour = lambda: insert_bbcode("color", has_option=True)
font_size = lambda: insert_bbcode("size", has_option=True)
spoiler = lambda: insert_bbcode("spoiler")
box = lambda: insert_bbcode("box", has_option=True, multiline=True)
spoilerbox = lambda: insert_bbcode("spoilerbox")
quote = lambda: insert_bbcode("quote", has_option=True, multiline=True)
code = lambda: insert_bbcode("code", multiline=True)
centre = lambda: insert_bbcode("centre")
url = lambda: insert_bbcode("url", has_option=True)
profile = lambda: insert_bbcode("profile", has_option=True)
list = lambda: insert_bbcode("list", multiline=True)
email = lambda: insert_bbcode("email", has_option=True)
images = lambda: insert_bbcode("img")
youtube = lambda: insert_bbcode("youtube")
audio = lambda: insert_bbcode("audio")
heading = lambda: insert_bbcode("heading")
notice = lambda: insert_bbcode("notice", multiline=True)


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
button_data = [
    ("Bold", bold),
    ("Italic", italic),
    ("Underline", underline),
    ("Strike", strikethrough),
    ("Colour", colour),
    ("Font Size", font_size),
    ("Spoiler", spoiler),
    ("Box", box),
    ("Spoilerbox", spoilerbox),
    ("Quote", quote),
    ("Code", code),
    ("Center", centre),
    ("URL", url),
    ("Profile", profile),
    ("List", list),
    ("Email", email),
    ("Images", images),
    ("YouTube", youtube),
    ("Audio", audio),
    ("Heading", heading),
    ("Notice", notice)
]

buttons = [Button(root, text=text, command=command, bg="#333", fg="#eee", font=("Vayu Sans", 12, "bold")) for
           text, command in button_data]

(bold_button, italic_button, underline_button, strikethrough_button, color_button, font_size_button,
 spoiler_button, box_button, spoilerbox_button, quote_button, code_block_button, center_button,
 url_button, profile_button, list_button, email_button, images_button, youtube_button,
 audio_button, heading_button, notice_button) = buttons

# Pack the buttons into a grid
editor.grid(row=0, column=0, columnspan=7)
buttons_grid = [
    (bold_button, 1, 0), (italic_button, 1, 1), (underline_button, 1, 2),
    (strikethrough_button, 1, 3), (color_button, 1, 4), (font_size_button, 1, 5),
    (spoiler_button, 1, 6), (box_button, 2, 0), (spoilerbox_button, 2, 1),
    (quote_button, 2, 2), (code_block_button, 2, 3), (center_button, 2, 4),
    (url_button, 2, 5), (profile_button, 2, 6), (list_button, 3, 0),
    (email_button, 3, 1), (images_button, 3, 2), (youtube_button, 3, 3),
    (audio_button, 3, 4), (heading_button, 3, 5), (notice_button, 3, 6)
]

for button, row, col in buttons_grid:
    button.grid(row=row, column=col)

# Set the size and border width of the buttons
button_size = 11
button_border = 5

buttons = [bold_button, italic_button, underline_button, strikethrough_button, color_button, font_size_button,
           spoiler_button, box_button, spoilerbox_button, quote_button, code_block_button, center_button,
           url_button, profile_button, list_button, email_button, images_button, youtube_button, audio_button,
           heading_button, notice_button]

for button in buttons:
    button.config(width=button_size, bd=button_border)


def update_html_page():
    start_index = editor.index("1.0")
    end_index = editor.index("end")
    text = editor.get(start_index, end_index)
    # Replace BBcode tags with HTML tags
    text = re.sub(r"!bbcode ", "", text)
    text = re.sub(r"\[b]", "<strong>", text)
    text = re.sub(r"\[/b]", "</strong>", text)
    text = re.sub(r"\[i]", "<i>", text)
    text = re.sub(r"\[/i]", "</i>", text)
    text = re.sub(r"\[u]", "<u>", text)
    text = re.sub(r"\[/u]", "</u>", text)
    text = re.sub(r"\[strike]", "<s>", text)
    text = re.sub(r"\[/strike]", "</s>", text)
    text = re.sub(r"\[color=(.*?)](.*?)\[/color]", r"<font color=\1>\2</font>", text)
    text = re.sub(r"\[size=(.*?)](.*?)\[/size]", r"<span class='font-\1'><span style='color: inherit;'>\2</span></span>", text)
    text = re.sub(r"\n?\[spoilerbox]", "<details><summary>Spoiler</summary>", text)
    text = re.sub(r"\n?\[/spoilerbox]", "</details>", text)
    text = re.sub(r"\n?\[centre]", "<div style='text-align: center; left: 600px;'>", text)
    text = re.sub(r"\n?\[/centre]", "</div>", text)
    text = re.sub(r"[ \n]?\[list]", "<ul>", text)
    text = re.sub(r"[ \n]?\[\*]", "<li>", text)
    text = re.sub(r"[ \n]?\[/list]", "</ul>", text)
    text = re.sub(r"\n?\[quote]", "<blockquote>", text)
    text = re.sub(r"\[/quote]", "</blockquote>", text)
    text = re.sub(r"\n?\[code]", "<pre><code>", text)
    text = re.sub(r"\[/code]", "</code></pre>", text)
    text = re.sub(r"\n?\[heading]", "<h1>", text)
    text = re.sub(r"\[/heading]", "</h1>", text)
    text = re.sub(r"\n?\[notice][ \n]", "<div class='notice'>", text)
    text = re.sub(r"\n?\[/notice]", "</div>", text)
    text = re.sub(r"[ \n]?\[box=(.*?)]", r"<details><summary>\1</summary><div class='indent'><br style='line-height: 10px;'>", text)
    text = re.sub(r"[ \n]?\[/box]", "</div></details>", text)
    text = re.sub(r"\[url=(.*?)](.*?)\[/url]", r"<a href='\1'>\2</a>", text)
    text = re.sub(r"\[profile=(.*?)](.*?)\[/profile]", r"<a href=https://osu.ppy.sh/users/\1><strong>\2</strong></a>", text)
    text = re.sub(r"\[email=(.*?)](.*?)\[/email]", r"<a href='mailto:\1'>\2</a>", text)
    text = re.sub(r"\[img](.*?)\[/img]", r"<img src='\1'></img>", text)
    text = re.sub(r"\[youtube](.*?)\[/youtube]", r"<div><iframe width='560' height='315' src=https://www.youtube.com/embed/\1></iframe></div>", text)
    text = re.sub(r"\[audio](.*?)\[/audio]", r"<audio src=\1></audio>", text)
    text = re.sub(r"\[spoiler](.*?)\[/spoiler]", r"<span style='background-color: #D9A7BC;'>\1</span>", text)
    text = re.sub(r'\n?^(?!\s*$)([^<>].*)$', r'<p>\1</p>', text, flags=re.MULTILINE)  # fix this shit
    text = re.sub(r"<p>ㅤ</p>|<p>\n</p>", "", text)

    html_page = "<html><head><style> @font-face {font-family: 'Vayu Sans'; src: url('VayuSans-Bold/VayuSans-Bold.ttf');}" \
                "* { font-family: 'Vayu Sans'; }" \
                "body {white-space: pre-wrap; background-color: #392E33; color: #D9A7BC; font-size: 20px;} " \
                ".notice {border: 2px solid #715C64; background-color: #2A2226; padding: 18px; border-radius: 5px; max-width: 1200px;} " \
                "a {color: #ADD8E6; text-decoration: none;} " \
                ".indent {margin: 0; padding-left: 20px;} " \
                "p {color: #f0dbe4; margin: 0; line-height: 1.2} " \
                "ul {margin: 0;} " \
                "details, summary { margin: 0;}" \
                ".inherit-styles {font-size: inherit; color: inherit; margin: inherit;} " \
                ".font-50 {font-size: 10;}" \
                ".font-85 {font-size: 17;}" \
                ".font-100 {font-size: 20;}" \
                ".font-150 {font-size: 30;}" \
                "strong {line-height: 20px;} i {line-height: 20px;} u {line-height: 20px;} s {line-height: 20px;}</style>" \
                f" </head><body>{text}</body></html>"

    # Create a directory for the HTML page
    os.makedirs('html_pages', exist_ok=True)

    # Write the HTML code to a file
    with io.open('html_pages/page.html', 'w', encoding='utf-8') as f:
        f.write(html_page)

    # Schedule the function to be executed again in 1 second
    Timer(1, update_html_page).start()


# Start the timer
update_html_page()

# open the html file in default web browser
# webbrowser.open('file://' + os.path.realpath("html_pages/page.html"))

# Run the exe in a subfolder in a separate thread to avoid interference with the tkinter window
import threading
threading.Thread(target=lambda: os.system("htmlDisplay.exe")).start()

# Start the main event loop
root.mainloop()
