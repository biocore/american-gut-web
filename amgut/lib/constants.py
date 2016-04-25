from collections import defaultdict

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

collapse_human_sites = defaultdict(lambda: '', {
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
    'Vaginal mucus': ''
    })

# What categories of summary data are available for each collapsed body site
available_summaries = {
    'stool': ['age-baby', 'age-child', 'age-teen', 'age-20s', 'age-30s',
              'age-40s', 'age-50s', 'age-60s', 'age-70+',
              'bmi-Underweight', 'bmi-Normal', 'bmi-Overweight', 'bmi-Obese',
              'sex-male', 'sex-female', 'diet-Omnivore',
              'diet-Omnivore but do not eat red meat',
              'diet-Vegetarian but eat seafood', 'diet-Vegetarian',
              'diet-Vegan'],
    'skin': ['age-baby', 'age-child', 'age-teen', 'age-20s', 'age-30s',
             'age-40s', 'age-50s', 'age-60s', 'age-70+',
             'sex-male', 'sex-female', 'cosmetics-Daily',
             'cosmetics-Regularly', 'cosmetics-Occasionally',
             'cosmetics-Rarely', 'cosmetics-Never'],
    'oral': ['age-child', 'age-teen', 'age-20s', 'age-30s',
             'age-40s', 'age-50s', 'age-60s', 'age-70+',
             'sex-male', 'sex-female', 'diet-Omnivore',
             'diet-Omnivore but do not eat red meat',
             'diet-Vegetarian but eat seafood', 'diet-Vegetarian',
             'diet-Vegan', 'flossing-Daily', 'flossing-Regularly',
             'flossing-Occasionally', 'flossing-Rarely', 'flossing-Never']
    }
