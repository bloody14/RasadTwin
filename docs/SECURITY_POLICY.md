# RasadTwin Security Policy — Agent Enforcement Version

## 1. Default security mode

`SECURITY_MODE=OFFLINE_SYNTHETIC`

Meaning:
- synthetic project data only;
- no outbound network traffic by the application;
- local execution preferred;
- no secrets in repo;
- no autonomous dispatch.

## 2. Prohibited agent behavior

The coding agent must not:
- upload files/logs/code to external services;
- paste source files into external APIs for convenience;
- use live military or government operational data;
- search for or reconstruct sensitive operational details;
- add hidden telemetry;
- bypass antivirus/firewall/policy controls;
- suppress security exceptions;
- disable tests to make the build green;
- falsify experiment outputs;
- modify protected research rules to obtain a preferred result.

## 3. External resources

Public services such as OSM, SRTM or Open-Meteo may be implemented through explicit adapters when the phase authorizes them. The synthetic/offline path must remain usable without those services.

The prototype's demo path should be able to run from local fixtures/cache.

## 4. Safe-by-default API

Required baseline:
- localhost binding;
- explicit request schemas;
- bounded request sizes/timeouts where applicable;
- no arbitrary file read/write endpoints;
- no shell-command execution endpoint;
- no dynamic Python evaluation;
- no arbitrary URL fetch endpoint;
- no unsanitized path input;
- no secret material in responses.

## 5. Security evidence

Each relevant phase report must state:
- whether network access was required;
- whether secrets were scanned;
- whether prohibited data was used;
- what security tests were run;
- any unresolved security risk.
