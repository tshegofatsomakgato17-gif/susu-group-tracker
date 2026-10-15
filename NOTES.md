# Project Notes — Susu Group Tracker

## Design Decisions and Assumptions

1. **Fixed contribution:** Every member must contribute GHS 50.00 per week. The amount is configured in `main.py`.
2. **Unique members:** Member names must be unique and cannot be blank.
3. **Membership restrictions:** New members cannot be added once payments have started or the first week has ended. This keeps the payout order fair.
4. **Partial payments:** Members may pay in multiple instalments, and each payment reduces their outstanding balance.
5. **Week closure:** A week can only close when every member has paid the full weekly contribution. If anyone owes money, the program reports the outstanding balances and does not issue a payout.
6. **Payout order:** The first member to join receives the first payout. The next member receives the following payout. The order repeats if the group continues into another round.
7. **Money calculations:** Python's `Decimal` type is used to avoid common floating-point rounding errors.
8. **Data storage:** Member information, payments, and payout history are stored in memory. They are lost when the application exits.

## Testing

Automated tests use Python's built-in `unittest` framework. They check member validation, payment validation, partial payments, outstanding balances, incomplete week closure, successful payouts, payout order, and membership restrictions.

## Possible Future Improvements

- Save group information and payment history to a database or file.
- Allow the user to configure the weekly contribution when starting the program.
- Add dates and timestamps to payments and payouts.
- Improve the user interface and provide more detailed financial summaries.
- Add more validation and tests for unusual input values.