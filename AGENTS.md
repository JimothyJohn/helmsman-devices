# For agents: mapping a device into this library

This file is written for a coding agent working for someone who has a device
on their network. The person's part is small and comes first. Everything
after it is yours.

## What the person does

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

## What you do

Work in a fork, on a branch from `dev`. One device, or one family that shares
a manual, per pull request.

### 1. Ask the device who it is

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

### 2. Look it up

Search `index.json` for the vendor id and product code, then for the vendor
and model text.

- **It is there.** Your job is to prove or correct the entry: go to step 4
  with the folder it names.
- **It is not.** Draft it: step 3.

### 3. Draft the entry from the vendor's documents

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

### 4. Test the entry against the unit

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

### 5. Write down only what was seen

- `checked_on`, `firmware` and `checked_by` go into `[device]` only when
  step 4 ran on a real unit, with the date and the firmware that unit
  reported. `checked_by` is how the person wants to be credited.
- Each point you confirmed gets `confirmed on a unit <date>` appended to its
  `source`. Points you did not exercise keep their document source alone.
- The folder's `README.md` says what was run and what was not.

### 6. Check and send

```sh
python3 -I scripts/build-index.py && python3 -I scripts/build-review.py
uvx ruff@0.17.4 check . && uvx ruff@0.17.4 format --check .
python3 -I scripts/build-index.py --check && python3 -I scripts/build-review.py --check
python3 -I -B -m unittest discover -s tests
```

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
