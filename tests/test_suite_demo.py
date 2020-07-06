import unittest
from tests.home.login_test import LoginTests
from tests.courses.register_courses_csv_data import RegisterCoursesCSVDataTests

tc1 = unittest.TestLoader().loadTestsFromTestCase(LoginTests)
tc2 = unittest.TestLoader().loadTestsFromTestCase(RegisterCoursesCSVDataTests)

smokeTest = unittest.TestSuite([tc1, tc2])

unittest.TextTestRunner(verbosity=2).run(smokeTest)
