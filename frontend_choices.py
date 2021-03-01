import calendar

PROFILE_CHOICES = [ ("Covermax","Covermax"),
                    ("Maxcover","Maxcover"),
                    ("IT4","IT4"),
                    ("Tekdek","Tekdek"),
                    ("Versatile","Versatile"),
                    ("Romantile","Romantile"),
                    ("Normal Corrugation","Normal Corrugation"),
                    ("Plain Sheet","Plain Sheet"),
                    ("Normal Ridge","Normal Ridge"),
                    ("Versatile Ridge","Versatile Ridge"),
                    ("Romantile Ridge","Romantile Ridge")
                    ]

PRODUCTION_TYPE_CHOICES = [('Work Order','Work Order'),
                            ('Standard','Standard')]

ORDER_COLOUR_CHOICES = [("Dark Green","Dark Green"),
                    ("Potters Clay","Potters Clay"),
                    ("Tile Red","Tile Red"),
                    ("Brick Red","Brick Red"),
                    ("Maroon","Maroon"),
                    ("Zincal","Zincal"),
                    ("Service Grey","Service Grey"),
                    ("Galvanized Iron","Galvanized Iron"),
                    ("Avocado","Avocado"),
                    ("Lagoon","Lagoon"),
                    ("Sky Blue","Sky Blue"),
                    ("Charcoal Black","Charcoal Black"),
                    ("Chocolate","Chocolate")]


ORDER_FINISH_CHOICES = [("Matt","Matt"),
                        ("Plain","Plain")]


PRODUCTION_BOND_CHOICES = [ ("Local","Local"),
                            ("Export","Export")]


PRODUCTION_SHIFT_CHOICES = [ ("Day","Day"),
                            ("Night","Night")]
                            

ORDER_GAUGE_CHOICES = [
                            (32,32),
                            (30,30),
                            (28,28),
                            (26,26),
                            (24,24),
                            (22,22),
                            (20,20),
                        ]

ORDER_WIDTH_CHOICES = [
                            (1220,1220),
                            (975, 975),
                            (960,960),
                            (487,487),
                            (462,462),
                            (320,320),
                            ]

PROFILE_MACHINE_CHOICES = [("Covermax","Covermax"),
                    ("Maxcover","Covermax"),
                    ("IT4","Tekdek"),
                    ("Tekdek","Tekdek"),
                    ("Versatile","Versatile"),
                    ("Romantile","Romantile"),
                    ("Normal Corrugation","Normal Corrugation"),
                    ("Plain Sheet","Plain Sheet"),
                    ("Normal Ridge","Normal Ridge"),
                    ("Versatile","Versatile Ridge"),
                    ("Romantile","Romantile Ridge")]

COIL_TYPES_CHOICES = [
                        ("HRC", "HRC"),
                        ("PPAZ", "PPAZ"),
                        ("AZ", "AZ"),
                        ("WIRE","WIRE"),
                    ]

COIL_LOCATION = [   
                    ("Bond", "Bond"),
                    ("Production", "Production"),
                ]

COIL_STATUS = [
                    ("New", "New"),
                    ("Baby coil", "Baby Coil"),
                    ("Finished", "Finished"),
                ]

PIECE_STATUS_CHOICES = [
                    ("Tranferred", "Transferred"),
                    ("Not Transferred", "Not Transferred"),
                ]

months = [month for month in range(1, 13)] 
MONTH_LIST_CHOICES = [(month, calendar.month_abbr[month]) for month in months]
DAYS_LIST_CHOICES = [day for day in range(1,32)] 