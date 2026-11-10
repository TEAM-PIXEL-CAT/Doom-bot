"""
Level themes for TIPO DOOM. Everything here is data the bot sends to the widget:
level 1 goes out as the widget's public_data, later levels as the answer to the
widget's request "lv:N". The widget parses both with the same function.

Pack format (one string, at most 1024 bytes):
    palette | monster | barrel | torch | column | medkit | ammo | colours | stats | name

palette  11 colours, 6 hex digits each, for the letters a..k used in the sprites:
         a outline, b body, c body light, d bone/teeth/skin, e red, f yellow,
         g steel, h slime/eye, i flame, j flame core, k stone
sprites  16x16 pixel art, only the LEFT half is stored (8 columns x 16 rows,
         row by row); the widget mirrors it. "." is transparent.
colours  sky, floor, brick, mortar, tech panel, tech light, stone, exit door
stats    monster health, speed (cells/s), damage per hit (plus up to +5 at random)
"""

BARREL = ("........" * 5 + "...aaaaa" + "..ahhhhh" + "..ahhhhh" + "..agkggg" + "..agkggg"
          + "..aaaaaa" + "..agkggg" + "..agkggg" + "..agkggg" + "..aaaaaa" + "...aaaaa")
TORCH = (".......i" + "......ij" + ".....ijj" + "......ij" + ".....iii" + ".....aaa"
         + "......aa" * 8 + ".....aaa" + "....aaaa")
COLUMN = ("....aaaa" + "....gkkk" + "....gkkk" + "....gddd" + "....gdad" + "....gddd" + "....gada"
          + "....gkkk" + "....gkkg" * 5 + "....gkkk" + "...aaaaa" + "..aaaaaa")
MEDKIT = ("........" * 8 + "...aaaaa" + "...addde" + "...addde" + "...adeee" + "...adeee"
          + "...addde" + "...addde" + "...aaaaa")
AMMO = ("........" * 9 + "..e.e.e." + "..e.e.e." + "..aaaaaa" + "..abbbbb" + "..abcccc"
        + "..abbbbb" + "..aaaaaa")

IMP = ("........" + "....d..." + ".....aaa" + "....abbb" + "....bfeb" + "....bcaa" + ".dd.abdd"
       + "dabbbbcc" + "abbcbbcc" + "abacbabc" + "ab.abbbc" + "ab.aabbb" + "dd.abbab" + "...abb.."
       + "...aab.." + "..aaaa..")

ZOMBIE = ("........" + ".....aaa" + "....abbb" + "....abbb" + "....addd" + "....aeda" + "....addd"
          + "...aabbb" + "..abbbcb" + "..abcbbb" + ".aggabbb" + ".agaabbb" + "....abbb" + "....abb."
          + "....aab." + "...aaa..")

CACODEMON = ("...d...." + "...d.aaa" + "...aabbb" + "..abbbbb" + "..abbbcc" + ".abbbcdd" + ".abbbcdh"
             + ".abbbcdd" + ".abbbbcc" + ".abbbbbb" + ".abaaaaa" + ".abadada" + "..aeeeee" + "..abbaaa"
             + "...aabbb" + ".....aaa")

THEMES = [
    {
        "name": "CATACOMBS",
        "palette": "24140c 7a4524 a8683a e9dcb4 ff3010 ffe040 4f5f58 4cff3a ff7a10 fff3a0 8c877c",
        "monster": IMP,
        "colours": "1c0e0a 3a332c 8a2c1c 2a0e08 5c6370 35e0ff 5e5a52 1e7a32",
        "stats": "2,1.1,6",
    },
    {
        "name": "TECH BASE",
        "palette": "121812 4a5a2a 6f8040 d8b090 ff3010 ffe040 6a7680 4cff3a 40d0ff e0ffff 9aa4ac",
        "monster": ZOMBIE,
        "colours": "0c1218 262c30 4a5058 1a1e22 5c6370 35e0ff 6a6e72 1e7a32",
        "stats": "3,1.4,8",
    },
    {
        "name": "HELL",
        "palette": "1a0404 b0201a e0503a f4ecd8 600808 ffd040 5a4040 40ff60 ff5a00 ffe060 7a5a50",
        "monster": CACODEMON,
        "colours": "2a0402 3a1008 6a1a10 ff6020 4a2a2a ff4000 5a2a20 1e7a32",
        "stats": "5,.8,14",
    },
]


def pack(level: int) -> str:
    """The asset pack for a level (1-based); themes repeat, the widget scales difficulty by level."""
    t = THEMES[(level - 1) % len(THEMES)]
    parts = [t["palette"].replace(" ", ""), t["monster"], BARREL, TORCH, COLUMN, MEDKIT, AMMO,
             t["colours"].replace(" ", ","), t["stats"], t["name"]]
    for sprite in parts[1:7]:
        assert len(sprite) == 128, "a sprite must be 8x16 characters"
    s = "|".join(parts)
    assert len(s.encode()) <= 1024, f"level {level} pack is {len(s.encode())} bytes, max 1024"
    return s


if __name__ == "__main__":
    for lv in range(1, len(THEMES) + 1):
        print(lv, THEMES[(lv - 1) % len(THEMES)]["name"], len(pack(lv).encode()), "bytes")
