# ----------------------------------------------------------------------------------------------------------------------
# ironthronedate.py
#
# Project: nakarina.com
#
# Description:
#     Calendrier du Trône de Fer :
#
#     Nombre de jours dans l'année : 479
#     Nombre de mois : 22
#     Nombre de jours dans le mois : Diffère selon le mois.
#     Nombre de jours dans la semaine : 11
#
#     Noms des mois :
#     1. Râ (20 jours)
#     2. Magnolia (25 jours)
#     3. Lúra (26 jours)
#     4. Ïn (20 jours)
#     5. Zarox (20 jours)
#     6. Pern (20 jours)
#     7. Sèn (25 jours)
#     8. Dimanche (24 jours)
#     9. Koil (24 jours)
#     10. Œil (27 jours)
#     11. Hydrogena (20 jours)
#     12. Jos (25 jours)
#     13. Bernoul (20 jours)
#     14. Delantea (18 jours)
#     15. Hoal (27 jours)
#     16. Alao (20 jours)
#     17. Nãl (20 jours)
#     18. Juista (20 jours)
#     19. Smiling (20 jours)
#     20. Treizce (13 jours)
#     21. Ylma (20 jours)
#     22. Stameta (25 jours)
#
#     Noms des Jours dans la Semaine :
#     1. Èran
#     2. Meàn
#     3. Rýsian
#     4. Jüman
#     5. Stefan
#     6. Arían
#     7. Diman
#     8. Ģan
#     9. Fán
#     10. Raïan
#     11. Tull
#
#     Le jour utilisé comme référence est le Fán 1/1/00 du Système du Trône de Fer
# ----------------------------------------------------------------------------------------------------------------------

from imaginarydate import ImaginaryCalendarFormat, ImaginaryTestingDate


# ----------------------------------------------------------------------------------------------------------------------
class IronThroneDate(ImaginaryTestingDate):
    """
    Class for Iron Throne from nakarina.com
    """
    # calendar configuration
    calendar_config = ImaginaryCalendarFormat(
        name="Iron Throne",
        days_per_week=[
            "Èran",
            "Meàn",
            "Rýsian",
            "Jüman",
            "Stefan",
            "Arían",
            "Diman",
            "Ģan",
            "Fán",
            "Raïan",
            "Tull",
        ],
        start_day_week_initial="Fán",
        months_per_year=[
            {"name": "Râ", "count": 20},
            {"name": "Magnolia", "count": 25},
            {"name": "Lúra", "count": 26},
            {"name": "Ïn", "count": 20},
            {"name": "Zarox", "count": 20},
            {"name": "Pern", "count": 20},
            {"name": "Sèn", "count": 25},
            {"name": "Dimanche", "count": 24},
            {"name": "Koil", "count": 24},
            {"name": "Œil", "count": 27},
            {"name": "Hydrogena", "count": 20},
            {"name": "Jos", "count": 25},
            {"name": "Bernoul", "count": 20},
            {"name": "Delantea", "count": 18},
            {"name": "Hoal", "count": 27},
            {"name": "Alao", "count": 20},
            {"name": "Nãl", "count": 20},
            {"name": "Juista", "count": 20},
            {"name": "Smiling", "count": 20},
            {"name": "Treizce", "count": 13},
            {"name": "Ylma", "count": 20},
            {"name": "Stameta", "count": 25},
        ]
    )

