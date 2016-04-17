human_sites = ['Stool',
               'Mouth',
               'Right hand',
               'Left hand',
               'Forehead',
               'Torso',
               'Left leg',
               'Right leg',
               'Nares',
               'Hair',
               'Tears',
               'Nasal mucus',
               'Ear wax',
               'Vaginal mucus']

animal_sites = ['Stool',
                'Mouth',
                'Nares',
                'Ears',
                'Skin',
                'Fur']

general_sites = ['Animal Habitat',
                 'Biofilm',
                 'Dust',
                 'Food',
                 'Fermented Food',
                 'Indoor Surface',
                 'Outdoor Surface',
                 'Plant habitat',
                 'Soil',
                 'Sole of shoe',
                 'Water']

collapse_human_sites = {
    'Stool': 'stool',
    'Mouth': 'oral',
    'Right hand': 'skin',
    'Left hand': 'skin',
    'Forehead': 'skin',
    'Torso': 'skin',
    'Left leg': 'skin',
    'Right leg': 'skin',
    'Nares': '',
    'Hair': '',
    'Tears': '',
    'Nasal mucus': '',
    'Ear wax': '',
    'Vaginal mucus': 'vaginal'
    }

# What categories of summary data aravailable for each collapsed body site
available_summaries = {
    'stool': ['age-baby', 'age-child', 'age-teen', 'age-20s', 'age-30s',
              'age-40s', 'age-50s', 'age-60s', 'age-70+',
              'bmi-Underweight', 'bmi-Normal', 'bmi-Overweight', 'bmi-Obese',
              'sex-male', 'sex-female'],
    'skin': ['age-baby', 'age-child', 'age-teen', 'age-20s', 'age-30s',
             'age-40s', 'age-50s', 'age-60s', 'age-70+',
             'sex-male', 'sex-female'],
    'oral': ['age-child', 'age-teen', 'age-20s', 'age-30s',
             'age-40s', 'age-50s', 'age-60s', 'age-70+',
             'sex-male', 'sex-female']
    }
