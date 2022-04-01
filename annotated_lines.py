nine = "751240100000800000000000003800000000"  # 512
eight = "751840100100800000000000001cffffff000019ffffffff"  # 256
seven = "75174010010080000000000a00ffffff000029ffffffff"  # 128
six = "75174010010080000000000200ffffff000031ffffffff"  # 64
five = "7515408000008000000000ffffff000035ffffffff"  # 32
four = "751340200000800000ffffff000037ffffffff"  # 16
three = "7512401000008000ffffff000038ffffffff"  # 8
two = "751240100000800fffffff000038ffffffff"  # 4
one = "751240100000803fffffff000038ffffffff"  # 2
zero = "751240100000807fffffff000038ffffffff"  # 1
none = "75 12 40 10000080ffffffff000038ffffffff"  # 0

###########################################################################################
# From the 25px checkerboard
# 10 25px black lines +1 12px line
# bbwwbbwwbbwwbbwwbbwwbbwwbbwwbbwwbbwwbbwwb
# bbwwbbwwbbwwbbwwb| bwwbbwwbbwwbbwwbbwwbbwwb
x = "00 000088 0000007fffffc000001ffffff0000007fffffc000001ffffff 000070 0321 fffff00000008000"
#                    ----  -------     -------      -------     -------
#                     136     1           2            3           4
#
#
# 1 13px line + 10 25px black lines
x2 = "00 000084 0007fffffc000001ffffff0000007fffffc000001ffffff0 000080 0322 ff000000"
#                   ------ ----     -------      -------     -------
#                    132    5          6            7           8
#                      (extra byte?)

# wwbbwwbbwwbbwwbbwwbbwwbbwwbbwwbbwwbbwwbbw
# wwbbwwbbwwbbwwbbw| wbbwwbbwwbbwwbbwwbbwwbbw
y = "0000 0088 ffffff8000003fffffe000000ffffff8000003fffffe000000 ffff70 0321 00000f 00000080ff"
#                                -------     -------      -------     -------
#                                   1           2            3           4
# It appears that after some prefixing there are 54byte (216 bits) that are just a bitmap. i.e.  1to1 with the
# display.   However, this leaves 74 bytes (296 bits) unaccounted for.  But this is a repeating pattern.
# It must be getting compressed.

# The lines above are cut symmetrically.  Sort of.  Cut at the halfway point for a non-repeating pattern.
#
# This is a dataline with just 4 25px lines on it.   It tells us that the 4 0s at the end of the datablock are
#   NOT part of the data.  This first one already has four lines drawn.
four_25px = "0000 0082 0000007fffffc000001ffffff0000007fffffc000001ffffff  000023 ffffffff"
#                         -------     -------      -------     -------

