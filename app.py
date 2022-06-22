import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data
import webbrowser
from tkinter import *
import os
import sqlite
from PIL import ImageTk, Image
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.use
path = os.getcwd()
root = Tk()
root.geometry('600x500')
root.resizable(width=False, height=False)
root.title("BAT")

# Labels
TitleLabel = Label(root, text="Bitcoin Analysis Tool", width=30, font=("Adobe Caslon Pro Bold", 35)).place(x=-100, y=20)
InfoLabel = Label(root, text="Use the entry boxes at the bottom to enter a block, transaction ID or Address.\n \
 A notepad is provided, containing examples.").place(x=100,y=90)

BlockLabel = Label(root, text="Block").place(x=30, y=300)
TransactionLabel = Label(root, text="Transaction").place(x=30, y=350)
AddressLabel = Label(root, text="Address").place(x=30, y=400)

# Radio Buttons
v = IntVar()
v.set(0)
r1 = Radiobutton(root, text="", variable=v, value=1,
                indicator=0, width=2, height=1, background="white").place(x=340, y=150)
r2 = Radiobutton(root, text="", variable=v, value=2,
                indicator=0, width=2, height=1, background="white").place(x=340, y=190)
r3 = Radiobutton(root, text="", variable=v, value=3,
                indicator=0, width=2, height=1, background="white").place(x=340, y=230)

r1Label = Label(root, text="blocks.db", font=("Adobe Caslon Pro Bold", 10)).place(x=370, y=150)
r2Label = Label(root, text="transactions.db", font=("Adobe Caslon Pro Bold", 10)).place(x=370, y=190)
r3Label = Label(root, text="address.db", font=("Adobe Caslon Pro Bold", 10)).place(x=370, y=230)

# Entry
entry1 = Entry(root, width=30, font=("Calibri", 20))
entry1.place(x=100, y=300)
entry2 = Entry(root, width=30, font=("Calibri", 20))
entry2.place(x=100, y=350)
entry3 = Entry(root, width=30, font=("Calibri", 20))
entry3.place(x=100, y=400)

# Redirect to dbbrowser
def callback(url):
    webbrowser.open_new(url)

text1 = Label(root, text="This software requires DB Browser to view the SQLite database")
link1 = Label(root, text=" Link to DB Browser", fg="blue", cursor="hand2")
text1.place(x=100, y=450)
link1.place(x=450, y=450)

link1.bind("<Button-1>", lambda e: callback("https://sqlitebrowser.org/dl/"))

# Assign filepath and open db
def viewDB(id):
    if id == 1:
        filename = path + '\\Database\\blocks.db'
        os.system("start " + filename)
    if id == 2:
        filename = path + '\\Database\\transactions.db'
        os.system("start " + filename)
    if id == 3:
        filename = path + '\\Database\\address.db'
        os.system("start " + filename)


viewButton = Button(root, text="View Database", font=("Calibri", 20), width=15, command=lambda: viewDB(v.get()))
viewButton.place(x=100, y=140)

# Open results page based on radio button selected
def getresults(id):
    print(id)
    if id == 1:
        blockdata = data.graphblock()
        blockResultScreen(blockdata)
    elif id == 2:
        txdata = data.graphtx()
        txResultScreen(txdata)
    elif id == 3:
        addrdata = data.graphaddr()
        addrResultScreen(addrdata)
    else:
        print("Something went wrong")


resultsButton = Button(root, text="View Results", font=("Calibri", 20), width=15,
                       command=lambda: getresults(v.get()))
resultsButton.place(x=100, y=200)
deletedbButton = Button(root, text="Delete DB", font=("Calibri", 10), width=10,
                  command=lambda: sqlite.deleteDB(v.get()))
deletedbButton.place(x=480,y=220)

# Open block with 'next_block' string
def nextblock(nextblock):
    newblock = nextblock[2:-2]
    dataframe = data.get_block(newblock)
    block(dataframe)

# Open block with 'prev_block' string
def prevblock(prevblock):
    prevblock = str(prevblock)
    dataframe = data.get_block(prevblock)
    block(dataframe)

def blocktoDB(dataframe):
    sqlite.create_connection(path + '\\Database\\blocks.db', dataframe.T)

