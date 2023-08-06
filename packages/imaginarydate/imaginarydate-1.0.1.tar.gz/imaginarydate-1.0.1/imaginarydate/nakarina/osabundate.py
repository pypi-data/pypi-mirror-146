# ----------------------------------------------------------------------------------------------------------------------
# osabundate.py
#
# Project: nakarina.com
#
# Description:
#     Calendrier d'Osabuñ
#
#     Nombre de jours dans l'année : 100
#     Nombre de mois : 10
#     Nombre de jours dans le mois : 10
# ----------------------------------------------------------------------------------------------------------------------

from imaginarydate import ImaginaryCalendarFormat, ImaginaryTestingDate


# ----------------------------------------------------------------------------------------------------------------------
class OsabunDate(ImaginaryTestingDate):
    """
    Class for Osabuñ from nakarina.com
    """
    # calendar configuration
    calendar_config = ImaginaryCalendarFormat(
        name="Osabuñ",
        months_per_year=[
            {"count": 10},
            {"count": 10},
            {"count": 10},
            {"count": 10},
            {"count": 10},
            {"count": 10},
            {"count": 10},
            {"count": 10},
            {"count": 10},
            {"count": 10},
        ]
    )

    # ------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        """
        string representation
        :return: str
        """
        return f"{self.year:02d}/{self.month:02d}/{self.day:02d}"

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def human(self):
        """
        string representation
        :return: str
        """
        return f"An {self.year:02d} Mois {self.month} Jour {self.day}"

