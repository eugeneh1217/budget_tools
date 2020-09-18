from budget import Budget
from budget import Stream
import pickle
from datetime import date
from datetime import timedelta
from os import system
import platform
import time

# get command for clearing screen for platform
clear = "cls"
platform_type = platform.system()
if platform_type == "Linux" or platform_type == "Darwin":
    clear = "clear"

# initialize pause time (seconds)
PAUSE = 2

# get budget data from bin
budgets = []
with open(r'bin\data.bin', "rb") as data_file:
    try:
        budgets = pickle.load(data_file)
    except EOFError:
        budgets = []

# budget names
budget_names = list(map(Budget.get_name, budgets))

# isolate budgets that are starting new periods
current_month = date.today().month
to_update_budgets = []
for budget in budgets:
    if budget.period_month != current_month:
        to_update_budgets.append(budget)

to_update_budget_names = list(map(Budget.get_name, to_update_budgets))

# clear screen
system(clear)

# running loop
"""
    COMMANDS:
        period
        edit 'budget_name'
        new 'budget_name'
        'budget_name'
        list
"""

# TODO:
#     test and debug
#     add input length counter for all user inputs
#     add confirmation for every successful action
#     change all while loops to break with if instead of while user_in!="done"
#     saving budgets after main loop

user_in = ""
while True:
    user_in = input("Budgets starting new periods: {}\n\nEnd of period: 'period'\nAdjust budget: 'edit budget_name'"
                    "\nnew budget: 'new budget_name'\n\n>>> ".format(str(to_update_budget_names)[1:-1]
                                                                     if len(to_update_budget_names) > 0 else "None"))
    user_in = user_in.split()
    system(clear)

    # user exits loop
    if user_in[0] == "done":
        break

    # user wants to update budgets moving into new period
    elif user_in[0] == "period":
        edited_budgets = []
        # user selects budget
        while user_in != "done":
            if len(to_update_budget_names) or len(edited_budgets):
                user_in = input("{} {}\nname of budget to edit: ".format(str(to_update_budget_names)[1:-1], '* '
                                                                         .join(edited_budgets) +
                                                                                                            "*" if len(
                    edited_budgets) else ""))
                try:
                    # create reference to budget we are currently editing
                    budget_editing = to_update_budgets[to_update_budget_names.index(user_in)]

                    # create lists with streams within budget and names of streams within budget to dump and reset
                    dump_streams = list(budget_editing.streams)
                    dump_stream_names = list(map(Stream.get_name, dump_streams))
                    reset_streams = []
                    reset_stream_names = list(map(Stream.get_name, reset_streams))

                    # variable to hold excess from resets
                    excess = 0

                    # user edits streams
                    while user_in != "done":
                        user_in = input("Dump: {}\nReset: {}\nEnter name of stream to swap: "
                                        .format(str(dump_stream_names)[1:-1], str(reset_stream_names)[1:-1]))

                        # swap specified stream to other list
                        if user_in in dump_stream_names:
                            stream_index = dump_stream_names.index(user_in)
                            del dump_stream_names[stream_index]
                            stream = dump_streams.pop(stream_index)
                            reset_streams.append(stream)
                            reset_stream_names.append(stream.name)
                        elif user_in in reset_stream_names:
                            stream_index = reset_stream_names.index(user_in)
                            del reset_stream_names[stream_index]
                            stream = reset_streams.pop(stream_index)
                            dump_streams.append(stream)
                            dump_stream_names.append(stream.name)

                        # clear screen
                        system(clear)

                    # apply dumps
                    [stream.dump() for stream in dump_streams]

                    # apply resets
                    for stream in reset_streams:
                        excess += stream.money
                        stream.pull()
                    budget_editing.money = excess

                    # reset user_in so budget selecting loop doesn't terminate
                    user_in = ""
                # if user input is not there
                except ValueError:
                    if user_in != "done":
                        print("invalid budget name")
            # if no budgets finished period
            else:
                user_in = "done"
                print("No budgets to edit")
                time.sleep(PAUSE)
            system(clear)
        user_in = ""

    # user wants to edit existing budget
    elif user_in[0] == "edit":
        try:
            budget_index = budget_names.index(user_in[1])
            while True:
                user_in = input("'streams' to edit streams\n'name' to edit name\n'done' to exit")
                if user_in == "done":
                    break
                elif user_in == "name":
                    budgets[budget_index] = input("New name: ")
                elif user_in == "streams":
                    while True:
                        stream_names = list(map(Stream.get_name, budgets[budget_index].streams))
                        user_in = input("'rename stream_name'\n'refinance stream_name additional_amount' (additional "
                                        "money will be added to initial_amount in future periods)\n\n"
                                        "enter 'done' to exit:\n{}\n\n"
                                        .format("\n".join(stream_names))).split()
                        if user_in[0] == "done":
                            break
                        elif user_in[0] == "rename" and len(user_in) == 2:
                            budgets[budget_index].streams[stream_names.index(user_in[1])].name = input(
                                "Enter new name: "
                            )
                            print("added {} to {}".format(user_in[2], user_in[1]))
                            time.sleep(2)
                            system(clear)
                        elif user_in[0] == "refinance" and len(user_in) == 3:
                            budgets[budget_index].streams[stream_names.index(user_in[1])].initial_money += user_in[2]
                            budgets[budget_index].streams[stream_names.index(user_in[1])].money += user_in[2]
                            print("added {} to {}".format(user_in[2], user_in[1]))
                            time.sleep(2)
                            system(clear)




        except ValueError:
            print("could not find budget named '{}'".format(user_in[1]))

    # user wants to create new budget
    elif user_in[0] == "new":
        budgets.append(Budget(user_in[1]))
        budget_names.append(user_in[1])
        print("initializing: {}\n".format(user_in[1]))
        while True:
            print("Current streams within {}: {}".format(
                budget_names[-1], str(budgets[-1].streams)[1:-1] if len(budgets[-1].streams) > 0 else "None")
            )
            user_in = input(
                            "Edit name of budget: 'edit_name stream_name new_stream_name'\n   Name: {}\n"
                            "Add stream: new 'stream_name initial_money\n   Streams: {}\n"
                            "Edit initial money in stream: 'edit_initial_money stream_name amount'\n"
                            "Delete stream: 'del stream_name'\n"
                            "To exit: 'done'\n\n>>> ".format(budgets[-1].name, "\n".join(list(map(
                                Stream.get_name, budgets[-1].streams
                            )))))
            try:
                stream = budgets[-1].streams[list(map(Stream.get_name, budgets[-1].streams)).index(user_in[1])]
            except ValueError:
                stream = None

            if user_in == 'done':
                break
            elif stream is None:
                print("Could not find stream named {}".format(user_in[1]))
            elif user_in[0] == "del":
                del stream
            elif user_in[0] == "edit_name":
                stream.name = user_in[2]
            elif user_in[0] == "edit_initial_money":
                try:
                    stream.initial_money = int(user_in[2])
                except ValueError:
                    print("invalid amount")
            elif user_in[0] == "new":
                try:
                    budgets[-1].streams.append(Stream(user_in[0], int(user_in[2], base=10)))
                except ValueError:
                    print("invalid initial_money_in_stream")

    # user wants to examine a specific budget
    elif user_in[0] in budget_names:
        budget_index = budget_names.index(user_in[1])
        streams = budgets[budget_index].streams
        stream_names = list(map(Stream.get_name, streams))
        while True:
            user_in = input(
                "Budget Name: {}\n"
                "Budget Total: {}\n"
                "Period Ends On: {}\n"
                "Streams: {}\n\n"
                "Enter 'done' to exit or 'trans stream_name' for transactions within stream".format(
                    budgets[budget_index].name,
                    budgets[budget_index].budget_total,
                    date(date.today().year, budgets[budget_index].period_month + 1, 1) - timedelta(days=1),
                    "\n   ".join(map(lambda s: s.name + ": " + s.money + " / " + s.initial_money,
                                     budgets[budget_index].streams))
                )
            ).split()
            if user_in[0] == "done":
                break
            elif user_in[0] == "trans":
                stream = streams[stream_names.index(user_in[1])]
                user_in = input("Transactions:\n{}".format("\n".join(
                    map(lambda e: str(e[1]) + ": " + str(stream.transactions[e[1]]),
                        list(enumerate(stream.transactions))
                        )
                )))
                while user_in != "done":
                    user_in = input("invalid input: enter 'done' to exit\n")
            else:
                print("enter 'done' to exit or 'stream_name' for more details")
                time.sleep(PAUSE)

    # user wants to list all budgets
    elif user_in[0] == "list":
        while True:
            user_in = input("{}\n\nEnter 'done' to exit\n".format("\n".join(map(Budget.get_name, budgets))))
            if user_in == "done":
                break

    # user wants to delete budget
    elif user_in[0] == "del":
        try:
            del budgets[budget_names.index(user_in[1])]
            print("Deleted {}".format(user_in[1]))
            time.sleep(PAUSE)
            system(clear)
        except ValueError:
            print("could not find budget")
            time.sleep(PAUSE)
