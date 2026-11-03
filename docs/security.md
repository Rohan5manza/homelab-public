# Access, boundaries & reliability

A self-hosted lab can publish useful demonstrations without opening the door to everything running on the same computer.

## Three kinds of access

| Layer | Visitor experience |
| --- | --- |
| **Public website** | Read project pages, browse documentation, use browser-based simulations. |
| **Dedicated demos** | Interact with explicitly published applications through controlled entry points. |
| **Private administration** | Maintain containers, databases, home controls, device settings, and development environments. |

## Design decisions

- Host the public website as static content where possible.
- Keep private service management separate from the public site.
- Put published compute-heavy demos behind a restricted application layer with protective limits.
- Treat credentials, access rules, and recovery settings as part of normal infrastructure maintenance.
- Keep the thermostat capable of standard independent operation if the automation host is unavailable.

## Reliability is more than uptime

A working homelab should be observable and recoverable. My priorities are persistent application data, clear service dependencies, useful alerts, backups and a repeatable recovery process.

The [status page](../site/lab/status/index.html) reports only checks configured for visitor-facing services; it does not try to represent the operational condition of every container on Buffy.

## Next engineering improvements

Document actual backup restores, record controlled incident simulations and measure recovery time. A tested recovery procedure is stronger evidence than a checklist that has never been exercised.
