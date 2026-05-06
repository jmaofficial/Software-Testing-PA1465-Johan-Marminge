import unittest
from unittest.mock import patch
from report import BlekingeBloomReporter


class TestClassifyBloom(unittest.TestCase):
    def test_classify_bloom_returns_normal(self):
        #simple check that the function returns "normal" for areas less than 5
        reporter = BlekingeBloomReporter()

        with patch("report.estimate_bloom_area", return_value=4.99999):
            classification = reporter.classify_bloom(num_samples=100)

        self.assertEqual(classification, "normal")

        with patch("report.estimate_bloom_area", return_value=0):
            classification = reporter.classify_bloom(num_samples=100)

        self.assertEqual(classification, "normal")

    def test_classify_bloom_returns_warning(self):
        #simple check that the function returns "warning" for areas between 5 and 10
        reporter = BlekingeBloomReporter()

        with patch("report.estimate_bloom_area", return_value=5):
            classification = reporter.classify_bloom(num_samples=100)

        self.assertEqual(classification, "warning")

        with patch("report.estimate_bloom_area", return_value=9.99999):
            classification = reporter.classify_bloom(num_samples=100)

        self.assertEqual(classification, "warning")


    def test_classify_bloom_returns_critical(self):
        #simple check that the function returns "critical" for values greater than or equal to 10

        reporter = BlekingeBloomReporter()
        with patch("report.estimate_bloom_area", return_value=10):
            classification = reporter.classify_bloom(num_samples=100)

        self.assertEqual(classification, "critical")

        with patch("report.estimate_bloom_area", return_value=99999999999999999999999):
            classification = reporter.classify_bloom(num_samples=100)

        self.assertEqual(classification, "critical")

    def test_classify_bloom_calls_estimate_bloom_area(self):
        reporter = BlekingeBloomReporter()
        #this checks that the classify_bloom function calls
        #the estimate_bloom_area function with the correct parameters
        with patch("report.estimate_bloom_area", return_value=4.0) as mock_estimate:
            reporter.classify_bloom(
                num_samples=100,
                center_x=1,
                center_y=2,
                radius_x=3,
                radius_y=4,
            )

        mock_estimate.assert_called_once_with(
            num_samples=100,
            center_x=1,
            center_y=2,
            radius_x=3,
            radius_y=4,
        )


if __name__ == "__main__":
    unittest.main()
