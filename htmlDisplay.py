import time
import threading
from pathlib import Path
import webview

def display_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # Add encoding='utf-8'
        return file.read()

def watch_file(file_path, window):
    global html_content
    last_modified_time = None
    while True:
        current_modified_time = Path(file_path).stat().st_mtime
        if last_modified_time != current_modified_time:
            last_modified_time = current_modified_time
            html_content = display_html(file_path)
            # Add buttons to open and close all details tags
            html_content = f'<button onclick="openAllDetails()">Open All</button><button onclick="closeAllDetails()">Close All</button>{html_content}'
            # Save the current state of the <details> tag
            details_state = window.evaluate_js(
                "Array.from(document.querySelectorAll('details')).map(details => details.open)")
            # Save the current scroll position
            scroll_position = window.evaluate_js("window.pageYOffset")
            window.load_html(html_content)
            # Add JavaScript functions to open and close all details tags
            window.evaluate_js("""
                function openAllDetails() {
                    Array.from(document.querySelectorAll('details')).forEach(details => details.open = true);
                }
                function closeAllDetails() {
                    Array.from(document.querySelectorAll('details')).forEach(details => details.open = false);
                }
            """)
            # Restore the state of the <details> tag after refresh
            for index, state in enumerate(details_state):
                window.evaluate_js(f"document.querySelectorAll('details')[{index}].open = {str(state).lower()}")
            # Restore the scroll position after refresh
            window.evaluate_js(f"window.scrollTo(0, {scroll_position})")
            time.sleep(0.2)

        # Wait for the file contents to change, checking every 0.25 seconds
        while True:
            new_html_content = display_html(file_path)
            if new_html_content != html_content:
                html_content = new_html_content
                break
            time.sleep(0.25)


def create_window(file_path):
    window = webview.create_window("HTML Viewer", width=1300, height=600)
    watch_thread = threading.Thread(target=watch_file, args=(file_path, window))
    watch_thread.daemon = True
    watch_thread.start()
    webview.start()

file_path = "page.html"
create_window(file_path)

