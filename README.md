# Susu Group Tracker

## Overview

Susu Group Tracker is a Python command-line application that manages a rotating savings group. Each member contributes a fixed amount every week, and the total pot is paid to one member in joining order once everyone has paid in full.

## Features

- Add members with unique names.
- Record full or partial weekly contributions.
- Calculate outstanding balances for each member.
- Prevent zero, negative, and excessive payments.
- Reject payments from unknown members.
- Prevent a week from closing while contributions are outstanding.
- Pay the full pot to the correct member in rotation.
- Display the current week, payment status, outstanding balances, and payout history.
- Use Python's Decimal type for accurate money calculations.
- Run automated tests using unittest.

## Requirements

- Python 3
- No external packages are required.

## How to Run

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run the application:

   ```bash
   py main.py