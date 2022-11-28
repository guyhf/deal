import random
import tkinter


global choice, root, cases, amounts
choice = None
cases = []

def switch_screens():
    global chooseBoxLabel, confirmBox, chooseBoxMenu, deal_button, offer_label
    chooseBoxLabel.pack_forget()
    confirmBox.pack_forget()
    chooseBoxMenu.pack_forget()
    drawCases()
    update_offer()
    offer_label.pack()
    deal_button.pack()


def choiceCallback(selection):
    global choice
    choice = selection

class Case(object):
    def __init__(self, number, amount, update_offer):
        self.number = number
        self.amount = amount
        self.revealed = False
        self.chosen = False
        self.button = tkinter.Button(root, text = str(self.number), command=self.reveal)
        self.update_offer = update_offer

    def reveal(self):
        if not self.chosen:
            self.revealed = True
            self.button.config(text = f"[ ${str(self.amount)} ]")
            self.update_offer()

    def choose(self):
        self.chosen = True
        self.button.config(text = f"[ Your Case ]")

    def __str__(self):
        if self.revealed:
            s = f"<{self.amount}>"
        elif self.chosen:
            s = f"[Your Case]"
        else:
            s = f"[{self.number}]"
        return s

def make_deal():
    newWindow = tkinter.Toplevel(root)
    newWindow.title("Deal is Made!")
 
    # sets the geometry of toplevel
    newWindow.geometry("300x300")
 
    # A Label widget to show in toplevel
    tkinter.Label(newWindow,
          text ="Thanks for playing!").pack()

    
def make_choice():
    global chooseBoxLabel, confirmBox, chooseBoxMenu, deal_button

    nrevealed = number_revealed()
    if nrevealed < 8:
        n_to_reveal = 8 - nrevealed

    chooseBoxLabel = tkinter.Label(
        root,
        text = f"""Welcome to Deal or No Deal!
        Choose your case, 1-10 with amounts $1-$1000

        Choose {n_to_reveal} cases to reveal.
        """)
    boxChoice = tkinter.StringVar()
    boxChoiceList = range(1,11)
    chooseBoxMenu = tkinter.OptionMenu(root, boxChoice, *boxChoiceList, command = choiceCallback)
    chooseBoxLabel.pack()
    chooseBoxMenu.pack(expand=True)
    confirmBox = tkinter.Button(root, text = "Confirm", command = switch_screens)
    confirmBox.pack()
    deal_button = tkinter.Button(root, text="Deal!", command=make_deal)

def drawCases():
    global cases
    print(f"choice is {choice}")
    for i, amount in enumerate(amounts, 1):
        case = Case(i, amount, update_offer)
        case.button.pack()
        if choice == i:
            case.choose()
        cases.append(case)


def number_revealed():
    global cases
    n = 0
    for case in cases:
        if case.revealed:
            n = n + 1
    return n
 
class Game(object):

    def __init__(self, values) -> None:
        shuffled = list(values)
        random.shuffle(shuffled)
        self.cases = [Case(i, val) for i, val in enumerate(shuffled, 1)]
        self.deal = False

    def offer(self) -> int:
        total = 0
        count = 0
        for c in self.cases:
            if not c.revealed:
                total += c.amount
                count += 1
        offer = round((total / count) * random.uniform(.8, .9))
        return offer

    def __str__(self) -> str:
        return "-".join([str(c) for c in self.cases])

def update_offer():
    global offer_var
    total = 0
    count = 0
    for c in cases:
        if not c.revealed:
            total += c.amount
            count += 1
    offer = round((total / count) * random.uniform(.8, .9))
    offer_var.set(f"Offer is ${offer}")
    return offer

def setup():
    global root, amounts, cases, offer_var, offer_label
    root = tkinter.Tk()
    root.title("Deal or No Deal!")
    root.geometry("800x800")

    make_choice()

    amounts = [1,2,5,10,25,50,100,250,500,1000]
    random.shuffle(amounts)

    offer_var = tkinter.StringVar()
    offer_var.set(f"Offer is $0")

    offer_label = tkinter.Label(root,
        textvariable=offer_var)

    cases = []


setup()
root.mainloop()
