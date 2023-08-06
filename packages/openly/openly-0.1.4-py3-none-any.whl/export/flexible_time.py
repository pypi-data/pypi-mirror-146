from typing import Tuple

"""
This monkey-business hides the complexity behind deciding what defines a certain time bracket
Specifically for "mohinga" where we have different "years" and different "quarters" depending on the year
"""


class DefaultDates:
    """
    flexible_time.DefaultDates(2019).get_all_quarters()
    >>> [
        ('2019-04-01', '2019-06-30'),
        ('2019-07-01', '2019-09-30'),
        ('2019-10-01', '2019-12-31'),
        ('2020-01-01', '2020-03-31')
    ]
    """

    def __init__(self, year):
        self.year = year
        self.fy_start_quarter = 2  # Starts in April by default

    @property
    def label(self):
        return "{}/{}".format(self.year, self.year + 1)

    def calendar_quarter(self, quarter=1) -> Tuple[str, str]:
        year = self.year

        while quarter >= 5:
            quarter = quarter - 4
            year += 1
        while quarter < 0:
            quarter = quarter + 4
            year -= 1

        if quarter == 1:
            return ("{year}-01-01".format(year=year), "{year}-03-31".format(year=year))
        elif quarter == 2:
            return ("{year}-04-01".format(year=year), "{year}-06-30".format(year=year))
        elif quarter == 3:
            return ("{year}-07-01".format(year=year), "{year}-09-30".format(year=year))
        elif quarter == 4:
            return ("{year}-10-01".format(year=year), "{year}-12-31".format(year=year))
        else:
            raise TypeError("Quarter invalid %s" % (quarter))

    def get_quarter_dates(self, quarter: int = 1):
        """
        Return the start and end dates as ISO format for quarters in a given year
        """
        fy_quarter = quarter + self.fy_start_quarter - 1
        return self.calendar_quarter(fy_quarter)

    def get_year_start_date(self):
        return self.get_quarter_dates(quarter=1)[0]

    def get_year_end_date(self):
        return self.get_quarter_dates(quarter=4)[1]

    def get_all_quarters(self) -> Tuple[Tuple[str, str], ...]:
        all_quarters = [
            self.get_quarter_dates(quarter=1),
            self.get_quarter_dates(quarter=2),
            self.get_quarter_dates(quarter=3),
            self.get_quarter_dates(quarter=4),
        ]
        return all_quarters


class MyanmarDates(DefaultDates):
    """
    flexible_time.MyanmarDates(2017).get_all_quarters()
    >>> [
        ('2017-04-01', '2017-06-30'),
        ('2017-07-01', '2017-09-30'),
        ('2017-10-01', '2017-12-31'),
        ('2018-01-01', '2018-03-31')
    ]
    flexible_time.MyanmarDates(2018).get_all_quarters()
    >>> [
            ('2018-10-01', '2018-12-31'),
            ('2019-01-01', '2019-03-31'),
            ('2019-04-01', '2019-06-30'),
            ('2019-07-01', '2019-09-30')
        ]
    # To get the special six-month in 2018,
    flexible_time.MyanmarDates(2018, six_month_period=True).get_all_quarters()
    >>> [('2018-04-01', '2018-06-30'), ('2018-07-01', '2018-09-30')]

    """

    def __init__(self, year, six_month_period=False):
        super().__init__(year)
        if year != 2018 and six_month_period:
            raise AssertionError("Only 2018 can have the special six_month_period")
        if year > 2017 and not six_month_period:
            self.fy_start_quarter = 4
        self.six_month_period = six_month_period

    def get_all_quarters(self):
        if self.six_month_period:
            return super().get_all_quarters()[:2]
        return super().get_all_quarters()

    def get_year_end_date(self):
        if self.six_month_period:
            return self.get_quarter_dates(quarter=2)[1]
        return super().get_year_end_date()

    @property
    def label(self):
        if self.six_month_period:
            return "2018"
        return super().label


class DefaultDateRange:
    def __init__(self, start_year: int = 2010, end_year: int = 2020):
        self.years = range(start_year, end_year + 1)

    def get_all_quarters(self):
        """
        Returns year label and nested quarters range
        """
        returns = {}

        for year in self.years:
            d = DefaultDates(year)
            returns[d.label] = d.get_all_quarters()
        return returns

    def get_all_years(self):
        """
        Returns year label and nested date range
        The extra nesting is to make the structure same as with "quarters"
        """
        returns = {}

        for year in self.years:
            d = DefaultDates(year)
            returns[d.label] = [(d.get_year_start_date(), d.get_year_end_date())]
        return returns


class MyanmarDateRange(DefaultDateRange):
    def get_all_quarters(self):
        returns = {}

        for year in self.years:

            if year == 2018:
                # Inject the "special" year
                special_year = MyanmarDates(year, six_month_period=True)
                returns[special_year.label] = special_year.get_all_quarters()

            d = MyanmarDates(year)
            returns[d.label] = d.get_all_quarters()

        return returns

    def get_all_years(self):
        returns = {}

        for year in self.years:
            if year == 2018:
                print("SPEC year")
                # Inject the "special" year
                special_year = MyanmarDates(year, six_month_period=True)
                returns[special_year.label] = [
                    (
                        special_year.get_year_start_date(),
                        special_year.get_year_end_date(),
                    )
                ]

            d = MyanmarDates(year)
            returns[d.label] = [(d.get_year_start_date(), d.get_year_end_date())]
        return returns
