import odoo.tests


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):

    def test_01_pos_is_loaded(self):
        env = self.env

        # From https://github.com/odoo/odoo/blob/12.0/addons/point_of_sale/tests/test_frontend.py#L292-L297
        #
        # needed because tests are run before the module is marked as
        # installed. In js web will only load qweb coming from modules
        # that are returned by the backend in module_boot. Without
        # this you end up with js, css but no qweb.
        env['ir.module.module'].search([('name', '=', 'pos_logout')], limit=1).state = 'installed'

        self.phantom_js(
            '/web',

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('pos_logout_tour')",

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.pos_logout_tour.ready",

            login="admin",
            timeout=240,
        )
