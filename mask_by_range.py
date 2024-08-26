import pyart
import numpy as np


def mask_by_range(
    radar,
    fields=None,
    max_range=100000.0,
    min_range=0.0,
    mask_type="outside",
    suffix="_mask",
):
    """
    Masks radar field values based on a specified range for multiple fields.

    Parameters
    ----------
    radar : Radar
        Py-ART Radar object containing the radar data.
    fields : list of str, optional
        List of field names in the radar object to mask. If None, all fields
        in the radar object will be masked. Default is None.
    max_range : float, optional
        Maximum range in meters used as the threshold for masking. Default is 100000.0 (100 km).
    min_range : float, optional
        Minimum range in meters used as the lower threshold for masking. Default is 0.0.
    mask_type : {'inside', 'outside', 'in_between'}, optional
        Specifies the type of masking:
        - 'outside' masks data beyond max_range.
        - 'inside' masks data within max_range.
        - 'in_between' masks data between min_range and max_range.
        Default is 'outside'.
    suffix : str or None, optional
        Suffix to append to the new masked field name. If None, the field
        name will not be altered. Default is '_mask'.

    Returns
    -------
    radar : Radar
        The radar object with the new masked fields added.

    Examples
    --------
    >>> radar = mask_fields_by_range(radar, fields=['REF', 'VEL'], max_range=200000., mask_type='outside', suffix="_masked")
    >>> radar = mask_fields_by_range(radar, max_range=200000., mask_type='inside', suffix="_masked")  # Mask all fields inside the range
    >>> radar = mask_fields_by_range(radar, min_range=50000., max_range=200000., mask_type='in_between', suffix="_masked")  # Mask all fields between 50 km and 200 km
    """
    if fields is None:
        fields = list(radar.fields.keys())

    gate_range = radar.range["data"]
    gate_range_2D = np.tile(gate_range, (radar.nrays, 1))

    for field in fields:
        if mask_type == "outside":
            mfield = np.ma.masked_where(
                gate_range_2D > max_range, radar.fields[field]["data"]
            )
        elif mask_type == "inside":
            mfield = np.ma.masked_where(
                gate_range_2D <= max_range, radar.fields[field]["data"]
            )
        elif mask_type == "in_between":
            mfield = np.ma.masked_where(
                (gate_range_2D > min_range) & (gate_range_2D <= max_range),
                radar.fields[field]["data"],
            )
        else:
            raise ValueError(
                "Invalid mask_type. Choose either 'inside', 'outside', or 'in_between'."
            )

        if suffix is None:
            newname = field
        else:
            newname = field + "".join(suffix)

        radar.add_field_like(field, newname, mfield, replace_existing=True)

    return radar
