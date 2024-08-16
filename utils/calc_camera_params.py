import math


def calculate_parameters(
    resolution_pixels, pixel_size_um, height_m, lens_focal_length_mm
):
    """
    Calculate the coverage and resolution of a line scan camera with varying lens focal lengths.

    :param resolution_pixels: Horizontal resolution of the camera in pixels.
    :param pixel_size_um: Size of a pixel in micrometers.
    :param height_m: Height at which the camera is mounted in meters.
    :param lens_focal_length_mm: Focal length of the lens in millimeters.
    :return: Coverage width in meters and resolution in pixels per millimeter.
    """
    # Convert pixel size from micrometers to millimeters
    pixel_size_mm = pixel_size_um / 1000

    # Calculate the physical width of the sensor
    sensor_width_mm = resolution_pixels * pixel_size_mm

    # Calculate the field of view width based on lens focal length and height
    # Field of view width (W) = 2 * (height) * tan(fov/2)
    # Assume FOV (Field of View) can be approximated as (2 * focal length) for a rough estimate
    fov_deg = 2 * math.degrees(math.atan(sensor_width_mm / (2 * lens_focal_length_mm)))

    # Field of view width in meters
    fov_width_m = 2 * height_m * math.tan(math.radians(fov_deg / 2))

    # Resolution in pixels per millimeter
    resolution_pix_per_mm = resolution_pixels / (fov_width_m * 1000)

    return fov_width_m, resolution_pix_per_mm


def main():
    # Camera specificationsexit()
    resolution_pixels = 4096
    pixel_size_um = 7
    height_m = 7  # Height in meters

    # Different lens focal lengths
    lens_focal_lengths_mm = [25, 35, 50]

    for focal_length in lens_focal_lengths_mm:
        coverage, resolution = calculate_parameters(
            resolution_pixels, pixel_size_um, height_m, focal_length
        )
        print(f"Lens focal length: {focal_length} mm")
        print(f"Coverage width: {coverage:.2f} meters")
        print(f"Resolution: {resolution:.2f} pixels/mm")
        print()


if __name__ == "__main__":
    main()
