# For agents

This file is written for a coding agent. It covers the two things an agent
does here:

- **Using a device**: find it in the list, by category, and put it into a
  Helmsman project. Three commands, no network, nothing to install.
- **Mapping a device**: someone has a unit on their network that the library
  does not have, or has only from documents. You draft or correct the entry,
  test it against the unit and send a pull request.

## Using a device

Every command here only reads this checkout. Nothing reaches a device or the
internet.

### 1. Find it

The library is one list, sorted into categories. Start from the category,
then narrow with words:

```sh
python3 -I scripts/find.py                     # the categories, with how many devices each holds
python3 -I scripts/find.py valve-terminal      # one category's devices
python3 -I scripts/find.py drive powerflex     # a category, narrowed: every word must match
python3 -I scripts/find.py tben 8dxp           # words alone search every category
python3 -I scripts/find.py panel-io relay      # words match what a device has, too
python3 -I scripts/find.py --id 48:14076       # the vendor id and product code a device answered with
```

Words match the vendor, the model, its channels as the entry states them
("6 DI, 6 relays"), the order numbers and the folder name, in any case.
Each line gives the folder, the device, its channels, the protocols it
speaks, what the folder gives a project (`profile`, `map`, `eds`, `record`,
the number of documented points, or `identity only`) and the date a unit
confirmed it, or `documents`.

`--protocol enip|modbus|iolink`, `--ready` (a profile or a map: the
channels are named already) and `--checked` (a unit confirmed it) narrow
any of these. `--json` prints one object a line for a program. Exit 0 with
matches, 1 with none, 2 for an argument it refuses. Python 3.9 or later.

Channels are what the entry's documents say the device has: "8 DI, 4 DO"
for a block, "8 IO-Link ports" for a master, "32 solenoid outputs" for a
valve terminal. The head of a modular station has none of its own and names
the modules behind it; a drive, a starter or a camera says what it
exchanges with a controller. The library does not know prices or stock.

[`CATALOG.md`](CATALOG.md) is the same list as tables, one per category,
for reading on GitHub. `index.json` is the same list as data, for a program
without a checkout: each device has a `category`, and `categories` names
them in order.

| category | what is in it |
| --- | --- |
| `io-block` | fixed channels in one sealed housing with M12 ports, on the machine |
| `panel-io` | fixed channels in one module with terminals, in the cabinet |
| `io-coupler` | the head of a row of I/O slices; the channels depend on what is fitted |
| `iolink-master` | ports that speak IO-Link to sensors and actuators |
| `valve-terminal` | pneumatic valve manifolds and their bus nodes |
| `drive` | frequency inverters, servo drives and their network option cards |
| `motor-starter` | starters, soft starters and motor management relays |
| `power-meter` | meters that give voltage, current, power and energy |
| `vision` | cameras that inspect, and readers of 1D and 2D codes |
| `robot` | robot controllers, as a device another controller reads and commands |
| `controller` | programmable controllers that also answer as a device |
| `sensor` | a sensor or actuator wired to a digital channel, not on the network |
| `other` | on the network, and none of the above |

When the person has the unit and not its name, ask the unit (Mapping a
device, step 1) and look up what it answers with `--id`.

### 2. See what its folder gives

```sh
python3 -I scripts/use.py devices/turck/tben-s2-8dxp
python3 -I scripts/use.py tben-s2-8dxp --address 192.168.1.20 --id rio   # words that match one device work too
```

It prints every way the folder supports, best first, each with the lines to
paste into the project's I/O map:

| way | the folder has | what you do |
| --- | --- | --- |
| `profile` | `NAME.device` | copy the file into the project; `device rio device:NAME ADDR`, and each signal binds a channel by name (`ch:DI-04`). The box picks the protocol |
| `map` | `enip.map`, `modbus.map` | copy the lines; keep the points, rename the signals |
| `eds` | the vendor's EDS, by name, size and SHA-256 | fetch the file from the link, check it with `--eds PATH`, add it to the project; `device rio enip-io ADDR eds=NAME.eds` |
| `explicit` | the EDS's assembly instances and sizes | `device rio enip-io ADDR config=N o2t=I:BYTES t2o=I:BYTES`, with no file |
| `modbus` | a Modbus TCP port, and a unit id if the documents give one | `device rio modbus-tcp ADDR:502`, then the points it lists |
| `wired` | a sensor's record from its IODD | add `wired=VENDOR/MODEL` to the signal on the point it is wired to |

