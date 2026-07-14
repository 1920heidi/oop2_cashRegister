#!/usr/bin/env python3


class CashRegister:
    """A simple point-of-sale cash register.

    Tracks a running total, the list of items rung up, and a log of every
    transaction so that the most recent one can be voided. An optional
    percentage discount can be applied to the running total.
    """

    def __init__(self, discount=0):
        # `_discount` backs the validated `discount` property below. It is set
        # to a safe default first so that an invalid argument leaves the object
        # in a usable state rather than raising an AttributeError later on.
        self._discount = 0
        self.discount = discount          # routed through the property setter
        self.total = 0                    # running price of everything rung up
        self.items = []                   # flat list, one entry per unit sold
        self.previous_transactions = []   # audit log used to void the last sale

    @property
    def discount(self):
        """Percentage taken off the total (e.g. 20 means 20% off)."""
        return self._discount

    @discount.setter
    def discount(self, value):
        # A discount only makes sense as a whole percentage from 0 to 100.
        # Anything else is rejected and the previous value is kept unchanged.
        if isinstance(value, int) and 0 <= value <= 100:
            self._discount = value
        else:
            print("Not valid discount")

    def add_item(self, item, price, quantity=1):
        """Ring up `quantity` units of `item` at `price` each.

        Grows the running total, records one `items` entry per unit (so a
        quantity of 3 appears three times), and appends a single transaction
        record used later by `void_last_transaction`.
        """
        self.total += price * quantity
        # One entry per unit keeps `items` an accurate itemized receipt.
        self.items.extend([item] * quantity)
        self.previous_transactions.append(
            {"item": item, "price": price, "quantity": quantity}
        )

    def apply_discount(self):
        """Reduce the total by the discount percentage and announce the result.

        With no discount set there is nothing to do, so a message is printed
        instead of silently changing the total.
        """
        if self.discount:
            self.total -= self.total * self.discount / 100
            # Cast to int so a whole-dollar result prints as "$800", not "$800.0".
            self.total = int(self.total)
            print(f"After the discount, the total comes to ${self.total}.")
        else:
            print("There is no discount to apply.")

    def void_last_transaction(self):
        """Undo the most recent `add_item` call.

        Subtracts that transaction's cost from the total and removes its units
        from the `items` list. Does nothing when there is no transaction to void.
        """
        if not self.previous_transactions:
            print("There is no transaction to void.")
            return

        last = self.previous_transactions.pop()
        self.total -= last["price"] * last["quantity"]
        # Remove exactly the units that were added by this transaction.
        for _ in range(last["quantity"]):
            if last["item"] in self.items:
                self.items.remove(last["item"])
