from tkinter import * # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
app = Tk()

# Code to add widgets will go here...
#--------------------------------------------------------------------------
frame_search = Frame(app)
frame_search.grid(row=0, column=0)
lbl_search = Label(frame_search, text='Search by Query',
                   font=('bold', 12), pady=20)
lbl_search.grid(row=0, column=0, sticky=W)
query_search = StringVar()
query_search_entry = Entry(frame_search, textvariable=query_search, width=40)
query_search_entry.grid(row=0, column=1)

#------------------------------------------------------------------------
frame_fields = Frame(app)
frame_fields.grid(row=1, column=0)
# hostname
hostname_text = StringVar()
hostname_label = Label(frame_fields, text='hostname', font=('bold', 12))
hostname_label.grid(row=0, column=0, sticky=E)
hostname_entry = Entry(frame_fields, textvariable=hostname_text)
hostname_entry.grid(row=0, column=1, sticky=W)
# BRAND
brand_text = StringVar()
brand_label = Label(frame_fields, text='Brand', font=('bold', 12))
brand_label.grid(row=0, column=2, sticky=E)
brand_entry = Entry(frame_fields, textvariable=brand_text)
brand_entry.grid(row=0, column=3, sticky=W)
# RAM
ram_text = StringVar()
ram_label = Label(frame_fields, text='RAM', font=('bold', 12))
ram_label.grid(row=1, column=0, sticky=E)
ram_entry = Entry(frame_fields, textvariable=ram_text)
ram_entry.grid(row=1, column=1, sticky=W)
# FLASH
flash_text = StringVar()
flash_label = Label(frame_fields, text='Flash', font=('bold', 12), pady=20)
flash_label.grid(row=1, column=2, sticky=E)
flash_entry = Entry(frame_fields, textvariable=flash_text)
flash_entry.grid(row=1, column=3, sticky=W)



#------------------------------------------------------------------
app.title('Student Planner')
app.geometry('700x550')

app.mainloop()
