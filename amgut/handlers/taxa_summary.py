from os.path import join
from re import sub

from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler
from amgut.lib.format import tab_delim_lines_to_table
from amgut.lib.config_manager import AMGUT_CONFIG


class TaxaSummary(BaseHandler):
    def get(self):
        barcode = self.get_argument('barcode', None)

        # nothing else to do
        if barcode is None:
            self.render("taxa_summary.html",
                        loginerror="ERROR: No barcode was requested")
            return

        taxa_summary_fp = join(AMGUT_CONFIG.base_data_dir, barcode+'.txt')

        # read lines from taxa summary table, omit comment lines
        lines = [x.replace(';', '\t').strip() for x in
            open(taxa_summary_fp, 'U').readlines() if not x.startswith('#')]

        # remove the greengenes prefixes. If hierarchy is delimitd by
        # semicolon- space, the GG prefix may be preceded by a space
        lines = [sub(' *?[kpcofg]__', '', x) for x in lines]

        # we must operate on the genus and percent abundance columns
        # individually, so it must be split into individual cells
        lines = [x.split('\t') for x in lines]

        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] == '':
                    lines[i][j] = '---'

            # format the last column to be a 2.2 number, and center it
            relative_abundance = float(lines[i][-1])
            relative_abundance *= 100
            lines[i][-1] = '%2.2f' % relative_abundance

        # generate headers
        headers = ['Kingdom', 'Phylum', 'Class', 'Order', 'Family',
            'Genus', 'Relative Abundance (%)']

        self.render("taxa_summary.html", headers=headers, data=lines,
                    loginerror="")

