# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH

import unittest

from odxtools.load_pdx_file import load_pdx_file

odxdb = load_pdx_file("./examples/somersault.pdx", enable_candela_workarounds=False)

class TestDatabase(unittest.TestCase):

    def test_db_structure(self):
        self.assertEqual([x.short_name for x in odxdb.diag_layer_containers],
                         ['somersault'])

        self.assertEqual([x.short_name for x in odxdb.diag_layers],
                         [
                             'somersault',
                             'somersault_lazy',
                             'somersault_assiduous'
                         ])

        self.assertEqual([x.short_name for x in odxdb.ecus],
                         [
                             'somersault_lazy',
                             'somersault_assiduous'
                         ])

    def test_admin_data(self):
        dlc = odxdb.diag_layer_containers.somersault

        self.assertTrue(dlc.admin_data is not None)
        ad = dlc.admin_data

        self.assertEqual(ad.language, 'en-US')

        self.assertTrue(ad.company_doc_infos is not None)
        cdi = ad.company_doc_infos

        self.assertEqual(len(cdi), 1)
        self.assertEqual(cdi[0].company_data_ref, 'CD.Suncus')
        self.assertTrue(cdi[0].company_data is not None)
        self.assertEqual(cdi[0].team_member_ref, 'TM.Doggy')
        self.assertTrue(cdi[0].team_member is not None)
        self.assertEqual(cdi[0].doc_label, 'A really meaningful label')

        self.assertTrue(ad.doc_revisions is not None)
        dr = ad.doc_revisions[0]

        self.assertEqual(len(dr.modifications), 2)
        mod = dr.modifications[0]

        self.assertEqual(mod.change, 'add somersault ECU')
        self.assertEqual(mod.reason, 'we needed a new artist')

        self.assertEqual(dr.revision_label, '1.0')
        self.assertEqual(dr.team_member_ref, 'TM.Doggy')
        self.assertTrue(dr.team_member is not None)
        self.assertEqual(dr.tool, 'odxtools 0.0.1')

    def test_company_datas(self):
        dlc = odxdb.diag_layer_containers.somersault

        self.assertTrue(dlc.company_datas is not None)
        cds = dlc.company_datas

        self.assertEqual([x.short_name for x in cds],
                         [
                             'Suncus',
                             'ACME_Corporation'
                         ])

        cd = cds.Suncus
        self.assertEqual(cd.id, 'CD.Suncus')
        self.assertEqual(cd.short_name, 'Suncus')
        self.assertEqual(cd.long_name, 'Circus of the sun')
        self.assertEqual(cd.description, '<p>Prestigious group of performers</p>')
        self.assertEqual(cd.roles, ['circus', 'gym'])

        self.assertEqual([x.short_name for x in cd.team_members],
                         [
                             'Doggy',
                             'Horsey'
                         ])

        doggy = cd.team_members.Doggy
        self.assertEqual(doggy.id, 'TM.Doggy')
        self.assertEqual(doggy.short_name, 'Doggy')
        self.assertEqual(doggy.long_name, 'Doggy the dog')
        self.assertEqual(doggy.description, "<p>Dog is man's best friend</p>")
        self.assertEqual(doggy.roles, ['gymnast', 'tracker'])
        self.assertEqual(doggy.department, 'sniffers')
        self.assertEqual(doggy.address, 'Some road')
        self.assertEqual(doggy.zip, '12345')
        self.assertEqual(doggy.city, 'New Dogsville')
        self.assertEqual(doggy.phone, '+0 1234/5678-9')
        self.assertEqual(doggy.fax, '+0 1234/5678-0')
        self.assertEqual(doggy.email, 'info@suncus.com')

        self.assertTrue(cd.company_specific_info is not None)
        self.assertTrue(cd.company_specific_info.related_docs is not None)

        rd = cd.company_specific_info.related_docs[0]

        self.assertEqual(rd.description, '<p>We are the best!</p>')
        self.assertTrue(rd.xdoc is not None)

        xdoc = rd.xdoc
        self.assertEqual(xdoc.short_name, 'best')
        self.assertEqual(xdoc.long_name, 'suncus is the best')
        self.assertEqual(xdoc.description, '<p>great propaganda...</p>')
        self.assertEqual(xdoc.number, '1')
        self.assertEqual(xdoc.state, 'published')
        self.assertEqual(xdoc.date, '2015-01-15T20:15:20+05:00')
        self.assertEqual(xdoc.publisher, 'Suncus Publishing')
        self.assertEqual(xdoc.url, 'https://suncus-is-the-best.com')
        self.assertEqual(xdoc.position, 'first!')

    def test_somersault_lazy(self):
        # TODO: this test is far from exhaustive
        ecu = odxdb.ecus.somersault_lazy

        self.assertEqual([x.short_name for x in ecu.services],
                         [
                             'compulsory_program',
                             'do_forward_flips',
                             'report_status',
                             'session_start',
                             'session_stop',
                             'tester_present'
                         ])

        service = ecu.services.do_forward_flips
        self.assertEqual([x.short_name for x in service.request.parameters],
                         [
                             'sid',
                             'forward_soberness_check',
                             'num_flips'
                         ])
        self.assertEqual([x.short_name for x in service.request.get_required_parameters()],
                         [
                             'forward_soberness_check',
                             'num_flips'
                         ])
        self.assertEqual(service.request.bit_length, 24)

        self.assertEqual([x.short_name for x in service.positive_responses],
                         [
                             'grudging_forward'
                         ])
        self.assertEqual([x.short_name for x in service.negative_responses],
                         [
                             'flips_not_done'
                         ])

        pr = service.positive_responses.grudging_forward
        self.assertEqual([x.short_name for x in pr.parameters],
                         [
                             'sid',
                             'num_flips_done'
                         ])
        self.assertEqual([x.short_name for x in pr.get_required_parameters()],
                         [
                             'num_flips_done'
                         ])
        self.assertEqual(pr.bit_length, 16)

        nr = service.negative_responses.flips_not_done
        self.assertEqual([x.short_name for x in nr.parameters],
                         [
                             'sid',
                             'rq_sid',
                             'reason',
                             'flips_successfully_done'
                         ])
        self.assertEqual(nr.bit_length, 32)

        nrc_const = nr.parameters.reason
        self.assertEqual(nrc_const.parameter_type, 'NRC-CONST')
        self.assertEqual(nrc_const.coded_values, [0, 1, 2])


