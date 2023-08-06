# ----------------------------------------------------------------------------------------------------------------------
# testingdate.py
#
# Class for create testing structure
# ----------------------------------------------------------------------------------------------------------------------

from imaginarydate import ImaginaryCalendarFormat, ImaginaryDate


# ----------------------------------------------------------------------------------------------------------------------
class ImaginaryTestingDate(ImaginaryDate):
    """
    Class for testing
    """
    calendar_config = ImaginaryCalendarFormat(
        name="TestingCal",
        days_per_week=["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
        start_day_week_initial="vendredi",
        months_per_year=[
            {"name": "janvier", "count": 31},
            {"name": "février", "count": 28},
            {"name": "mars", "count": 31},
            {"name": "avril", "count": 30},
        ]
    )

    # ------------------------------------------------------------------------------------------------------------------
    # constructor
    def __init__(self, day=0, month=0, year=0, calendar=None):
        """
        pick a date constructor

        :param day: current day
        :param month: current month
        :param year: current year
        :param calendar: set a new calendar from external
        """
        # calendar configuration from arguments
        if calendar is None:
            calendar = self.calendar_config

        # make object
        super(ImaginaryTestingDate, self).__init__(calendar=calendar, day=day, month=month, year=year)

    # ------------------------------------------------------------------------------------------------------------------
    # tools for testing
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def tests(self):
        """
        All tests
        """
        print(self.calendar)
        print()

        self.tests_months_change()
        print()

        self.tests_days_change()
        print()

        self.tests_adding_date()
        print()

        self.tests_from_date()
        print(80 * "-")

    # ------------------------------------------------------------------------------------------------------------------
    def tests_months_change(self):
        """
        Change months situation for tests
        """
        print("** testing with improbable months")
        for i in range(-17, 17):
            print(f"1/{i + 1}/1900 => {self.set_date(day=1, month=i + 1, year=1900)}")

    # ------------------------------------------------------------------------------------------------------------------
    def tests_days_change(self):
        """
        Change days situation for tests
        """
        print("** testing with improbable days")
        for i in range(-128, -1):
            print(f"{i + 1}/1/1900 => {self.set_date(day=i+1, month=1, year=1900).human}")
        print(f"31/4/1900 => {self.set_date(day=31, month=4, year=1900)}")
        print(f"64/4/1900 => {self.set_date(day=64, month=4, year=1900)}")
        print(f"64/4/1900 => {self.set_date(day=64, month=4, year=1900).human}")
        print(f"01/01/1900 => {self.set_date(day=1, month=1, year=1900).datestamp}")
        print(f"01/01/1900 => {self.set_date(day=1, month=1, year=1900).day_of_week_human}")

    # ------------------------------------------------------------------------------------------------------------------
    def tests_adding_date(self):
        """
        add element to date
        """
        print("** testing add date")
        print(f"1/4/1900 +1 day, +2 months => {self.set_date(day=1, month=4, year=1900).add(day=1, month=2).human}")
        print(f"28/4/1900 -27 days => {self.set_date(day=28, month=4, year=1900).add(day=-27).human}")
        print(f"28/4/1900 -28 days => {self.set_date(day=28, month=4, year=1900).add(day=-28).human}")
        print(f"1/4/1900 -1 days => {self.set_date(day=1, month=4, year=1900).add(day=-1).human}")
        print(f"-32/1/1900 -1 year => {self.set_date(day=-32, month=1, year=1900).add(year=-1).human}")

    # ------------------------------------------------------------------------------------------------------------------
    def tests_from_date(self):
        """
        new date from other date
        """
        print("** testing new date from other date")
        import random
        for dd in range(1, 5):
            d = self.set_date(day=random.randint(-17, 17), month=random.randint(-4, 5), year=1900 + random.randint(-10, 11))
            print(f"d = {d}; datestamp = {d.datestamp}; new date from date = {self.from_date(date=d).human}")