def txtoDB(dataframe, df):
    sqlite.create_connection(path + "\\Database\\transactions.db", dataframe.T)
    sqlite.create_connection(path + "\\Database\\inputs.db", df)

def addresstoDB(dataframe):
    sqlite.create_connection(path + '\\Database\\address.db', dataframe.T)

def blocksearch():
    string = entry1.get()
    print(string)
    dataframe = data.get_block(string)
    block(dataframe)

def block(dataframe):
    blockscreen = Toplevel(root)  # Child window
    blockscreen.geometry("600x550")  # Size of the window
    blockscreen.title("Block Viewer")
    blockscreen.resizable(0, 0)
    for i in [200, 320, 150]:
        Frame(blockscreen, height=i, width=600, bg='white', highlightbackground='GREY', highlightthickness=0.5).pack()
    counter = 0
    if dataframe.shape[0] == 17:
        dataframe.drop(dataframe.tail(1).index, inplace=True)
    global blockimage
    blockimage = ImageTk.PhotoImage(file="Images/blockimage.gif")
    label = Label(blockscreen, image=blockimage)
    label.place(x=120, y=10)
    headerhash = Label(blockscreen, text= "Block " + dataframe.iat[11, 0], bg='white', width=12,
                       font=("Adobe Caslon Pro Bold", 13))
    headerhash.place(x=260, y=5)

    for index, row in dataframe.iterrows():
        name = dataframe.index.values[counter]
        name = Label(blockscreen, text=dataframe.iat[counter, 0], bg='white')
        i = Label(blockscreen, text=dataframe.index.values[counter], bg='white')
        name.place(x=110, y=210 + counter * 20)
        i.place(x=20, y=210 + counter * 20)
        counter = counter + 1
        if counter == 15:
            break

    blockSavetoDB = Button(blockscreen, text="Save to Database", width=15,
                           command=lambda:blocktoDB(dataframe))
    blockSavetoDB.place(x=10, y=522)
    blockPrevBlock = Button(blockscreen, text='Previous Block', command=lambda: prevblock(dataframe.iat[2, 0]))
    blockPrevBlock.place(x=130, y=90)
    blockNextBlock = Button(blockscreen, text='Next Block', command=lambda: nextblock(dataframe.iat[6, 0]))
    blockNextBlock.place(x=420, y=90)
    closeButton = Button(blockscreen, text=' Close Child',
                         command=blockscreen.destroy)
    closeButton.place(x=520, y=522)

BlockButton = Button(text="Go", command=blocksearch).place(x=550, y=300)

