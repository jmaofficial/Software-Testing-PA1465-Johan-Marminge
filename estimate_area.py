import random


def survey_area(x_min, x_max, y_min, y_max):
    """Return the area of the surveyed sea rectangle."""
    if x_min >= x_max or y_min >= y_max:
        raise ValueError("Invalid survey bounds")
    return (x_max - x_min) * (y_max - y_min)


def is_inside_bloom(x, y, center_x=0.0, center_y=0.0, radius_x=2.0, radius_y=1.0):
    """
    Return True if a sampled sea point lies inside the detected algal bloom.

    The bloom is approximated as an ellipse:
        ((x - center_x)^2 / radius_x^2) + ((y - center_y)^2 / radius_y^2) <= 1
    """
    if radius_x <= 0 or radius_y <= 0:
        raise ValueError("Bloom radii must be > 0")

    normalized_x = ((x - center_x) ** 2) / (radius_x ** 2)
    normalized_y = ((y - center_y) ** 2) / (radius_y ** 2)
    return normalized_x + normalized_y <= 1.0


def random_sample_point(x_min, x_max, y_min, y_max):
    """Generate a random sample point inside the surveyed sea area."""
    return (
        random.uniform(x_min, x_max),
        random.uniform(y_min, y_max),
    )


def estimate_bloom_area(num_samples, center_x=0.0, center_y=0.0, radius_x=2.0, radius_y=1.0):
    """
    Estimate the area of an algal bloom in a surveyed coastal region.
    """
    if num_samples <= 0:
        raise ValueError("num_samples must be > 0")
    if radius_x <= 0 or radius_y <= 0:
        raise ValueError("Bloom radii must be > 0")

    x_min, x_max = center_x - radius_x, center_x + radius_x
    y_min, y_max = center_y - radius_y, center_y + radius_y

    inside = 0
    for _ in range(num_samples):
        x, y = random_sample_point(x_min, x_max, y_min, y_max)
        if is_inside_bloom(x, y, center_x, center_y, radius_x, radius_y):
            inside += 1

    total_survey_area = survey_area(x_min, x_max, y_min, y_max)

    return total_survey_area * (inside / (num_samples + 1))