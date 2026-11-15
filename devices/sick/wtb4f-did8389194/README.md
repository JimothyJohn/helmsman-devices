> **Draft from documents.** No unit has been checked; every value here is the
> IODD's, read by `scripts/iodd-draft.py`. Which signal the switching wire
> carries without an IO-Link master is still to be read from the manual, with
> its page.

# SICK WTB4F_DID8389194

IODD identity: vendor 26 SICK AG, device 8389194;
IODD file V1.30612 (2021-10-14).
Switches without a master (SIO): yes.

## Variants

| product id | name | description |
| --- | --- | --- |
| 1222998 | WTB4FP-22161120A00 | Photoelectric proximity sensor |
| 1223017 | WTB4FP-1H161120A00 | Photoelectric proximity sensor |
| 1105505 | WTB4FP-32161120A00 | Photoelectric proximity sensor |
| 1123751 | WTB4FP-84161120A00 | Photoelectric proximity sensor |
| 1123757 | WTB4FP-6H161120A00 | Photoelectric proximity sensor |

## Connections

| connector | products | wires |
| --- | --- | --- |
| M8 | 1222998, 1105505 | 1: L+ (BN); 2: Other (WH); 3: L- (BU); 4: C/Q (BK) |
| M12-4 | 1123751 | 1: L+ (BN); 2: Other (WH); 3: L- (BU); 4: C/Q (BK) |
| Cable | 1223017, 1123757 | 1: L+ (BN); 2: Other (WH); 3: L- (BU); 4: C/Q (BK) |

## Signals, as the device names them over IO-Link

| dir | name | type | bits | values |
| --- | --- | --- | --- | --- |
| in | QL1 | bool | 0 |  |
| in | QL2 | bool | 1 |  |
| in | Current receive level (live) | uint | 2..15 |  |

## Settings and their factory values

| setting | index | factory value | choices |
| --- | --- | --- | --- |
| Teach-in channel | 58 | default Qint. = Qint.1 | default Qint. = Qint.1, Qint.1, Qint.2 |
| Qint.1 SP1 / SP2: SP2 sensing range | 60.2 | SP2 not used | SP2 not used |
| Qint.1 configuration: Switchpoint logic | 61.1 | Vendor specific | Vendor specific |
| Qint.1 configuration: Switchpoint mode | 61.2 | Vendor specific | Vendor specific |
| Qint.1 configuration: Switchpoint hysteresis | 61.3 | Autodefined hysteresis | Autodefined hysteresis |
| Qint.2 SP1 / SP2: SP2 sensing range | 62.2 | SP2 not used | SP2 not used |
| Qint.2 configuration: Switchpoint logic | 63.1 | Vendor specific | Vendor specific |
| Qint.2 configuration: Switchpoint mode | 63.2 | Vendor specific | Vendor specific |
| Qint.2 configuration: Switchpoint hysteresis | 63.3 | Autodefined hysteresis | Autodefined hysteresis |
| Physical input / output type configuration pin2 | 92 | Push/Pull | PNP, NPN, Push/Pull |
| Sender configuration | 97 | Sender active | Sender active, Sender not active |
| Pin 2 configuration | 121 | Switching signal QL1/ | Deactivated / no function, External input (Smart Task), Sender off, Teach-in, Switching signal QL2, Detection output Qint.1, Switching signal QL1, Switching signal QL1/ |
| Find me | 204 | Find me deactivated | Find me deactivated, Find me activated |
| Notification handling | 227 | All enabled | All enabled, All disabled, Events enabled, PD invalid flag disabled, Events disabled, PD invalid flag enabled |
| Logic 1 | 1083 | DIRECT | DIRECT, AND, OR |
| Logic 2 | 1084 | DIRECT | DIRECT, AND, OR |
| Timer 1 Mode | 1085 | deactivated | deactivated, T-on delay, T-off delay, T-on/T-off delay, Impulse (one shot) |
| Timer 2 Mode | 1086 | deactivated | deactivated, T-on delay, T-off delay, T-on/T-off delay, Impulse (one shot) |
| Inverter 1 | 1089 | not inverted | not inverted, inverted |
| Inverter 2 | 1090 | not inverted | not inverted, inverted |
| Inverter Ext. Input | 1093 | not inverted | not inverted, inverted |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| IODD SICK-WTB4F_DID8389194-20211014-IODD1.1.xml | `b90941d68a47a7b4…` | https://ioddfinder.io-link.com/api/vendors/26/iodds/12863/files/zip/rated |

Vendor files are not in this repository; download the IODD and check the hash.