def tx():
    string = entry2.get()
    dataframe = data.get_transaction(string)
    txscreen = Toplevel(root)  # Child window
    txscreen.geometry("600x550")  # Size of the window
    txscreen.title("Transaction Viewer")
    txscreen.resizable(0, 0)

    for i in [200, 320, 150]:
        Frame(txscreen, height=i, width=600, bg='white', highlightbackground='GREY', highlightthickness=0.5).pack()
    if dataframe.shape[0] == 17:
        dataframe.drop(dataframe.tail(1).index, inplace=True)

    global img1
    img1 = ImageTk.PhotoImage(file="Images/person.png")
    label = Label(txscreen, image=img1)
    label.place(x=10, y=10)

    global img2
    img2 = ImageTk.PhotoImage(file="Images/person.png")
    label = Label(txscreen, image=img2)
    label.place(x=470, y=10)

    counter = 0
    for index, row in dataframe.iterrows():
        name = dataframe.index.values[counter]
        name = Label(txscreen, text=dataframe.iat[counter, 0], bg='white', pady=5)
        i = Label(txscreen, text=dataframe.index.values[counter], bg='white', pady=5)

        name.place(x=100, y=220 + counter * 20)
        i.place(x=20, y=220 + counter * 20)
        counter = counter + 1
        if counter == 14:
            break

    df, inpAddrList, inpValList, outpAddrList, outpValList = data.gettxdetails(dataframe)

    counter = 0
    if not inpAddrList:
        noinput = Label(txscreen, text="Newly generated tokens", bg='white',
                  font=("Adobe Caslon Pro Bold", 9)).place(x=2, y=105)
    for address in inpAddrList:
        i = Label(txscreen, text=address, bg='white',
                  font=("Adobe Caslon Pro Bold", 7)).place(x=2, y=105+counter*20)
        counter = counter + 1
        if counter == 5:
            break
    counter = 0
    for value in inpValList:
        val = data.valuetoBTC(value)
        val = str(val)
        i = Label(txscreen, text=val + "BTC", bg='white',
                  font=("Adobe Caslon Pro Bold", 7)).place(x=205, y=105 + counter*20)
        counter = counter + 1
        if counter == 5:
            break
    counter = 0
    for address in outpAddrList:
        i = Label(txscreen, text=address, bg='white',
                  font=("Adobe Caslon Pro Bold", 7)).place(x=305, y=105 + counter*20)
        counter = counter + 1
        if counter == 5:
            break
    counter = 0
    for value in outpValList:
        val = data.valuetoBTC(value)
        val = str(val)
        i = Label(txscreen, text=val + "BTC", bg='white',
                  font=("Adobe Caslon Pro Bold", 7)).place(x=517, y=105 + counter*20)
        counter = counter + 1
        if counter == 5:
            break

    sentvalue = df.iat[0, 0]
    txtime = df.iat[0, 1]

    SentLabel = Label(txscreen, text=sentvalue + " BTC", bg='white', width=20, font=("Adobe Caslon Pro Bold", 20))
    SentLabel.place(x=130, y=40)
    TimeLabel = Label(txscreen, text=txtime, bg='white', width=20, font=("Adobe Caslon Pro Bold", 20))
    TimeLabel.place(x=130, y=10)

    SavetoDB = Button(txscreen, text="Save to Database", width=15, command=lambda: txtoDB(dataframe, df))
    SavetoDB.place(x=10, y=522)

    closeButton = Button(txscreen, text=' Close Child',
                         command=txscreen.destroy)
    closeButton.place(x=520, y=522)

def address():
    string = entry3.get()
    dataframe = data.get_address(string)
    addressScreen = Toplevel(root)  # Child window
    addressScreen.geometry("600x550")  # Size of the window
    addressScreen.title("Address Viewer")
    addressScreen.resizable(0, 0)

    for i in [200, 320, 150]:
        Frame(addressScreen, height=i, width=600, bg='white', highlightbackground='GREY', highlightthickness=0.5).pack()

    global addressIMG
    addressIMG = ImageTk.PhotoImage(file="Images/qr.gif")
    label = Label(addressScreen, image=addressIMG)
    label.place(x=230, y=70)

    global addressArrow
    addressArrow = ImageTk.PhotoImage(file="Images/arrow.gif")
    label = Label(addressScreen, image=addressArrow)
    label.place(x=90, y=70)

    global addressArrow2
    addressArrow2 = ImageTk.PhotoImage(file="Images/arrow.gif")
    label = Label(addressScreen, image=addressArrow2)
    label.place(x=370, y=70)

    addrLabel = Label(addressScreen, text=dataframe.iat[1, 0], bg='white',
                      font=("Adobe Caslon Pro Bold", 15)).place(x=100, y=30)

    sentInt = data.valuetoBTC(dataframe.iat[4, 0])
    recievedInt = data.valuetoBTC(dataframe.iat[4, 0])

    sentLabel = Label(addressScreen, text=recievedInt + " BTC", bg='white',
                      font=("Adobe Caslon Pro Bold", 13)).place(x=375, y=160)
    recievedLabel = Label(addressScreen, text=sentInt + " BTC", bg='white',
                      font=("Adobe Caslon Pro Bold", 13)).place(x=65, y=160)

    counter = 0
    for index, row in dataframe.iterrows():
        name = dataframe.index.values[counter]
        name = Label(addressScreen, text=dataframe.iat[counter, 0], bg='white', pady=5)
        i = Label(addressScreen, text=dataframe.index.values[counter], bg='white', pady=5)

        name.place(x=110, y=220 + counter * 20)
        i.place(x=20, y=220 + counter * 20)
        counter = counter + 1
        if counter == 7:
            break
    SavetoDB = Button(addressScreen, text="Save to Database", width=15, command=lambda: addresstoDB(dataframe))
    SavetoDB.place(x=10, y=522)
    closeButton = Button(addressScreen, text=' Close Child',
                         command=addressScreen.destroy)
    closeButton.place(x=520, y=522)


