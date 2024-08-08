import unittest
from datetime import datetime
from datetime import datetime, timedelta
import sslPDF
  # assuming this is the function that calculates start_date and end_date

class TestSslPDF(unittest.TestCase):
    def test_dates(self):
        # Read dates from file
        with open('dates.txt', 'r') as f:
            lines = f.readlines()
            start_date = lines[0].strip().split(': ')[1]
            end_date = lines[1].strip().split(': ')[1]

        # Convert dates back to datetime objects for comparison
        start_date = datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.strptime(end_date, "%m/%d/%Y")
        print(start_date, end_date)

        # Check that start_date is not in the future
        self.assertTrue(start_date <= datetime.today())

        # Check that start_date is before end_date
        self.assertTrue(start_date <= end_date)

        # Check that start_date is not too far in the past
        self.assertTrue(start_date >= datetime.today() - timedelta(days=365*100))

        # Check that end_date is not in the future
        self.assertTrue(end_date <= datetime.today())

        # Check that date range is within expected limits
        self.assertTrue(end_date - start_date <= timedelta(days=365*10))

        # Check that end_date is not more than one day before the current date
        self.assertTrue(end_date >= datetime.today() - timedelta(days=1))

if __name__ == '__main__':
    unittest.main()