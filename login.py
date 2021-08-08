from tkinter import *
from tkinter import messagebox
import psycopg2
from datetime import *
from centerscreen import *
from PIL import ImageTk, Image


class Login(Tk):
    """This class sets the login window
            STATUS 100%
    """

    def __init__(self):
        Tk.__init__(self)
        self.geometry(f'230x90+'
                      f'{centerx(self.winfo_screenwidth(), 230)}+{centery(self.winfo_screenheight(), 90)}')
        self.title("Login")
        self.iconphoto(True, ImageTk.PhotoImage(Image.open('Da.png')))
        self.resizable(False, False)
        self.login_label = Label(self, text='Username: ')  # Create label username
        self.login_label.grid(row=0, padx=10, pady=4)  # Label positioning
        self.login_entry = Entry(self)  # Create Entry for login input
        self.login_entry.grid(row=0, column=1)  # Entry positioning
        self.login_entry.insert(0, 'admin')  # Insert 'admin' to username

        self.pass_label = Label(self, text="Login")  # Create label password
        self.pass_label.grid(row=1, padx=10)  # Label positioning
        self.pass_entry = Entry(self, show="*")  # Create Entry for password input
        self.pass_entry.grid(row=1, column=1)  # Entry positioning
        self.pass_entry.insert(0, 'admin')  # Insert 'admin' to password

        self.button_login = Button(self, text='Login', width=8, command=self.check_user)  # Create login button
        self.button_login.place(x=60, y=55)  # Login button positioning

        self.button_exit = Button(self, text='Exit', width=8, command=self.destroy)  # Create exit button
        self.button_exit.place(x=130, y=55)  # Exit button positiong

    def check_user(self):  # Verify if user exist
        conn = psycopg2.connect(host='localhost', database='mylibrary', user='postgres', password='postgres')  # connect
        sql = "SELECT * FROM users WHERE username = '{}'".format(self.login_entry.get())  # SQL command to select user
        cur = conn.cursor()  # Create cursor for better control over the sql command
        cur.execute(sql)  # Uses var sql to select user
        users = cur.fetchone()  # Fetch cur.execute command to it

        if self.login_entry.get() and self.pass_entry.get():  # Check if these fields are 'blank'
            if users:  # If user exists, launches a new window
                MainWindow((users[0], users[2]))  # Sends user name to the main window

                self.destroy()  # destroy current window
            else:
                messagebox.showinfo("Warning", "Wrong username or password")  # Show a message if user doesn't exist
        else:
            messagebox.showinfo("Warning", "Please enter both username and password")  # Show a message if any field is
        conn.close()  # blank