TransactionButton = Button(text="Go", command=tx).place(x=550, y=350)
AddressButton = Button(text="Go", command=address).place(x=550, y=400)

def blockResultScreen(data2):
    # Define Screen
    blockresultscreen = Toplevel(root)  # Child window
    blockresultscreen.geometry("1200x900")  # Size of the window
    blockresultscreen.title("Block Viewer")
    blockresultscreen.resizable(0, 0)
    blockresultscreen.configure(bg='white')
    block = Frame(blockresultscreen, height=800, width=300, bg='white')
    block.pack(side=RIGHT)
    #BlockIndex: Date: NumberofTx:
    indexlist = data2["BlockIndex"]
    datelist = data2["Date"]
    txamountlist = data2["NumberofTx"]
    print(data2)

    counter = 0
    numberlist = []
    for i in indexlist:
        counter = counter + 1
        numberlist.append(counter)

    figure = plt.Figure(figsize=(10, 5), dpi=100)
    line = FigureCanvasTkAgg(figure, blockresultscreen)
    ax2 = figure.add_subplot(111)
    line.get_tk_widget().pack(side=BOTTOM,fill=BOTH)
    data2 = data2[['Date', 'BlockIndex']].groupby('Date').sum()
    data2.plot(kind='line', legend=True, ax=ax2, color='g', marker='o', fontsize=9)
    ax2.set_title('Block Creation Timeline')
    ax2.set_ylabel("Block Index")

    figure2 = plt.Figure(figsize=(10, 4), dpi=100)
    ax1 = figure2.add_subplot(111)
    bar2 = FigureCanvasTkAgg(figure2, blockresultscreen)
    bar2.get_tk_widget().pack(side=TOP,fill=BOTH)
    ax1.bar(numberlist, txamountlist, color='orange')
    ax1.set_title("Number of Transactions per block")
    ax1.set_xlabel('Block')
    ax1.set_ylabel('No of TX')

    indexLabel = Label(blockresultscreen, text="Index", bg='white',
                      font=("Adobe Caslon Pro Bold", 9)).place(x=840, y=80)
    dateLabel = Label(blockresultscreen, text="Date/Time", bg='white',
                          font=("Adobe Caslon Pro Bold", 9)).place(x=890, y=80)
    txamountLabel = Label(blockresultscreen, text="Amount of TX", bg='white',
                      font=("Adobe Caslon Pro Bold", 9)).place(x=1000, y=80)

    counter = 0
    for i in numberlist:
        a = Label(blockresultscreen, text=i, bg='white',
                  font=("Adobe Caslon Pro Bold", 9)).place(x=820, y=100 + 20 * counter)

        b = Label(blockresultscreen, text=indexlist[counter], bg='white',
                  font=("Adobe Caslon Pro Bold", 8)).place(x=840, y=100 + 20 * counter)

        c = Label(blockresultscreen, text=datelist[counter], bg='white',
                  font=("Adobe Caslon Pro Bold", 8)).place(x=890, y=100 + 20 * counter)

        d = Label(blockresultscreen, text=txamountlist[counter], bg='white',
                  font=("Adobe Caslon Pro Bold", 8)).place(x=1010, y=100 + 20 * counter)
        counter = counter + 1

