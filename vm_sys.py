
class TLBEntry:

    def __init__(self):
        self.lru = 0
        self.s = -1
        self.p = -1
        self.f = -1

    def set_spf(self, s, p, f):
        self.s = s
        self.p = p
        self.f = f


class VirtualMemory:

    def __init__(self):
        self._pm = [0] * 1024 * 512
        self._bitmap = [0] * 1024
        self._TLB = [TLBEntry(), TLBEntry(), TLBEntry(), TLBEntry()]

    def _va_to_components(self, va):
        va_bin = bin(int(va))[2:]
        if len(va_bin) != 32:
            va_bin = (32-len(va_bin))*'0' + va_bin

        s = int(va_bin[4:13], 2)
        p = int(va_bin[13:23], 2)
        w = int(va_bin[23:], 2)
        return s, p, w

    def _read(self, va):
        s, p, w = self._va_to_components(va)

        # TLB hit
        for i in range(4):
            if self._TLB[i].s == s and self._TLB[i].p == p:
                for j in range(4):
                    if self._TLB[j].lru > self._TLB[i].lru and self._TLB[j].lru > 0:
                        self._TLB[j].lru -= 1

                self._TLB[i].lru = 3
                print("h", self._TLB[i].f + w, end=' ')
                return

        # TLB miss
        st_entry = self._pm[s]
        if st_entry == -1:
            print("m pf", end=' ')
        elif st_entry == 0:
            print("m err", end=' ')
        else:
            pt_entry = self._pm[st_entry + p]
            if pt_entry == -1:
                print("m pf", end=' ')
            elif pt_entry == 0:
                print("m err", end=' ')
            else:
                for i in range(4):
                    if self._TLB[i].lru == 0:
                        self._TLB[i].lru = 3
                        self._TLB[i].set_spf(s, p, pt_entry)

                        for j in range(4):
                            if j != i and self._TLB[j].lru > 0:
                                self._TLB[j].lru -= 1

                        print("m", self._pm[st_entry + p] + w, end=' ')
                        break

    def _write(self, va):
        s, p, w = self._va_to_components(va)

        # TLB hit
        for i in range(4):
            if self._TLB[i].s == s and self._TLB[i].p == p:
                for j in range(4):
                    if self._TLB[j].lru > self._TLB[i].lru and self._TLB[j].lru > 0:
                        self._TLB[j].lru -= 1

                self._TLB[i].lru = 3
                print("h", self._TLB[i].f + w, end=' ')
                return

        # TLB miss
        st_entry = self._pm[s]
        if st_entry == -1:
            print("m pf", end=' ')
            return
        elif st_entry == 0:
            # Create PT
            frame = 1
            while self._bitmap[frame] != 0 or self._bitmap[frame+1] != 0:
                frame += 1

            self._pm[s] = frame * 512
            self._bitmap[frame] = 1
            self._bitmap[frame+1] = 1

        pt_entry = self._pm[st_entry + p]
        if pt_entry == -1:
            print("m pf", end=' ')
            return
        elif pt_entry == 0:
            # Create page
            frame = 1
            while self._bitmap[frame] != 0:
                frame += 1

            self._pm[st_entry + p] = frame * 512
            self._bitmap[frame] = 1

        for i in range(4):
            if self._TLB[i].lru == 0:
                self._TLB[i].lru = 3
                self._TLB[i].set_spf(s, p, pt_entry)

                for j in range(4):
                    if j != i and self._TLB[j].lru > 0:
                        self._TLB[j].lru -= 1

                print("m", self._pm[st_entry + p] + w, end=' ')
                break

    def init(self):
        self._bitmap[0] = 1

        st_entries_input = input()
        st_entries = st_entries_input.split(" ")
        for s, f in zip(st_entries[0::2], st_entries[1::2]):
            self._pm[int(s)] = int(f)
            if int(f) >= 0:
                frame = int(int(f)/512)
                self._bitmap[frame] = 1
                self._bitmap[frame+1] = 1

        pt_entries_input = input()
        pt_entries = pt_entries_input.split(" ")
        for p, s, f in zip(pt_entries[0::3], pt_entries[1::3], pt_entries[2::3]):
            self._pm[self._pm[int(s)] + int(p)] = int(f)
            if int(f) >= 0:
                frame = int(int(f)/512)
                self._bitmap[frame] = 1

    def translate(self):
        cmds_input = input()
        cmds = cmds_input.split(" ")
        for op, va in zip(cmds[0::2], cmds[1::2]):
            if int(op) == 0:
                self._read(va)
            elif int(op) == 1:
                self._write(va)


if __name__ == '__main__':
    VM = VirtualMemory()
    VM.init()
    VM.translate()
