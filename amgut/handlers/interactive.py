from os.path import join
from ast import literal_eval
from collections import defaultdict
from json import dumps

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


def _build_taxa(taxa_list):
    datasets = []
    for otu, value in taxa_list.items():
        taxonomy = otu.split(';')
        # Find the highest classified level by looping backwards through
        # the list and breaking once we find the first classified level
        highest = ''
        for tax in reversed(taxonomy):
            if not tax.endswith('__'):
                highest = 'Unclassified (%s)' % tax.replace('__', '. ')
                break
        datasets.append({
            'full': otu,
            'phylum': taxonomy[1].split("__")[1],
            'class': taxonomy[2].split("__")[1] if not
            taxonomy[2].endswith('__') else highest,
            'order': taxonomy[3].split("__")[1] if not
            taxonomy[3].endswith('__') else highest,
            'family': taxonomy[4].split("__")[1] if not
            taxonomy[4].endswith('__') else highest,
            'genus': taxonomy[5].split("__")[1] if not
            taxonomy[5].endswith('__') else highest,
            'data': value
        })
    return datasets


class TaxaHandler(BaseHandler):
    @authenticated
    def get(self):
        user = ag_data.get_user_for_kit(self.current_user)
        barcodes = ag_data.get_barcodes_by_user(user, results=True)
        otus = {}
        files = []
        # Load in all possible OTUs that can be seen by loading files to memory
        # Files are small (5kb) so this should be fine.
        for barcode in barcodes:
            with open(join(AMGUT_CONFIG.base_data_dir, 'taxa-summaries',
                      '%s.txt' % barcode)) as f:
                f.readline()
                files.append(f.readlines())
            for line in files[-1]:
                otus[line.split('\t')[0]] = []

        # Read in counts
        for barcode, file in zip(barcodes, files):
            seen_otus = set()
            for line in file:
                otu, percent = line.strip().split('\t', 1)
                otus[otu].append(float(percent) * 100)
                seen_otus.add(otu)
            # make the samples without the OTU all zero count
            unseen = set(otus.keys()) - seen_otus
            for otu in unseen:
                otus[otu].append(0.0)

        datasets = _build_taxa(otus)

        meta_cats = ['age-baby', 'age-child', 'age-teen', 'age-20s', 'age-30s',
                     'age-40s', 'age-50s', 'age-60s', 'age-70+']
        self.render('bar_stacked.html', barcodes=barcodes, meta_cats=meta_cats,
                    datasets=datasets)


class MetadataHandler(BaseHandler):
    @authenticated
    def get(self):
        site = self.get_argument('site')
        cat = self.get_argument('category')
        otus = defaultdict(list)

        with open(join(AMGUT_CONFIG.base_data_dir, 'taxa-summaries',
                  'ag-%s-%s.txt' % (site, cat)), 'rU') as f:
            # Read in counts
            for line in f:
                otu, percent = line.strip().split('\t', 1)
                otus[otu] = float(percent) * 100
        self.write(dumps(_build_taxa(otus)))
        self.set_header("Content-Type", "application/json")
