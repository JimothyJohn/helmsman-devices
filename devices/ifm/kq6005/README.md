> **Draft from documents.** No unit has been checked; every value here is the
> IODD's, read by `scripts/iodd-draft.py`. Which signal the switching wire
> carries without an IO-Link master is still to be read from the manual, with
> its page.

# ifm KQxxxx

IODD identity: vendor 310 ifm electronic gmbh, device 371;
IODD file V1.0.26 (2026-04-20).
Switches without a master (SIO): yes.

## Variants

| product id | name | description |
| --- | --- | --- |
| KQ6001 | KQ6001 | Capacitive sensor. Connection: 1x open collector with automatic load detection (DC PNP or DC NPN); PVC cable |
| KQ6002 | KQ6002 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |
| KQ6003 | KQ6003 | Capacitive sensor. Connection: 1x open collector with automatic load detection (DC PNP or DC NPN); PVC cable |
| KQ6004 | KQ6004 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |
| KQ6005 | KQ6005 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |
| KQ6006 | KQ6006 | Capacitive sensor. Connection: 1x open collector DC NPN; PVC cable |
| KQ6007 | KQ6007 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |
| KQ6008 | KQ6008 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |
| KQ6010 | KQ6010 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |
| KQ6015 | KQ6015 | Capacitive sensor. Connection: 1x open collector DC NPN; PVC cable |
| KQ6016 | KQ6016 | Capacitive sensor. Connection: 1x open collector DC NPN; PVC cable |
| KQ5100 | KQ5100 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |
| KQ5101 | KQ5101 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |
| KQ5102 | KQ5102 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |
| KQ5105 | KQ5105 | Capacitive sensor. Connection: 1x open collector DC NPN; PVC cable |
| KQ5108 | KQ5108 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |
| KQ5109 | KQ5109 | Capacitive sensor. Connection: 1x open collector DC NPN; PVC cable |
| KQ5110 | KQ5110 | Capacitive sensor. Connection: 1x open collector DC NPN; PVC cable |
| KQ5111 | KQ5111 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |
| KQ5112 | KQ5112 | Capacitive sensor. Connection: 1x open collector DC NPN; PVC cable |
| KQ5113 | KQ5113 | Capacitive sensor. Connection: 1x open collector DC NPN; PVC cable |
| KQ5114 | KQ5114 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |
| KQ5115 | KQ5115 | Capacitive sensor. Connection: 1x open collector DC PNP; PVC cable |

## Connections

| connector | products | wires |
| --- | --- | --- |
| Cable | KQ6001 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Cable | KQ6002 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Other | KQ6003 |  |
| Other | KQ6004 |  |
| Other | KQ6005 |  |
| Cable | KQ6006 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Cable | KQ6007 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Other | KQ6008 |  |
| Other | KQ6010 |  |
| Cable | KQ6015 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Cable | KQ6016 |  |
| Cable | KQ5100 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Other | KQ5101 |  |
| Other | KQ5102 |  |
| Cable | KQ5105 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Other | KQ5108 |  |
| Cable | KQ5109 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Cable | KQ5110 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Cable | KQ5111 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Cable | KQ5112 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Cable | KQ5113 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Cable | KQ5114 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |
| Cable | KQ5115 | 1: L+ (BN); 3: L- (BU); 4: C/Q (BK) |

## Signals, as the device names them over IO-Link

| dir | name | type | bits | values |
| --- | --- | --- | --- | --- |
| in | Process value | int | 4..15 |  |
| in | Switch state [OUT1] | bool | 0 | false = inactive, true = active |

## Settings and their factory values

| setting | index | factory value | choices |
| --- | --- | --- | --- |
| TeachIn Channel | 58 | BDC1 | BDC1 |
| SP: Switch Point 2 | 60.2 | (not used) | (not used) |
| SP: Switchpoint Mode | 61.2 | Single Point | Single Point |
| Keylock | 100 | unlocked | locked, unlocked |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| IODD ifm-000173-20260420-IODD1.1.xml | `58a21e485078ac3c…` | https://ioddfinder.io-link.com/api/vendors/310/iodds/25170/files/zip/rated |

Vendor files are not in this repository; download the IODD and check the hash.
