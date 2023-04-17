import re
import io
import webbrowser
from threading import Timer
import customtkinter


class editor(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Just add this search function:
        import sys, os

        def resource(relative_path):
            base_path = getattr(
                sys,
                '_MEIPASS',
                os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)

        # Then use this function to find the asset, eg: resource("my_file")
        import pyglet, tkinter
        VayuSans = pyglet.font.add_file('VayuSans-Bold\VayuSans-Bold.ttf')


        self.title("BBCode editor")
        self.geometry("885x450")
        self.resizable(False, False)
        self.configure(fg_color="#0d1015")

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=2, columnspan=7, padx=(2.5, 5), pady=5, sticky="nsew")
        self.textbox.configure(fg_color="#12171d",
                               wrap="none",
                               font=(VayuSans, 14),
                               scrollbar_button_color="#12171d",
                               scrollbar_button_hover_color="#12171d")

        self.lineNumber = customtkinter.CTkTextbox(master=self, width=55)
        self.lineNumber.grid(row=0, column=1, padx=(5, 2.5), pady=5, sticky="nsew")
        self.lineNumber.configure(fg_color="#0d1015",
                                  wrap="none",
                                  font=(VayuSans, 14),
                                  state='disabled',
                                  scrollbar_button_color="#0d1015",
                                  scrollbar_button_hover_color="#0d1015",)

        # Create a tag for the hyperlink
        self.textbox.tag_config("hyperlink", foreground="#05c0eb", underline=True)

        # Define a function that opens the link in a web browser
        def open_link(event):
            webbrowser.open_new(event.widget.get("3.8", "3.41"))

        # Bind the function to the "hyperlink" tag
        self.textbox.tag_bind("hyperlink", "<Control-Button-1>", open_link)
        self.textbox.insert("0.0", "# to scroll in this editor use scroll wheel for up/down\n# and shift + scroll wheel for left/right\n# help: ")
        self.textbox.insert("3.28", "https://osu.ppy.sh/wiki/en/BBCode\n\n", "hyperlink")

        def on_key_released(event):
            if self.textbox.get("0.0", "3.end") != "# to scroll in this editor use scroll wheel for up/down\n# and shift + scroll wheel for left/right\n# help: https://osu.ppy.sh/wiki/en/BBCode":
                self.textbox.delete("0.0", "3.end")
                self.textbox.insert("0.0", "# to scroll in this editor use scroll wheel for up/down\n# and shift + scroll wheel for left/right\n# help: ")
                self.textbox.insert("3.28", "https://osu.ppy.sh/wiki/en/BBCode\n\n", "hyperlink")

        # Bind the <KeyRelease> event to the callback function
        self.textbox.bind("<KeyRelease>", on_key_released)

        # Define functions for applying bbcode formatting to selected text
        def insert_bbcode(tag, has_option=False, multiline=False):
            index = self.textbox.index(tkinter.INSERT)
            option = f"={tag.upper()}" if has_option else ""
            content = f"\n\n" if multiline else " "
            self.textbox.insert(index, f"[{tag}{option}]{content}[/{tag}]")
            if multiline:
                self.textbox.mark_set("insert", "%d.0" % (int(index.split(".")[0]) + 1))
            else:
                self.textbox.mark_set("insert", "%d.%d" % (int(index.split(".")[0]), int(index.split(".")[1]) + len(f"[{tag}{option}]")))
            update_line_numbers()
            highlight_brackets()

        width = 120
        padx = 2.5
        pady = 2.5
        self.Bold = customtkinter.CTkButton(master=self, width=width, text="Bold", command=lambda: insert_bbcode("b")).grid(row=1, column=1, padx=(padx * 2, padx), pady=pady)
        self.Italic = customtkinter.CTkButton(master=self, width=width, text="Italic", command=lambda: insert_bbcode("i")).grid(row=1, column=2, padx=padx, pady=pady)
        self.Underline = customtkinter.CTkButton(master=self, width=width, text="Underline", command=lambda: insert_bbcode("u")).grid(row=1, column=3, padx=padx, pady=pady)
        self.Strike = customtkinter.CTkButton(master=self, width=width, text="Strike", command=lambda: insert_bbcode("strike")).grid(row=1, column=4, padx=padx, pady=pady)
        self.Color = customtkinter.CTkButton(master=self, width=width, text="Color", command=lambda: insert_bbcode("color", has_option=True)).grid(row=1, column=5, padx=padx, pady=pady)
        self.Font_Size = customtkinter.CTkButton(master=self, width=width, text="Font Size", command=lambda: insert_bbcode("size", has_option=True)).grid(row=1, column=6, padx=padx, pady=pady)
        self.Spoiler = customtkinter.CTkButton(master=self, width=width, text="Spoiler", command=lambda: insert_bbcode("spoiler")).grid(row=1, column=7, padx=(padx, padx * 2), pady=pady)

        self.Box = customtkinter.CTkButton(master=self, width=width, text="Box", command=lambda: insert_bbcode("box", has_option=True, multiline=True)).grid(row=2, column=1, padx=(padx * 2, padx), pady=pady)
        self.Spoilerbox = customtkinter.CTkButton(master=self, width=width, text="Spoilerbox", command=lambda: insert_bbcode("spoilerbox")).grid(row=2, column=2, padx=padx, pady=pady)
        self.Quote = customtkinter.CTkButton(master=self, width=width, text="Quote", command=lambda: insert_bbcode("quote", has_option=True, multiline=True)).grid(row=2, column=3, padx=padx, pady=pady)
        self.Code = customtkinter.CTkButton(master=self, width=width, text="Code", command=lambda: insert_bbcode("code", multiline=True)).grid(row=2, column=4, padx=padx, pady=pady)
        self.Center = customtkinter.CTkButton(master=self, width=width, text="Center", command=lambda: insert_bbcode("centre")).grid(row=2, column=5, padx=padx, pady=pady)
        self.URL = customtkinter.CTkButton(master=self, width=width, text="URL", command=lambda: insert_bbcode("url", has_option=True)).grid(row=2, column=6, padx=padx, pady=pady)
        self.Profile = customtkinter.CTkButton(master=self, width=width, text="Profile", command=lambda: insert_bbcode("profile", has_option=True)).grid(row=2, column=7, padx=(padx, padx * 2), pady=pady)

        self.List = customtkinter.CTkButton(master=self, width=width, text="List", command=lambda: insert_bbcode("list", multiline=True)).grid(row=3, column=1, padx=(padx * 2, padx), pady=(pady, pady * 2))
        self.Email = customtkinter.CTkButton(master=self, width=width, text="Email", command=lambda: insert_bbcode("email", has_option=True)).grid(row=3, column=2, padx=padx, pady=(pady, pady * 2))
        self.Images = customtkinter.CTkButton(master=self, width=width, text="Images", command=lambda: insert_bbcode("img")).grid(row=3, column=3, padx=padx, pady=(pady, pady * 2))
        self.Youtube = customtkinter.CTkButton(master=self, width=width, text="Youtube", command=lambda: insert_bbcode("youtube")).grid(row=3, column=4, padx=padx, pady=(pady, pady * 2))
        self.Audio = customtkinter.CTkButton(master=self, width=width, text="Audio", command=lambda: insert_bbcode("audio")).grid(row=3, column=5, padx=padx, pady=(pady, pady * 2))
        self.Heading = customtkinter.CTkButton(master=self, width=width, text="Heading", command=lambda: insert_bbcode("heading")).grid(row=3, column=6, padx=padx, pady=(pady, pady * 2))
        self.Notice = customtkinter.CTkButton(master=self, width=width, text="Notice", command=lambda: insert_bbcode("notice", multiline=True)).grid(row=3, column=7, padx=(padx, padx * 2), pady=(pady, pady * 2))

        def highlight_brackets(event=None):
            index = self.textbox.index("1.0")  # start at the beginning of the text
            while True:
                index = self.textbox.search("[", index, stopindex="end")  # search for a "["
                if not index:  # if no more "[" are found, break out of the loop
                    break
                end_index = self.textbox.search("]", index, stopindex="end")  # search for the corresponding "]"
                if not end_index:  # if no corresponding "]" is found, break out of the loop
                    break

                # Highlight the entire bracketed text
                start = f"{index}+1c"
                end = f"{end_index}"
                self.textbox.tag_add("bracket", start, end)

                index = end_index  # move to the end of the current bracket pair
                self.textbox.tag_add("bracket", index, end_index)  # add a tag to highlight the bracket


        self.textbox.tag_config("bracket", foreground="#5CFFFB")
        # Bind the highlight_brackets function to the "<Key>" event
        self.textbox.bind("<KeyRelease>", highlight_brackets)
        self.textbox.bind("<Button>", highlight_brackets)

        # Function to update line numbers
        def update_line_numbers(event=None):
            lines = self.textbox.get("1.0", "end-1c").count("\n") + 2
            self.lineNumber.configure(state="normal")
            self.lineNumber.delete("1.0", "end")
            self.lineNumber.insert("1.0", "\n".join(str(i) for i in range(1, lines)))
            self.lineNumber.configure(state="disabled")
            # Move line numbers with text area
            self.lineNumber.yview_moveto(self.textbox.yview()[0])

            # Move line numbers with text area
            def scroll_both(*args):
                self.lineNumber.yview_moveto(args[0])
                self.textbox.yview_moveto(args[0])

            self.textbox.configure(yscrollcommand=scroll_both)
            self.lineNumber.configure(yscrollcommand=scroll_both)

        # Bind to the KeyRelease event instead of Modified
        self.textbox.bind("<KeyRelease>", update_line_numbers)

        # Update line numbers when the window is opened
        self.bind("<Configure>", update_line_numbers)
        self.textbox.bind("<Button>", update_line_numbers)

        def update_html_page():
            start_index = self.textbox.index("1.0")
            end_index = self.textbox.index("end")
            text = self.textbox.get(start_index, end_index)
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
            text = re.sub(r'\n?^(?!\s*$)([^<>].*)$', r'<p>\1</p>', text, flags=re.MULTILINE)
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

            # Write the HTML code to a file
            with io.open('page.html', 'w', encoding='utf-8') as f:
                f.write(html_page)

            # Schedule the function to be executed again in 0.5 seconds
            Timer(0.5, update_html_page).start()

        # Start the timer
        update_html_page()

        # Run the exe in a separate thread to avoid interference with the tkinter window
        import threading
        threading.Thread(target=lambda: os.system("RunDisplay.vbs")).start()


if __name__ == "__main__":
    app = editor()
    app.mainloop()
