# Catalog

<!-- Written by scripts/build-index.py from every device.toml. Do not edit: run the script. -->

176 devices in 12 categories.
Pick a category, pick a row, then
`python3 -I scripts/use.py <folder>` prints what goes into a Helmsman project
([AGENTS.md](AGENTS.md), Using a device). The same list from a shell:
`python3 -I scripts/find.py [category] [words]`.

| category | devices | what is in it |
| --- | --- | --- |
| [I/O blocks (on the machine)](#io-block) | 25 | Fixed channels in one sealed housing with M12 ports. |
| [I/O modules (in the cabinet)](#panel-io) | 35 | Fixed channels in one module with terminals, on a DIN rail. |
| [Modular I/O couplers](#io-coupler) | 25 | The head of a row of I/O slices or modules; the channels depend on what is fitted. |
| [IO-Link masters](#iolink-master) | 15 | Ports that speak IO-Link to sensors and actuators. |
| [Valve terminals](#valve-terminal) | 17 | Pneumatic valve manifolds and their bus nodes; an output switches a solenoid. |
| [Drives](#drive) | 32 | Frequency inverters, servo drives and their network option cards. |
| [Motor starters and protection](#motor-starter) | 5 | Starters, soft starters and motor management relays. |
| [Power meters](#power-meter) | 3 | Meters that give voltage, current, power and energy. |
| [Vision sensors and code readers](#vision) | 11 | Cameras that inspect, and readers of 1D and 2D codes. |
| [Robots](#robot) | 1 | Robot controllers, as a device another controller reads and commands. |
| [Controllers](#controller) | 2 | Programmable controllers that also answer as a device. |
| [Sensors and actuators on a digital channel](#sensor) | 5 | Wired to a point of an I/O block, not on the network; described from the IODD. |

In each table, **to use it** is what the folder gives, best first: a `profile`
(channels by name, the box picks the protocol), a `map` (I/O map lines to copy),
an `EDS connection` (the assembly instances and sizes of the vendor's file),
a `record` (a wired sensor's signals), and the number of documented points.
**checked** is the date a unit confirmed the entry; `documents` means none has.

<a name="io-block"></a>

## I/O blocks (on the machine)

Fixed channels in one sealed housing with M12 ports. `find.py io-block`

| model | vendor | speaks | channels | to use it | checked |
| --- | --- | --- | --- | --- | --- |
| [BNI EIP-104-105-Z015](devices/balluff/bni-eip-104-105-z015/) | Balluff | EtherNet/IP | 8 M12 ports, 16 inputs | EDS connection, 4 points | documents |
| [BNI EIP-202-105-Z015](devices/balluff/bni-eip-202-105-z015/) | Balluff | EtherNet/IP | 8 M12 ports, 8 outputs (pin 4, 2 A each) | EDS connection, 6 points | documents |
| [BNI EIP-302-105-Z015](devices/balluff/bni-eip-302-105-z015/) | Balluff | EtherNet/IP | 8 M12 ports, 16 channels (pins 2 and 4 each input or 2 A output) | EDS connection, 6 points | documents |
| [IMPACT67 E DI16](devices/murrelektronik/impact67-e-di16/) | Murrelektronik | EtherNet/IP | 16 DI (8 on pin 4, 8 on pin 2 of 8 M12 ports) | profile, map, EDS connection | documents |
| [IMPACT67 E DI8 DO8](devices/murrelektronik/impact67-e-di8-do8/) | Murrelektronik | EtherNet/IP | 8 DI, 8 DO (2 A each) | profile, map, EDS connection | documents |
| [IMPACT67 E DIO8 (DIO8)](devices/murrelektronik/impact67-e-dio8-dio8/) | Murrelektronik | EtherNet/IP | 16 DIO (pin 4 and pin 2 of 8 M12 ports, each an input or an output, 1.6 A) | profile, map, EDS connection | 2026-11-16 |
| [IMPACT67 E DO16](devices/murrelektronik/impact67-e-do16/) | Murrelektronik | EtherNet/IP | 16 DO (0.5 A each) | profile, map, EDS connection | documents |
| [IMPACT67 E DO8](devices/murrelektronik/impact67-e-do8/) | Murrelektronik | EtherNet/IP | 8 DO (2 A each) | profile, map, EDS connection | documents |
| [ICE1-8DI8DO-G60L-V1D](devices/pepperl-fuchs/ice1-8di8do-g60l-v1d/) | Pepperl+Fuchs | EtherNet/IP |  | EDS connection | documents |
| [1732E-16CFGM12R](devices/rockwell-automation/1732e-16cfgm12r/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [1732E-8X8M12DR](devices/rockwell-automation/1732e-8x8m12dr/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [1732E-IB16M12R](devices/rockwell-automation/1732e-ib16m12r/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [1732E-OB16M12R](devices/rockwell-automation/1732e-ob16m12r/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S1-4DIP-4DOP](devices/turck/tben-s1-4dip-4dop/) | Turck | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S1-4DXP](devices/turck/tben-s1-4dxp/) | Turck | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S1-8DIP](devices/turck/tben-s1-8dip/) | Turck | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S1-8DIP-D](devices/turck/tben-s1-8dip-d/) | Turck | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S1-8DOP](devices/turck/tben-s1-8dop/) | Turck | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S1-8DXP](devices/turck/tben-s1-8dxp/) | Turck | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S2-2COM-4DXP](devices/turck/tben-s2-2com-4dxp/) | Turck | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S2-2RFID-4DXP](devices/turck/tben-s2-2rfid-4dxp/) | Turck | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S2-4AI](devices/turck/tben-s2-4ai/) | Turck | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S2-4AO](devices/turck/tben-s2-4ao/) | Turck | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S2-8DIP](devices/turck/tben-s2-8dip/) | Turck | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S2-8DXP](devices/turck/tben-s2-8dxp/) | Turck | EtherNet/IP |  | EDS connection | documents |

<a name="panel-io"></a>

## I/O modules (in the cabinet)

Fixed channels in one module with terminals, on a DIN rail. `find.py panel-io`

| model | vendor | speaks | channels | to use it | checked |
| --- | --- | --- | --- | --- | --- |
| [XT1111-000](devices/acromag/xt1111-000/) | Acromag | Modbus TCP | 16 DI (active-low), 16 DO (low-side, sinking) | 4 points | documents |
| [XT1121-000](devices/acromag/xt1121-000/) | Acromag | Modbus TCP | 16 DI (active-high), 16 DO (high-side, sourcing) | 4 points | documents |
| [ADAM-6015](devices/advantech/adam-6015/) | Advantech | Modbus TCP | 7 RTD AI | 8 points | documents |
| [ADAM-6017](devices/advantech/adam-6017/) | Advantech | Modbus TCP | 8 AI, 2 DO | 9 points | documents |
| [ADAM-6018](devices/advantech/adam-6018/) | Advantech | Modbus TCP | 8 TC AI, 8 DO | 5 points | documents |
| [ADAM-6024](devices/advantech/adam-6024/) | Advantech | Modbus TCP | 6 AI, 2 AO, 2 DI, 2 DO | 8 points | documents |
| [ADAM-6050](devices/advantech/adam-6050/) | Advantech | Modbus TCP | 12 DI, 6 DO (isolated) | 5 points | documents |
| [ADAM-6052](devices/advantech/adam-6052/) | Advantech | Modbus TCP | 8 DI, 8 DO (source type) | 4 points | documents |
| [ADAM-6060](devices/advantech/adam-6060/) | Advantech | Modbus TCP | 6 DI, 6 relay (form A) | 4 points | documents |
| [ADAM-6066](devices/advantech/adam-6066/) | Advantech | Modbus TCP | 6 DI, 6 relay DO | 5 points | documents |
| [ADAM-6250](devices/advantech/adam-6250/) | Advantech | Modbus TCP | 8 DI, 7 DO (sink) | 5 points | documents |
| [ADAM-6251](devices/advantech/adam-6251/) | Advantech | Modbus TCP | 16 DI | 4 points | documents |
| [ADAM-6256](devices/advantech/adam-6256/) | Advantech | Modbus TCP | 16 DO (sink) | 3 points | documents |
| [ADAM-6260](devices/advantech/adam-6260/) | Advantech | Modbus TCP | 6 relay DO (5 Form C, 1 Form A) | 3 points | documents |
| [ED-538](devices/brainboxes/ed-538/) | Brainboxes | Modbus TCP | 8 DI, 4 DO | 4 points | documents |
| [ED-588](devices/brainboxes/ed-588/) | Brainboxes | Modbus TCP | 8 DI, 8 DO | 4 points | documents |
| [ioLogik E1210](devices/moxa/iologik-e1210/) | Moxa | Modbus TCP | 16 DI | profile, map, 2 points | documents |
| [ioLogik E1211](devices/moxa/iologik-e1211/) | Moxa | Modbus TCP | 16 DO | profile, map, 1 point | documents |
| [ioLogik E1212](devices/moxa/iologik-e1212/) | Moxa | EtherNet/IP, Modbus TCP | 8 DI, 8 DIO | profile, map, EDS connection, 3 points | documents |
| [ioLogik E1213](devices/moxa/iologik-e1213/) | Moxa | EtherNet/IP, Modbus TCP | 8 DI, 4 DO, 4 DIO (source type) | profile, map, EDS connection, 3 points | 2026-11-02 |
| [ioLogik E1214](devices/moxa/iologik-e1214/) | Moxa | Modbus TCP | 6 DI, 6 relays | profile, map, 4 points | documents |
| [ioLogik E1240](devices/moxa/iologik-e1240/) | Moxa | Modbus TCP | 8 AI | profile, map, 2 points | documents |
| [ioLogik E1241](devices/moxa/iologik-e1241/) | Moxa | Modbus TCP | 4 AO | profile, map, 1 point | documents |
| [ioLogik E1242](devices/moxa/iologik-e1242/) | Moxa | Modbus TCP | 4 AI, 4 DI, 4 DIO | profile, map, 5 points | documents |
| [ioLogik E1260](devices/moxa/iologik-e1260/) | Moxa | Modbus TCP | 6 RTD | profile, map, 1 point | documents |
| [ioLogik E1262](devices/moxa/iologik-e1262/) | Moxa | Modbus TCP | 8 TC | profile, map, 1 point | documents |
| [ioLogik E2210](devices/moxa/iologik-e2210/) | Moxa | Modbus TCP | 12 DI, 8 DO (sink) | identity and sources | documents |
| [ioLogik E2212](devices/moxa/iologik-e2212/) | Moxa | Modbus TCP | 8 DI, 8 DO, 4 DIO | identity and sources | documents |
| [ioLogik E2242](devices/moxa/iologik-e2242/) | Moxa | Modbus TCP | 4 AI, 12 DIO | identity and sources | documents |
| [ERT1-HD16CH-1](devices/omron/ert1-hd16ch-1/) | Omron | EtherNet/IP |  | EDS connection | documents |
| [ERT1-ID32SLH-1](devices/omron/ert1-id32slh-1/) | Omron | EtherNet/IP |  | EDS connection | documents |
| [ERT1-MD32SLH-1](devices/omron/ert1-md32slh-1/) | Omron | EtherNet/IP |  | EDS connection | documents |
| [ERT1-OD32SLH-1](devices/omron/ert1-od32slh-1/) | Omron | EtherNet/IP |  | EDS connection | documents |
| [ERT1-WD16CH-1](devices/omron/ert1-wd16ch-1/) | Omron | EtherNet/IP |  | EDS connection | documents |
| [FEN20-4DIP-4DXP](devices/turck/fen20-4dip-4dxp/) | Turck | EtherNet/IP |  | EDS connection | documents |

<a name="io-coupler"></a>

## Modular I/O couplers

The head of a row of I/O slices or modules; the channels depend on what is fitted. `find.py io-coupler`

| model | vendor | speaks | channels | to use it | checked |
| --- | --- | --- | --- | --- | --- |
| [BK9050](devices/beckhoff/bk9050/) | Beckhoff | Modbus TCP | up to 64 Bus Terminals, 512 bytes in and 512 bytes out | 5 points | documents |
| [EK9000](devices/beckhoff/ek9000/) | Beckhoff | Modbus TCP | none of its own: the EtherCAT terminals behind it set the I/O | 6 points | documents |
| [EK9500](devices/beckhoff/ek9500/) | Beckhoff | EtherNet/IP | none of its own: the EtherCAT terminals behind it set the I/O | EDS connection, 1 point | documents |
| [CPX-AP-A-EP](devices/festo/cpx-ap-a-ep/) | Festo | EtherNet/IP |  | EDS connection | documents |
| [CPX-AP-I-EP-M12](devices/festo/cpx-ap-i-ep-m12/) | Festo | EtherNet/IP |  | EDS connection | documents |
| [CPX-E-EP](devices/festo/cpx-e-ep/) | Festo | EtherNet/IP |  | EDS connection | documents |
| [CPX-FB32](devices/festo/cpx-fb32/) | Festo | EtherNet/IP |  | EDS connection | documents |
| [CPX-FB36](devices/festo/cpx-fb36/) | Festo | EtherNet/IP |  | EDS connection | documents |
| [ioThinx 4510](devices/moxa/iothinx-4510/) | Moxa | Modbus TCP | modular, up to 32 I/O modules | 5 points | documents |
| [NX-EIC202](devices/omron/nx-eic202/) | Omron | EtherNet/IP |  | EDS connection | documents |
| [AXL F BK EIP EF](devices/phoenix-contact/axl-f-bk-eip-ef/) | Phoenix Contact | EtherNet/IP | none of its own: the Axioline F modules behind it (up to 63) set the I/O | EDS connection, 1 point | documents |
| [1719-AENTR](devices/rockwell-automation/1719-aentr/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [1734-AENT](devices/rockwell-automation/1734-aent/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [1734-AENTR](devices/rockwell-automation/1734-aentr/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [1738-AENT](devices/rockwell-automation/1738-aent/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [1769-AENTR](devices/rockwell-automation/1769-aentr/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [1794-AENT](devices/rockwell-automation/1794-aent/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [1794-AENTR](devices/rockwell-automation/1794-aentr/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [5069-AEN2TR](devices/rockwell-automation/5069-aen2tr/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [5094-AEN2TR](devices/rockwell-automation/5094-aen2tr/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [5094-AENTR](devices/rockwell-automation/5094-aentr/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [Modicon STB NIP2311](devices/schneider-electric/stb-nip2311/) | Schneider Electric | Modbus TCP |  | 3 points | documents |
| [Modicon TM3 bus coupler TM3BCEIP](devices/schneider-electric/tm3bceip/) | Schneider Electric | Modbus TCP |  | identity and sources | documents |
| [SIMATIC ET 200SP IM 155-6 MF HF](devices/siemens/im-155-6-mf-hf/) | Siemens |  |  | identity and sources | documents |
| [750-363](devices/wago/750-363/) | WAGO | EtherNet/IP |  | EDS connection | documents |

<a name="iolink-master"></a>

## IO-Link masters

Ports that speak IO-Link to sensors and actuators. `find.py iolink-master`

| model | vendor | speaks | channels | to use it | checked |
| --- | --- | --- | --- | --- | --- |
| [BNI EIP-508-105-Z015](devices/balluff/bni-eip-508-105-z015/) | Balluff | EtherNet/IP |  | EDS connection | documents |
| [DXMR90-4K](devices/banner/dxmr90-4k/) | Banner | EtherNet/IP, Modbus TCP |  | EDS connection | documents |
| [AL1122](devices/ifm/al1122/) | ifm | EtherNet/IP |  | EDS connection | documents |
| [AL1222](devices/ifm/al1222/) | ifm | EtherNet/IP |  | EDS connection | documents |
| [AL1322](devices/ifm/al1322/) | ifm | EtherNet/IP |  | EDS connection | documents |
| [AL1326](devices/ifm/al1326/) | ifm | EtherNet/IP |  | EDS connection | documents |
| [AL1590](devices/ifm/al1590/) | ifm | EtherNet/IP |  | EDS connection | documents |
| [ICE2-8IOL-G65L-V1D](devices/pepperl-fuchs/ice2-8iol-g65l-v1d/) | Pepperl+Fuchs | EtherNet/IP |  | EDS connection | documents |
| [ICE2-8IOL-K45S-RJ45](devices/pepperl-fuchs/ice2-8iol-k45s-rj45/) | Pepperl+Fuchs | EtherNet/IP |  | EDS connection | documents |
| [ICE21-8IOL2-G70L-V1D](devices/pepperl-fuchs/ice21-8iol2-g70l-v1d/) | Pepperl+Fuchs | EtherNet/IP |  | EDS connection | documents |
| [IOLG2EI-03208R01](devices/sick/iolg2ei/) | SICK | EtherNet/IP |  | EDS connection | documents |
| [SIG300](devices/sick/sig300/) | SICK | EtherNet/IP |  | EDS connection | documents |
| [SIG350](devices/sick/sig350-0005ap100/) | SICK | EtherNet/IP |  | EDS connection | documents |
| [TBEN-L5-8IOL](devices/turck/tben-l5-8iol/) | Turck | EtherNet/IP |  | EDS connection | documents |
| [TBEN-S2-4IOL](devices/turck/tben-s2-4iol/) | Turck | EtherNet/IP |  | EDS connection | documents |

<a name="valve-terminal"></a>

## Valve terminals

Pneumatic valve manifolds and their bus nodes; an output switches a solenoid. `find.py valve-terminal`

| model | vendor | speaks | channels | to use it | checked |
| --- | --- | --- | --- | --- | --- |
| [Numatics 580 Ethernet/IP](devices/emerson/numatics-580-ethernet-ip/) | Emerson | EtherNet/IP |  | EDS connection | documents |
| [Numatics 580 Ethernet/IP DLR+QC](devices/emerson/numatics-580-ethernet-ip-dlr/) | Emerson | EtherNet/IP |  | EDS connection | documents |
| [Numatics G3 EtherNet/IP](devices/emerson/numatics-g3-ethernet-ip/) | Emerson | EtherNet/IP |  | EDS connection | documents |
| [CTEU-EP](devices/festo/cteu-ep/) | Festo | EtherNet/IP |  | EDS connection | documents |
| [VABX-A-S-EL-E12-CTED-EP](devices/festo/vabx-a-cted-ep/) | Festo | EtherNet/IP |  | EDS connection | documents |
| [VR1X-EP](devices/imi-norgren/vr1x-ep/) | IMI Norgren | EtherNet/IP |  | EDS connection | documents |
| [VS18/VS26](devices/imi-norgren/vs18-vs26/) | IMI Norgren | EtherNet/IP |  | EDS connection | documents |
| [P2H Node 32DO EtherNet/IP](devices/parker/p2h-node-ethernet-ip/) | Parker | EtherNet/IP |  | EDS connection | documents |
| [P2M Lite Node 24DO ETHERNET/IP](devices/parker/p2m-lite-node-ethernet-ip/) | Parker | EtherNet/IP |  | EDS connection | documents |
| [P2M Node 24DO ETHERNET/IP](devices/parker/p2m-node-ethernet-ip/) | Parker | EtherNet/IP |  | EDS connection | documents |
| [EX260-SEN1](devices/smc/ex260-sen1/) | SMC | EtherNet/IP |  | EDS connection | documents |
| [EX260-SEN2](devices/smc/ex260-sen2/) | SMC | EtherNet/IP |  | EDS connection | documents |
| [EX260-SEN3](devices/smc/ex260-sen3/) | SMC | EtherNet/IP |  | EDS connection | documents |
| [EX260-SEN4](devices/smc/ex260-sen4/) | SMC | EtherNet/IP |  | EDS connection | documents |
| [EX600-SEN1/SEN2](devices/smc/ex600-sen1/) | SMC | EtherNet/IP |  | EDS connection | documents |
| [EX600-SEN3/SEN4](devices/smc/ex600-sen3/) | SMC | EtherNet/IP |  | EDS connection | documents |
| [EX600-SEN7/SEN8](devices/smc/ex600-sen7/) | SMC | EtherNet/IP |  | EDS connection | documents |

<a name="drive"></a>

## Drives

Frequency inverters, servo drives and their network option cards. `find.py drive`

| model | vendor | speaks | channels | to use it | checked |
| --- | --- | --- | --- | --- | --- |
| [ABB Drive via Ethernet/IP FEIP-21](devices/abb/feip-21/) | ABB | EtherNet/IP |  | EDS connection | documents |
| [CMM-EIP01](devices/delta-electronics/cmm-eip01/) | Delta Electronics | EtherNet/IP |  | EDS connection | documents |
| [PowerXL DG1](devices/eaton/powerxl-dg1/) | Eaton | EtherNet/IP |  | EDS connection | documents |
| [PowerXL DM1 PRO](devices/eaton/powerxl-dm1-pro/) | Eaton | EtherNet/IP |  | EDS connection | documents |
| [PowerXL VFD EIP Comm. Card](devices/eaton/powerxl-vfd-eip-comm-card/) | Eaton | EtherNet/IP |  | EDS connection | documents |
| [CMMT-AS-EP](devices/festo/cmmt-as/) | Festo | EtherNet/IP |  | EDS connection | documents |
| [i550 cabinet](devices/lenze/i550/) | Lenze | EtherNet/IP |  | EDS connection | documents |
| [FR-D800-E](devices/mitsubishi-electric/fr-d800-e/) | Mitsubishi Electric | EtherNet/IP |  | EDS connection | documents |
| [FR-E800-E](devices/mitsubishi-electric/fr-e800-e/) | Mitsubishi Electric | EtherNet/IP |  | EDS connection | documents |
| [FR-E800-SCE](devices/mitsubishi-electric/fr-e800-sce/) | Mitsubishi Electric | EtherNet/IP |  | EDS connection | documents |
| [Liberty / Lexium MDrive Ethernet (LMD), EtherNet/IP](devices/novanta/lexium-mdrive-ethernet/) | Novanta IMS | EtherNet/IP |  | EDS connection, 9 points | 2026-11-16 |
| [Armor PowerFlex 35E](devices/rockwell-automation/armor-powerflex-35e/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [PowerFlex 523 with 25-COMM-E2P](devices/rockwell-automation/powerflex-523-25-comm-e2p/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [PowerFlex 525 (embedded EtherNet/IP)](devices/rockwell-automation/powerflex-525/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [PowerFlex 527 (embedded EtherNet/IP, STO CIP Safety listing)](devices/rockwell-automation/powerflex-527/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [PowerFlex 6000T](devices/rockwell-automation/powerflex-6000t/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [PowerFlex 70 (EtherNet/IP adapter)](devices/rockwell-automation/powerflex-70/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [PowerFlex 70EC](devices/rockwell-automation/powerflex-70ec/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [PowerFlex 753 with 20-750-ENETR](devices/rockwell-automation/powerflex-753/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [PowerFlex 753TS](devices/rockwell-automation/powerflex-753ts/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [PowerFlex 755 (embedded EtherNet/IP)](devices/rockwell-automation/powerflex-755/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [PowerFlex 755TS](devices/rockwell-automation/powerflex-755ts/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [Altivar Machine ATV320 with VW3A3616](devices/schneider-electric/atv320-vw3a3616/) | Schneider Electric | EtherNet/IP |  | EDS connection | documents |
| [Altivar Machine ATV340 (embedded Ethernet)](devices/schneider-electric/atv340/) | Schneider Electric | EtherNet/IP |  | EDS connection | documents |
| [Altivar Process ATV630 / ATV930 (embedded Ethernet)](devices/schneider-electric/atv630/) | Schneider Electric | EtherNet/IP |  | EDS connection | documents |
| [Lexium 32M with VW3A3616](devices/schneider-electric/lexium-32m-vw3a3616/) | Schneider Electric | EtherNet/IP |  | EDS connection | documents |
| [SINAMICS G120 CU240E-2 PN (EtherNet/IP)](devices/siemens/sinamics-g120-cu240e-2-pn/) | Siemens | EtherNet/IP |  | EDS connection, 2 points | documents |
| [CFW300](devices/weg/cfw300/) | WEG | EtherNet/IP |  | EDS connection | documents |
| [CFW320](devices/weg/cfw320/) | WEG | EtherNet/IP |  | EDS connection | documents |
| [CFW500](devices/weg/cfw500/) | WEG | EtherNet/IP |  | EDS connection | documents |
| [Yaskawa GA501](devices/yaskawa/ga500-ga501/) | Yaskawa | EtherNet/IP |  | EDS connection | documents |
| [Yaskawa SI-EN3D for CIPR-GA80U2004](devices/yaskawa/ga800-si-en3d/) | Yaskawa | EtherNet/IP |  | EDS connection | documents |

<a name="motor-starter"></a>

## Motor starters and protection

Starters, soft starters and motor management relays. `find.py motor-starter`

| model | vendor | speaks | channels | to use it | checked |
| --- | --- | --- | --- | --- | --- |
| [ArmorStart 280E/281E (EtherNet/IP)](devices/rockwell-automation/armorstart-280e-281e/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [ArmorStart LT 290E/291E/294E (EtherNet/IP)](devices/rockwell-automation/armorstart-lt/) | Rockwell Automation | EtherNet/IP |  | EDS connection | documents |
| [TeSys island bus coupler TPRBCEIP](devices/schneider-electric/tprbceip/) | Schneider Electric | Modbus TCP |  | identity and sources | documents |
| [TeSys T LTMR E (Ethernet)](devices/schneider-electric/ltmr-e-ethernet/) | Schneider Electric | EtherNet/IP |  | EDS connection | documents |
| [SSW900](devices/weg/ssw900/) | WEG | EtherNet/IP |  | EDS connection | documents |

<a name="power-meter"></a>

## Power meters

Meters that give voltage, current, power and energy. `find.py power-meter`

| model | vendor | speaks | channels | to use it | checked |
| --- | --- | --- | --- | --- | --- |
| [PowerLogic PM5560](devices/schneider-electric/pm5560/) | Schneider Electric | Modbus TCP |  | identity and sources | documents |
| [SENTRON PAC3200](devices/siemens/sentron-pac3200/) | Siemens | Modbus TCP |  | 4 points | documents |
| [SENTRON PAC4200](devices/siemens/sentron-pac4200/) | Siemens | Modbus TCP |  | 4 points | documents |

<a name="vision"></a>

## Vision sensors and code readers

Cameras that inspect, and readers of 1D and 2D codes. `find.py vision`

| model | vendor | speaks | channels | to use it | checked |
| --- | --- | --- | --- | --- | --- |
| [DataMan 300 Series Reader](devices/cognex/dataman-dm36x/) | Cognex | EtherNet/IP |  | EDS connection | documents |
| [In-Sight 2800 Series](devices/cognex/in-sight-2800/) | Cognex | EtherNet/IP |  | EDS connection | documents |
| [In-Sight 7000 Series](devices/cognex/in-sight-7000/) | Cognex | EtherNet/IP |  | EDS connection | documents |
| [In-Sight 7900-7500 Series](devices/cognex/in-sight-7800/) | Cognex | EtherNet/IP |  | EDS connection | documents |
| [Matrix N Series](devices/datalogic/matrix-n/) | Datalogic | EtherNet/IP |  | EDS connection | documents |
| [IV3 Series](devices/keyence/iv3/) | Keyence | EtherNet/IP |  | EDS connection | documents |
| [IV4 Series](devices/keyence/iv4/) | Keyence | EtherNet/IP |  | EDS connection | documents |
| [SR-1000 Series](devices/keyence/sr-1000/) | Keyence | EtherNet/IP |  | EDS connection | documents |
| [SR-2000 Series](devices/keyence/sr-2000/) | Keyence | EtherNet/IP |  | EDS connection | documents |
| [SR-5000 Series](devices/keyence/sr-5000/) | Keyence | EtherNet/IP |  | EDS connection | documents |
| [SR-X1H3H Series](devices/keyence/sr-x1h3h/) | Keyence | EtherNet/IP |  | EDS connection | documents |

<a name="robot"></a>

## Robots

Robot controllers, as a device another controller reads and commands. `find.py robot`

| model | vendor | speaks | channels | to use it | checked |
| --- | --- | --- | --- | --- | --- |
| [e-Series](devices/universal-robots/e-series/) | Universal Robots | EtherNet/IP, Modbus TCP | robot state, joints, TCP, control box and tool I/O, general purpose registers | profile, map, EDS connection, 6 points | documents |

<a name="controller"></a>

## Controllers

Programmable controllers that also answer as a device. `find.py controller`

| model | vendor | speaks | channels | to use it | checked |
| --- | --- | --- | --- | --- | --- |
| [750-823](devices/wago/750-823/) | WAGO | EtherNet/IP |  | EDS connection | documents |
| [750-893](devices/wago/750-893/) | WAGO | EtherNet/IP |  | EDS connection | documents |

<a name="sensor"></a>

## Sensors and actuators on a digital channel

Wired to a point of an I/O block, not on the network; described from the IODD. `find.py sensor`

| model | vendor | speaks | channels | to use it | checked |
| --- | --- | --- | --- | --- | --- |
| [(PN7072, PN7092, PN7572, PN7592) Status B](devices/ifm/pn7092/) | ifm | IO-Link, or a plain switching wire |  | record | documents |
| [IF6123, IF6124, IG6615, IG6616, II5973, II5974, IM5172, IM5173](devices/ifm/if6123/) | ifm | IO-Link, or a plain switching wire |  | record | documents |
| [KQxxxx](devices/ifm/kq6005/) | ifm | IO-Link, or a plain switching wire |  | record | documents |
| [O5D100/O5D102/O5D150/O5D152/O5D159](devices/ifm/o5d100/) | ifm | IO-Link, or a plain switching wire |  | record | documents |
| [WTB4F\_DID8389194](devices/sick/wtb4f-did8389194/) | SICK | IO-Link, or a plain switching wire |  | record | documents |
