> **Draft from documents.** No unit has been checked; every value here is the
> IODD's, read by `scripts/iodd-draft.py`. Which signal the switching wire
> carries without an IO-Link master is still to be read from the manual, with
> its page.

# ifm IF6123, IF6124, IG6615, IG6616, II5973, II5974, IM5172, IM5173

IODD identity: vendor 310 ifm electronic gmbh, device 791;
IODD file V1.3.14.18 (2017-07-07).
Switches without a master (SIO): yes.

## Variants

| product id | name | description |
| --- | --- | --- |
| IF6123 | IF6123 | Inductive sensor |
| IF6124 | IF6124 | Inductive sensor |
| IG6615 | IG6615 | Inductive sensor |
| IG6616 | IG6616 | Inductive sensor |
| II5973 | II5973 | Inductive sensor |
| II5974 | II5974 | Inductive sensor |
| IM5172 | IM5172 | Inductive sensor |
| IM5173 | IM5173 | Inductive sensor |

## Connections

| connector | products | wires |
| --- | --- | --- |
| Other | IF6123 |  |
| Other | IF6124 |  |
| Other | IG6615 |  |
| Other | IG6616 |  |
| Other | II5973 |  |
| Other | II5974 |  |
| Other | IM5172 |  |
| Other | IM5173 |  |

## Signals, as the device names them over IO-Link

| dir | name | type | bits | values |
| --- | --- | --- | --- | --- |
| in | PDV1 | int | 2..15 | -8184 = UL, 8184 = OL |
| in | SSC2 | bool | 1 | false = inactive, true = active |
| in | SSC1 | bool | 0 | false = inactive, true = active |

## Settings and their factory values

| setting | index | factory value | choices |
| --- | --- | --- | --- |
| TI Select | 58 | SSC1 | SSC1, SSC2 |
| SSC1 Config: Logic | 61.1 | High active | High active, Low active |
| SSC1 Config: Mode | 61.2 | Single point | Single point, Window, Two point |
| SSC2 Config: Logic | 63.1 | High active | High active, Low active |
| SSC2 Config: Mode | 63.2 | Single point | Single point, Window, Two point |
| P-n | 500 | PnP | PnP, nPn |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| IODD ifm-000317-20170707-IODD1.1.xml | `4de29691d78892a0…` | https://ioddfinder.io-link.com/api/vendors/310/iodds/4071/files/zip/rated |

Vendor files are not in this repository; download the IODD and check the hash.
