#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2015-2022, AllWorldIT.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Docplates utils."""

import datetime

__all__ = [
    "format_timedelta",
]


def format_timedelta(delta: datetime.timedelta, microseconds: bool = True) -> str:
    """
    Convert a timedelta into its string representation.

    Parameters
    ----------
    delta : :class:`datetime.timedelta`
        Time delta to format.

    microseconds : :class:`bool`
        Whether or not to include microseconds in output.

    Return
    ------
    :class:`str` :
        Retruns formatted time delta string.

    """

    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    components = []
    if days:  # pragma: no cover
        components.append(f"{days}d")
    if hours:  # pragma: no cover
        components.append(f"{hours}h")
    if minutes:  # pragma: no cover
        components.append(f"{minutes}m")
    if seconds:  # pragma: no cover
        components.append(f"{seconds}s")
    if delta.microseconds and microseconds:  # pragma: no cover
        components.append(f"{int(delta.microseconds/1000)}ms")

    return " ".join(components)
