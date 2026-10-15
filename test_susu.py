
import unittest
from decimal import Decimal

from main import SusuGroup


class TestSusuGroup(unittest.TestCase):

    def setUp(self):
        self.group = SusuGroup("50.00")
        self.group.add_member("Ama")
        self.group.add_member("Kofi")
        self.group.add_member("Esi")

    def test_group_starts_at_week_one(self):
        self.assertEqual(self.group.current_week, 1)
        
    def test_invalid_weekly_contribution_is_rejected(self):
        with self.assertRaises(ValueError):
            SusuGroup("0")

        with self.assertRaises(ValueError):
            SusuGroup("-10")

    def test_empty_member_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.group.add_member("   ")

    def test_add_duplicate_member_is_rejected(self):
        with self.assertRaises(ValueError):
            self.group.add_member("Ama")

    def test_unknown_member_payment_is_rejected(self):
        with self.assertRaises(ValueError):
            self.group.record_payment("Kwame", "50.00")

    def test_zero_payment_is_rejected(self):
        with self.assertRaises(ValueError):
            self.group.record_payment("Ama", "0.00")

    def test_negative_payment_is_rejected(self):
        with self.assertRaises(ValueError):
            self.group.record_payment("Ama", "-5.00")

    def test_partial_payment_records_correct_balance(self):
        self.group.record_payment("Esi", "30.00")

        report = self.group.get_report()

        self.assertEqual(
            report["amounts_owed"]["Esi"],
            Decimal("20.00")
        )

    def test_overpayment_is_rejected(self):
        with self.assertRaises(ValueError):
            self.group.record_payment("Ama", "50.01")

    def test_week_cannot_close_when_payments_are_incomplete(self):
        self.group.record_payment("Ama", "50.00")
        self.group.record_payment("Kofi", "50.00")
        self.group.record_payment("Esi", "30.00")

        result = self.group.close_week()

        self.assertFalse(result["closed"])
        self.assertEqual(result["unpaid"]["Esi"], Decimal("20.00"))
        self.assertEqual(self.group.current_week, 1)
        self.assertEqual(len(self.group.payout_history), 0)

    def test_week_closes_when_everyone_pays_in_full(self):
        for name in self.group.members:
            self.group.record_payment(name, "50.00")

        result = self.group.close_week()

        self.assertTrue(result["closed"])
        self.assertEqual(result["recipient"], "Ama")
        self.assertEqual(result["amount"], Decimal("150.00"))
        self.assertEqual(self.group.current_week, 2)

    def test_next_payout_follows_joining_order(self):
        for name in self.group.members:
            self.group.record_payment(name, "50.00")
        self.group.close_week()

        for name in self.group.members:
            self.group.record_payment(name, "50.00")
        result = self.group.close_week()

        self.assertEqual(result["recipient"], "Kofi")

    def test_payment_above_remaining_balance_is_rejected(self):
        self.group.record_payment("Ama", "30.00")

        with self.assertRaises(ValueError):
            self.group.record_payment("Ama", "21.00")

    def test_membership_is_locked_after_payments_begin(self):
        self.group.record_payment("Ama", "10.00")

        with self.assertRaises(ValueError):
            self.group.add_member("Lerato")


if __name__ == "__main__":
    unittest.main(verbosity=2)
