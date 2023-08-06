# ----------------------------------------------------------------------------------------------------------------------
# imaginarydate.py
#
# Class for create basic structure date
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
class ImaginaryCalendarFormat:
    """
    Object to store date definition (day, month, year)
    """

    # ------------------------------------------------------------------------------------------------------------------
    # constructor
    def __init__(self, name, months_per_year, days_per_week=None, start_day_week_initial=""):
        """
        Structure of a year

        :param name: Calendar name

        :param days_per_week: days names listing per week
        format: ['monday', 'tuesday', ...]

        :param months_per_year: months names listring per year with days count
        format: [{'name': 'January', 'count': 31}, ...]

        :param start_day_week_initial: name of day where 1/1/00 start
        """
        # properties
        self.name = name
        self.countMonths = 0
        self.monthsDays = []
        self.weekDuration = 0
        self.daysName = []
        self.countDaysPerYear = 0
        self.start_day_week_initial_index = None
        self.set_calendar(days_per_week=days_per_week, months_per_year=months_per_year, start_day_week_initial=start_day_week_initial)

    # ------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        """
        string representation
        :return: str
        """
        return f"{self.name}: {self.countDaysPerYear} days per year, {self.countMonths} months per year, {self.weekDuration} days per week"

    # ------------------------------------------------------------------------------------------------------------------
    def set_calendar(self, months_per_year, days_per_week=None, start_day_week_initial=""):
        """
        Set a new calendar configuration

        :param days_per_week: days names listing per week
        format: ['monday', 'tuesday', ...]

        :param months_per_year: months names listring per year with days count
        format: [{'name': 'January', 'count': 31}, ...]

        :param start_day_week_initial: name of day where 1/1/00 start
        """
        # check days_per_week format
        try:
            # parse datas
            self.daysName = []
            if days_per_week is not None:
                self.daysName = [name.strip() for name in days_per_week]
            self.weekDuration = len(self.daysName)

            # check
            if self.weekDuration < 1:
                self.daysName.append("")
                self.weekDuration = len(self.daysName)

        except Exception as e:
            raise Exception(f"ImaginaryDateException: days_per_week: {e}")

        # check months_per_year
        try:
            # parse datas
            month_id = 1
            self.countDaysPerYear = 0
            self.monthsDays = []  # list to store all month name and count days
            for d in months_per_year:
                countdays = int(d["count"])
                namemonth = f"{d['name']}" if "name" in d else f"{month_id}"
                self.monthsDays.append({
                    "name": namemonth,
                    "count": countdays,
                })
                self.countDaysPerYear += countdays
                month_id += 1

            self.countMonths = len(self.monthsDays)

            # check
            if self.countMonths < 1:
                raise Exception(f"bad count month in year: {self.countMonths}")

        except Exception as e:
            raise Exception(f"ImaginaryDateException: months_per_year: {e}")

        # start day in 1/1/00
        start_day_week_initial = start_day_week_initial.strip()
        if len(start_day_week_initial) == 0 or start_day_week_initial not in self.daysName:
            # first day of the week
            self.start_day_week_initial_index = 0

        else:
            self.start_day_week_initial_index = 0
            for d in self.daysName:
                if d == start_day_week_initial:
                    break
                self.start_day_week_initial_index += 1


# ----------------------------------------------------------------------------------------------------------------------
class ImaginaryDate:
    """
    Date manipulation form imaginary calendar
    """

    # ------------------------------------------------------------------------------------------------------------------
    # constructor
    def __init__(self, calendar, day=0, month=0, year=0):
        """
        pick a date constructor

        :param calendar: instance of ImaginaryCalendarFormat
        :param day: current day
        :param month: current month
        :param year: current year
        """
        if not isinstance(calendar, ImaginaryCalendarFormat):
            raise Exception("ImaginaryDate: calendar bad format")

        # check
        if calendar.countDaysPerYear < 1:
            raise Exception("ImaginaryDate: calendar empty")

        # store
        self.calendar = calendar
        self.day = 1
        self.month = 1
        self.year = 0

        # pick a date
        self.set_date(day=day, month=month, year=year)

    # ------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        """
        string representation
        :return: str
        """
        return f"{self.day:02d}/{self.month:02d}/{self.year:02d}"

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def name(self):
        """
        Name of current calendar
        :return: str
        """
        return self.calendar.name

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def human(self):
        """
        string representation
        :return: str
        """
        return f"{self.day_of_week_human} {self.day} {self.calendar.monthsDays[self.month - 1]['name']} {self.year:02d}"

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def day_of_week_human(self):
        """
        String representation of day of week
        :return: string
        """
        return self.calendar.daysName[self.day_of_week - 1]

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_valid(self):
        """
        Check if current date is valid
        :return: boolean
        """
        return self.day < 1 or self.day > self.calendar.monthsDays[self.month - 1]["count"] or self.month < 1 or self.month > self.calendar.countMonths

    # ------------------------------------------------------------------------------------------------------------------
    # Date manipulation
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def set_date(self, day=0, month=0, year=0):
        """
        pick a date

        :param day: current day
        :param month: current month
        :param year: current year
        :return: self
        """
        if day == 0:
            day = 1
        if month == 0:
            month = 1

        # store
        self.day = day
        self.month = month
        self.year = year
        self._calculate_date()
        return self

    # ------------------------------------------------------------------------------------------------------------------
    def parse(self, date_string):
        """
        Parse string date format
        :param date_string:
        :return:
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def add(self, day=0, month=0, year=0):
        """
        Add a day/month/year to current day
        :param day:
        :param month:
        :param year:
        :return: self
        """
        self.day += day
        self.month += month
        self.year += year
        self._calculate_date()
        return self

    # ------------------------------------------------------------------------------------------------------------------
    def from_datestamp(self, datestamp, datestamp_offset=0):
        """
        create new date from datestamp
        :param datestamp: days count from 0
        :param datestamp_offset: day offset from 0
        :return: self
        """
        # décalage du datestamp (bidouille)
        datestamp += datestamp_offset - 1 if datestamp_offset != 0 else 0

        # to optimize big datestamp, reduce count to year/month/day
        year = int(datestamp / self.calendar.countDaysPerYear)
        month = 0
        day = datestamp - year * self.calendar.countDaysPerYear

        # new date
        self.set_date(day=day, month=month, year=year)
        assert (self.datestamp == datestamp)
        return self

    # ------------------------------------------------------------------------------------------------------------------
    def from_date(self, date, datestamp_offset=0, date_offset=None):
        """
        create new date from date
        :param date: date
        :param datestamp_offset: day offset from 0
        :param date_offset: day offset from 0
        :return: self
        """
        if not isinstance(date, ImaginaryDate):
            raise Exception("from_date: date bad format")

        # real date offset
        offset_add = 0
        if date_offset is not None:
            if not isinstance(date_offset, ImaginaryDate):
                raise Exception("from_date: date_offset bad format")
            offset_add = date_offset.datestamp

        return self.from_datestamp(date.datestamp, datestamp_offset=datestamp_offset + offset_add)

    # ------------------------------------------------------------------------------------------------------------------
    # tools
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def _calculate_date(self):
        """
        Calculate real date from current date in object
        """
        # --------------------------------------------------------------------------------------------------------------
        def calc_month():
            # parse month (+)
            if self.month > self.calendar.countMonths:
                # change current year
                self.year += int((self.month-1) / self.calendar.countMonths)
                # change current month
                self.month = (self.month-1) % self.calendar.countMonths + 1

            # parse month (-)
            if self.month < 0:
                # change current year
                self.year += int((self.month+1) / self.calendar.countMonths) - 1
                # change current month
                self.month = self.month % self.calendar.countMonths + 1

        # parse month
        calc_month()

        # parse day (+)
        while self.day > self.calendar.monthsDays[self.month - 1]["count"]:
            self.day -= self.calendar.monthsDays[self.month - 1]["count"]
            self.month += 1
            calc_month()

        # parse day (-)
        while self.day < 1:
            self.month -= 1
            if self.month == 0:
                self.month = -1
            calc_month()
            self.day += self.calendar.monthsDays[self.month - 1]["count"]

        # calulate datestamp
        self.datestamp = self._calculate_total_days()

        # calculate day of week
        # self.day_of_week = (self.datestamp) % self.calendar.weekDuration
        self.day_of_week = (self.datestamp + self.calendar.start_day_week_initial_index) % self.calendar.weekDuration

    # ------------------------------------------------------------------------------------------------------------------
    def _calculate_total_days(self):
        """
        Get days count from 0/00/0000 to date (negative)
        :return: int
        """
        # convert date to days
        days_count = self.year * self.calendar.countDaysPerYear

        current_month = self.month - 1
        while current_month > 0:
            days_count += self.calendar.monthsDays[current_month - 1]["count"]
            current_month -= 1

        days_count += self.day
        return days_count
