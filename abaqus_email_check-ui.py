# -*- coding: mbcs -*-

# """
#                                                                                                ..;fxxx?.
#                                                                                             .^1xf;.  .fn.
#                                                                                            .jx:.      .r.
#                                                                                          .fj '       .?n.
#                                                                                         'f) .     ..trf`.
#                                      .'.'                                              >x.      !xn} .
#                                     :r';"                                             }j     .`x)'
#                          .       ..rx ..j.                                          .)x..   .fx`.
#                       .rux.    . fn.  ..n`                                          .x` .  .jf
#                       .n.tj..  .f{.    .x.                                        .'x^    'ff.
#                       /j. nurc1-..     ./f/ .                                      :r.    :r.
#                       fl.zcJJJJY        ...!j1                                    .j!    .x..
#                       fczJJJJJJU           . in~.                                 .x..  .\j
#                     . xXJJYCJUJC              .fx.                               .>j   .'n.
#                     .jYJJCli!?!i..             .jr.                              .xj  ..rj.
#                    ./XJJJJi!!!!i!               .jf'                             .n'   .x'
#                    'cJJJJLi!!!!i.                'n^.                            .x.   jt.
#                    tzJJU!!!!!i!.                  'tjf(.   '.^)jrrrrx|; .       'x'. .;n.
#                   'nYJJQii`iii                      .`|..nnzzzJCJUUJJU[rnux/ ..lr".  ln .
#                   .nJJL.     l.                     .j<zcJJJJUJJJJJJC!!!!iilnv\    .\n..
#                    nn`      ,vr.                  ../tYJJJJJJJJJililli!!!!!!i>jf...nj .
#                   .n.      .jn.                   ..}.YCJJUCJCJ!!!!!!!!!!!!!!!!I'zx .
#                    xl.       ..                  .'t...i!!!tJJ!!!!!!!!!!!!!!!!!!..fj..
#                   .x\.'      `)(+. . .            f   .i!!!i .!!!!!!!!!!i:.i!!!!  . x^.
#                   .j .j        ;<; ..           .t" .  .. .' ..`i'!;"'.^'  .'l;...   x~.
#                  .j...t.       '    ..       .../                                   ..x'.
#                   /f..-        .`t..         .).      Date: 20241018              ,r.
#                   .xj             .-       '..                                        'x
#                    . xj..                                                              j.
#                       'txxj~ ^.                                                     ...?xrrr`'
#                          .'.`ff/..            BY:ERGOUGOU~  MEOW!              ..   .!!!!!,.`jt.
#                              .^|f'.                                         .UJJJJc!!!!!!i. .fr..
#                              .t' x:.                                       .UJJJJJ!i!!!!!!I  . xr.
#                           .'f[.  .j\.....                                   JJJJJJJ!X>!!!i.    .^fx..
#                          .,r      .:j!/.          '..                   .../\YJJJJJJJCv!l'....     f.
#                        . j).       .<r           ./t^              . .!rvxf. ixzcXXYUYzcr^>xncx}'.?j.
#                       .)r.        .vt'         .~n-..... ."~\jjxnxxxxfI'      .. .  .  .    .'. I?;.
#                      .xI.     .')nX,.        ',xj...'l_]_<".....
#                    `j/ .   ..<rxrr..       ..nr.
#                  .\j..   ..jrl\n..       .>xj.'
#                \jf.    .jnj..j\'.     ../xf'.
#                t'. '.]xn. `rx        .xn-.
#                .{^+tj.. .rx'     ..tnx...
#                       /f'..    '{xj
#                       "jl.  .~jj..
#                        ..)))"..
# """

import smtplib
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# from abaqus import *
# from abaqusConstants import *
# from caeModules import *
# from math import *
# from odbAccess import *

# Function to send email when Abaqus job completes
def abaqus_email(address, password, email_user):
    try:
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # SMTP server can be customized
        smtp.login(address, password)
        message = 'Subject:Abaqus\n\nThe analysis is completed'
        smtp.sendmail(email_user, address, message)
        smtp.quit()
        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")

# Function to check Abaqus job status in the log file
def check_abaqus_job_complet(filename, search_string='COMPLETED'):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print(content)

            if search_string in content:
                return True
            else:
                return False
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return False

# Function to monitor Abaqus job completion
def monitor_abaqus_job(filename, address, password, email_user, check_interval=10):
    print("Beginning to monitor...")
    email_sent = False

    while True:
        if check_abaqus_job_complet(filename):
            if not email_sent:
                abaqus_email(address, password, email_user)
                email_sent = True
            break
        else:
            print("Job is running, please wait...")
            time.sleep(check_interval)

    print("Monitoring over!")

# Function to open file dialog to select filename
def select_file():
    filename = filedialog.askopenfilename(
        title="Select Abaqus log file", filetypes=[("Log Files", "*.log"), ("All Files", "*.*")]
    )
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

# Function to start monitoring job with inputs from UI
def start_monitoring():
    filename = file_entry.get()
    address = email_entry.get()
    password = password_entry.get()
    email_user = email_user_entry.get()

    if filename and address and password and email_user:
        monitor_abaqus_job(filename, address, password, email_user)
    else:
        messagebox.showerror("Input Error", "Please fill in all fields.")

# GUI setup
root = tk.Tk()
root.title("Abaqus Job Monitor")

# UI for filename selection
tk.Label(root, text="Abaqus Log File:").grid(row=0, column=0, padx=10, pady=10)
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

# UI for email address
tk.Label(root, text="Your Email:").grid(row=1, column=0, padx=10, pady=10)
email_entry = tk.Entry(root, width=50)
email_entry.grid(row=1, column=1, padx=10, pady=10)

# UI for email password
tk.Label(root, text="Your Email Password:").grid(row=2, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, width=50, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=10)

# UI for sender email (user)
tk.Label(root, text="Sender Email (Optional):").grid(row=3, column=0, padx=10, pady=10)
email_user_entry = tk.Entry(root, width=50)
email_user_entry.grid(row=3, column=1, padx=10, pady=10)

# Start monitoring button
tk.Button(root, text="Start Monitoring", command=start_monitoring).grid(row=4, column=1, pady=20)

# Run the GUI loop
root.mainloop()
