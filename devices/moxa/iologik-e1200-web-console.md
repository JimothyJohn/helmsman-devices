# ioLogik E1200 web console, as a protocol

How the console's settings are read and written without a browser. Mapped on
the bench E1213 (192.168.3.60, firmware V3.1 Build19110615) on 2026-11-12,
headless, from the pages it serves. One write was made and undone, to the
Server Location. The other nine models share the firmware line (see
[iologik-e1200-series.md](iologik-e1200-series.md)), so the shape is
expected to hold, but it is checked on this unit only.

The client is `scripts/moxa-e1200-console.py` (`export`, `form`, `set`). Its
tests are `tests/test_moxa_console.py` (synthetic pages) and
`tests/test_moxa_console_bench.py` (the real unit, opt-in with
`MOXA_E1200_HOST`).

## The server

- HTTP/1.1 on port 80, `Server: ioLogik Web Server/1.0`, no TLS. Its `Date`
  header is fixed (`Fri, 18 June 2009 09:00:00 GMT`), so ignore it.
- `Allow: OPTIONS, GET, PUT` and `Access-Control-Allow-Origin: *` on every
  page: any web page a browser on the plant network opens can send it
  requests.
- The front page sets two cookies, `ChallID` (a number) and `MoxaPass`. With no
  password set (3.1 ships without one) every page answers with or without them.
- **A new connection right after the last one is sometimes dropped** without
  a response (it happened once while mapping it). The client waits 0.3 s between
  requests and retries a read once. It never retries a write.
- "Network Connection" (`06_3.htm`) lists the TCP connections the unit has
  open, by source and type (`Web/HTTP`).

## Reading

Every page is a plain GET. The menu is `contents.htm` (a JavaScript tree of
`gLnk(0, "Label", "page.htm")` calls); the settings pages are `NN_N.htm`.

**The configuration export** is the whole configuration as INI-style text:
`06_6.htm` links it as `ik1213.txt` (`ik12xx.txt` by model), 17 409 bytes and
849 lines here. Sections: `[System Information]` (firmware and build),
`[1. Model]`, `[2. I/O Configurations]` (per channel: mode, filter, the DO
power-on state `DOnn_PWN`, safe value `DOnn_SAFE`, DIO direction),
`[3. Modbus address table]`, `[4. Network Settings]` (address, MAC, idle
timeout, `CONNECTION_WATCHDOG`, the IP filter, `AUTOCLEAR_SAFEMODE`),
`[5. Alias Settings]`, `[6. Active OPC Server Settings]`, `[7. Peer to peer
I/O Settings]`, `[8. SNMP Settings]`, `[9. Protocol Enable]` (`REST_ENABLE`,
`EIP_ENABLE`), then `<END>`. This one file answers most of what the
firmware-and-resilience plan asks a unit (firmware, watchdog, safe values,
protocols).

**The export shows staged settings, not running ones.** A write changes it
at once, before the unit has applied anything (below).

## Writing

Each settings page has one form, `method="GET" action="set.htm"`. It carries
a hidden `code` naming the page and a hidden `token`, fresh on each load of
the page. A write is the form's fields as a browser submits them:

```text
GET /set.htm?token=<token>&MOD_DESC=&MOD_LOC=helmsman+bench&EnableIDLE=1&IdleTime=60&Submit=Submit&code=41
```

- An unticked checkbox is left out. A field the page's script disables is
  left out too: in General Settings, `checkWDValue()` disables `IdleTime`
  unless `EnableIDLE` is ticked, and `WDTime` unless `EnableWD` is.
- The reply is a page saying "Configuration Complete" and "The changes will
  not take effect until you Save/Restart the I/O Server".
- **Never GET `set.htm` while exploring.** A GET there is a write.

| page | `code` | what | fields |
| --- | --- | --- | --- |
| `04_1.htm` General Settings | 41 | name, location, idle timeout, **communication watchdog**, Safe Mode auto-clear | `MOD_DESC`, `MOD_LOC`, `EnableIDLE`, `IdleTime`, `EnableWD`, `WDTime`, `EnableSafeModeAutoClear` |
| `11_safeM.htm` DO Safe Mode | 116 | each DO's safe state | `SetSM00`..`SetSM07` (selects); `Clear_Safe_Flag1` is a separate button |
| `13_1.htm` RESTful | 131 | RESTful API on/off | `REST_ENABLE` |
| `14_1.htm` EtherNet/IP | 141 | **EtherNet/IP on/off** (what firmware 4.0 turns off by default) | `EIP_ENABLE`; the page disables it unless hidden `eipActed` is 1 (activated) |
| `07.htm` Change Password | | the password | `OldPassword`, `NewPassword`, `ReTypePassword`, hashed in the page with MD5 and the `ChallID` cookie (`md5.js`). **Not used by the client.** |

The other settings pages (`03_1.htm` Modbus addressing, `04_2.htm` Ethernet,
`05_1.htm`/`05_2.htm` channels, `06_1.htm` IP accessibility, `10_1.htm` AOPC,
`11_1.htm`.. peer to peer, `12_1.htm`/`12_2.htm` SNMP) have the same shape and
were read, not written. `04_2.htm` holds the unit's IP settings, and changing
those always asks Nick first.

Not done, and why:
- **Save/Restart** (`09.htm`) and **Load Factory Default** (`08.htm`) were not
  even fetched, in case a GET acts. Applying a staged change needs
  Save/Restart, which takes the unit off the network for its reboot. That's
  the next step, with Nick's go, since the P4 node reads this unit over
  Modbus.
- **Import** (`06_5.htm`, a multipart POST of the export file to
  `06_5_1.htm`) and **Firmware Update** (`06_4.htm` to `06_4_1.htm`). Import
  is the restore path for a replaced unit.
- **A password-protected console** (3.3 and later default to "moxa"): the
  login exchange is in `md5.js` and not read yet.

## What the bench unit's export says (2026-11-12)

- `CONNECTION_WATCHDOG=0,(Disabled)`, `AUTOCLEAR_SAFEMODE=0`: the factory
  default. The unit holds its outputs when its controller vanishes.
- `DO00_PWN=1,(On)` and `DO01_PWN=1,(On)`: **DO-00 and DO-01 switch on at
  power-up**, before any controller connects. Nothing in the library's E1213
  profile knows this; a box program should not assume outputs start off.
- `DOnn_SAFE=0,(Off)` for all eight: Safe Mode, if the watchdog were on,
  would turn every output off.
- `REST_ENABLE=1`, `EIP_ENABLE=1`; EtherNet/IP activated (`eipActed=1`).
