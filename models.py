"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from typing import Optional

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation: str, name: str, diameter: str, hazardous: str):
        """Create a new `NearEarthObject`.

        :param designation: The primary designation for this NearEarthObject.
        :param name: The IAU name for this NearEarthObject.
        :param diameter: The diameter, in kilometers, of this NearEarthObject.
        :param hazardous: Whether or not this NearEarthObject is potentially hazardous.
        """

        designation = designation.strip()
        name = name.strip()

        # empty name should be coerced to None
        if not name:
            name = None

        try:
            diameter = float(diameter)
        except ValueError:
            diameter = float("nan")

        hazardous = bool(hazardous)

        # TODO: Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        self.designation = designation
        self.name = name
        self.diameter = diameter
        self.hazardous = hazardous

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # TODO: Use self.designation and self.name to build a fullname for this object.
        return_val = self.designation.upper()
        if self.name:
            return_val += " (" + self.name.title() + ")"

        return return_val

    def __str__(self):
        """Return `str(self)`.

        e.g. NEO 433 (Eros) has a diameter of 16.840 km and is not potentially hazardous.
        """
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        is_or_is_not_map = {
            True: "is",
            False: "is not",
        }
        is_or_is_not = is_or_is_not_map[self.hazardous]
        return f"{self.fullname} has a diameter of {self.diameter:.2f} km and {is_or_is_not} potentially hazardous"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
        )


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, time, distance: str, velocity: str):
        """Create a new `CloseApproach`.

        :param designation: primary designation of the asteroid or comet (e.g., 443, 2000 SG344)
        :param time: time of close-approach (formatted calendar date/time, in UTC)
        :param distance: nominal approach distance (au)
        :param velocity: velocity relative to the approach body at close approach (km/s)
        """
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        self._designation = designation.strip()
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # TODO: Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time.
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`.

        e.g. "On 2021-08-21 15:10, '2016 AJ193' approaches Earth at a distance of 0.02 au and a velocity of 26.17 km/s."
        """
        neo_name = self._designation
        if self.neo:
            neo_name = self.neo.full_name

        return f"On {self.time_str}, '{neo_name}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )
