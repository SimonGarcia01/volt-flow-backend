# volt-flow-backend

Backend for VoltFlow. The app acts as an OCPP server for electric vehicle
chargers and exposes REST endpoints for a Flutter client used by station
owners.

## Project structure

This project uses a module-oriented structure. A module is a business or
protocol area that owns its own models, schemas, repositories, services, and
routes.

```text
app/
  api/          REST API router aggregation
  auth/         Users, roles, permissions, and authentication
  charging/     Station-owner domain: stations, chargers, connectors, sessions
  core/         Application settings and global configuration
  database/     Database engine, sessions, base class, and model registry
  middleware/   Cross-cutting FastAPI middleware
  ocpp/         OCPP protocol connection handling
  realtime/     Realtime app communication, such as WebSocket updates
```

The important rule is: avoid large global `models`, `schemas`, `services`, or
`repositories` folders. Put those files inside the module that owns the
business concept.

For example, future charger code should live under `app/charging/`:

```text
app/charging/
  models/
  schemas/
  repositories/
  services/
  router.py
```

This keeps related code together. When you work on chargers later, you should
not need to jump between global folders to understand one feature.
