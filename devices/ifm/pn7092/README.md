> **Draft from documents.** No unit has been checked; every value here is the
> IODD's, read by `scripts/iodd-draft.py`. Which signal the switching wire
> carries without an IO-Link master is still to be read from the manual, with
> its page.

# ifm (PN7072, PN7092, PN7572, PN7592) Status B

IODD identity: vendor 310 ifm electronic gmbh, device 599;
IODD file V1.3.54.803448 (2019-03-07).
Switches without a master (SIO): yes.

## Variants

| product id | name | description |
| --- | --- | --- |
| PN7072 | PN7072 Status B | Electronic pressure sensor, 0.0...100.0 bar, ISO228 - G1/4I |
| PN7092 | PN7092 Status B | Electronic pressure sensor, 0.0...100.0 bar, ISO228 - G1/4I |
| PN7572 | PN7572 Status B | Electronic pressure sensor, 0.0...100.0 bar, ISO228 - G1/4A |
| PN7592 | PN7592 Status B | Electronic pressure sensor, 0.0...100.0 bar, ISO228 - G1/4A |

## Connections

| connector | products | wires |
| --- | --- | --- |
| M12-4 | PN7072 | 1: L+ (BN); 2: Other (WH); 3: L- (BU); 4: C/Q (BK) |
| M12-4 | PN7092 | 1: L+ (BN); 2: Other (WH); 3: L- (BU); 4: C/Q (BK) |
| M12-4 | PN7572 | 1: L+ (BN); 2: Other (WH); 3: L- (BU); 4: C/Q (BK) |
| M12-4 | PN7592 | 1: L+ (BN); 2: Other (WH); 3: L- (BU); 4: C/Q (BK) |

## Signals, as the device names them over IO-Link

| dir | name | type | bits | values |
| --- | --- | --- | --- | --- |
| in | Pressure | int | 16..31 | 32760 = OL, 32764 = NoData |
| in | Device status | uint | 4..7 | 0 = Device is OK, 1 = Maintenance required, 2 = Out of specification, 3 = Functional check, 4 = Failure |
| in | OUT2 | bool | 1 | false = OFF, true = On |
| in | OUT1 | bool | 0 | false = OFF, true = On |

## Settings and their factory values

| setting | index | factory value | choices |
| --- | --- | --- | --- |
| P-n | 500 | PnP | PnP, nPn |
| Loc | 550 | uLoc | Loc, uLoc |
| uni | 551 | bar | MPa, bar, psi |
| diS: Display On / OFF | 552.1 | On | On, OFF |
| diS: Display orientation | 552.2 | Not rotated | Not rotated, Rotated 180° |
| diS: Update rate | 552.3 | d2 / medium | d1 / fast, d2 / medium, d3 / slow |
| coLr | 554 | rEd / Displayed value red | rEd / Displayed value red, GrEn / Displayed value green, r1ou / Displayed value red when OUT1 switches, G1ou / Displayed value green when OUT1 switches, r2ou / Displayed value red when OUT2 switches, G2ou / Displayed value green when OUT2 switches, r-12 / Displayed value red when the measured value is inside the limits of OUT1 and OUT2, G-12 / Displayed value green when the measured value is inside the limits of OUT1 and OUT2, r-cF / Displayed value red when the measured value is inside the limits of [cFL] and [cFH], G-cF / Displayed value green when the measured value is inside the limits of [cFL] and [cFH] |
| ou1 | 580 | Hno / Hysteresis fct normally open | Hno / Hysteresis fct normally open, Hnc / Hysteresis fct normally closed, Fno / Window fct normally open, Fnc / Window fct normally closed, OFF / Output Off |
| ou2 | 590 | Hno / Hysteresis fct normally open | Hno / Hysteresis fct normally open, Hnc / Hysteresis fct normally closed, Fno / Window fct normally open, Fnc / Window fct normally closed, OFF / Output Off |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| IODD ifm-000257-20190307-IODD1.1.xml | `e3f88b9148e5defd…` | https://ioddfinder.io-link.com/api/vendors/310/iodds/9066/files/zip/rated |

Vendor files are not in this repository; download the IODD and check the hash.