# This dataline has the same 4 25px lines but then another that is 16px long.   This runs out of the original pattern
#  fit.  The prefix number is 0x16 (22) larger.  The bitmap datablock is the same as the above example.    
four_25px_ = "0000 0098 0000007fffffc000001ffffff0000007fffffc000001ffffff  000001 0000001effff00000080ffff"
#                          -------     -------      -------     -------
###########################################################################################
cleaned______512 = "1000 0080 00000000                  000038 00000000"  # 512 0x200
cleaned______256 = "1001 0080 00000000 00001c ffffff    000019 ffffffff"  # 256 0x100
cleaned______128 = "1001 0080 00000000 0a00   ffffff    000029 ffffffff"  # 128  0x80
cleaned_______92 = "1002 0080 00000000 0500   0fffffff  00002d ffffffff"  # 92   0x5C
cleaned_______88 = "1001 0080 00000000 0500   ffffff    00002e ffffffff"  # 88   0x58
cleaned_______84 = "1002 0080 00000000 0400   0fffffff  00002e ffffffff"  # 84   0x54
cleaned_______80 = "1001 0080 00000000 0400   ffffff    00002f ffffffff"  # 80   0x50
cleaned_______76 = "1002 0080 00000000 0300   0fffffff  00002f ffffffff"  # 76   0x4C
cleaned_______72 = "1001 0080 00000000 0300   ffffff    000030 ffffffff"  # 72   0x48
cleaned_______70 = "1002 0080 00000000 0200   03ffffff  000030 ffffffff"  # 70   0x46
cleaned_______69 = "1002 0080 00000000 0200   07ffffff  000030 ffffffff"  # 69   0x45
cleaned_______68 = "1002 0080 00000000 0200   0fffffff  000030 ffffffff"  # 68   0x44
cleaned_______67 = "1002 0080 00000000 0200   1fffffff  000030 ffffffff"  # 67   0x43
cleaned_______66 = "1002 0080 00000000 0200   3fffffff  000030 ffffffff"  # 66   0x42
cleaned_______65 = "1002 0080 00000000 0200   7fffffff  000030 ffffffff"  # 65   0x41
cleaned_______64 = "1001 0080 00000000 0200   ffffff    000031 ffffffff"  # 64   0x40
cleaned_______63 = "0008 0080 0000000000000001ffffff    000031 ffffffff"  # 63   0x3F # Bitmapped.  No compression
cleaned_______62 = "0008 0080 0000000000000003ffffff    000031 ffffffff"  # 62   0x3E
cleaned_______61 = "0008 0080 0000000000000007ffffff    000031 ffffffff"  # 61   0x3D
cleaned_______60 = "0008 0080 000000000000000fffffff    000031 ffffffff"  # 60   0x3C # Bitmapped.  No compression
cleaned_______56 = "0004 0080 00000000000000ffffff      000032 ffffffff"  # 56   0x38
cleaned_______52 = "0004 0080 0000000000000fffffff      000032 ffffffff"  # 52   0x34
cleaned_______48 = "0002 0080 000000000000ffffff        000033 ffffffff"  # 48   0x30
cleaned_______44 = "0002 0080 00000000000fffffff        000033 ffffffff"  # 44   0x2C
cleaned_______43 = "0002 0080 00000000001fffffff        000033 ffffffff"  # 43   0x2B
cleaned_______42 = "0002 0080 00000000003fffffff        000033 ffffffff"  # 42   0x2A
cleaned_______41 = "0002 0080 00000000007fffffff        000033 ffffffff"  # 41   0x29
cleaned_______40 = "0001 0080 0000000000ffffff          000034 ffffffff"  # 40   0x28
cleaned_______39 = "0001 0080 0000000001ffffff          000034 ffffffff"  # 39   0x27
cleaned_______38 = "0001 0080 0000000003ffffff          000034 ffffffff"  # 38   0x26
cleaned_______37 = "0001 0080 0000000007ffffff          000034 ffffffff"  # 37   0x25
cleaned_______36 = "0001 0080 000000000fffffff          000034 ffffffff"  # 36   0x24
cleaned_______32 = "8000 0080 00000000ffffff            000035 ffffffff"  # 32   0x20
cleaned_______28 = "8000 0080 0000000fffffff            000035 ffffffff"  # 28   0x1C
cleaned_______24 = "4000 0080 000000ffffff              000036 ffffffff"  # 24   0x18
cleaned_______20 = "4000 0080 00000fffffff              000036 ffffffff"  # 20   0x14
cleaned_______16 = "2000 0080 0000ffffff                000037 ffffffff"  # 16   0x10
cleaned_______12 = "2000 0080 000fffffff                000037 ffffffff"  # 12   0x0C
cleaned________8 = "1000 0080 00ffffff                  000038 ffffffff"  # 8    0x08
cleaned________4 = "1000 0080 0fffffff                  000038 ffffffff"  # 4    0x04
cleaned________2 = "1000 0080 3fffffff                  000038 ffffffff"  # 2    0x02
cleaned________1 = "1000 0080 7fffffff                  000038 ffffffff"  # 1    0x01
cleaned_______1_ = "1000 0080 bfffffff                  000038 ffffffff"  # 1 (over 1)
cleaned________0 = "1000 0080 ffffffff                  000038 ffffffff"  # 0    0x00

negative____00_8 = "1000 0080 ffffffff                  000038 ffffff00"  # -8
negative___00_16 = "1000 0080 ffffffff                  000038 ffff0000"  # -16
negative___00_32 = "1000 0080 ffffffff                  000038 00000000"  # -32
negative___00_48 = "1000 0080 ffffffff                  000036 000000000000"  # -48
negative___00_64 = "1000 0080 ffffffff                  000034 0000000000000000"  # -64

