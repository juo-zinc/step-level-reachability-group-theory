from dataclasses import dataclass
from typing import List, Tuple

# ----------------------------
# Cubie indexing 
# Corners: 0 URF, 1 UFL, 2 ULB, 3 UBR, 4 DFR, 5 DLF, 6 DBL, 7 DRB
# Edges:   0 UR,  1 UF,  2 UL,  3 UB,  4 DR,  5 DF,  6 DL,  7 DB,  8 FR,  9 FL, 10 BL, 11 BR
# ----------------------------

CORNER_NAMES = ["URF","UFL","ULB","UBR","DFR","DLF","DBL","DRB"]
EDGE_NAMES   = ["UR","UF","UL","UB","DR","DF","DL","DB","FR","FL","BL","BR"]

# T0=UFR(URF), T1=UBR(UBR), T2=UBL(ULB), T3=UFL(UFL)
TOP_POS = [0, 3, 2, 1]  # positions of (URF, UBR, ULB, UFL) 
TOP_NAMES = ["UFR","UBR","UBL","UFL"]

BC_CORNER_POS = [4, 5, 6, 7]                 # DFR, DLF, DBL, DRB
BE_EDGE_POS   = [6, 9, 10, 4, 8, 11]         # DL, FL, BL, DR, FR, BR

@dataclass
class CubieCube:
    cp: List[int]  # corner permutation: which corner cubie is in each position
    co: List[int]  # corner orientation (0,1,2) for the cubie in each position
    ep: List[int]  # edge permutation
    eo: List[int]  # edge orientation (0,1) for the cubie in each position

    @staticmethod
    def solved() -> "CubieCube":
        return CubieCube(
            cp=list(range(8)), co=[0]*8,
            ep=list(range(12)), eo=[0]*12
        )

    def multiply(self, m: "CubieCube") -> "CubieCube":
        """
        Return self * m (apply move m to current cube self).
        Move cube m is encoded as the effect on a solved cube.
        """
        new_cp = [0]*8
        new_co = [0]*8
        for i in range(8):
            new_cp[i] = self.cp[m.cp[i]]
            new_co[i] = (self.co[m.cp[i]] + m.co[i]) % 3

        new_ep = [0]*12
        new_eo = [0]*12
        for i in range(12):
            new_ep[i] = self.ep[m.ep[i]]
            new_eo[i] = (self.eo[m.ep[i]] + m.eo[i]) % 2

        return CubieCube(new_cp, new_co, new_ep, new_eo)

# ----------------------------
# Basic face moves as CubieCubes (effect on solved cube)
# ----------------------------

MOVE_U = CubieCube(
    cp=[1,2,3,0,4,5,6,7],
    co=[0,0,0,0,0,0,0,0],
    ep=[1,2,3,0,4,5,6,7,8,9,10,11],
    eo=[0]*12
)

MOVE_R = CubieCube(
    cp=[4,1,2,0,7,5,6,3],
    co=[2,0,0,1,1,0,0,2],
    ep=[8,1,2,3,11,5,6,7,4,9,10,0],
    eo=[0]*12
)

MOVE_F = CubieCube(
    cp=[1,5,2,3,0,4,6,7],
    co=[1,2,0,0,2,1,0,0],
    ep=[0,9,2,3,4,8,6,7,1,5,10,11],
    eo=[0,1,0,0,0,1,0,0,1,1,0,0]
)

MOVE_D = CubieCube(
    cp=[0,1,2,3,5,6,7,4],
    co=[0]*8,
    ep=[0,1,2,3,5,6,7,4,8,9,10,11],
    eo=[0]*12
)

MOVE_L = CubieCube(
    cp=[0,2,6,3,4,1,5,7],
    co=[0,1,2,0,0,2,1,0],
    ep=[0,1,10,3,4,5,9,7,8,2,6,11],
    eo=[0]*12
)

MOVE_B = CubieCube(
    cp=[0,1,3,7,4,5,2,6],
    co=[0,0,1,2,0,0,2,1],
    ep=[0,1,2,11,4,5,6,10,8,9,3,7],
    eo=[0,0,0,1,0,0,0,1,0,0,1,1]
)

MOVE_MAP = {
    "U": MOVE_U, "R": MOVE_R, "F": MOVE_F,
    "D": MOVE_D, "L": MOVE_L, "B": MOVE_B
}

def parse_moves(seq: str) -> List[Tuple[str,int]]:
    """
    Parse sequences like: "R2B2RFR'B2RF'R" or with spaces.
    Returns list of (face, power) where power in {1,2,3} meaning:
      1 = face
      2 = face2
      3 = face'  (i.e., three quarter turns)
    """
    s = seq.replace(" ", "")
    i = 0
    out = []
    while i < len(s):
        face = s[i]
        if face not in MOVE_MAP:
            raise ValueError(f"Unexpected move face '{face}' in: {seq}")
        i += 1
        power = 1
        if i < len(s) and s[i] in ["2", "'"]:
            if s[i] == "2":
                power = 2
            else:
                power = 3
            i += 1
        out.append((face, power))
    return out