class MainWindow(Tk):
    """
    This window is for the main window
    Here you'll find functionalities to search, add and delete books
    """

    def __init__(self, user_name):
        Tk.__init__(self)
        self.user = user_name
        self.title('Darling\'s Library')
        # self.iconphoto(True, PhotoImage(file='Da.png'))
        wx = 400  # Sets window width
        hy = 200  # Sets window height
        button_width = 15  # Sets buttons width
        dateaccess = datetime.now()
        self.dateaccessmonth, self.dateaccesshour = dateaccess.strftime("%d/%m/%Y"), dateaccess.strftime("%H:%M:%S")

        self.register_access()  # Register when an user access the system
        data_show = ("Accessed on " + self.dateaccessmonth + " at " + self.dateaccesshour)  # Creates a string
        # to show the data when the system was accessed
        self.geometry(f"{wx}x{hy}+"
                      f"{centerx(self.winfo_screenwidth(), wx)}+"
                      f"{centery(self.winfo_screenheight(), hy)}")  # Create the window
        # =========================================================================================================
        # ======= Username
        self.frame_data = Frame(self)  # Frame to hold username and time of access
        self.frame_data.pack()

        self.l_user_name_description = Label(self.frame_data,
                                             text=f'Acessador por: {user_name[1]} \t {data_show}')  # User
        self.l_user_name_description.pack(side=LEFT)

        # =========================================================================================================
        # ======= Frame Buttons (Search, Delete, Add, List All)
        self.centerFrame = Frame(self)  # Centers the buttons
        self.centerFrame.pack(pady=5)  # Frame centered

        self.frame_choice_LEFT = LabelFrame(self.centerFrame)  # Frame for the buttons on LEFT side
        self.frame_choice_LEFT.pack(side=LEFT, pady=5, padx=5)
        self.frame_choice_RIGHT = LabelFrame(self.centerFrame)  # Frame for the buttons on RIGHT side
        self.frame_choice_RIGHT.pack(side=RIGHT, pady=5, padx=5)
        # Button ADD on the LEFT
        self.button_Add = Button(self.frame_choice_LEFT, text='Add', width=button_width, command=self.open_Add)
        self.button_Add.pack()
        # Button SEARCH on the RIGHT
        self.button_Search = Button(self.frame_choice_RIGHT, text='Search', width=button_width, command=self.open_Search)
        self.button_Search.pack()
        # Button DELETE on the LEFT
        self.button_Delete = Button(self.frame_choice_LEFT, text='Delete', width=button_width, command=self.open_Delete)
        self.button_Delete.pack()
        # Button LISTALL on the RIGHT
        self.button_ListAll = Button(self.frame_choice_RIGHT, text='List all', width=button_width, state=DISABLED)
        self.button_ListAll.pack()

        # =========================================================================================================
        # ======= Buttons Frame
        self.frame_buttons = Frame(self)
        self.frame_buttons.pack(pady=15)
        # ======= Button logout
        self.button_login_window = Button(self.frame_buttons, text="Logout", width=button_width,
                                          command=self.return_to_login)  # Create a button to return to login
        self.button_login_window.pack(side=LEFT)

        # ======= Buttons exit
        self.button_exit = Button(self.frame_buttons, text='Exit', width=button_width, command=self.exit)
        self.button_exit.pack(side=RIGHT)
        # =========================================================================================================

    def register_logout(self):
        timelogout = datetime.now().strftime('%H:%M:%S')
        conn = psycopg2.connect(host='localhost', database='mylibrary', user='postgres', password='postgres')
        cur = conn.cursor()
        sql = f"UPDATE user_access SET timelogout = '{timelogout}' WHERE datetime = '{self.dateaccessmonth}'" \
              f" AND datehour = '{self.dateaccesshour}'"
        cur.execute(sql)
        conn.commit()
        conn.close()

    def exit(self):
        self.register_logout()
        self.destroy()

    def return_to_login(self):
        """Returns to login window"""
        self.destroy()
        self.register_logout()
        Login()

    def register_access(self):
        conn = psycopg2.connect(host='localhost', database='mylibrary', user='postgres', password='postgres')
        cur = conn.cursor()
        sql = f"INSERT INTO user_access VALUES " \
              f"('{self.user[0]}', '{self.user[1]}', '{self.dateaccessmonth}', '{self.dateaccesshour}')"
        cur.execute(sql)
        conn.commit()
        conn.close()

    # ================================================================================================================
    def open_Add(self):
        Add_Book()

    def open_Search(self):
        Search()

    def open_Delete(self):
        Delete()


