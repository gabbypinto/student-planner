from tkinter import *

app = Tk()

frame=Frame(app,width=500,height=500)
frame.grid(row=0,column=0)
canvas=Canvas(frame,bg='#FFFFFF',width=500,height=500,scrollregion=(0,0,500,800))

vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(yscrollcommand=vbar.set)
canvas.pack()

canvas.create_rectangle((200,300,300,600))

app.mainloop()
