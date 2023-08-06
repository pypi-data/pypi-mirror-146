from decimal import *
import numpy_financial as npf


class Calculator:

    @staticmethod
    def precise(input):
        """
        This method can be used to convert a value that would considered invalid in our system , for example -
        float with more than 8 tail digits  to a valid value.
        The value is rounded down to 8 tail digits and converted to decimal.
        :param input: float
        :return Decimal
        """

        num_to_line = str(input)

        cnt = 0
        pos = 0

        for _char in num_to_line:
            if _char == '.':
                pos = cnt
            cnt += 1

        num_8_digits = num_to_line[:pos + 9]

        result = Decimal(num_8_digits)

        # Rounding - handling special case when 9'th digit after the decimal point greater than 5
        if len(num_to_line) > pos + 9:
            if int(num_to_line[pos + 9]) >= 5:
                result += Decimal(0.00000001)
                result = Decimal(str(result)[:pos + 9])

        return result

    @staticmethod
    def calculate_monthly_payment(loan: Decimal, interest: Decimal, months: int, round_places:int):
        """
         This method can be used to calculate a MONTHLY loan payment basing on loan sum, loan interest
         and loan duration in months. It wraps numpy_financial 'pmt' method.
        :param round_places: rounding the final result according to this arg
        :param loan: loan sum
        :param interest: loan ANNUAL interest
        :param months: loan duration in months
        :return: loan MONTHLY payment
        """
        result = Decimal(npf.pmt(rate=interest / 12, nper=months, pv=-loan))
        return Decimal.__round__(result, round_places)