# Class created to add books to the library
class Add_Book(Tk):
    def __init__(self):
        Tk.__init__(self)

        x = 300  # Sets window width
        y = 200  # Sets window height
        self.geometry(f'{x}x{y}+'
                      f'{int(self.winfo_screenwidth() / 2 - x / 2)}+{int(self.winfo_screenheight() / 2 - y / 2)}')
        self.title("Darling's Library - Add book")
        # self.config(font=('Verdana', 15))
        self.fields_frame = Frame(self)
        self.fields_frame.pack()
        self.num = self.bookid()
        # Grid to position fields
        # For each field label, there is on entry
        self.fieldid = Label(self.fields_frame, text='ID: ', anchor='w', width=10, )
        self.fieldid.grid(row=0, column=0, pady=1)
        self.fid_entry = Entry(self.fields_frame, width=5, state=NORMAL)
        self.fid_entry.insert(0, self.num)
        self.fid_entry.config(state=DISABLED)
        self.fid_entry.grid(row=0, column=1, sticky='w')

        self.field_title = Label(self.fields_frame, text='Title: ', anchor='w', width=10)
        self.field_title.grid(row=1, column=0, pady=1)

        self.f_title_entry = Entry(self.fields_frame, width=30)
        self.f_title_entry.grid(row=1, column=1, )

        self.field_author = Label(self.fields_frame, text='Author: ', anchor='w', width=10)
        self.field_author.grid(row=2, column=0, pady=1)

        self.f_author_entry = Entry(self.fields_frame, width=30)
        self.f_author_entry.grid(row=2, column=1)

        self.field_publisher = Label(self.fields_frame, text='Publisher: ', anchor='w', width=10)
        self.field_publisher.grid(row=3, column=0, pady=1)

        self.f_publisher_entry = Entry(self.fields_frame, width=30)
        self.f_publisher_entry.grid(row=3, column=1)
        # Buttons
        self.button_frame = Frame(self)
        self.button_frame.pack()

        self.b_add_desc = Button(self.button_frame, text='Add sinopse?', width=12, command=self.addsinopse,
                                 state=DISABLED)
        self.b_add_desc.grid(row=0, column=0, columnspan=2, sticky='we')

        self.b_save = Button(self.button_frame, text='Save', width=6, command=self.save)
        self.b_save.grid(row=1, column=0, padx=2, pady=10)

        self.b_exit = Button(self.button_frame, text='Exit', width=6, command=self.destroy)
        self.b_exit.grid(row=1, column=1, padx=2)

    def addsinopse(self):
        self.b_add_desc.destroy()
        x = 300
        y = 300
        self.geometry(f'{x}x{y}+'
                      f'{int(self.winfo_screenwidth() / 2 - x / 2)}+{int(self.winfo_screenheight() / 2 - y / 2)}')
        field_sinopse = Label(self.fields_frame, text='Sinopse', anchor='w', width=10)
        field_sinopse.grid(row=4, column=0, pady=1)

        f_sinopse_entry = Text(self.fields_frame, width=23, height=8)
        f_sinopse_entry.grid(row=4, column=1, )

    def bookid(self):
        conn = psycopg2.connect(host='localhost', database='mylibrary', user='postgres', password='postgres')
        cur = conn.cursor()
        cur.execute('SELECT last_value FROM books_id_seq')
        value = int(cur.fetchone()[0]) + 1
        conn.close()
        return value

        # self.fid_entry.config(state=NORMAL)  # Enables the field so it can receive the value
        # self.fid_entry.delete(0, END)
        # self.fid_entry.insert(0, num)  # Set the value
        # self.fid_entry.config(state=DISABLED)  # And DISABLE the entry again

    def save(self):
        conn = psycopg2.connect(host='localhost', database='mylibrary', user='postgres', password='postgres')
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM authors WHERE name='{self.f_author_entry.get()}'")
        author = cur.fetchone()
        cur.execute(f"SELECT id FROM publisher WHERE name='{self.f_publisher_entry.get()}'")
        publisher = cur.fetchone()

        if self.f_title_entry.get() and self.f_author_entry.get() and self.f_publisher_entry.get():
            cur.execute(f"SELECT title, author FROM books "
                        f"WHERE author=(SELECT id FROM authors WHERE name='{self.f_author_entry.get()}')"
                        f"AND id=(SELECT id from books WHERE title='{self.f_title_entry.get()}')")
            existe = cur.fetchone()

            if existe:
                messagebox.showwarning('Warning', 'Book already registered')
            else:
                if not author:
                    if not publisher:
                        cur.execute(f"INSERT INTO authors (name) VALUES ('{self.f_author_entry.get()}')")
                        cur.execute(f"INSERT INTO publisher (name) VALUES ('{self.f_publisher_entry.get()}')")
                        cur.execute(f"INSERT INTO books (title, publisher, author) "
                                    f"VALUES ('{self.f_title_entry.get()}',"
                                    f" (SELECT id FROM publisher WHERE name='{self.f_publisher_entry.get()}'),"
                                    f" (SELECT id FROM authors WHERE name='{self.f_author_entry.get()}'))")
                    else:
                        cur.execute(f"INSERT INTO authors (name) VALUES ('{self.f_author_entry.get()}')")
                        cur.execute(f"INSERT INTO books (title, publisher, author) "
                                    f"VALUES ('{self.f_title_entry.get()}',"
                                    f" (SELECT id FROM publisher WHERE name='{self.f_publisher_entry.get()}'),"
                                    f" (SELECT id FROM authors WHERE name='{self.f_author_entry.get()}'))")
                else:
                    if not publisher:
                        cur.execute(f"INSERT INTO publisher (name) VALUES ('{self.f_publisher_entry.get()}')")
                        cur.execute(f"INSERT INTO books (title, publisher, author) "
                                    f"VALUES ('{self.f_title_entry.get()}',"
                                    f" (SELECT id FROM publisher WHERE name='{self.f_publisher_entry.get()}'),"
                                    f" (SELECT id FROM authors WHERE name='{self.f_author_entry.get()}'))")
                    else:
                        cur.execute(f"INSERT INTO books (title, publisher, author) "
                                    f"VALUES ('{self.f_title_entry.get()}',"
                                    f" (SELECT id FROM publisher WHERE name='{self.f_publisher_entry.get()}'),"
                                    f" (SELECT id FROM authors WHERE name='{self.f_author_entry.get()}'))")
                messagebox.showinfo('Success', 'Successfully added to the database')

                if messagebox.askquestion('What now?', 'Add another book?') == 'yes':
                    self.num += 1
                    self.fid_entry.config(state=NORMAL)
                    self.fid_entry.delete(0, END)
                    self.fid_entry.insert(0, self.num)
                    self.fid_entry.config(state=DISABLED)
                    self.f_author_entry.delete(0, END)
                    self.f_title_entry.delete(0, END)
                    self.f_publisher_entry.delete(0, END)
                else:
                    self.destroy()
        else:
            messagebox.showwarning('Warning', 'Please fill out all the boxes')

        conn.commit()
        conn.close()


