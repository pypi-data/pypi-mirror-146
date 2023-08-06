#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Circuit"]

from zepben.opendss import BusConnection


class Circuit:

    def __init__(
            self,
            uid: str,
            bus_conn: BusConnection,
            pu: float,
            base_kv: float,
            phases: int,
            rpos: float,
            xpos: float,
            rneg: float,
            xneg: float,
            rzero: float,
            xzero: float
    ):
        self.uid = uid
        self.bus_conn = bus_conn
        self.pu = pu
        self.base_kv = base_kv
        self.phases = phases
        self.rpos = rpos
        self.xpos = xpos
        self.rneg = rneg
        self.xneg = xneg
        self.rzero = rzero
        self.xzero = xzero
