Setup instructions:

Requirements:
Android Phone
ADB tools

Enable Bluetooth HCI Snoop


# Misc Notes
Register for the app.   Google translate on another phone is really helpful.   This login will get you into the Template editor as well

Nothing seems very secure at all.   It appears that I can see and read all other tags (but not write to them without being in BT range).  SQL injections look like a strong possibility.


# TODO: Insert adding tag to app instructions


Some important links:

# Original app location
https://www.gicisky.net/app/ble-app-release-v3.0.13.apk
https://www.gicisky.net/app/ble-app-release-v3.0.24.apk  # <- much more responsive version of the app

# Template Editor
http://a.picksmart.cn:8081



4.2 Screen is 400x300


Forward Slashes (/) are illegal in template names but it doesn't stop you from putting them in

235 lines are Black & White
235 lines are Red
Lines are 512px long.  This requires 234.375 lines of data.
The last line will be 192 pixels long. Confirmed
The lines don't appear to be linked in any way.

Compression (or whatever is happening) is only happening on a per line basis.

### Sample Line (From pathological_dataline.hex)

This is an 1px x 512px line alternating between black and white.  This covers a 400px line on the screen and then 112px of the next line.  
751540500000805555555500002d54080055555555

Annotating what I know:
```
75 15 40 50 00 00 80 55 55 55 55 00 00 2d 54 08 00 55 55 55 55
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
✅ ✅ ✅ ✅ ✅       ✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅
```

**1** - Start of Line code  

**2** - Line length in bytes (Each character is 1/2 of a byte.  Includes Start of line characters i.e. 0x15 -> 21bytes -> 42 characters)  

**3** - How many data bytes on this line 0x40 (64 for 64 * 8 = 512) on most lines.  0x18 on the last line of the section (24 for 24*8 = 192)

**4-5** Logical byte length of the first segment.  Sort of.  Still hashing this out.

**6-7** ???? Logical Byte length of the second Segment?????

**8-11** - Bit pattern.   In this case 55 -> 0101 0101.  This is the same pattern as our line.  BUT our line is 512bits and this is only 32bits.  This data length is variable and encompasses 256bits  

**12-14** This seems to be the center padding for the two pieces of data.  Full padding is 0x38.  Both sides decrement it.  0x37 means one more byte of data was added to either bit pattern.   This isn't entirely linear.     

**15-21** Bit pattern.   Same as above.  This is another 32 bits but encompasses 256bits.  Length is variable.


Other notes:  
16:17 and 6:7 are the same here but mirrored. 


# TODO
Make a pathological data line that is 256bits, 128 and 64, 32, 16, 8, 4 (maybe even 384)  
Make a black line that is 256, 128, 64, 32, 16  
Try some random noise? Fibonacci maybe  
Try some other patterns (every 2, every 3, etc)  



##### Max length of GH markdown color line is 339 (no including markers) 