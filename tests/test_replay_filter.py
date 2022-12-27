from unittest import TestCase
from constants.constants import EventStringCode
from filters.ReplayFilter import ReplayFilter
from utilities.parse import parse_packet
from tests.packet_utilities import (
    create_generic_event_data, create_car_telemetry_data)


# TODO: expand when ReplayFilter implementation is updated.
class TestReplayFilter(TestCase):
    def test_packet_data_stored(self):
        filter = ReplayFilter()
        self.assertEqual(filter.is_session_started, False)
        filter.filter(parse_packet(create_generic_event_data(
            EventStringCode.SESSION_START.value)))
        self.assertEqual(filter.is_session_started, True)
        data = filter.data['car_telemetry'][0]['speed']
        self.assertEqual(len(data), 0)
        filter.filter(parse_packet(create_car_telemetry_data()))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], 6.5)
        self.assertEqual(data[0][1], 1)

    def test_packet_ignored_if_session_not_started(self):
        filter = ReplayFilter()
        data = filter.data['car_telemetry'][0]['speed']
        self.assertEqual(len(data), 0)
        filter.filter(parse_packet(create_car_telemetry_data()))
        self.assertEqual(len(data), 0)
        filter.filter(parse_packet(create_generic_event_data(
             EventStringCode.SESSION_START.value)))

    def test_duplicate_session_start_clears_data(self):
        filter = ReplayFilter()
        filter.filter(parse_packet(create_generic_event_data(
            EventStringCode.SESSION_START.value)))
        filter.filter(parse_packet(create_car_telemetry_data()))
        self.assertEqual(len(filter.data['car_telemetry'][0]['speed']), 1)
        filter.filter(parse_packet(create_generic_event_data(
            EventStringCode.SESSION_START.value)))
        self.assertEqual(len(filter.data['car_telemetry'][0]['speed']), 0)
