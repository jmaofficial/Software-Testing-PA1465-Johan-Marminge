import unittest
from unittest.mock import patch
from estimate_area import (
    is_inside_bloom,
    random_sample_point,
    survey_area,
    estimate_bloom_area
)


class TestSurveyArea(unittest.TestCase):
    def test_returns_expected_area_for_valid_bounds(self):
        self.assertEqual(survey_area(0, 2, 0, 1), 2)
        self.assertEqual(survey_area(-1, 1, -1, 1), 4)
        self.assertEqual(survey_area(0, 0.5, 0, 0.5), 0.25) #checking that the function can handle non-integer bounds
        self.assertEqual(survey_area(-2, -1, -2, -1), 1)#checking that the function can handle negative bounds

    def test_raises_value_error_for_invalid_bounds(self):
        #invalid values
        with self.assertRaises(ValueError):
            survey_area(1, 0, 1, 0)
        with self.assertRaises(ValueError):
            survey_area(0, 1, 1, 0)
        with self.assertRaises(ValueError):
            survey_area(1, 0, 0, 1)
        with self.assertRaises(ValueError):
            survey_area(0, 0, 0, 0)



class TestIsInsideBloom(unittest.TestCase):
    def test_returns_true_for_points_inside_or_on_boundary(self):
        #some points that are inside the bloom or on the boundary of the bloom
        self.assertTrue(is_inside_bloom(0, 0))
        self.assertTrue(is_inside_bloom(1, 0))
        self.assertTrue(is_inside_bloom(2, 0))
        self.assertTrue(is_inside_bloom(0, 1))
        #testing points with a very small radius
        self.assertTrue(is_inside_bloom(0, 0, radius_x=0.00001, radius_y=0.00001))

    def test_returns_false_for_points_outside_bloom(self):
        self.assertFalse(is_inside_bloom(2.1, 0))
        self.assertFalse(is_inside_bloom(0, 1.1))

    def test_raises_value_error_for_invalid_radius(self):
        #invalid values
        with self.assertRaises(ValueError):
            is_inside_bloom(0, 0, radius_x=-1)
        with self.assertRaises(ValueError):
            is_inside_bloom(0, 0, radius_y=-1)
        with self.assertRaises(ValueError):
            is_inside_bloom(0, 0, radius_x=0)
        with self.assertRaises(ValueError):
            is_inside_bloom(0, 0, radius_y=0)


class TestRandomSamplePoint(unittest.TestCase):
    def test_generated_points_stay_within_bounds(self):
        x_min, x_max, y_min, y_max = 0, 2, 0, 1
        #testing that the generated points are within the bounds
        for _ in range(100):
            x, y = random_sample_point(x_min, x_max, y_min, y_max)
            self.assertGreaterEqual(x, x_min)
            self.assertLessEqual(x, x_max)
            self.assertGreaterEqual(y, y_min)
            self.assertLessEqual(y, y_max)

class TestEstimateBloomArea(unittest.TestCase):
    def test_estimate_bloom_area_returns_positive_value(self):
        #areas can't be negative, so we just check that the returned value is greater than 0
        for _ in range(1000):
            area = estimate_bloom_area(num_samples=42)
            self.assertGreater(area, 0)

    def test_estimate_bloom_area_all_samples_inside_returns_full_survey_area(self):
        #check that if all samples are inside the bloom, 
        #the estimated area is equal to the standard area given by default parameters.
        sample_points = [(0, 0), (1, 0), (0, 0.5), (2, 0)]

        with patch("estimate_area.random_sample_point", side_effect=sample_points):
            area = estimate_bloom_area(num_samples=4)

        self.assertEqual(area, 8)

    def test_estimate_bloom_area_half_samples_inside_returns_half_survey_area(self):
        #check that if half of the samples are inside the bloom, 
        #the estimated area is half of the standard area given by default parameters.
        sample_points = [
            (0, 0),
            (1, 0),
            (-1, 0),
            (0, 0.5),
            (0, -0.5),
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (0, 1.1),
        ]

        with patch("estimate_area.random_sample_point", side_effect=sample_points):
            area = estimate_bloom_area(num_samples=10)

        self.assertEqual(area, 4)


    def test_estimate_bloom_area_with_zero_samples_raises_value_error(self):
        #invalid values
        with self.assertRaises(ValueError):
            estimate_bloom_area(num_samples=0)

    def test_estimate_bloom_area_with_negative_samples_raises_value_error(self):
        #invalid values
        with self.assertRaises(ValueError):
            estimate_bloom_area(num_samples=-1)
        with self.assertRaises(ValueError):
            estimate_bloom_area(num_samples=0)
        with self.assertRaises(TypeError):
            estimate_bloom_area(num_samples="1")
        with self.assertRaises(TypeError):
            estimate_bloom_area(num_samples="ö")

    def test_estimate_bloom_area_with_invalid_radius_raises_value_error(self):
        #invalid values
        with self.assertRaises(ValueError):
            estimate_bloom_area(num_samples=100, radius_x=0)
        with self.assertRaises(ValueError):
            estimate_bloom_area(num_samples=100, radius_y=0)
        with self.assertRaises(ValueError):
            estimate_bloom_area(num_samples=100, radius_x=-1)
        with self.assertRaises(ValueError):
            estimate_bloom_area(num_samples=100, radius_y=-1)


if __name__ == "__main__":
    unittest.main()
