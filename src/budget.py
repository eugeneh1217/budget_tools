from datetime import date


class Stream:
    """Object that represents a portion of budget"""

    transactions = {}

    def __init__(self, name, initial_money=None):
        self.name = name
        self.initial_money = initial_money
        self.money = initial_money

    def pull(self, amount=None):
        """
            removes money from this stream
            returns remaining balance
        """
        if amount is None:
            self.money = 0
        else:
            self.money -= amount
        return self.money

    def push(self, amount):
        """
            pushes money into this stream
            returns current balance
        """
        self.money += amount
        return self.money

    def dump(self):
        """
            dumps current balance into next period
            returns current balance
        """
        self.money = self.money + self.initial_money
        return self.money

    @staticmethod
    def get_name(stream):
        return stream.name


class Budget:
    budget_total = 0
    excess = 0
    """Budget Object that holds streams"""
    def __init__(self, name, streams=None):
        self.streams = []
        self.name = name
        self.period_month = date.today().month
        if streams is not None:
            for stream in streams:
                self.streams.append(stream)

    @staticmethod
    def get_name(budget):
        return budget.name
    # def save(self):
    #     with open(self.data_file_name, "w") as data_file:
    #         json.dump(vars(self), data_file)
    #
    # def load(self):
    #     with open(self.data_file_name, "r") as data_file:
    #         data = json.loads(data_file.read())
    #         for data_key in list(data.keys):
    #             try:
    #                 locals()[data_key] = data[data_key]
    #             except (NameError, KeyError):
    #                 pass


budget0 = Budget("first", [Stream("Food", 300), Stream("Electricity", 200), Stream("Electronics", 50)])


