import tkinter as tk

def show_frame(frame):
    frame.tkraise()

window = tk.Tk()

# Fit the background immediately
window.state('zoomed')

# Fit the background responsive
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

# Display the first frame
frame1 = tk.Frame(window, bg='red')
frame2 = tk.Frame(window, bg='red')
frame3 = tk.Frame(window, bg='red')
frame_lst = [frame1, frame2, frame3]
for frame in frame_lst:
    frame.grid(row=0, column=0, sticky='nsew')

# Frame 1 code
frame1_title = tk.Label(frame1,  text='This is frame 1', bg='red')
frame1_title.pack(fill='x')

frame1_btn = tk.Button(frame1, text='Enter', command=lambda:show_frame(frame2))
frame1_btn.pack()

# Frame 2 code
frame2_title = tk.Label(frame2,  text='This is frame 2', bg='green')
frame2_title.pack(fill='x')

frame2_btn = tk.Button(frame2, text='Enter', command=lambda:show_frame(frame3))
frame2_btn.pack()

# Frame 3 code
frame3_title = tk.Label(frame3,  text='This is frame 3', bg='blue')
frame3_title.pack(fill='x')

frame3_btn = tk.Button(frame3, text='Enter', command=lambda:show_frame(frame1))
frame3_btn.pack()

show_frame(frame1)

window.mainloop()