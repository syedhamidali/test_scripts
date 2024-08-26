import pyart
import numpy as np


def mask_by_range(
    radar, fields=None, max_range=100000.0, mask_type="outside", suffix="_mask"
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
        Range in meters used as the threshold for masking. Default is 100000.0 (100 km).
    mask_type : {'inside', 'outside'}, optional
        Specifies whether to mask data inside or outside the max_range.
        'outside' masks data beyond max_range, 'inside' masks data within max_range.
        Default is 'outside'.
    suffix : str or None, optional
        Suffix to append to the new masked field name. If None, the field
        name will not be altered. Default is '_mask'.

    Returns
    -------
    radar : Radar
        The radar object with the new masked fields added.

    Notes
    -----
    This function creates a 2D array of gate ranges by tiling the 1D range
    array along the number of rays. It then masks the radar field values
    based on the specified range for each field in the list. The masked
    fields are added to the radar object with new names formed by appending
    the suffix to the original field names.

    Examples
    --------
    >>> radar = mask_fields_by_range(
                    radar, fields=['REF', 'VEL'],
                    max_range=200000.,
                    mask_type='outside',
                    suffix="_masked")
    >>> radar = mask_fields_by_range(
                    radar, max_range=200000.,
                    mask_type='inside',
                    suffix="_masked")  # Mask all fields inside the range
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
        else:
            raise ValueError("Invalid mask_type. Choose either 'inside' or 'outside'.")

        if suffix is None:
            newname = field
        else:
            newname = field + "".join(suffix)

        radar.add_field_like(field, newname, mfield, replace_existing=True)

    return radar
