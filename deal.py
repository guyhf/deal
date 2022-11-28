import random
import tkinter


global choice, root, cases, amounts
choice = None
cases = []

def switch_screens():
    global chooseBoxLabel, confirmBox, chooseBoxMenu, deal_button, offer_label, instruction_label
    chooseBoxLabel.pack_forget()
    confirmBox.pack_forget()
    chooseBoxMenu.pack_forget()
    drawCases()
    update_offer()

    spacer.pack()
    instruction_label.pack()

def offer_screen():
    global root, offer_label, offer_var
    for widget in root.winfo_children():
       widget.destroy()
    
    offer_label = tkinter.Label(root,
        textvariable=offer_var)
    offer_label.pack()
    deal_button = tkinter.Button(root, text="Deal!", command=make_deal)
    deal_button.pack()
    no_deal_button = tkinter.Button(root, text="No Deal!", command=make_no_deal)
    no_deal_button.pack()
    spacer = tkinter.Label(root, text="", pady=4)
    spacer.pack()
    displayCases()


def choiceCallback(selection):
    global choice, num_to_choose, instruction_var
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
            s = f"${self.amount}"
        elif self.chosen:
            s = f"[Your Case]"
        else:
            s = f"[case {self.number}]"
        return s


def end():
    root.destroy()

def make_deal():
    global offer
    newWindow = tkinter.Toplevel(root)
    newWindow.title("Deal is Made!")
 
    # sets the geometry of toplevel
    newWindow.geometry("500x500")
 
    tkinter.Label(newWindow,
          text =f"You win ${offer}").pack()

    your_case = get_chosen_case()
    tkinter.Label(newWindow,
          text =f"Your case had ${your_case.amount}").pack()

    # A Label widget to show in toplevel
    tkinter.Label(newWindow,
          text ="Thanks for playing!").pack()

    tkinter.Button(newWindow, text = "Done", command = end).pack()

    
def make_no_deal():
    global offer
    newWindow = tkinter.Toplevel(root)
    newWindow.title("You chose to keep your case!")
 
    # sets the geometry of toplevel
    newWindow.geometry("500x500")
 
    your_case = get_chosen_case()
    tkinter.Label(newWindow,
          text =f"You win ${your_case.amount}").pack()

    tkinter.Label(newWindow,
          text =f"You turned down a deal for ${offer}").pack()

    # A Label widget to show in toplevel
    tkinter.Label(newWindow,
          text ="Thanks for playing!").pack()

    tkinter.Button(newWindow, text = "Done", command = end).pack()

    
def make_choice():
    global chooseBoxLabel, confirmBox, chooseBoxMenu, deal_button, num_to_choose, instruction_var

    nrevealed = number_revealed()
    if nrevealed < 8:
        n_to_reveal = 8 - nrevealed

    chooseBoxLabel = tkinter.Label(
        root,
        text = """Welcome to Deal or No Deal!
        Choose your case, 1-10 with amounts $1-$1000
        """)
    boxChoice = tkinter.StringVar()
    boxChoiceList = range(1,11)
    chooseBoxMenu = tkinter.OptionMenu(root, boxChoice, *boxChoiceList, command = choiceCallback)
    chooseBoxLabel.pack()
    chooseBoxMenu.pack(expand=True)
    confirmBox = tkinter.Button(root, text = "Confirm", command = switch_screens)
    confirmBox.pack()

def drawCases():
    global cases
    for i, amount in enumerate(amounts, 1):
        case = Case(i, amount, update_offer)
        case.button.pack()
        if choice == i:
            case.choose()
        cases.append(case)

def displayCases():
    global cases
    for case in cases:
        case_label = tkinter.Label(root, text=case)
        case_label.pack()

def number_revealed():
    global cases
    n = 0
    for case in cases:
        if case.revealed:
            n = n + 1
    return n


def get_chosen_case():
    global cases
    for case in cases:
        if case.chosen:
            return case
    return None
 
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
    global offer_var, offer
    total = 0
    count = 0
    for c in cases:
        if not c.revealed:
            total += c.amount
            count += 1
    offer = round((total / count) * random.uniform(.8, .9))
    offer_var.set(f"Offer is ${offer}")
    nrevealed = number_revealed()
    remaining = num_to_choose - nrevealed
    if remaining == 0:
        offer_screen()
    else:
        instruction_var.set(f"Choose {remaining}")


def setup():
    global root, amounts, cases, offer_var, offer_label, instruction_var, instruction_label, spacer, num_to_choose
    root = tkinter.Tk()
    root.title("Deal or No Deal!")
    root.geometry("800x800")


    amounts = [1,2,5,10,25,50,100,250,500,1000]
    random.shuffle(amounts)

    offer_var = tkinter.StringVar()
    offer_var.set(f"Offer is $0")

    offer_label = tkinter.Label(root,
        textvariable=offer_var)

    instruction_var = tkinter.StringVar()
    instruction_var.set("Choose 4 cases")

    instruction_label = tkinter.Label(root,
        textvariable=instruction_var)

    spacer = tkinter.Label(root, text="", pady=4)

    num_to_choose = 4

    make_choice()


setup()
root.mainloop()
