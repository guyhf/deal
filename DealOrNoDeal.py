import random
import tkinter

#put globals into dictionary that holds game settings

global choice, root, cases, amounts
choice = None
cases = []

class Game(object):
    def __init__(self, amounts):
        self.root = tkinter.Tk()
        self.amounts = list(amounts)
        random.shuffle(self.amounts)
        self.offer_var = tkinter.StringVar()
        self.offer_var.set(f"Offer is $0")
        self.offer_label = tkinter.Label(root, textvariable=offer_var)
        self.instruction_var = tkinter.StringVar()
        self.instruction_var.set("Choose 4 cases to eliminate")
        self.instruction_label = tkinter.Label(root, textvariable=instruction_var)
        self.spacer = tkinter.Label(root, text="", pady=4)
        self.num_to_choose = 4

    def run(self):
        self.root.mainloop()



def switch_screens():
    global chooseBoxLabel, confirmBox, chooseBoxMenu, deal_button, offer_label, instruction_label
    chooseBoxLabel.pack_forget()
    confirmBox.pack_forget()
    chooseBoxMenu.pack_forget()
    drawCases()
    update_offer()
    spacer.pack()
    #spacer is for formatting
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




    
    


class Game(object):

    def __init__(self, amounts) -> None:
        shuffled = list(amounts)
        random.shuffle(shuffled)
        self.cases = [Case(i, val) for i, val in enumerate(shuffled, 1)]
        self.deal = False
        self.offer = 0

    def __str__(self) -> str:
        return "-".join([str(c) for c in self.cases])

    def number_revealed(self):
        n = 0
        for case in self.cases:
            if case.revealed:
                n = n + 1
        return n

    def get_chosen_case(self):
        for case in self.cases:
            if case.chosen:
                return case
        return None
 
    def displayCases(self):
        for case in self.cases:
            case_label = tkinter.Label(self.root, text=case)
            case_label.pack()

    def drawCases(self):
        for i, amount in enumerate(amounts, 1):
            case = Case(i, amount, self.update_offer)
            case.button.pack()
            if choice == i:
                case.choose()
            cases.append(case)

    def end(self):
        self.root.destroy()

    def update_offer(self):
        total = 0
        count = 0
        for c in self.cases:
            if not c.revealed:
                total += c.amount
                count += 1
        self.offer = round((total / count) * random.uniform(.8, .9))
        offer_var.set(f"Offer is ${offer}")
        nrevealed = self.number_revealed()
        remaining = num_to_choose - nrevealed
        if remaining == 0:
            self.offer_screen()
        else:
            instruction_var.set(f"Choose {remaining} cases")

    def setup(self):
        root.title("Deal or No Deal!")
        root.geometry("800x800")
        self.choose_case()

    def choose_case(self):
        nrevealed = self.number_revealed()
        if nrevealed < 8:
            n_to_reveal = 8 - nrevealed
        self.chooseBoxLabel = tkinter.Label(
            root,
            text = """Welcome to Deal or No Deal!
            Choose your case, 1-10 with amounts $1-$1000
            """)
        boxChoice = tkinter.StringVar()
        boxChoiceList = range(1,11)
        self.chooseBoxMenu = tkinter.OptionMenu(root, boxChoice, *boxChoiceList, command = choiceCallback)
        self.chooseBoxLabel.pack()
        self.chooseBoxMenu.pack(expand=True)
        self.confirmBox = tkinter.Button(root, text = "Confirm", command = switch_screens)
        self.confirmBox.pack()

    def make_deal(self):
        newWindow = tkinter.Toplevel(self.root)
        newWindow.title("Deal is Made!")
    
        # sets the geometry of toplevel
        newWindow.geometry("500x500")
    
        tkinter.Label(newWindow,
            text =f"You win ${self.offer}").pack()

        your_case = self.get_chosen_case()
        tkinter.Label(newWindow,
            text =f"Your case had ${your_case.amount}").pack()

        # A Label widget to show in toplevel
        tkinter.Label(newWindow,
            text ="Thanks for playing!").pack()

        tkinter.Button(newWindow, text = "Done", command = self.end).pack()

    def make_no_deal(self):
        newWindow = tkinter.Toplevel(self.root)
        newWindow.title("You chose to keep your case!")
    
        # sets the geometry of toplevel
        newWindow.geometry("500x500")
    
        your_case = self.get_chosen_case()
        tkinter.Label(newWindow,
            text =f"You win ${your_case.amount}").pack()

        tkinter.Label(newWindow,
            text =f"You turned down a deal for ${offer}").pack()

        # A Label widget to show in toplevel
        tkinter.Label(newWindow,
            text ="Thanks for playing!").pack()

        tkinter.Button(newWindow, text = "Done", command = end).pack()



game = Game()