class Search(Tk):
    def __init__(self):
        Tk.__init__(self)
        x = 400
        y = 250
        self.geometry(f'{x}x{y}+'
                      f'{int(self.winfo_screenwidth()/2 - x/2)}+{int(self.winfo_screenheight()/2 - y/2)}')
        self.title('Search book')

        # Frame for the fields
        self.fields_frame = Frame(self)
        self.fields_frame.pack()
        # Search label
        self.l_search = Label(self.fields_frame, text='Search:', font=('Verdana', 12))
        self.l_search.grid(row=0, column=0, padx=4, pady=4)
        # Entry search
        self.e_search = Entry(self.fields_frame, font=('Verdana', 12), )
        self.e_search.grid(row=0, column=1)
        self.e_search.bind('<KeyRelease>', self.check)

        # Load books
        self.lbox_frame = Frame(self)
        self.lbox_frame.pack(fill=BOTH, expand=True,)
        # Scrollbar
        self.listbox_scrollbar = Scrollbar(self.lbox_frame, orient=VERTICAL)

        # Listbox
        self.listbox = Listbox(self.lbox_frame, yscrollcommand=self.listbox_scrollbar.set)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

        # config scrollbar
        self.listbox_scrollbar.config(command=self.listbox.yview)
        self.listbox_scrollbar.pack(side=RIGHT, fill=Y)

        # Button close
        self.b_frame = Frame(self)
        self.b_frame.pack()
        self.b_exit = Button(self.b_frame, text='Close', command=self.destroy, font=('Verdana', 10))
        self.b_exit.pack(side=LEFT, pady=5)

        # Create a list to populate the listbox
        self.list_listbox = []
        self.fill_list_box_list()
        self.populate_list_box(self.list_listbox)

    def check(self, e):
        """Check if what we typed is in the listbox and shows only what matches"""
        # Typed
        typed = self.e_search.get()

        if typed == '':
            data = self.list_listbox
        else:
            data = []
            for item in self.list_listbox:
                if typed.lower() in item.lower():
                    data.append(item)

        self.populate_list_box(data)

    def populate_list_box(self, data=None):
        """Populate the listbox"""
        # First, clears the listbox
        self.listbox.delete(0, END)

        # then add everthing to the listbox
        for i in data:
            self.listbox.insert(END, i)

    def fill_list_box_list(self):
        """Fill the list box"""
        conn = psycopg2.connect(host='localhost', database='mylibrary', user='postgres', password='postgres')
        cur = conn.cursor()
        cur.execute("SELECT * FROM booksview")
        rows = cur.fetchall()

        for title, aname, pname in rows:
            self.list_listbox.append(f'{title} - {aname} - {pname}')


