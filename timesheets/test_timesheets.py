import unittest
from unittest import TestCase
from unittest.mock import patch, call # patch the library that can deal with with patching so replacing things with mock objects

import timesheets # import the code we are testing

# Make test case. subclass test case
class TestTimeSheet(TestCase):
    
    """ Mock input() and force it to return a value """

    @patch('builtins.input', side_effect=['2']) # @patch will create a mock version and will replace builtins.input with a mock to return the value of 2
    # Review self represents the instance of the class, by usingn self we can access the attributes and methods of the class
    def test_get_hours_for_day(self, mock_input): # the arguement mock_input can be named anything, it is a reference to the mock object, required to have this arguement here
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(2, hours) # Assert the value we want

    @patch('builtins.input', side_effect=['cat', '', 'fish', '123bird', 'pizza1234','2']) # side_effect is a list for reason, it is a list of return values
    def test_get_hours_for_day_non_numeric_rejected(self, mock_input): 
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(2, hours) 

    @patch('builtins.input', side_effect=['-1', '-1000', '5']) 
    def test_get_hours_for_day_hours_greater_than_zero(self, mock_input): 
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(5, hours)

    @patch('builtins.input', side_effect=['24.0000000001', '1000', '25', '9']) # First four values should not be ok except 9
    def test_get_hours_for_day_hours_less_than24(self, mock_input): 
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(9, hours)

    @patch('builtins.print') # create a mock print function and replace it with the mock, again we'll use the patch decorator
    # No side_effect for 'builtins.print', side_effect=[] because print does not return anything
    def test_display_total(self, mock_print): # Again self is the first arguement, since this is a method in a class, we need another arguement which is the mock object
        timesheets.display_total(123)
        # How do we know the right thing was printed? we do that by replacing the regular print function with the mock. Basically calls the mock print instead of the the built-in print
        mock_print.assert_called_once_with('Total hours worked: 123')


    """ Notes: side_effect if you want to return different values everytime
        return_value if you always want to return the same value """


    """ Write a test for aler_not_meet_min_hours() if the hours is less than the minimum then run the alert function which gives off a beep noise """
    @patch('timesheets.alert') # name of the function, does not need a return value because it is not returning anything. Patch remember creates a fake function, replaces our real time sheets alert function
    def test_alert_meet_min_hours_doesnt_meet(self, mock_alert): # Need self because it is a method in a class and variable for our mock
        timesheets.alert_not_meet_min_hours(12, 30) # if 12 is smaller than 30 then we expect an alery to happen
        mock_alert.assert_called_once()

    @patch('timesheets.alert') 
    def test_alert_meet_min_hours_does_meet_min(self, mock_alert): 
        timesheets.alert_not_meet_min_hours(40, 30) 
        mock_alert.assert_not_called() # we want to assert that the alert is not called

    """ Write a test for get_hours(). This function is creating a dictionary. It's getting the hours for a day and then adding that data to the dictionary. 
    This function calls another function get_hours_for_day(). """
    @patch('timesheets.get_hours_for_day') # We are mocking get_hours_for_day() and this will have return values
    def test_get_hours(self, mock_get_hours): # Need self because it is a method in a class
        mock_hours = [5, 7, 9]
        mock_get_hours.side_effect = mock_hours # Set the side effect here instead. We do this because we want our data in a variable above for example
        days = ['m', 't', 'w']
        expected_hours = dict(zip(days, mock_hours)) # {'m': 5, 't': 7, 'w': 9}
        hours = timesheets.get_hours(days) # This is what the program returns. We need to give get hours a list of days
        self.assertEqual(expected_hours, hours) # expected hours with hours
        # We do not need to mock inputs because we are mocking get_hours_for_days() in the get_hours() function (line 24). So we have a mock that replaces get_hours()

    """ Write a test for display_hours() which prints a table """
    @patch('builtins.print')
    def test_display_hours(self, mock_print):

        # Arrange 
        """ Setting out what we expect the calls to be"""
        example = {'M': 3, 'T': 12, 'W': 8.5}
        # A call object is a tuple or an ordered and unchangable list
        expected_table_calls = [
            call('Day            Hours Worked   '),
            call('M              3              '),
            call('T              12             '),
            call('W              8.5            '),
        ]

        # Action
        """ Take the action """
        timesheets.display_hours(example) # needs a dictionary example

        # Assert
        """ Assert things are the way we think they are"""
        mock_print.assert_has_calls(expected_table_calls)

    def test_total_hours(self):
        example = {'M': 3, 'T': 12, 'W': 8.5}
        total = timesheets.total_hours(example) # Call total hours with our example
        expected_total = 3 + 12 + 8.5
        self.assertEqual(total, expected_total)

if __name__ == '__main__':
    unittest.main()