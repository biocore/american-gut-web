from os.path import join
from json import dumps
from StringIO import StringIO

from tornado.web import authenticated, HTTPError
from PIL import Image

from amgut.handlers.base_handlers import BaseHandler
from amgut.connections import ag_data
from amgut.lib.constants import available_summaries, collapse_human_sites
from amgut.lib.config_manager import AMGUT_CONFIG


def _build_taxa(taxa_list):
    def clean(taxa):
        cleaned = taxa.split("__")[1]
        if "[" in cleaned:
            cleaned = "%s (Contested)" % cleaned.translate(None, '[]')
        return cleaned

    datasets = []
    taxa_levels = ['phylum', 'class', 'order', 'family', 'genus']
    for otu, value in taxa_list.items():
        taxonomy = [x.strip() for x in otu.split(';')]
        # Find the highest classified level by looping backwards through
        # the list and breaking once we find the first classified level
        highest = ''
        for tax in reversed(taxonomy):
            if not tax.endswith('__'):
                highest = 'Unclassified (%s)' % tax.replace('__', '. ')
                break

        info = {level: clean(val) if not val.endswith('__') else highest
                for level, val in zip(taxa_levels, taxonomy[1:])}
        info['full'] = otu
        info['data'] = value
        datasets.append(info)
    return datasets


def _read_taxonomy(barcodes):
    otus = {}
    files = []
    # Load in all possible OTUs that can be seen by loading files to memory
    # Files are small (5kb) so this should be fine.
    for barcode in barcodes:
        with open(join(AMGUT_CONFIG.base_data_dir, 'taxa-summaries',
                  '%s.txt' % barcode['barcode'])) as f:
            f.readline()
            files.append(f.readlines())
        for line in files[-1]:
            otus[line.split('\t')[0]] = []

    # Read in counts
    full_otus = set(otus.keys())
    for file in files:
        seen_otus = set()
        for line in file:
            otu, percent = line.strip().split('\t', 1)
            otus[otu].append(float(percent) * 100)
            seen_otus.add(otu)
        # make the samples without the OTU all zero count
        unseen = full_otus - seen_otus
        for otu in unseen:
            otus[otu].append(0.0)

    return _build_taxa(otus)


class MultiSampleHandler(BaseHandler):
    @authenticated
    def get(self):
        user = ag_data.get_user_for_kit(self.current_user)
        bc_info = ag_data.get_barcodes_by_user(user, results=True)
        titles = [bc['sample_date'].strftime('%b %d, %Y') for bc in bc_info]
        datasets = _read_taxonomy(bc_info)

        self.render('taxa.html', titles=titles, barcodes=bc_info,
                    available_summaries=available_summaries,
                    collapse=collapse_human_sites, datasets=datasets)


class MetadataHandler(BaseHandler):
    @authenticated
    def get(self):
        user = ag_data.get_user_for_kit(self.current_user)
        barcode = self.get_argument('barcode', False)
        if barcode:
            barcodes = [b['barcode'] for b in
                        ag_data.get_barcodes_by_user(user, results=True)]
            # Make sure barcode passed is owned by the user
            if barcode not in barcodes:
                raise HTTPError(403, 'User %s does not have access to barcode '
                                '%s' % (self.current_user, barcode))
            site = ag_data.getAGBarcodeDetails(barcode)['site_sampled'].upper()
        else:
            site = self.get_argument('site')
        cat = self.get_argument('category').replace(' ', '_')
        if cat == '':
            file = join(AMGUT_CONFIG.base_data_dir, 'taxa-summaries',
                        'ag-%s-average.txt' % site)
        else:
            file = join(AMGUT_CONFIG.base_data_dir, 'taxa-summaries',
                        'ag-%s-%s.txt' % (site, cat))

        otus = {}
        with open(file, 'rU') as f:
            # Read in counts
            for line in f:
                otu, percent = line.strip().split('\t', 1)
                otus[otu] = [float(percent) * 100]
        self.write(dumps(_build_taxa(otus)))
        self.set_header("Content-Type", "application/json")


class AlphaDivImgHandler(BaseHandler):
    @authenticated
    def get(self, barcode):
        user = ag_data.get_user_for_kit(self.current_user)
        barcodes = [b['barcode'] for b in
                    ag_data.get_barcodes_by_user(user)]
        # Make sure barcode passed is owned by the user
        if barcode not in barcodes:
            raise HTTPError(403, 'User %s does not have access to barcode '
                            '%s' % (self.current_user, barcode))
        # These variables are introduced but not used
        # site = ag_data.getAGBarcodeDetails(barcode)['site_sampled'].lower()
        # cat = self.get_argument('category', False)

        # Build alpha div image by layering the sample and, optionally,
        # category lines onto the base alpha diversity distribution image
        new_image = Image.open(join(AMGUT_CONFIG.base_data_dir, 'alpha-div',
                               '%s.png' % barcode))
        # Deactivated until pipeline can support category overlay
        # if cat:
        #    cat = Image.open(join(AMGUT_CONFIG.base_data_dir, 'alpha-div',
        #                     'pd_%s-%s.png' % (site, cat)))
        #    new_image = Image.alpha_composite(cat, new_image)
        full_image = StringIO()
        new_image.save(full_image, format="png")
        self.write(full_image.getvalue())
        self.set_header("Content-type",  "image/png")
