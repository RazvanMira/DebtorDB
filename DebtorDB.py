from src import commands as c
from src import presentation as p


def loop():
    options = {
        "A": p.Option(
            name="Add a Debtor",
            command=c.AddDebtorCommand(),
            prep_call=p.get_new_debtor_data,
        ),
        "I": p.Option(
            name="Get Debtor by ID",
            command=c.GetDebtorCommand(),
            prep_call=p.get_debtor_id,
        ),
        "T": p.Option(
            name="List Debtors by due date", 
            command=c.ListDebtorsCommand()
        ),
        "N": p.Option(
            name="List Debtors by name",
            command=c.ListDebtorsCommand(order_by="name"),
        ),
        "E": p.Option(
            name="Edit a Debtor's information",
            command=c.EditDebtorCommand(),
            prep_call=p.get_update_debtor_data,
        ),
        "D": p.Option(
            name="Delete a Debtor",
            command=c.DeleteDebtorCommand(),
            prep_call=p.get_debtor_id,
        ),
        "Q": p.Option(
            name="Quit", 
            command=c.QuitCommand()
        ),
    }

    p.clear_screen()
    p.print_options(options)
    chosen_option = p.get_option_choice(options)
    p.clear_screen()
    chosen_option.choose()

    _ = input("Press ENTER to return to menu")

if __name__ == "__main__":
    c.CreateDebtorsTableCommand().execute()
    print("Welcome to DebtorDB!")

    while True:
        loop()