class Delete(Tk):
    def __init__(self):
        Tk.__init__(self)
        x = 400
        y = 350
        self.geometry(f'{x}x{y}+'
                      f'{int(self.winfo_screenwidth() / 2 - x / 2)}+{int(self.winfo_screenheight() / 2 - y / 2)}')
        self.title('Delete')

        # Search entry
        self.f_search = Frame(self)
        self.f_search.pack()

        self.l_search = Label(self.f_search, text='Search', font=('Verdana', 12))
        self.l_search.grid(row=0, column=0, padx=5, pady=5)

        self.e_search = Entry(self.f_search, font=('Verdana', 12))
        self.e_search.grid(row=0, column=1)
        self.e_search.bind('<KeyRelease>', self.check)

        self.b_search = Button(self.f_search, text='Delete', font=('Verdana', 12), command=self.delete)
        self.b_search.grid(row=0, column=2, padx=5)

        # Radiobuttons
        self.opt = StringVar(value='book')

        self.radios_frame = Frame(self)
        self.radios_frame.pack()

        self.l_radios = Label(self.radios_frame, text='Search using: ')
        self.l_radios.grid(row=0, column=0)
        self.r_book = Radiobutton(self.radios_frame, text='Book title', variable=self.opt, value='book',
                                  command=lambda: self.check_radio(self.opt.get()))
        self.r_book.grid(row=0, column=1)

        self.r_author = Radiobutton(self.radios_frame, text='Author', variable=self.opt, value='author',
                                    command=lambda: self.check_radio(self.opt.get()))
        self.r_author.grid(row=0, column=2)

        self.r_publisher = Radiobutton(self.radios_frame, text='Publisher', variable=self.opt, value='publisher',
                                       command=lambda: self.check_radio(self.opt.get()))

        self.r_publisher.grid(row=0, column=3)

        for i in (self.r_book, self.r_author, self.r_publisher):
            i.config(state=DISABLED)

        # List books
        self.f_list = Frame(self)
        self.f_list.pack(fill=BOTH, expand=True, pady=5, padx=5)

        self.lbox_scroll = Scrollbar(self.f_list, orient=VERTICAL)
        self.lbox = Listbox(self.f_list, yscrollcommand=self.lbox_scroll.set, height=15)
        self.lbox.pack(side=LEFT, fill=BOTH, expand=True)

        self.lbox_scroll.config(command=self.lbox.yview)
        self.lbox_scroll.pack(side=RIGHT, fill=Y)

        # Button exit
        self.b_exit_frame = Frame(self)
        self.b_exit_frame.pack(pady=5)

        self.b_exit = Button(self.b_exit_frame, text='Close', font=('Verdana', 12), command=self.destroy)
        self.b_exit.pack()

        self.original_msg = 'You can search using book title and author or publisher name.'
        self.lbox.insert(END, self.original_msg)

        self.books_list = []
        self.populate_books_list()

    def check(self, e):
        """Verify if the book exist inside the list and print it to the listbox"""
        typed = self.e_search.get()

        if typed == '':
            self.lbox.delete(0, END)
            self.lbox.insert(END, self.original_msg)
        else:
            self.lbox.delete(0, END)
            for i in self.books_list:
                if typed.lower() in i.lower():
                    self.lbox.insert(END, i)

    def populate_books_list(self):
        """Populate the list"""
        conn = psycopg2.connect(host='localhost', database='mylibrary', user='postgres', password='postgres')
        cur = conn.cursor()
        cur.execute('SELECT * FROM booksview')
        books = cur.fetchall()

        for book, author, publisher in books:
            self.books_list.append(f'{book} -+- {author} -+- {publisher}')
        conn.close()

    def delete(self):
        conn = psycopg2.connect(host='localhost', database='mylibrary', user='postgres', password='postgres')
        cur = conn.cursor()

        book_to_delete = self.lbox.get(ANCHOR).split(' -+- ')
        if messagebox.askquestion('Delete?', f'I\'m about to delete: \n'
                                          f'\n{book_to_delete[0]} by {book_to_delete[1]}\n '
                                          f'from the database. \n\nConfirm?') == 'yes':
            cur.execute(f"DELETE FROM books WHERE title ILIKE '%{book_to_delete[0]}%'")
            conn.commit()
            messagebox.showinfo('Delete', 'Successfully deleted!')

            for i, v in enumerate(self.books_list):
                if book_to_delete[0] in v:
                    self.books_list.pop(i)

            self.e_search.delete(0, END)
            self.lbox.delete(0, END)
            self.lbox.insert(END, self.original_msg)

        else:
            self.e_search.delete(0, END)
            self.lbox.delete(0, END)
            self.lbox.insert(END, self.original_msg)
        conn.close()


if __name__ == "__main__":
    mainapp = Login()
    mainapp.mainloop()