def txResultScreen(data2):
    #Define Screen
    txresultscreen = Toplevel(root)  # Child window
    txresultscreen.geometry("1200x600")
    txresultscreen.configure(bg='white')
    txresultscreen.title("Tx Viewer")
    txresultscreen.resizable(0, 0)
    transaction = Frame(txresultscreen, height = 800 , width= 200, bg = 'white')
    transaction.pack(side = RIGHT)
    #Date: Amount:
    print(data2)

    amountlist = data2["Amount"].tolist()
    datelist = data2["Date"].tolist()

    figure = plt.Figure(figsize=(10, 4), dpi=100)
    line = FigureCanvasTkAgg(figure, txresultscreen)
    ax2 = figure.add_subplot(111)
    line.get_tk_widget().pack(side=LEFT, fill=BOTH)
    data2 = data2[['Date', 'Amount']].groupby('Date').sum()
    data2.plot(kind='line', legend=True, ax=ax2, color='b', marker='o', fontsize=9)
    ax2.set_title('Transaction Timeline')
    ax2.set_ylabel("Amount")

    timeLabel = Label(txresultscreen, text="Date/Time", bg='white',
                      font=("Adobe Caslon Pro Bold", 9)).place(x=930, y=80)
    amountLabel = Label(txresultscreen, text="Amount", bg='white',
                          font=("Adobe Caslon Pro Bold", 9)).place(x=1100, y=80)
    counter = 0
    for i in amountlist:
        a = Label(txresultscreen, text=datelist[counter], bg='white',
                  font=("Adobe Caslon Pro Bold", 9)).place(x=930, y=100 + 20 * counter)

        b = Label(txresultscreen, text=amountlist[counter], bg='white',
                  font=("Adobe Caslon Pro Bold", 9)).place(x=1100, y=100 + 20 * counter)
        counter = counter + 1


def addrResultScreen(data2):
    addrResultScreen = Toplevel(root)  # Child window
    addrResultScreen.geometry("1100x800")  # Size of the window
    addrResultScreen.title("Address Viewer")
    addrResultScreen.resizable(0, 0)
    #Address: Sent: Received: Total:
    addrFrame = Frame (addrResultScreen,width = 500 , height = 800, bg = 'white')
    addrFrame.pack(side = RIGHT)
    print(data2)
    addrlist = data2['Address'].tolist()
    sentlist = data2['Sent'].tolist()
    receivedlist = data2['Received'].tolist()
    counter = 0
    numberlist = []
    for i in addrlist:
        counter = counter + 1
        numberlist.append(counter)

    figure1 = plt.Figure(figsize=(6, 4), dpi=100)
    ax = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, addrResultScreen)
    bar1.get_tk_widget().pack(side=TOP, fill=BOTH)
    ax.bar(numberlist, sentlist)
    ax.set_title("Amount of Bitcoin Sent")
    ax.set_xlabel('Address')
    ax.set_ylabel('Amount (BTC)')

    figure2 = plt.Figure(figsize=(6, 4), dpi=100)
    ax1 = figure2.add_subplot(111)
    bar2 = FigureCanvasTkAgg(figure2, addrResultScreen)
    bar2.get_tk_widget().pack(side=BOTTOM, fill=BOTH)
    ax1.bar(numberlist, receivedlist, color = 'orange')
    ax1.set_title("Amount of Bitcoin Received")
    ax1.set_xlabel('Address')
    ax1.set_ylabel('Amount (BTC)')

    addrLabel = Label(addrResultScreen,text = "Address",bg='white',
                  font=("Adobe Caslon Pro Bold", 9)).place (x = 600, y=80)
    receivedLabel = Label(addrResultScreen,text = "Received",bg='white',
                  font=("Adobe Caslon Pro Bold", 9)).place (x = 880, y=80)
    sentLabel =  Label(addrResultScreen,text = "Sent",bg='white',
                  font=("Adobe Caslon Pro Bold", 9)).place (x = 1000, y=80)

    counter = 0
    for i in numberlist:
        a = Label(addrResultScreen,text = i,bg='white',
                  font=("Adobe Caslon Pro Bold", 9)).place(x = 580, y=100 + 20*counter)

        b = Label(addrResultScreen, text = addrlist[counter],bg='white',
                  font=("Adobe Caslon Pro Bold", 8)).place(x = 600, y=100 + 20*counter)

        c = Label(addrResultScreen, text = receivedlist[counter],bg='white',
                  font=("Adobe Caslon Pro Bold", 8)).place(x = 880, y=100 + 20*counter)

        d = Label(addrResultScreen, text = sentlist[counter],bg='white',
                  font=("Adobe Caslon Pro Bold", 8)).place(x = 1000, y=100 + 20*counter)
        counter=counter + 1

root.mainloop()
