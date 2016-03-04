from os.path import join
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
                    md_headers=pcoa_data[3].strip(),
                    metadata=pcoa_data[4].strip())
