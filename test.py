import unittest

from get_gcal_next_event import _parse_event

# detail see. https://developers.google.com/calendar/v3/reference/events
event_base = {"summary": "event_name", "start": {"dateTime": "2020-01-01T00:00:00+09:00"}}

event_with_meet = event_base.copy()
event_with_meet["hangoutLink"] = "https://meet.google.com/xxx-xxxx-xxx"

event_with_stream = event_base.copy()
event_with_stream["conferenceData"] = {
    "entryPoints": [{"uri": "https://stream.meet.google.com/stream/dummy_stream_id"}]
}


class TestCase(unittest.TestCase):
    def test_parse_event(self):
        got = _parse_event(event_base)
        expected = ("event_name", "00:00", None, None)

        self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main()