# Byte Length of first chunk  (Logical Byte Length)  There are some weird exceptions.
#   The 68px line should have (68/8) 8.5bytes of 0s and the rest (3-4) Fs.  17 zeros + 7 Fs = 24/2 -> 12 Bytes
#       BUT it leads with 1002 which should be 13 bytes
# 1000 = 4 = 0x04
# 2000 = 5 = 0x05
# 4000 = 6 = 0x06
# 8000 = 7 = 0x07
# 0001 = 8 = 0x08
# 0002 = 9 = 0x09
# 0004 = 10 = 0x0A
# 0008 = 11 = 0x0B
# 1001 = 12 = 0x0C  # ACTUALLY 9 but likely expands to 12 with decompression
# 1002 = 13 = 0x0D

# UPDATE The first part of the prefix is Big endian!  AND it is likely a bitmask sort
#  of thing.   Looking at the chart below you can see them rearranged as little endian
#  values and the 1 is the "stop bit" all the zeros that follow determine how long the
#  first segment is.   i.e. 16 is 4 zeros,  32 is 5, etc.
# Where it gets interesting is the >0800.   Multiple 1s seem to indicate where the
#  breaks are for compression.  I haven't figured this part out yet.

# 0010 = 16 = 0000 0001 0000
# 0020 = 32 = 0000 0010 0000
# 0040 = 64 = 0000 0100 0000
# 0080 = 128 = 0000 1000 0000
# 0100 = 256 = 0001 0000 0000
# 0200 = 512 = 0010 0000 0000
# 0400 = 1024 = 0100 0000 0000
# 0800 = 2048 = 1000 0000 0000
# 0110 = 272 = 0001 0001 0000  # <- first you take 4bytes (8chars) and then 3 from the end of the segment.  The middle is the compression?
# 0210 = 528 = 0010 0001 0000

# It gets better.  this is actually a 4 byte value that always starts with 8.
# This `1000 0080`  turns into this `80000010` which is this bit pattern:
#       `1000 0000 0000 0000 0000 0000 0001 0000`
# This matches the lines we see that start with this value but in reverse.  The 4 0s at the end are the
#   first values (4 bytes long).  For example on cleaned________2 this is `3f ff ff ff` the `1` lets you
#   know there is a break and then there you fill in 26 bytes in the remaining.
# I can now divide up simple lines.   This bit pattern gets more complex though.  For example
#       one of the values is: 0x80022880
#       Which translates to a bit pattern of:
#           `1000 0000 0000 0010 0010 1000 1000 0000`
#            ^                ^    ^  ^    ^
#  Or this one:  0x80180000
#   Which translates to a bit pattern with two 1s side by side
#       `1000 0000 0001 1000 0000 0000 0000 0000`
#        ^            ^ ^


# ALSO The bit pattern seems too short.
# 32 bit string (4 bytes)
# each bit represents one byte
# each byte is one chr
# each chr is 4 bits
#
# SO:
# 32 * 2 * 4 = 256
# or 32 * 8 = 256
# This is only half of the logical data for the line.  It *should* be 512.




neg_pos__64_00_64 = "1001 0080 000000000200ffffff    00002d 0000000000000000"  # 64 // -64
# 0x2d ->   -64 has 0x34   64 has 0x31
# 0x38 - 0x34 = 0x4 (4 additional bytes on right side)
# 0x38 - 0x31 = 0x7 (5 additional bytes on left side)
# 0x38 - 0x4 - 0x7 = 0x2d

one_px_at_256 = "10 020080 ffffffff              00001c 7fffffff   000018 ffffffff"

# 1 is white
# 0 is black
# You can see the bit move across unadulterated in the first 32bit block

# The block grows.   And by doing so subtracts from the second block.
# I should walk these same lines backwards on a data line and try and combine front and back

# TODO NEXT
# Less than 64 bits appears to be uncompressed.   I should experiment with this.
#   Generate a random bit string and see what happens

# I'm ALMOST to the point where I can start focusing on the compression.   I almost know how the lines are constructed

# TODO NEXT
# Look at all the available data.   Get all the different byte length pieces.  Then see
# what everyone else has instead of 0080
#  See if we can determine that midpoint number for an arbitrary line.  If we can then we start looking at data.
#  See if the

# TODO NEXT
# Values >256 are very interesting. I think doing byte leaps might be illuminating.   Do 257-260 but then 264, 272, 280, 288.

# TODO NEXT
# Can I move an 8px line through these numbers with the same change?
