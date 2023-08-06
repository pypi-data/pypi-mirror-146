# SPDX-FileCopyrightText: 2019 4am
#
# SPDX-License-Identifier: MIT

from .wozardry import Track, raise_if
from . import a2rchery
import bitarray
import collections

class A2RSeekError(a2rchery.A2RError): pass

class A2RImage:
    def __init__(self, iostream):
        self.tracks = collections.OrderedDict()
        self.a2r_image = a2rchery.A2RReader(stream=iostream)
        self._speed = 32

    @property
    def speed(self):
        if self._speed is None:
            fluxxen = flux_record["data"][1:]
            speeds = [(len([1 for i in fluxxen[:8192] if i%t==0]), t) for t in range(0x1e,0x23)]
            self._speed = speeds[-1][1]
        return self._speed

    def to_json(self):
        return self.a2r_image.to_json()

    def to_bits(self, flux_record):
        """|flux_record| is a dictionary of 'capture_type', 'data_length', 'tick_count', and 'data'"""
        bits = bitarray.bitarray()
        if not flux_record or flux_record["capture_type"] != a2rchery.kCaptureTiming:
            return bits
        tick_count = flux_record['tick_count']
        fluxxen = flux_record["data"][1:]
        speed = self.speed
        flux_total = flux_start = -speed//2
        rev_total = 0
        for flux_value in fluxxen:
            rev_total += flux_value
            flux_total += flux_value
            if flux_value == 0xFF:
                continue
            if flux_total >= speed:
                bits.extend("0" * (flux_total // speed))
            bits.extend("1")
            flux_total = flux_start
#            if rev_total > tick_count:
#                print(f"bailing out at {rev_total}")
#                break
        return bits

    def seek(self, track_num):
        if type(track_num) != float:
            track_num = float(track_num)
        if track_num < 0.0 or \
           track_num > 35.0 or \
           track_num.as_integer_ratio()[1] not in (1,2,4):
            raise A2RSeekError("Invalid track %s" % track_num)
        location = int(track_num * 4)
        if not self.tracks.get(location):
            # just return the bits from the first flux read
            # (if the caller determines that they're not good, it will call reseek()
            # which is smarter but takes longer)
            bits = bitarray.bitarray()
            if location in self.a2r_image.flux:
                global flux_
                flux_record = self.a2r_image.flux[location][0]
                bits = self.to_bits(flux_record)
                est_bit_len = round(flux_record['tick_count'] / self.speed)
            else:
                est_bit_len = None
            self.tracks[location] = Track(bits, len(bits), est_bit_len)
        return self.tracks[location]

    def reseek(self, track_num):
        location = int(track_num * 4)
        # reset cached speed so we'll recalculate it
        self.speed = 0
        # read the rest of the flux records and concatenate them on the end
        # of the existing bitstream (this assumes you've called seek() before
        # on this track)
        all_bits = self.tracks[location].bits
        for flux_record in self.a2r_image.flux[location][1:]:
            all_bits.extend(self.to_bits(flux_record))
        self.tracks[location] = Track(all_bits, len(all_bits))
        return self.tracks[location]
