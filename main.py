
from decimal import Decimal, InvalidOperation


class SusuGroup:
    def __init__(self, weekly_contribution):
        try:
            contribution = Decimal(str(weekly_contribution))
        except InvalidOperation:
            raise ValueError("Enter a valid contribution amount.")

        if not contribution.is_finite() or contribution <= 0:
            raise ValueError("Weekly contribution must be greater than zero.")

        self.weekly_contribution = contribution
        self.members = []
        self.current_week = 1
        self.payments = {}
        self.payout_history = []

    def add_member(self, name):
        name = name.strip()

        if not name:
            raise ValueError("Member name cannot be empty.")

        if name in self.members:
            raise ValueError("This member already exists.")

        if self.payments or self.current_week > 1:
            raise ValueError("Membership is fixed once payments begin.")

        self.members.append(name)

    def record_payment(self, name, amount):
        if name not in self.members:
            raise ValueError("Member does not exist.")

        try:
            amount = Decimal(str(amount))
        except InvalidOperation:
            raise ValueError("Enter a valid payment amount.")

        if not amount.is_finite() or amount <= 0:
            raise ValueError("Payment must be greater than zero.")

        week_payments = self.payments.setdefault(
            self.current_week, {}
        )

        already_paid = week_payments.get(
            name, Decimal("0.00")
        )
        remaining = self.weekly_contribution - already_paid

        if amount > remaining:
            raise ValueError(
                f"Payment exceeds the balance of GHS {remaining:.2f}."
            )

        week_payments[name] = already_paid + amount

    def close_week(self):
        if not self.members:
            raise ValueError("Add members before closing a week.")

        week_payments = self.payments.get(self.current_week, {})
        unpaid = {}

        for name in self.members:
            paid = week_payments.get(name, Decimal("0.00"))
            owed = self.weekly_contribution - paid

            if owed > 0:
                unpaid[name] = owed

        if unpaid:
            return {
                "closed": False,
                "week": self.current_week,
                "unpaid": unpaid,
            }

        payout_index = (self.current_week - 1) % len(self.members)
        recipient = self.members[payout_index]
        pot = self.weekly_contribution * len(self.members)

        self.payout_history.append({
            "week": self.current_week,
            "recipient": recipient,
            "amount": pot,
        })

        self.current_week += 1

        return {
            "closed": True,
            "recipient": recipient,
            "amount": pot,
        }

    def get_report(self):
        week_payments = self.payments.get(self.current_week, {})
        paid_in_full = []
        amounts_owed = {}

        for name in self.members:
            paid = week_payments.get(name, Decimal("0.00"))
            owed = self.weekly_contribution - paid

            if owed == 0:
                paid_in_full.append(name)
            else:
                amounts_owed[name] = owed

        return {
            "current_week": self.current_week,
            "paid_in_full": paid_in_full,
            "amounts_owed": amounts_owed,
            "payout_history": list(self.payout_history),
        }


def show_report(group):
    report = group.get_report()

    print("\n--- SUSU GROUP REPORT ---")
    print("Current week:", report["current_week"])
    print("Paid in full:", report["paid_in_full"])

    print("Amounts owed:")
    if not report["amounts_owed"]:
        print("  Nobody owes money.")
    else:
        for name, amount in report["amounts_owed"].items():
            print(f"  {name}: GHS {amount:.2f}")

    print("Payout history:")
    if not report["payout_history"]:
        print("  No payouts yet.")
    else:
        for payout in report["payout_history"]:
            print(
                f"  Week {payout['week']}: "
                f"{payout['recipient']} received "
                f"GHS {payout['amount']:.2f}"
            )


def main():
    group = SusuGroup("50.00")

    # Example members from the challenge description.
    group.add_member("Ama")
    group.add_member("Kofi")
    group.add_member("Esi")

    print("Welcome to the Susu Group Tracker!")
    print(f"Weekly contribution: GHS {group.weekly_contribution:.2f}")
    print("Initial members:", ", ".join(group.members))

    while True:
        print("\n=== SUSU GROUP TRACKER ===")
        print("1. Add a member")
        print("2. Record a payment")
        print("3. Close the current week")
        print("4. View report")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            name = input("Enter the member's name: ")

            try:
                group.add_member(name)
                print(f"{name.strip()} added successfully.")
            except ValueError as error:
                print("Error:", error)

        elif choice == "2":
            name = input("Member name: ").strip()
            amount_text = input("Payment amount (GHS): ").strip()

            try:
                amount = Decimal(amount_text)
                group.record_payment(name, amount)
                print("Payment recorded successfully.")
            except (ValueError, InvalidOperation) as error:
                print("Error:", error)

        elif choice == "3":
            try:
                result = group.close_week()

                if result["closed"]:
                    print(
                        f"Week closed! {result['recipient']} received "
                        f"GHS {result['amount']:.2f}."
                    )
                else:
                    print(
                        f"Week {result['week']} cannot close yet. "
                        "Outstanding payments:"
                    )

                    for name, amount in result["unpaid"].items():
                        print(f"  {name} owes GHS {amount:.2f}")

            except ValueError as error:
                print("Error:", error)

        elif choice == "4":
            show_report(group)

        elif choice == "5":
            print("Thank you for using the Susu Group Tracker!")
            break

        else:
            print("Invalid option. Choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
