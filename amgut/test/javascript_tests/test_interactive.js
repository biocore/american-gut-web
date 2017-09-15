
$(document).ready(function() {

  module("Interactivity Functionality", {

    setup: function(){
      rawData = [{'full': 'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Lachnospiraceae;g__', 'family': 'Lachnospiraceae', 'order': 'Clostridiales', 'phylum': 'Firmicutes', 'genus': 'Unclassified (f. Lachnospiraceae)', 'data': [9.084], 'class': 'Clostridia'}, {'full': 'k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enterobacteriales;f__Enterobacteriaceae;g__', 'family': 'Enterobacteriaceae', 'order': 'Enterobacteriales', 'phylum': 'Proteobacteria', 'genus': 'Unclassified (f. Enterobacteriaceae)', 'data': [0.0073999999999999995], 'class': 'Gammaproteobacteria'}, {'full': 'k__Bacteria;p__Firmicutes;c__Erysipelotrichi;o__Erysipelotrichales;f__Erysipelotrichaceae;g__Bulleidia', 'family': 'Erysipelotrichaceae', 'order': 'Erysipelotrichales', 'phylum': 'Firmicutes', 'genus': 'Bulleidia', 'data': [0.0073999999999999995], 'class': 'Erysipelotrichi'}, {'full': 'k__Bacteria;p__Actinobacteria;c__Actinobacteria;o__Actinomycetales;f__Corynebacteriaceae;g__Corynebacterium', 'family': 'Corynebacteriaceae', 'order': 'Actinomycetales', 'phylum': 'Actinobacteria', 'genus': 'Corynebacterium', 'data': [0.0271], 'class': 'Actinobacteria'}, {'full': 'k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Pasteurellales;f__Pasteurellaceae;g__Haemophilus', 'family': 'Pasteurellaceae', 'order': 'Pasteurellales', 'phylum': 'Proteobacteria', 'genus': 'Haemophilus', 'data': [0.0222], 'class': 'Gammaproteobacteria'}, {'full': 'k__Bacteria;p__Actinobacteria;c__Coriobacteriia;o__Coriobacteriales;f__Coriobacteriaceae;g__Eggerthella', 'family': 'Coriobacteriaceae', 'order': 'Coriobacteriales', 'phylum': 'Actinobacteria', 'genus': 'Eggerthella', 'data': [0.0173], 'class': 'Coriobacteriia'}, {'full': 'k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enterobacteriales;f__Enterobacteriaceae;g__Proteus', 'family': 'Enterobacteriaceae', 'order': 'Enterobacteriales', 'phylum': 'Proteobacteria', 'genus': 'Proteus', 'data': [0.0444], 'class': 'Gammaproteobacteria'}, {'full': 'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Porphyromonadaceae;g__Parabacteroides', 'family': 'Porphyromonadaceae', 'order': 'Bacteroidales', 'phylum': 'Bacteroidetes', 'genus': 'Parabacteroides', 'data': [0.009899999999999999], 'class': 'Bacteroidia'}, {'full': 'k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Thiohalorhabdales;f__;g__', 'family': 'Unclassified (o. Thiohalorhabdales)', 'order': 'Thiohalorhabdales', 'phylum': 'Proteobacteria', 'genus': 'Unclassified (o. Thiohalorhabdales)', 'data': [0.0073999999999999995], 'class': 'Gammaproteobacteria'}, {'full': 'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Clostridiaceae;g__Clostridium', 'family': 'Clostridiaceae', 'order': 'Clostridiales', 'phylum': 'Firmicutes', 'genus': 'Clostridium', 'data': [0.0395], 'class': 'Clostridia'}, {'full': 'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Bacteroidaceae;g__Bacteroides', 'family': 'Bacteroidaceae', 'order': 'Bacteroidales', 'phylum': 'Bacteroidetes', 'genus': 'Bacteroides', 'data': [56.4695], 'class': 'Bacteroidia'}, {'full': 'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Prevotellaceae;g__Prevotella', 'family': 'Prevotellaceae', 'order': 'Bacteroidales', 'phylum': 'Bacteroidetes', 'genus': 'Prevotella', 'data': [0.39709999999999995], 'class': 'Bacteroidia'}, {'full': 'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__[Paraprevotellaceae];g__Paraprevotella', 'family': 'Paraprevotellaceae (Contested)', 'order': 'Bacteroidales', 'phylum': 'Bacteroidetes', 'genus': 'Paraprevotella', 'data': [0.0025], 'class': 'Bacteroidia'}];
      colData = [{'full': 'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Lachnospiraceae;g__', 'family': 'Lachnospiraceae', 'order': 'Clostridiales', 'phylum': 'Firmicutes', 'genus': 'Unclassified (f. Lachnospiraceae)', 'data': [.09084], 'class': 'Clostridia'}, {'full': 'k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enterobacteriales;f__Enterobacteriaceae;g__', 'family': 'Enterobacteriaceae', 'order': 'Enterobacteriales', 'phylum': 'Proteobacteria', 'genus': 'Unclassified (f. Enterobacteriaceae)', 'data': [0.0995], 'class': 'Gammaproteobacteria'}, {'full': 'k__Bacteria;p__Firmicutes;c__Erysipelotrichi;o__Erysipelotrichales;f__Erysipelotrichaceae;g__Bulleidia', 'family': 'Erysipelotrichaceae', 'order': 'Erysipelotrichales', 'phylum': 'Firmicutes', 'genus': 'Bulleidia', 'data': [0.073999999999999995], 'class': 'Erysipelotrichi'}, {'full': 'k__Bacteria;p__Actinobacteria;c__Actinobacteria;o__Actinomycetales;f__Corynebacteriaceae;g__Corynebacterium', 'family': 'Corynebacteriaceae', 'order': 'Actinomycetales', 'phylum': 'Actinobacteria', 'genus': 'Corynebacterium', 'data': [0.0217], 'class': 'Actinobacteria'}, {'full': 'k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Pasteurellales;f__Pasteurellaceae;g__Haemophilus', 'family': 'Pasteurellaceae', 'order': 'Pasteurellales', 'phylum': 'Proteobacteria', 'genus': 'Haemophilus', 'data': [0.1111], 'class': 'Gammaproteobacteria'}, {'full': 'k__Bacteria;p__Actinobacteria;c__Coriobacteriia;o__Coriobacteriales;f__Coriobacteriaceae;g__Eggerthella', 'family': 'Coriobacteriaceae', 'order': 'Coriobacteriales', 'phylum': 'Actinobacteria', 'genus': 'Eggerthella', 'data': [0.0242], 'class': 'Coriobacteriia'}, {'full': 'k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enterobacteriales;f__Enterobacteriaceae;g__Proteus', 'family': 'Enterobacteriaceae', 'order': 'Enterobacteriales', 'phylum': 'Proteobacteria', 'genus': 'Proteus', 'data': [0.2444], 'class': 'Gammaproteobacteria'}, {'full': 'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Porphyromonadaceae;g__Parabacteroides', 'family': 'Porphyromonadaceae', 'order': 'Bacteroidales', 'phylum': 'Bacteroidetes', 'genus': 'Parabacteroides', 'data': [0.2900999999999], 'class': 'Bacteroidia'}, {'full': 'k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Thiohalorhabdales;f__;g__', 'family': 'Unclassified (o. Thiohalorhabdales)', 'order': 'Thiohalorhabdales', 'phylum': 'Proteobacteria', 'genus': 'Unclassified (o. Thiohalorhabdales)', 'data': [0.00199999999999995], 'class': 'Gammaproteobacteria'}, {'full': 'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Clostridiaceae;g__Clostridium', 'family': 'Clostridiaceae', 'order': 'Clostridiales', 'phylum': 'Firmicutes', 'genus': 'Clostridium', 'data': [0.0395], 'class': 'Clostridia'}, {'full': 'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Bacteroidaceae;g__Bacteroides', 'family': 'Bacteroidaceae', 'order': 'Bacteroidales', 'phylum': 'Bacteroidetes', 'genus': 'Bacteroides', 'data': [55.4695], 'class': 'Bacteroidia'}, {'full': 'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Prevotellaceae;g__newthing', 'family': 'Prevotellaceae', 'order': 'Bacteroidales', 'phylum': 'Bacteroidetes', 'genus': 'newthing', 'data': [0.14709999999999995], 'class': 'Bacteroidia'}];
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
      };
      translate_summaries = {
        'age-baby': 'age-baby', 'age-child': 'age-child',
        'age-teen': 'age-teen', 'age-20s': 'age-20s', 'age-30s': 'age-30s',
        'age-40s': 'age-40s', 'age-50s': 'age-50s', 'age-60s': 'age-60s',
        'age-70+': 'age-70+', 'bmi-Underweight': 'bmi-Underweight',
        'bmi-Normal': 'bmi-Normal', 'bmi-Overweight': 'bmi-Overweight',
        'bmi-Obese': 'bmi-Obese', 'sex-male': 'sex-male',
        'sex-female': 'sex-female', 'diet-Omnivore': 'diet-Omnivore',
        'diet-Omnivore but do not eat red meat':
            'diet-Omnivore but do not eat red meat',
        'diet-Vegetarian but eat seafood': 'diet-Vegetarian but eat seafood',
        'diet-Vegetarian': 'diet-Vegetarian', 'diet-Vegan': 'diet-Vegan',
        'cosmetics-Daily': 'cosmetics-Daily',
        'cosmetics-Regularly': 'cosmetics-Regularly',
        'cosmetics-Occasionally': 'cosmetics-Occasionally',
        'cosmetics-Rarely': 'cosmetics-Rarely',
        'cosmetics-Never': 'cosmetics-Never',
        'flossing-Regularly': 'flossing-Regularly',
        'flossing-Occasionally': 'flossing-Occasionally',
        'flossing-Rarely': 'flossing-Rarely', 'flossing-Never': 'flossing-Never'
      };
    },

    teardown: function() {
        rawData = null;
        colData = null;
        available_summaries = null;
        translate_summaries = null;


    }

  });

  test("Test grouping OTUs phylum level", function() {
    var obs = group(rawData, 'phylum');
    var exp = {
"Actinobacteria": [
  {
    "class": "Actinobacteria",
    "data": [
      0.0271
    ],
    "family": "Corynebacteriaceae",
    "full": "k__Bacteria;p__Actinobacteria;c__Actinobacteria;o__Actinomycetales;f__Corynebacteriaceae;g__Corynebacterium",
    "genus": "Corynebacterium",
    "order": "Actinomycetales",
    "phylum": "Actinobacteria"
  },
  {
    "class": "Coriobacteriia",
    "data": [
      0.0173
    ],
    "family": "Coriobacteriaceae",
    "full": "k__Bacteria;p__Actinobacteria;c__Coriobacteriia;o__Coriobacteriales;f__Coriobacteriaceae;g__Eggerthella",
    "genus": "Eggerthella",
    "order": "Coriobacteriales",
    "phylum": "Actinobacteria"
  }
],
"Bacteroidetes": [
  {
    "class": "Bacteroidia",
    "data": [
      0.009899999999999999
    ],
    "family": "Porphyromonadaceae",
    "full": "k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Porphyromonadaceae;g__Parabacteroides",
    "genus": "Parabacteroides",
    "order": "Bacteroidales",
    "phylum": "Bacteroidetes"
  },
  {
    "class": "Bacteroidia",
    "data": [
      56.4695
    ],
    "family": "Bacteroidaceae",
    "full": "k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Bacteroidaceae;g__Bacteroides",
    "genus": "Bacteroides",
    "order": "Bacteroidales",
    "phylum": "Bacteroidetes"
  },
  {
    "class": "Bacteroidia",
    "data": [
      0.39709999999999995
    ],
    "family": "Prevotellaceae",
    "full": "k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Prevotellaceae;g__Prevotella",
    "genus": "Prevotella",
    "order": "Bacteroidales",
    "phylum": "Bacteroidetes"
  },
  {
    "class": "Bacteroidia",
    "data": [
      0.0025
    ],
    "family": "Paraprevotellaceae (Contested)",
    "full": "k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__[Paraprevotellaceae];g__Paraprevotella",
    "genus": "Paraprevotella",
    "order": "Bacteroidales",
    "phylum": "Bacteroidetes"
  }
],
"Firmicutes": [
  {
    "class": "Clostridia",
    "data": [
      9.084
    ],
    "family": "Lachnospiraceae",
    "full": "k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Lachnospiraceae;g__",
    "genus": "Unclassified (f. Lachnospiraceae)",
    "order": "Clostridiales",
    "phylum": "Firmicutes"
  },
  {
    "class": "Erysipelotrichi",
    "data": [
      0.0073999999999999995
    ],
    "family": "Erysipelotrichaceae",
    "full": "k__Bacteria;p__Firmicutes;c__Erysipelotrichi;o__Erysipelotrichales;f__Erysipelotrichaceae;g__Bulleidia",
    "genus": "Bulleidia",
    "order": "Erysipelotrichales",
    "phylum": "Firmicutes"
  },
  {
    "class": "Clostridia",
    "data": [
      0.0395
    ],
    "family": "Clostridiaceae",
    "full": "k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Clostridiaceae;g__Clostridium",
    "genus": "Clostridium",
    "order": "Clostridiales",
    "phylum": "Firmicutes"
  }
],
"Proteobacteria": [
  {
    "class": "Gammaproteobacteria",
    "data": [
      0.0073999999999999995
    ],
    "family": "Enterobacteriaceae",
    "full": "k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enterobacteriales;f__Enterobacteriaceae;g__",
    "genus": "Unclassified (f. Enterobacteriaceae)",
    "order": "Enterobacteriales",
    "phylum": "Proteobacteria"
  },
  {
    "class": "Gammaproteobacteria",
    "data": [
      0.0222
    ],
    "family": "Pasteurellaceae",
    "full": "k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Pasteurellales;f__Pasteurellaceae;g__Haemophilus",
    "genus": "Haemophilus",
    "order": "Pasteurellales",
    "phylum": "Proteobacteria"
  },
  {
    "class": "Gammaproteobacteria",
    "data": [
      0.0444
    ],
    "family": "Enterobacteriaceae",
    "full": "k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enterobacteriales;f__Enterobacteriaceae;g__Proteus",
    "genus": "Proteus",
    "order": "Enterobacteriales",
    "phylum": "Proteobacteria"
  },
  {
    "class": "Gammaproteobacteria",
    "data": [
      0.0073999999999999995
    ],
    "family": "Unclassified (o. Thiohalorhabdales)",
    "full": "k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Thiohalorhabdales;f__;g__",
    "genus": "Unclassified (o. Thiohalorhabdales)",
    "order": "Thiohalorhabdales",
    "phylum": "Proteobacteria"
  }
]
};
    deepEqual(obs, exp);
  });

  test("Test grouping OTUs order level", function() {
    var obs = group(rawData, 'order');
    var exp = {
"Actinomycetales": [
  {
    "class": "Actinobacteria",
    "data": [
      0.0271
    ],
    "family": "Corynebacteriaceae",
    "full": "k__Bacteria;p__Actinobacteria;c__Actinobacteria;o__Actinomycetales;f__Corynebacteriaceae;g__Corynebacterium",
    "genus": "Corynebacterium",
    "order": "Actinomycetales",
    "phylum": "Actinobacteria"
  }
],
"Bacteroidales": [
  {
    "class": "Bacteroidia",
    "data": [
      0.009899999999999999
    ],
    "family": "Porphyromonadaceae",
    "full": "k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Porphyromonadaceae;g__Parabacteroides",
    "genus": "Parabacteroides",
    "order": "Bacteroidales",
    "phylum": "Bacteroidetes"
  },
  {
    "class": "Bacteroidia",
    "data": [
      56.4695
    ],
    "family": "Bacteroidaceae",
    "full": "k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Bacteroidaceae;g__Bacteroides",
    "genus": "Bacteroides",
    "order": "Bacteroidales",
    "phylum": "Bacteroidetes"
  },
  {
    "class": "Bacteroidia",
    "data": [
      0.39709999999999995
    ],
    "family": "Prevotellaceae",
    "full": "k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Prevotellaceae;g__Prevotella",
    "genus": "Prevotella",
    "order": "Bacteroidales",
    "phylum": "Bacteroidetes"
  },
  {
    "class": "Bacteroidia",
    "data": [
      0.0025
    ],
    "family": "Paraprevotellaceae (Contested)",
    "full": "k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__[Paraprevotellaceae];g__Paraprevotella",
    "genus": "Paraprevotella",
    "order": "Bacteroidales",
    "phylum": "Bacteroidetes"
  }
],
"Clostridiales": [
  {
    "class": "Clostridia",
    "data": [
      9.084
    ],
    "family": "Lachnospiraceae",
    "full": "k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Lachnospiraceae;g__",
    "genus": "Unclassified (f. Lachnospiraceae)",
    "order": "Clostridiales",
    "phylum": "Firmicutes"
  },
  {
    "class": "Clostridia",
    "data": [
      0.0395
    ],
    "family": "Clostridiaceae",
    "full": "k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Clostridiaceae;g__Clostridium",
    "genus": "Clostridium",
    "order": "Clostridiales",
    "phylum": "Firmicutes"
  }
],
"Coriobacteriales": [
  {
    "class": "Coriobacteriia",
    "data": [
      0.0173
    ],
    "family": "Coriobacteriaceae",
    "full": "k__Bacteria;p__Actinobacteria;c__Coriobacteriia;o__Coriobacteriales;f__Coriobacteriaceae;g__Eggerthella",
    "genus": "Eggerthella",
    "order": "Coriobacteriales",
    "phylum": "Actinobacteria"
  }
],
"Enterobacteriales": [
  {
    "class": "Gammaproteobacteria",
    "data": [
      0.0073999999999999995
    ],
    "family": "Enterobacteriaceae",
    "full": "k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enterobacteriales;f__Enterobacteriaceae;g__",
    "genus": "Unclassified (f. Enterobacteriaceae)",
    "order": "Enterobacteriales",
    "phylum": "Proteobacteria"
  },
  {
    "class": "Gammaproteobacteria",
    "data": [
      0.0444
    ],
    "family": "Enterobacteriaceae",
    "full": "k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enterobacteriales;f__Enterobacteriaceae;g__Proteus",
    "genus": "Proteus",
    "order": "Enterobacteriales",
    "phylum": "Proteobacteria"
  }
],
"Erysipelotrichales": [
  {
    "class": "Erysipelotrichi",
    "data": [
      0.0073999999999999995
    ],
    "family": "Erysipelotrichaceae",
    "full": "k__Bacteria;p__Firmicutes;c__Erysipelotrichi;o__Erysipelotrichales;f__Erysipelotrichaceae;g__Bulleidia",
    "genus": "Bulleidia",
    "order": "Erysipelotrichales",
    "phylum": "Firmicutes"
  }
],
"Pasteurellales": [
  {
    "class": "Gammaproteobacteria",
    "data": [
      0.0222
    ],
    "family": "Pasteurellaceae",
    "full": "k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Pasteurellales;f__Pasteurellaceae;g__Haemophilus",
    "genus": "Haemophilus",
    "order": "Pasteurellales",
    "phylum": "Proteobacteria"
  }
],
"Thiohalorhabdales": [
  {
    "class": "Gammaproteobacteria",
    "data": [
      0.0073999999999999995
    ],
    "family": "Unclassified (o. Thiohalorhabdales)",
    "full": "k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Thiohalorhabdales;f__;g__",
    "genus": "Unclassified (o. Thiohalorhabdales)",
    "order": "Thiohalorhabdales",
    "phylum": "Proteobacteria"
  }]};
    deepEqual(obs, exp);
  });

  test("Test average", function() {
    var obs = getAvg([1,2,3,4,5,6,7,8,9,10]);
    equal(obs, 5.5);

    obs = getAvg([27, 5, 2.22476, -2.2, 47]);
    equal(obs, 15.804952);
  });

  test("Test sumArrays", function() {
    var obs = sumArrays([1,2,3,4,5,6,7,8,9,10], [10,9,8,7,6,5,4,3,2,1]);
    deepEqual(obs, [11,11,11,11,11,11,11,11,11,11]);

    obs = sumArrays([0.002, 0.0004, 0.02], [0.5, 0.8, 0.7]);
    deepEqual(obs, [0.502, 0.8004, 0.72]);
  });

  test("Test sumArrays unequal length", function() {
    throws(
        function() {
          var obs = sumArrays([1,2,3,4,5,6], [10,9,8,7,6,5,4,3,2,1]);
        },
        "Arrays unequal length: 6 10",
        "Error if arrays are not equal length"
        );
  });

  test("Test findOTU", function() {
    var obs = findOTU(rawData, "k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Thiohalorhabdales;f__;g__", "full");
    equal(obs, 8);

    obs = findOTU(rawData, "Thiohalorhabdales", "order");
    equal(obs, 8);

  //Search for an OTU that is not present
    obs = findOTU(rawData, "jvrieopwbrwjojvewbhwirobuihw0", "full");
    equal(obs, -1);
  });

  test("Test buildCats", function() {
    var select = $('<select>');

    // test building for skin
    var exp = ["","age-baby","age-child","age-teen","age-20s","age-30s",
               "age-40s","age-50s","age-60s","age-70+","sex-male","sex-female"];
    buildCats('skin', select);
    var values = [];
    select.find('option').each(function() {
        values.push($(this).attr('value'));
    });
    deepEqual(values, exp);

    //test no disabling
    var exp = [];
    buildCats('', select);
    var values = [];
    select.find('option').each(function() {
        values.push($(this).attr('value'));
    });
    deepEqual(values, exp);
    deepEqual(select.prop('disabled'), false)

    //test disabling
    var exp = [];
    buildCats('', select, true);
    var values = [];
    select.find('option').each(function() {
        values.push($(this).attr('value'));
    });
    deepEqual(values, exp);
    deepEqual(select.prop('disabled'), true)
  });

  test("Test collapse", function() {
    var obs = collapse(rawData, 'phylum');
    var exp = [{
    "backgroundColor": "rgb(203,106,97)",
    "data": [
      9.1309
    ],
    "label": "Firmicutes",
    "phylum": "Firmicutes"
  },
  {
    "backgroundColor": "rgb(225,152,69)",
    "data": [
      56.879
    ],
    "label": "Bacteroidetes",
    "phylum": "Bacteroidetes"
  },
  {
    "backgroundColor": "rgb(255,255,141)",
    "data": [
      0.0814
    ],
    "label": "Proteobacteria",
    "phylum": "Proteobacteria"
  },
  {
    "backgroundColor": "rgb(178,152,104)",
    "data": [
      0.0444
    ],
    "label": "Actinobacteria",
    "phylum": "Actinobacteria"
  }];
    deepEqual(obs, exp);

    obs = collapse(rawData, 'genus');
    exp = [{
    "backgroundColor": "rgb(139,0,0)",
    "data": [
      9.084
    ],
    "label": "Unclassified (f. Lachnospiraceae)",
    "phylum": "Firmicutes"
  },
  {
    "backgroundColor": "rgb(197,96,101)",
    "data": [
      0.0395
    ],
    "label": "Clostridium",
    "phylum": "Firmicutes"
  },
  {
    "backgroundColor": "rgb(255,192,203)",
    "data": [
      0.0074
    ],
    "label": "Bulleidia",
    "phylum": "Firmicutes"
  },
  {
    "backgroundColor": "rgb(190,94,0)",
    "data": [
      56.4695
    ],
    "label": "Bacteroides",
    "phylum": "Bacteroidetes"
  },
  {
    "backgroundColor": "rgb(211,132,42)",
    "data": [
      0.3971
    ],
    "label": "Prevotella",
    "phylum": "Bacteroidetes"
  },
  {
    "backgroundColor": "rgb(233,171,84)",
    "data": [
      0.0099
    ],
    "label": "Parabacteroides",
    "phylum": "Bacteroidetes"
  },
  {
    "backgroundColor": "rgb(255,210,127)",
    "data": [
      0.0025
    ],
    "label": "Paraprevotella",
    "phylum": "Bacteroidetes"
  },
  {
    "backgroundColor": "rgb(255,255,0)",
    "data": [
      0.0444
    ],
    "label": "Proteus",
    "phylum": "Proteobacteria"
  },
  {
    "backgroundColor": "rgb(255,255,74)",
    "data": [
      0.0222
    ],
    "label": "Haemophilus",
    "phylum": "Proteobacteria"
  },
  {
    "backgroundColor": "rgb(255,255,149)",
    "data": [
      0.0074
    ],
    "label": "Unclassified (f. Enterobacteriaceae)",
    "phylum": "Proteobacteria"
  },
  {
    "backgroundColor": "rgb(255,255,224)",
    "data": [
      0.0074
    ],
    "label": "Unclassified (o. Thiohalorhabdales)",
    "phylum": "Proteobacteria"
  },
  {
    "backgroundColor": "rgb(115,91,43)",
    "data": [
      0.0271
    ],
    "label": "Corynebacterium",
    "phylum": "Actinobacteria"
  },
  {
    "backgroundColor": "rgb(243,219,171)",
    "data": [
      0.0173
    ],
    "label": "Eggerthella",
    "phylum": "Actinobacteria"
  }];
    deepEqual(obs, exp);
  });


  test("Test calcFoldChange", function(){
    var obs = calcFoldChange(colData, rawData, 'phylum', 0);
    var exp = [["Firmicutes","Bacteroidetes","Actinobacteria","Proteobacteria"],
               [5.48,0.02,-0.05,-2.49]];
    deepEqual(obs[0], exp[0]);
    deepEqual(obs[1], exp[1]);

    obs = calcFoldChange(colData, rawData, 'genus', 0);
    exp = [ ["Unclassified (f. Lachnospiraceae)","Unclassified (o. Thiohalorhabdales)","Corynebacterium","Bacteroides","Clostridium","Eggerthella","Haemophilus","Proteus","Bulleidia","Unclassified (f. Enterobacteriaceae)","Parabacteroides"],
            [6.64,1.88,0.32,0.02,0,-0.49,-2.33,-2.47,-3.33,-3.75,-4.88]];
    deepEqual(obs[0], exp[0]);
    deepEqual(obs[1], exp[1]);
  });

  test("Test addMetadata", function(){
    testData = JSON.parse(JSON.stringify(rawData));
    var obs = addMetadata(testData, colData, 'genus');
    var exp = [{
    "backgroundColor": "rgb(139,0,0)",
    "data": [
      9.084,
      0.0908
    ],
    "label": "Unclassified (f. Lachnospiraceae)",
    "phylum": "Firmicutes"
  },
  {
    "backgroundColor": "rgb(197,96,101)",
    "data": [
      0.0074,
      0.074
    ],
    "label": "Bulleidia",
    "phylum": "Firmicutes"
  },
  {
    "backgroundColor": "rgb(255,192,203)",
    "data": [
      0.0395,
      0.0395
    ],
    "label": "Clostridium",
    "phylum": "Firmicutes"
  },
  {
    "backgroundColor": "rgb(190,94,0)",
    "data": [
      56.4695,
      55.4695
    ],
    "label": "Bacteroides",
    "phylum": "Bacteroidetes"
  },
  {
    "backgroundColor": "rgb(211,132,42)",
    "data": [
      0.3971,
      0
    ],
    "label": "Prevotella",
    "phylum": "Bacteroidetes"
  },
  {
    "backgroundColor": "rgb(233,171,84)",
    "data": [
      0.0099,
      0.2901
    ],
    "label": "Parabacteroides",
    "phylum": "Bacteroidetes"
  },
  {
    "backgroundColor": "rgb(255,210,127)",
    "data": [
      0,
      0.1471
    ],
    "label": "newthing",
    "phylum": "Bacteroidetes"
  },
  {
    "backgroundColor": "rgb(255,255,0)",
    "data": [
      0.0444,
      0.2444
    ],
    "label": "Proteus",
    "phylum": "Proteobacteria"
  },
  {
    "backgroundColor": "rgb(255,255,112)",
    "data": [
      0.0222,
      0.1111
    ],
    "label": "Haemophilus",
    "phylum": "Proteobacteria"
  },
  {
    "backgroundColor": "rgb(255,255,224)",
    "data": [
      0.0074,
      0.0995
    ],
    "label": "Unclassified (f. Enterobacteriaceae)",
    "phylum": "Proteobacteria"
  },
  {
    "backgroundColor": "rgba(180,180,180)",
    "data": [
      0.0542,
      0.0478
    ],
    "label": "Other"
  }];
    deepEqual(obs, exp);
  });
});
