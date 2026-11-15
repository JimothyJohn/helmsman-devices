> **Draft from documents.** No unit has been checked; every value here is the
> IODD's, read by `scripts/iodd-draft.py`. Which signal the switching wire
> carries without an IO-Link master is still to be read from the manual, with
> its page.

# ifm O5D100/O5D102/O5D150/O5D152/O5D159

IODD identity: vendor 310 ifm electronic gmbh, device 372;
IODD file V1.0.8 (2021-05-26).
Switches without a master (SIO): yes.

## Variants

| product id | name | description |
| --- | --- | --- |
| O5D100 | O5D100 | Optical distance sensor. Visible laser light, protection class 2 laser. Connection: 2 switching outputs normally open /  |
| O5D102 | O5D102 | Optical distance sensor. Visible laser light, protection class 2 laser. Connection: 2 switching outputs normally open /  |
| O5D150 | O5D150 | Optical distance sensor. Visible laser light, protection class 1 laser. Connection: 2 switching outputs normally open /  |
| O5D152 | O5D152 | Optical distance sensor. Visible laser light, protection class 1 laser. Connection: 2 switching outputs normally open /  |
| O5D159 | O5D159 | Optical distance sensor. Visible laser light, protection class 1 laser. Connection: 2 switching outputs normally open /  |

## Connections

| connector | products | wires |
| --- | --- | --- |
| M12-4 | O5D100 | 1: L+ (BN); 2: Other (WH); 3: L- (BU); 4: C/Q (BK) |
| M12-4 | O5D150 | 1: L+ (BN); 2: Other (WH); 3: L- (BU); 4: C/Q (BK) |
| M12-4 | O5D159 | 1: L+ (BN); 2: Other (WH); 3: L- (BU); 4: C/Q (BK) |
| M12-4 | O5D102 | 1: L+ (BN); 2: Other (WH); 3: L- (BU); 4: C/Q (BK) |
| M12-4 | O5D152 | 1: L+ (BN); 2: Other (WH); 3: L- (BU); 4: C/Q (BK) |

## Signals, as the device names them over IO-Link

| dir | name | type | bits | values |
| --- | --- | --- | --- | --- |
| in | Distance | uint | 4..15 |  |
| in | Switch state [OUT1] | bool | 0 | false = Inactive, true = Active |

## Settings and their factory values

| setting | index | factory value | choices |
| --- | --- | --- | --- |
| SP: Switch Point 2 | 60.2 | (Not used) | (Not used) |
| SP: Switchpoint Logic | 61.1 | Closing Contact | Closing Contact, Break Contact |
| SP: Switchpoint Mode | 61.2 | Single Point | Single Point |
| SP: Switchpoint Hysteresis | 61.3 | (Not used) | (Not used) |
| Laser | 80 | Laser on | Laser off, Laser on |
| Display | 96 | Display on | Display off, Display on, Display rotated |
| Keylock | 100 | Unlocked | Locked, Unlocked |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| IODD ifm-000174-20210526-IODD1.1.xml | `1c71ca9fb45ae4d4…` | https://ioddfinder.io-link.com/api/vendors/310/iodds/11838/files/zip/rated |

Vendor files are not in this repository; download the IODD and check the hash.
