from estimate_area import estimate_bloom_area

class BlekingeBloomReporter:
    """Creates a report for algal bloom observations."""

    def __init__(self, warning_threshold=5.0, critical_threshold=10.0):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold

    def classify_bloom(self, num_samples, center_x=0.0, center_y=0.0, radius_x=2.0, radius_y=1.0):
        area = estimate_bloom_area(
            num_samples=num_samples,
            center_x=center_x,
            center_y=center_y,
            radius_x=radius_x,
            radius_y=radius_y,
        )

        if area >= self.critical_threshold:
            return "critical"
        if area >= self.warning_threshold:
            return "warning"
        return "normal"