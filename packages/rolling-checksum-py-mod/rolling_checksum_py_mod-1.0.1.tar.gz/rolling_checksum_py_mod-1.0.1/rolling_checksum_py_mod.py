
'''Provides a very simple rolling checksum for file data'''

import sys




def min_max_chunker(file_):
    '''Make sure chunk sizes are above and below a pair of thresholds'''

    empty = True
    minimum_length = 2 ** 19  # 0.5 mebibytes
    maximum_length = 2 ** 22  # 4.0 mebibytes

    for chunk in n_level_chunker(file_, levels=3):
        if empty:
            chunk_so_far = chunk
        else:
            chunk_so_far += chunk
        empty = False

        len_chunk_so_far = len(chunk_so_far)

        if len_chunk_so_far < minimum_length:
            # go back up for another piece
            continue

        if len_chunk_so_far < maximum_length:
            # good - we're in the sweet spot
            yield chunk_so_far
            empty = True
            continue

        if len_chunk_so_far >= maximum_length:
            # we have a long chunk - split it and go around for more
            yield chunk_so_far[:maximum_length]
            chunk_so_far = chunk_so_far[maximum_length:]
            continue

        raise AssertionError("Should never reach this point")

    if not empty and chunk_so_far:
        yield chunk_so_far


def n_level_chunker(file_, levels=1):

    # pylint: disable=R0912,R0914
    # R0912: I looked into reducing the branch count here, but it seemed to make things more complex, not less
    # R0914: I believe we need a few local variables

    '''Divide a file up into portions when we get 3 in-range checksums in a row'''









    rolling_checksum = Rolling_checksum()

    # this threshold should give us about 2**20 byte chunks on average
    modulus = rolling_checksum.get_modulus()
    threshold = modulus * 0.007

    consecutive_boundaries = 0

    two_to_the_22nd = 2 ** 22
    preferred_block_len = two_to_the_22nd

    block = file_.read(preferred_block_len)

    while True:
        if not block[preferred_block_len - 1:]:
            block = block + file_.read(preferred_block_len - len(block))

        if not block:
            break

        for byteno, character in enumerate(block):
            # This if deals with python 2 returing single-character str's, and python 3 returning an integer between 0 and 255
            byte = character

            checksum = rolling_checksum.add_byte(byte)

            if checksum < threshold:
                consecutive_boundaries += 1
            else:
                consecutive_boundaries = 0
                continue

            if consecutive_boundaries == levels:
                consecutive_boundaries = 0
                result = block[:byteno]
                block = block[byteno:]

                if result:
                    # result is not empty, so yield it
                    yield result
                # we must break out of the loop to restart byteno at 0
                break
        else:
            # We made it all the way through the enumeration without yielding anything, so yield all we have and empty block
            if block:
                yield block
                # in other words, make block an empty string
                block = block[0:0]

    # we're done processing chunks - return what's left, if it's not empty
    if block:
        # result is not empty, so yield it
        sys.stderr.write('yielding block (3) of length %d\n' % len(result))
        yield block
        block = file_.read(two_to_the_22nd)
        assert not block


# This one actually seems to be better as an iterator than a generator
class Rolling_checksum(object):











    # pylint: disable=R0902
    # R0902: We need a few instance attributes; we're a nontrivial iterator - but I suspect this'll beat polynomials bigtime

    '''
    Compute a very simple, fast, rolling checksum.  We don't maintain a list of bytes or anything - we just produce checksums
    on demand.  Inspired by linear congruential random number generation.  It's not quite the same thing though.
    '''

    def __init__(self, width=607, multiplicand=7, modulus=3677, addend=66041):
        # pylint: disable=R0913
        # R0913: We need a few arguments
        self._total = addend * width
        self._width = width
        self._multiplicand = multiplicand
        self._modulus = modulus
        self._addend = addend
        self._offset = 0
        self._window = [addend] * self._width

    def add_byte(self, byte):
        '''Add a byte into our rolling checksum function'''
        adjusted = byte * self._multiplicand + self._addend
        self._window[self._offset] = adjusted
        self._total += adjusted
        new_offset = (self._offset + 1) % self._width
        self._offset = new_offset
        self._total -= self._window[new_offset]
        return self._total % self._modulus

    def get_modulus(self):
        '''Return the modulus'''
        return self._modulus