`--address` fills in `ADDR`: a host, `host:port`, or an identity the box
resolves when it connects (`cip=48:14076`, `mac=00-90-e8-7e-af-be`).
`--id` is the device's name in every line; without it the written lines
say `dev` and a copied map keeps the name it has. `--json` gives the same
as data: `ways[].lines` are the lines. Exit 2 for a device it cannot find
or an argument it refuses. Python 3.11 or later.

After the lines it prints the points the documents give, each with its
source, then **Not known yet**. Read that part to the person. Most entries
were drafted from the vendor's files and no unit has confirmed them: the
first line under the device's name says which.

### 3. Put it in the project

1. Copy what the chosen way names (a `.device` profile, an EDS) into the
   project, then paste its lines into the I/O map. A vendor's file is never
   in this repository: fetch it from the link the entry gives (out of the
   vendor's zip when it comes in one) and run
   `python3 -I scripts/use.py <folder> --eds PATH` on the `.eds` itself,
   which says whether it is the file the entry was read from.
2. An entry with no points gives you the connection and not the channels.
   Read them from the manual under Sources, or work them out on the unit
   (Mapping a device, step 4).
3. Inputs first. Have the person change one input and see the signal you
   expect move, before anything is driven.
4. Outputs are the person's to switch, never yours: an output moves
   whatever is wired to it. On a valve terminal, a drive or a starter that
   is a cylinder or a motor.

### 4. Send back what the unit showed

What you confirmed on a unit is what the next person needs: the firmware,
the points that moved, a size the EDS had wrong. That is the second half of
this file from step 4, or a `Unit check:` issue when you are not changing
the entry yourself.

## Mapping a device

Someone has a device on their network. The person's part is small and comes
first. Everything after it is yours.

### What the person does

1. Put the device on the same network as the computer you run on, and power it.
2. Make the machine safe: nothing dangerous may be wired to the device's
   outputs while it is being mapped.
3. Tell you the device's address, or let you find it.
4. Look at the device when you ask what it is doing (which input is on, which
   lamp is lit). Their eyes are the ground truth for what the bytes mean.

If they have no time for any of that, they can send the unit to the project's
bench instead. The project pays a bounty for units it has not tested; the
terms are in the Devices section of the Helmsman site, and an offer is an
issue titled `Unit offer: <vendor> <model>` in this repository.

### What you do

Work in a fork, on a branch from `dev`. One device, or one family that shares
a manual, per pull request.

#### 1. Ask the device who it is

Both scripts only read. Standard library, Python 3.9 or later.

```sh
python3 -I scripts/enip-list.py <the subnet's broadcast address>   # every EtherNet/IP device that answers
python3 -I scripts/enip-identify.py <address> [assembly ...]       # identity, and each assembly's size and bytes
python3 -I scripts/modbus-read.py <address> [range ...]            # Modbus TCP: identification, bits and registers
```

`enip-identify.py` prints an `[identity.enip]` fragment and one line per
assembly: `# assembly 101: 51 bytes, now 0100…`. Keep that output; it is the
evidence for the pull request. Leave the serial number out of anything you
commit or post.

For Modbus TCP, `modbus-read.py` takes the ranges in the library's own
point syntax (`di:0..di:11`, `ir:16:u32..ir:38:u32`, `coil:0..7`) and prints
one line a range: `# di 0..11: 001000000000`, one digit an address. It sends
read function codes only. Many devices refuse Read Device Identification
(the ioLogik E1213 on firmware 3.1 does); that is not a fault, and the
entry then has no `[identity.modbus]`.

#### 2. Look it up

Search for the vendor id and product code, then for the vendor and model
text:

```sh
python3 -I scripts/find.py --id <vendor id>:<product code>
python3 -I scripts/find.py <vendor> <model>
```

- **It is there.** Your job is to prove or correct the entry: go to step 4
  with the folder it names.
- **It is not.** Draft it: step 3.

#### 3. Draft the entry from the vendor's documents

`.claude/skills/collect-docs/SKILL.md` is the procedure: find the EDS and the
manual, record where each came from in `collect/<vendor>.toml`, fetch them
with `scripts/docs-fetch.py`, draft the folder with `scripts/eds-draft.py`,
then read the manual for `[[points]]` and `[wiring]`. `docs/device-toml.md`
is the format. Follow both as written; the rules in them are not optional:

- Every URL comes from a page you opened. Never build one from a pattern.
- Vendor files are never committed. A folder names each by size, SHA-256 and
  link.
- Every point names the document and page it was read from. Anything you
  worked out instead of read is marked **inferred**.
- A field nobody has read or seen is left out.

Give the entry its shelf: `category = "..."` under `[device]`, one of the
ids in the table above, from what the vendor calls the device. An entry
without one is listed under "Not yet sorted" and `build-index.py` names it.

Say what it has: `channels = "8 DI, 4 DO (2 A each)"   # from: data sheet p. 2`,
one line of at most 120 characters, in the words a search uses (DI, DO, DIO,
AI, AO, relays, IO-Link ports, solenoid outputs, the count first), with the
document it was read from in the comment. The model number alone is not a
source. `docs/device-toml.md` has the forms for a modular head and a drive.

`eds-draft.py` refuses an EDS written for another network (DeviceNet,
ControlNet): ODVA lists those beside the EtherNet/IP files, sometimes in the
same package. Find the EtherNet/IP file or drop the device with the reason.

#### 4. Test the entry against the unit

1. Compare what the device reported in step 1 with `[identity.enip]` and the
   assembly sizes in `[protocols.enip]`. A difference is a finding: fix the
   entry and say which firmware showed it. A revision the entry does not
   list is added to `revisions`.
2. Decode the assembly bytes, or the Modbus bits and registers, the way each `[[points]]` entry says, and tell
   the person in plain words what that means: "the entry says input 4 is on
   and the rest are off". Ask whether that is what the device is doing.
3. Have the person change one input at a time (press the sensor, bridge the
   terminal) and read again. A point is confirmed when the bit or value you
   predicted is the one that moved.
4. Outputs: you do not switch them. Switching an output moves whatever is
   wired to it, so that step belongs to the person. For a Modbus TCP coil,
   ask them to run `python3 -I scripts/modbus-pulse.py <address> coil:N`
   in their own terminal: it shows what it will do, waits for a word typed
   back, switches the one coil for two seconds and writes the first state
   back. It refuses to run without a terminal, so it will not run from your
   shell. Ask what moved, and paste the line it printed into the pull
   request. For an EtherNet/IP output there is no such script yet: if the
   person switches one with their own tools, record what they tell you as
   their observation.

Stop and report when the unit and the documents disagree and you cannot tell
which is right. A contradiction written down is worth more than a guess.

#### 5. Write down only what was seen

- `checked_on`, `firmware` and `checked_by` go into `[device]` only when
  step 4 ran on a real unit, with the date and the firmware that unit
  reported. `checked_by` is how the person wants to be credited.
- Each point you confirmed gets `confirmed on a unit <date>` appended to its
  `source`. Points you did not exercise keep their document source alone.
- The folder's `README.md` says what was run and what was not.

#### 6. Check and send

```sh
python3 -I scripts/build-index.py && python3 -I scripts/build-review.py && python3 -I scripts/build-records.py
uvx ruff@0.17.5 check . && uvx ruff@0.17.5 format --check .
python3 -I scripts/build-index.py --check && python3 -I scripts/build-review.py --check && python3 -I scripts/build-records.py --check
python3 -I -B -m unittest discover -s tests
python3 -I scripts/use.py <your folder>      # read it as the next person will
```

`build-index.py` writes `index.json` and `CATALOG.md`; commit both with the
folder, `review.json` and any `record.json` that changed.

Open the pull request into `dev`. In its description give the unit's
firmware, paste the `enip-identify.py` output without the serial line, and
list what the person confirmed by eye and what stayed unconfirmed.

## When you cannot finish

Open an issue instead of a partial folder, with what you have:

| title starts | for |
| --- | --- |
| `New device:` | a device the library should have, with any document links |
| `Review:` | an entry that is wrong, with the document page or the reading that shows it |
| `Unit check:` | a reading from a unit, when you are not changing the entry yourself |
| `Unit offer:` | a unit the person would send to the bench |

Never put an address, a serial number, a password or a payment detail in an
issue or a pull request. They are public.
