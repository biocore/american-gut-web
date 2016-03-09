from os.path import join
from ast import literal_eval
from collections import defaultdict
from random import randint

from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler
from amgut.connections import ag_data
from amgut.lib.config_manager import AMGUT_CONFIG


class EmperorHandler(BaseHandler):
    @authenticated
    def get(self):
        user = ag_data.get_user_for_kit(self.current_user)
        barcodes = ag_data.get_barcodes_by_user(user, results=True)
        with open(join(AMGUT_CONFIG.base_data_dir, 'emperor',
                  'emperor.txt')) as f:
            pcoa_data = f.readlines()
        self.render("emperor.html", barcodes=barcodes,
                    coords_ids=pcoa_data[0].strip(),
                    coords=pcoa_data[1].strip(),
                    pct_var=pcoa_data[2].strip(),
                    md_headers=literal_eval(pcoa_data[3].strip()),
                    metadata=pcoa_data[4].strip())


class TaxaHandler(BaseHandler):
    @authenticated
    def get(self):
        user = ag_data.get_user_for_kit(self.current_user)
        barcodes = ag_data.get_barcodes_by_user(user, results=True)
        datasets = []
        otus = defaultdict(list)
        for barcode in barcodes:
            with open(join(AMGUT_CONFIG.base_data_dir, 'taxa_tables',
                      '%s.txt' % barcode)) as f:
                seen_otus = set()
                f.readline()
                for line in f:
                    otu, percent = line.strip().split('\t', 1)
                    otus[otu].append(float(percent) * 100)
                    seen_otus.add(otu)
                for otu in set(otus.keys()) - seen_otus:
                    otus[otu].append(0.0)
        for otu, value in otus.items():
            datasets.append({
                'label': otu,
                'backgroundColor': "rgba(%d,%d,%d,0.5)" % (randint(0, 255),
                                                           randint(0, 255),
                                                           randint(0, 255)),
                'data': value
            })
        self.render('bar_stacked.html', barcodes=barcodes, datasets=datasets)
