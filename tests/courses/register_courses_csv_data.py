from pages.courses.register_courses_page import RegisterCoursesPage
from pages.home.navigation_page import NavigationPage
from utilities.teststatus import TestStatus
import unittest, pytest
from ddt import ddt, data, unpack
from utilities.read_data import getCSVData
import time

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class RegisterCoursesCSVDataTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        self.course = RegisterCoursesPage(self.driver)
        self.ts = TestStatus(self.driver)
        self.nav = NavigationPage(self.driver)

    def setUp(self):
        # self.driver.find_element_by_link_text("All Courses").click()
        # self.driver.find_element_by_xpath("//a[@class='navbar-brand header-logo']").click()
        # self.driver.get("https://learn.letskodeit.com/courses")
        self.nav.navigateToAllCourses()

    @pytest.mark.run(order=1)
    @data(*getCSVData("C:\Users\Durga\workspace_python\myframework\testdata.csv"))
    @unpack
    def test_invalidEnrollment(self, courseName, ccNum, ccExp, ccCVV):
        self.courses.enterCourseName(courseName)
        time.sleep(2)
        self.courses.selectCourseToEnroll(courseName)
        time.sleep(2)
        self.courses.enrollCourse(num=ccNum, exp=ccExp, cvv=ccCVV)
        time.sleep(2)
        result = self.courses.verifyEnrollFailed()
        self.ts.markFinal("test_invalidEnrollment", result, "Enrollment Failed Verification")