def moves_to_cube(seq: str) -> CubieCube:
    c = CubieCube.solved()
    for face, power in parse_moves(seq):
        m = MOVE_MAP[face]
        for _ in range(power):
            c = c.multiply(m)
    return c

def invert_moves(seq: str) -> str:
    """
    Invert a move string (no spaces required).
    Example: "R U2 F'" -> inverse is "F U2 R'"
    """
    toks = parse_moves(seq)
    inv = []
    for face, power in reversed(toks):
        inv_power = (4 - power) % 4
        if inv_power == 0:
            continue
        if inv_power == 1:
            inv.append(face)
        elif inv_power == 2:
            inv.append(face + "2")
        elif inv_power == 3:
            inv.append(face + "'")
    return " ".join(inv)

def compose_sequences(*seqs: str) -> str:
    return " ".join([s for s in seqs if s.strip()])

def check_blocks_preserved(c: CubieCube) -> None:
    # BC corners: positions 4,5,6,7 must contain same cubie and orientation 0
    for pos in BC_CORNER_POS:
        if c.cp[pos] != pos or c.co[pos] != 0:
            raise AssertionError(
                f"BC not preserved at corner pos {CORNER_NAMES[pos]}: "
                f"has cubie {CORNER_NAMES[c.cp[pos]]}, co={c.co[pos]}"
            )
    # BE edges: positions 6,9,10,4,8,11 must contain same cubie and orientation 0
    for pos in BE_EDGE_POS:
        if c.ep[pos] != pos or c.eo[pos] != 0:
            raise AssertionError(
                f"BE not preserved at edge pos {EDGE_NAMES[pos]}: "
                f"has cubie {EDGE_NAMES[c.ep[pos]]}, eo={c.eo[pos]}"
            )

def phi_on_top_corners(c: CubieCube) -> Tuple[List[int], List[int]]:
    """
    Returns (perm, twist) on top 4 corner cubies, in the order (T0,T1,T2,T3) = (URF, UBR, ULB, UFL).
    - perm[i] = j means cubie originally at Ti ends up at Tj
    - twist[i] in {0,1,2} is the orientation of that original cubie after applying c
    """
    # original top cubies are the cubie indices at those positions in solved state:
    top_cubies = TOP_POS[:]  # in solved, cubie id == position id

    # Build map: cubie_id -> (position, orientation) in current cube
    cubie_pos = [0]*8
    cubie_ori = [0]*8
    for pos in range(8):
        cid = c.cp[pos]
        cubie_pos[cid] = pos
        cubie_ori[cid] = c.co[pos]

    # For each original top cubie, find where it went among top positions
    perm = [0]*4
    twist = [0]*4
    for i, cid in enumerate(top_cubies):
        pos_now = cubie_pos[cid]
        if pos_now not in TOP_POS:
            raise AssertionError(f"Top corner cubie {CORNER_NAMES[cid]} left the top layer (pos={pos_now}).")
        j = TOP_POS.index(pos_now)   # which Tj position
        perm[i] = j
        twist[i] = cubie_ori[cid]
    return perm, twist

def pretty_perm(perm: List[int]) -> str:
    # show mapping T0->T?, etc.
    parts = [f"{TOP_NAMES[i]}->{TOP_NAMES[perm[i]]}" for i in range(4)]
    return ", ".join(parts)

def main():
    A = "R2B2RFR'B2RF'R"
    f = "R' D R D' R' D R"
    f = f.replace(" ", "")  # allow spaces in source
    U = "U"

    finv = invert_moves(f)
    W = compose_sequences(f, U, finv, "U'")
    Ainv = invert_moves(A)
    Winv = invert_moves(W)

    # T = W^-1 A W A^-1
    T = compose_sequences(Winv, A, W, Ainv)

    for name, seq in [("A", A), ("U", U), ("f", f), ("W", W), ("T", T)]:
        cube = moves_to_cube(seq)
        # verify blocks for A, U, W, T (f may not preserve H, depends)
        if name in ["A", "U", "W", "T"]:
            check_blocks_preserved(cube)
        perm, twist = phi_on_top_corners(cube)
        print(f"{name} = {seq}")
        print(f"  Phi({name}) top-corner mapping: {pretty_perm(perm)}")
        print(f"  Phi({name}) top-corner twists (mod 3) in order (UFR,UBR,UBL,UFL): {twist}")
        print()

    print("All requested H-elements (A, U, W, T) preserve BC and BE: OK.")

if __name__ == "__main__":
    main()