class TestDecode(unittest.TestCase):

    def test_decode_request(self):
        messages = odxdb.ecus.somersault_assiduous.decode(bytes([0x03, 0x45]))
        self.assertTrue(len(messages) == 1)
        m = messages[0]
        self.assertEqual(m.coded_message, bytes([0x03, 0x45]))
        self.assertEqual(m.service, odxdb.ecus.somersault_assiduous.services.headstand)
        self.assertEqual(m.structure, odxdb.ecus.somersault_assiduous.services.headstand.request)
        self.assertEqual(m.param_dict, {"sid": 0x03, "duration": 0x45})

    def test_decode_inherited_request(self):
        raw_message = odxdb.ecus.somersault_assiduous.services.do_backward_flips(backward_soberness_check=0x21,
                                                                                 num_flips=2)
        messages = odxdb.ecus.somersault_assiduous.decode(raw_message)
        self.assertTrue(len(messages) == 1)
        m = messages[0]
        self.assertEqual(m.coded_message, bytes([0xbb, 0x21, 0x02]))
        self.assertEqual(m.service, odxdb.ecus.somersault_assiduous.services.do_backward_flips)
        self.assertEqual(m.structure, odxdb.ecus.somersault_assiduous.services.do_backward_flips.request)
        self.assertEqual(m.param_dict, {"sid": 0xbb, "backward_soberness_check": 0x21, "num_flips": 0x02})

    def test_decode_response(self):
        raw_request_message = odxdb.ecus.somersault_lazy.services.do_forward_flips(forward_soberness_check=0x12, num_flips=3)
        # TODO: responses currently don't seem to be inherited. (if
        # done, change "diag_layers.somersault" to
        # "ecus.somersault_lazy" here)
        db_response = next(filter(lambda x: x.short_name == "grudging_forward", odxdb.diag_layers.somersault.positive_responses))
        raw_response_message = db_response.encode(raw_request_message)

        messages = odxdb.diag_layers.somersault.decode_response(raw_response_message, raw_request_message)
        self.assertTrue(len(messages) == 1, f"There should be only one service for 0x0145 but there are: {messages}")
        m = messages[0]
        self.assertEqual(m.coded_message, bytes([0xfa, 0x03]))
        self.assertEqual(m.structure, db_response)
        self.assertEqual(m.param_dict,
                         { 'sid': 0xfa, 'num_flips_done': bytearray([0x03]) })


class TestNavigation(unittest.TestCase):

    def test_finding_services(self):
        # Find base variant
        self.assertIsNotNone(odxdb.diag_layers.somersault.services.do_backward_flips)
        self.assertIsNotNone(odxdb.diag_layers.somersault.services.do_forward_flips)
        self.assertIsNotNone(odxdb.diag_layers.somersault.services.report_status)

        # Find ecu variant
        self.assertIsNotNone(odxdb.ecus.somersault_assiduous.services.headstand)
        # Inherited services
        self.assertIsNotNone(odxdb.ecus.somersault_assiduous.services.do_backward_flips)
        self.assertIsNotNone(odxdb.ecus.somersault_assiduous.services.do_forward_flips)
        self.assertIsNotNone(odxdb.ecus.somersault_assiduous.services.report_status)
        self.assertIsNotNone(odxdb.ecus.somersault_assiduous.services.compulsory_program)

        # The lazy ECU variant only inherits services but does not add any.
        self.assertIsNotNone(odxdb.ecus.somersault_lazy.services.do_forward_flips)
        self.assertIsNotNone(odxdb.ecus.somersault_lazy.services.report_status)

        # also, the lazy ECU does not do backward flips. (this is
        # reserved for swots...)
        with self.assertRaises(AttributeError):
            odxdb.ecus.somersault_lazy.services.do_backward_flips

if __name__ == '__main__':
    unittest.main()
