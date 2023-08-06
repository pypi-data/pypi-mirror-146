# imaginarydate

> Fast tool to manipulate imaginary date for RPG or else...

Status: Beta

Compatibilité : Python 3.6, 3.7, 3.8, 3.9, 3.10.

### installation

**imagniarydate** s'installe comme les autres packages à l'aide de ``pip``, de préférence dans une environnement virtuel
tel que ``virtualenv`` ou ``pipenv``.

```bash
$ pip install imaginarydate
```

Pour contribuer avec le code, clonez le dépôt et installez le mode développement : [https://github.com/mickbad/pyImaginaryDate]()

```bash
$ git clone git@github.com:mickbad/pyImaginaryDate.git
$ cd pyImaginaryDate
$ pipenv install
$ pipenv shell
(pyImaginaryDate) $ 
```

### utilisation

Utilisation basique de tests sur les calendriers déjà programmés

```bash
(pyImaginaryDate) $ python main.py
** testing add date
...
Iron Throne: 479 days per year, 22 months per year, 11 days per week
...
1/4/1900 +1 day, +2 months => Jüman 2 Pern 1900
...
Osabuñ: 100 days per year, 10 months per year, 1 days per week
...
[Reference date] date 01/01/00 from Iron Throne <=> 00/09/01 from Osabuñ
date 25/12/925 from Iron Throne <=> 4434/04/01 from Osabuñ
date 13/05/1764 from Iron Throne <=> 8451/04/10 from Osabuñ
date 14/07/1255 from Iron Throne <=> 6013/07/10 from Osabuñ
date 12/02/1814 from Iron Throne <=> 8690/02/08 from Osabuñ
date 08/13/4014 from Iron Throne <=> 19230/07/10 from Osabuñ
```

Utilisation console

```python
>>> from imaginarydate import ImaginaryTestingDate
>>> ImaginaryTestingDate(day=-10, month=2, year=1900).human
'dimanche 21 janvier 1900'

>>> ImaginaryTestingDate(day=-10, month=2, year=1900).add(day=10).human
'mercredi 31 janvier 1900'

>>> print(ImaginaryTestingDate(day=-10, month=2, year=1900).add(year=10))
21/01/1910

>>> print(ImaginaryTestingDate(day=10, month=2, year=1900).datestamp)
228041

>>> from imaginarydate.nakarina import IronThroneDate
>>> # convertion date différents calendrier sachant que IronThrone a un décalage de 9 mois sur le début du calendrier Testing
>>> IronThroneDate().from_date(ImaginaryTestingDate(day=10, month=2, year=1900), date_offset=IronThroneDate(month=1)).human
'Ģan 17 Magnolia 476'
```

### Origine

Cette bibliothèque a pour origine de faciliter les convertions des différents univers de [www.nakarina.com](https://www.nakarina.com/). 
Cela sert dans JDR/RPG (jeux de rôles) de manière plus générale

### Création

On peut créer un calendrier particulier à partir de la base de ce module afin d'établir son propre gestion de dates.

Il suffit de créer une classe de configuration.

```python
from imaginarydate import ImaginaryCalendarFormat, ImaginaryDate


class MyTestingDate(ImaginaryDate):
    """
    Class for testing
    """
    calendar_config = ImaginaryCalendarFormat(
        name="TestingCal",
        days_per_week=[
          "lundi", 
          "mardi", 
          "mercredi", 
          "jeudi", 
          "vendredi", 
          "samedi", 
          "dimanche"
        ],
        start_day_week_initial="vendredi",
        months_per_year=[
            {"name": "janvier", "count": 31},
            {"name": "février", "count": 28},
            {"name": "mars", "count": 31},
            {"name": "avril", "count": 30},
        ]
    )

# >>> print(MyTestingDate().human)
# vendredi 1 janvier 00
```

La propriété ```calendar_config``` contient la configuration du calendrier fictif mais on peut le traduire directement dans le constructeur comme suit.
Cela permet de gérer des cas particulier suivant les circonstances du jeu de construction.

```python
from imaginarydate import ImaginaryCalendarFormat, ImaginaryDate


class MyTestingDate(ImaginaryDate):
    """
    Class for testing
    """
    def __init__(self, day=0, month=0, year=0):
        """
        pick a date constructor

        :param day: current day
        :param month: current month
        :param year: current year
        """
        # new calendar configuration
        greg = ImaginaryCalendarFormat(
            name="TestingCal",
            days_per_week=[
              "lundi", 
              "mardi", 
              "mercredi", 
              "jeudi", 
              "vendredi", 
              "samedi", 
              "dimanche"
            ],
            start_day_week_initial="vendredi",
            months_per_year=[
                {"name": "janvier", "count": 31},
                {"name": "février", "count": 28},
                {"name": "mars", "count": 31},
                {"name": "avril", "count": 30},
            ]
        )

        # make object
        super(MyTestingDate, self).__init__(
          calendar=greg, 
          day=day, 
          month=month,
          year=year
        )

# >>> print(MyTestingDate().human)
# vendredi 1 janvier 00
```

La classe ``ImaginaryCalendarFormat`` contient des paramètres de configuration
* ``name`` (obligatoire) : nom du calendrier
* ``days_per_week`` (optionnel) : liste des noms de jours d'une semaine (si vide, un seul jour numérique est créé)
* ``start_day_week_initial`` (optionnel) : jour commençant l'origine du calendrier (différent du premier jour de la semaine, ici lundi) : 1/1/00 donne ici un vendredi
* ``months_per_year`` (obligatoire) : dictionnaire pour configurer la liste des mois d'une année
  * ``name`` (optionnel) : nom du mois (si vide, il est remplacé par une valeur numérique)
  * ``count`` (obligatoire) : nombre de jour dans le mois courant

Parfois la représentation d'un jour ne se fait pas normalement si par exemple il n'y a pas de nom du jour de la semaine ou de nom des mois. 
On peut surcharger la représentation dans la classe comme ceci

```python
from imaginarydate import ImaginaryCalendarFormat, ImaginaryDate


class MyTestingDate(ImaginaryDate):
    """
    Class for testing
    """
    calendar_config = ImaginaryCalendarFormat(
        name="TestingCal",
        days_per_week=[
          "lundi", 
          "mardi", 
          "mercredi", 
          "jeudi", 
          "vendredi", 
          "samedi", 
          "dimanche"
        ],
        start_day_week_initial="vendredi",
        months_per_year=[
            {"name": "janvier", "count": 31},
            {"name": "février", "count": 28},
            {"name": "mars", "count": 31},
            {"name": "avril", "count": 30},
        ]
    )
    
    # représentation de l'objet au format string
    def __str__(self):
      """
      string representation
      :return: str
      """
      return f"{self.year:02d}/{self.month:02d}/{self.day:02d}"


    # sortie plus évolué pour l'humain
    @property
    def human(self):
        """
        string representation
        :return: str
        """
        return f"Le jour est '{self.day_of_week_human} {self}'"


# >>> print(MyTestingDate(year=1900).human)
# Le jour est 'vendredi 1900/01/01'
```

Pour bénéficier du moteur interne de tests sur des dates pseudos aléatoires, la classe doit hériter de ``ImaginaryTestingDate``

```python
from imaginarydate import ImaginaryCalendarFormat, ImaginaryTestingDate


class MyTesting2Date(ImaginaryTestingDate):
    """
    Class for testing 2
    """
    # calendar configuration
    calendar_config = ImaginaryCalendarFormat(
        name="Testing 2",
        months_per_year=[
            {"count": 10},
            {"count": 10},
        ]
    )

print(MyTesting2Date.calendar_config)
# Testing 2: 20 days per year, 2 months per year, 1 days per week

MyTesting2Date().tests()
# ... results...
```

### Limitations

Les calendriers inventés ou déjà configurés ne gèrent pas :
* les années bisextilles
* les doublons de nom de mois (_à venir_)
* les doublons de nom de semaine (_à venir_)

### licence

Ce projet est librement utilisable, publié sous licence MIT.

MIT Licence.
