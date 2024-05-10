
from sqlite3 import *
from webbrowser import open as urldisplay
from re import *
from tkinter.ttk import Progressbar
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from urllib.request import urlopen
from sys import exit as abort
from tkinter import PhotoImage
import re

student_number = 11569088
student_name = "Adi"


if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()


def download(url='https://www.abc.net.au/triplej/featured-music',
             target_filename='downloaded_document',
             filename_extension='html',
             save_file=True,
             char_set='UTF-8',
             incognito=False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception sometimes raised when a web server
    # denies access to a document
    from urllib.error import HTTPError

    # Import an exception raised when a web document cannot
    # be downloaded due to some communication error
    from urllib.error import URLError

    # Open the web document for reading (and make a "best
    # guess" about why if the attempt fails, which may or
    # may not be the correct explanation depending on how
    # well behaved the web server is!)
    try:
        if incognito:
            # Pretend to be a web browser instead of
            # a Python script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                               'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                               'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
            print("Warning - Request does not reveal client's true identity.")
            print("          This is both unreliable and unethical!")
            print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError as message:  # probably a syntax error
        print("\nCannot find requested document '" + url + "'")
        print("Error message was:", message, "\n")
        return None
    except HTTPError as message:  # possibly an authorisation problem
        print("\nAccess denied to document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None
    except URLError as message:  # probably the wrong server address
        print("\nCannot access web server at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None
    except Exception as message:  # something entirely unexpected
        print("\nSomething went wrong when trying to download " +
              "the document at URL '" + str(url) + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError as message:
        print("\nUnable to decode document from URL '" +
              url + "' as '" + char_set + "' characters")
        print("Error message was:", message, "\n")
        return None
    except Exception as message:
        print("\nSomething went wrong when trying to decode " +
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding=char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("\nUnable to write to file '" +
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents
# --------------------------------------------------------------------#


# -----Student's Solution---------------------------------------------#

# opening a connection to the database
connection = connect(database='media_reviews.db')
reviews_db = connection.cursor()

# Define the URL of the websites:
# (Tripple J - Radiostation)
url = 'https://www.abc.net.au/triplej/featured-music'
url1 = "https://bandcamp.com/live"  # (Bandcamp - Livestream)
url2 = "https://www.eventfinda.com.au/concerts-gig-guide/events/queensland"


# ---------Retreving recently played song for radio station 1. (Tripple J)---------
def get_recent_song(web_page_contents):
    pattern = r'<span[^>]*class="KeyboardFocus_keyboardFocus__uwAUh"[^>]*>(.*?)<\/span>'
    match = re.search(pattern, web_page_contents)

    if match:
        song_title = match.group(1).strip()
        # Some prefixes of the titles cause a coding error when printing. This line replaces aposthrephes in the titles ect.
        decoded_song_title = song_title.replace("&#x27;", "'")
        global current_song
        current_song = decoded_song_title
        return decoded_song_title
    else:
        return None


# Retrieveing the Artist
def get_artist(web_page_contents):
    pattern = r'<p\s+class="Typography_base__k7c9F TracklistCard_secondaryTitle__e1gyh Typography_sizeMobile16__Wygfe Typography_lineHeightMobile24__xwyV0 Typography_regular__Aqp4p Typography_colourInherit__xnbjy"\s+data-component="Text">(.*?)<\/p>'
    match = re.search(pattern, web_page_contents)

    if match:
        artist_title = match.group(1).strip()
        global current_artist
        current_artist = artist_title
        return artist_title
    else:
        return None


# Download the web page
web_page_contents = download(url)

if web_page_contents:
    # Extract the recently played song and artist
    song = get_recent_song(web_page_contents)
    artist = get_artist(web_page_contents)

    print("Recently Played Song:", song)
    print("By", artist)
else:
    print("Unable to download the web page.")


# ------Fucntion for BANDCAMP----------
def get_recent_live_stream(web_page_contents):
    pattern = r'<div\s+class="show-title"\s+data-bind="text:\s+title">(.*?)<\/div>'
    match = re.search(pattern, web_page_contents)

    if match:
        live_stream_title = match.group(1).strip()
        decoded_live_title = live_stream_title.replace("&#x27;", "'")

        # Get price of the event
        global price
        price = get_price_of_event(web_page_contents)

        return decoded_live_title, price
    else:
        return None, None


def get_price_of_event(web_page_contents):
    pattern = r'span\sclass="price"\sdata-bind="text:\sprice">([^<]+)<\/span>\s+<span\sclass="currency"\sdata-bind="text:\scurrency">([^<]+)<\/span>'
    match = re.search(pattern, web_page_contents)

    if match:
        get_price_of_event_title = match.group(1).strip()
        return get_price_of_event_title
    else:
        return None
# ---------evenfinda--------


def get_event_title(web_page_contents):
    pattern = r'<a[^>]+class="url summary">(.*?)<\/a>'
    match = re.search(pattern, web_page_contents)

    if match:
        event_title = match.group(1).strip()
        return event_title
    else:
        return None


def get_location_title(web_page_contents):
    pattern = r'<span class="p-locality"><a[^>]+class="location">(.*?)<\/a>,\s*(.*?)<\/span>'
    match = re.search(pattern, web_page_contents)

    if match:
        event_location = match.group(1).strip()
        return event_location
    else:
        return None


web_page_contents2 = download(url2)

# Displays the song and artist under the status table in the gui


def show_tripplej_summary(song):
    status_label.config(text="Current Song: " + song +
                        ' by ' + artist)


# Displays the livestream and price of the event
def show_bandcamp__summary(stream, price):
    status_label.config(text="Current Stream: " + stream + ', Price: ' + price)


# displays the title
def show_eventfinda_summary(event_title, event_location):
    if event_title is None:
        status_label.config(text="No event found.")
    else:
        status_label.config(text="Current Event: " +
                            event_title + " at " + event_location)

# This function sees if a checkbox has been checked and if so, it then downloads the webpage contents from the designated url and begins to search for the keywrods


def show_summary_wrapper():
    if value1.get() == 1:
        web_page_contents = download(url)
        song = get_recent_song(web_page_contents)
        show_tripplej_summary(song)
    elif value2.get() == 1:
        web_page_contents1 = download(url1)
        live_stream, price = get_recent_live_stream(web_page_contents1)
        show_bandcamp__summary(live_stream, price)
    elif value3.get() == 1:
        web_page_contents2 = download(url2)
        event_title = get_event_title(web_page_contents2)
        event_location = get_location_title(web_page_contents2)
        show_eventfinda_summary(event_title, event_location)
    else:
        status_label.config(text="No media source selected!")


def show_details():
    if value1.get() == 1:
        urldisplay(url)
    elif value2.get() == 1:
        urldisplay(url1)
    elif value3.get() == 1:
        urldisplay(url2)
        pass


# def confrim button value

def confirm_review():
    global current_song, current_artist, live_stream, price

    selected_rating = clicked.get()

    if selected_rating == "Select your rating":
        # No rating was selected, don't do anything
        return

    if value1.get() == 1:
        # Tripple J was selected
        review_data = (selected_rating, "Tripple J",
                       f"{current_song} by {current_artist}", url)
    elif value2.get() == 1:
        # Bandcamp was selected
        review_data = (selected_rating, "Bandcamp",
                       f"Stream: {live_stream}, Price: {price}", url1)

    elif value3.get() == 1:
        # eventfinda was selected
        event_title = get_event_title(web_page_contents2)
        event_location = get_location_title(web_page_contents2)
        review_data = (selected_rating, "Eventfinda",
                       f"{event_title} at {event_location}", url2)
    else:
        # Neither Tripple J nor Bandcamp were selected
        status_label.config(
            text="Please select a media source! ")
        return

    try:
        # Execute the insert query
        reviews_db.execute('''
            INSERT INTO reviews (review, event_source, event_summary, url)
            VALUES (?, ?, ?, ?)
        ''', review_data)

        # Commit the changes
        connection.commit()

        status_label.config(text='Review saved Successfully :) ')

    except Exception as e:
        print("An error occurred while saving the review:", str(e))


# Create the main window
task_2_main_window = Tk()
task_2_main_window.title("Adi's Album Auditions")

# setting window width and height and creating a frame
task_2_main_window.geometry('1300x600')
task_2_main_window.config(bg="#25242b")

# creating the top frame for the title
frame0 = LabelFrame(task_2_main_window, padx=200, pady=100, bg="#dcdbcf")
frame0.grid(row=0, column=0, padx=10, pady=10)

top_frame = Frame(frame0, bg="#dcdbcf")
top_frame.grid(row=0, column=0, columnspan=3)

# creating a title using custom fonts and colours
title = Label(top_frame, text="Adi's Album Auditions", font=(
    "Impact", 40, "bold"), bg="#dcdbcf", fg="#c73031")
title.grid(row=0, column=0, columnspan=3)

# Using downloaded imaege file in the top frame
image = PhotoImage(file="record1.png")
image_label = Label(top_frame, image=image, bg="#dcdbcf")
image_label.grid(row=1, column=0, columnspan=3)

# the below frames are now inside of frame0
frame1 = LabelFrame(frame0, text="2023's Top Auditions", font=("Impact", 20, "bold"),
                    padx=5, pady=5, width=350, height=250, bg="#25242b", fg="#f6f6f6")

frame1.grid(row=1, column=0, padx=10, pady=10)
frame1.grid_propagate(0)

frame2 = LabelFrame(frame0, text="Status", padx=5, pady=5, font=("Impact", 20, "bold"),
                    bg="#25242b", width=300, height=180, fg="#f6f6f6")
frame2.grid(row=1, column=1, padx=10, pady=10)
status_label = Label(frame2, text="Please select a live Audition...",
                     font=("Times New Roman", 20, "bold"), bg="#25242b", fg="#f6f6f6", wraplength=300)
status_label.grid(row=0, column=0)
frame2.grid_propagate(0)

frame3 = LabelFrame(frame0, text="Ratings", padx=5, pady=5,
                    bg="#25242b", fg="#f6f6f6",  width=300, height=180, font=("Impact", 20, "bold"))
frame3.grid(row=1, column=2, padx=10, pady=10)
frame3.grid_propagate(0)


# creates a working function where if the user clicks a checkbox, it updates the status description.

# 1st radio station


def update_label():
    status_list = []
    if value1.get() == 1:
        status_list.append("Tripple J selected")
    if value2.get() == 1:
        status_list.append("Bandcamp selected")
    if value3.get() == 1:
        status_list.append("Eventfinda Selected")

    if len(status_list) > 0:
        status_label.config(text=", ".join(status_list))
    else:
        status_label.config(text="Please select a live Audition...")


# creating checkboxes
value1 = IntVar()
value2 = IntVar()
value3 = IntVar()
var = IntVar()

Chkbutton1 = Checkbutton(frame1, text="Tripple J (Radio)", fg="#f6f6f6",
                         activeforeground="#f6f6f6",
                         selectcolor=task_2_main_window.cget("bg"),
                         bg="#25242b", variable=value1,
                         font=("Times New Roman bold", 16), command=update_label)

Chkbutton2 = Checkbutton(frame1, text="Bandcamp (Livestream)", fg="#f6f6f6",
                         activeforeground="#f6f6f6",
                         selectcolor=frame1.cget("bg"),
                         bg="#25242b", variable=value2, font=("Times New Roman bold", 16), command=update_label)

Chkbutton3 = Checkbutton(frame1, text="Eventfinda (Events)", fg="#f6f6f6",
                         activeforeground="#f6f6f6",
                         selectcolor=frame1.cget("bg"),
                         bg="#25242b", variable=value3, font=("Times New Roman bold", 16), command=update_label)

Chkbutton1.grid(row=0, column=0, sticky='w', padx=5, pady=5)
Chkbutton2.grid(row=1, column=0, sticky='w', padx=5, pady=5)
Chkbutton3.grid(row=2, column=0, sticky='w', padx=5, pady=5)

# Creating buttons show summary and show details
buttons_frame = Frame(frame1, bg="#25242b")
buttons_frame.grid(row=3, column=0, pady=10)

button1 = Button(buttons_frame, text="Show summary", bg="#25242b",
                 font=("Times New Roman", 15), command=show_summary_wrapper)

button2 = Button(buttons_frame, text="Show details", bg="#25242b",
                 font=("Times New Roman", 15), command=show_details)

button1.grid(row=0, column=0, padx=(0, 5))
button2.grid(row=0, column=1, padx=(5, 0))


# creating a drop down menue where the user can leave a review.
clicked = StringVar()
clicked.set("Select your rating")
drop = OptionMenu(frame3, clicked,  "1-Terrible",
                  "2-Mediocre", "3-Good", "4-Excellent", "5-Outstanding")

button4 = Button(frame3, bg="#25242b",  text="Confirm",
                 font=("Times New Roman", 15), command=confirm_review)

drop.grid(row=0, column=0)
# Set a fixed width for the dropdown menu
drop.config(width=10)
button4.grid(row=2, column=0, sticky='w')


# Start the event loop to detect user inputs
task_2_main_window.mainloop()
