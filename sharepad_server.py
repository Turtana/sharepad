import tkinter as tk
import socket

root = tk.Tk()
root.title("Sharepad")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

T = tk.Text(root,
            height=10,
            width=30,
            wrap=tk.WORD)

kopypasta = " "
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

##################

#    FUNKTIOT

#################

def tallennus():
    t = T.get("1.0", 'end-1c')
    print("Saved:")
    print(t)
    filu = open("textdump.txt","w")
    filu.write(t)
    filu.close()

def lataus():
    try:
        filu = open("textdump.txt","r")
        t = filu.read()
        T.delete("1.0", 'end-1c')
        T.insert('end', t)
        filu.close()
        print("Loaded:")
        print(t)
    except FileNotFoundError:
        print("No file!")

def paivitys():
    global conn
    global s

    if paivita.cget("text") == "Disconnect":
        global conn
        conn.send(str.encode("%CONNECTIONLOST"))
        paivita.config(text="Connect")
        conn.close()
        info.config(text="Disconnected")
        try:
            conn.send(str.encode("%CONNECTIONLOST"))
        except:
            print("The other one disconnected already")
        return
        
    
    host = socket.gethostbyname(socket.gethostname())
    port = 9025 # Vaikka tuosta portista

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    

    while True:
        
        conn, addr = s.accept()
        T.delete("1.0", 'end-1c')
        
        paivita.config(text="Disconnect")
        info.config(text="Connected: " + addr[0])
        conn.sendto(str.encode(kopypasta), addr)
        print("Sent: " + kopypasta)
        print("Client says: " + conn.recvfrom(1024)[0].decode())
        conn.settimeout(0.1)
        # TESTIYHTEYS
        #conn.close()
        break
        
    
    print("Connected")

def leikkaus():
    global kopypasta
    try:
        kopypasta = T.selection_get()
        T.delete(tk.SEL_FIRST,tk.SEL_LAST)
        print("Cut:")
        print(kopypasta)
        conn.send(str.encode("#" + kopypasta))
        conn.send(str.encode(T.get("1.0", 'end-1c')))
    except BaseException:
        print("No selections.")

def kopiointi():
    global kopypasta
    try:
        kopypasta = T.selection_get()
        print("Copied:")
        print(kopypasta)
        conn.send(str.encode("@" + kopypasta))
    except BaseException:
        print("No selections.")
    

def liitanta():
    try:
        T.delete(tk.SEL_FIRST,tk.SEL_LAST)
    except:
        print("No selections.")
    
    T.insert(tk.INSERT, kopypasta)
    print("Pasted:")
    print(kopypasta)
    conn.send(str.encode(T.get("1.0", 'end-1c')))

def nappain(event):
    try:
        conn.send(str.encode(T.get("1.0", 'end-1c') + event.char))
    except:
        return

######################

#     NAPPULAT

######################

tallenna = tk.Button(root,
                     text="Save",
                     width=10,
                     padx=2,
                     command=tallennus)

lataa = tk.Button(root,
                  text="Load",
                  width=10,
                  padx=2,
                  command=lataus)

paivita = tk.Button(root,
                    text="Connect",
                    width=10,
                    padx=2,
                    command=paivitys)

kopioi = tk.Button(root,
                    text="Copy",
                    width=10,
                    padx=2,
                    command=kopiointi)

leikkaa = tk.Button(root,
                    text="Cut",
                    width=10,
                    padx=2,
                    command=leikkaus)

liita = tk.Button(root,
                    text="Paste",
                    width=10,
                    padx=2,
                    command=liitanta)

info = tk.Label(root,
                text="No connection",
                width=30)

#################################

#      SIJOITUS RUUDUKKOON      #

#################################

T.grid(row=1, columnspan=3, sticky=tk.NSEW)
tallenna.grid(row=0, column=0, sticky=tk.NSEW)
lataa.grid(row=0, column=1, sticky=tk.NSEW)
paivita.grid(row=0, column=2, sticky=tk.NSEW)
kopioi.grid(row=2, column=0, sticky=tk.NSEW)
leikkaa.grid(row=2, column=1, sticky=tk.NSEW)
liita.grid(row=2, column=2, sticky=tk.NSEW)
info.grid(row=3, columnspan=3, sticky=tk.NSEW)

T.bind("<Key>", nappain)

########################

T.insert('end', socket.gethostbyname(socket.gethostname()))

while True:
    root.update_idletasks()
    root.update()

    try:
        data = conn.recv(1024).decode()
        if data[0] == "@":
            kopypasta = data[1:]
            continue
        if data[0] == "#":
            kopypasta = data[1:]
            data = conn.recv(1024).decode()
            T.delete("1.0", 'end-1c')
            T.insert('end', data)
            continue
        if data == "%CONNECTIONLOST":
            paivitys()
            continue
        T.delete("1.0", 'end-1c')
        T.insert('end', data)
    except:
        continue
