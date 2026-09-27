# Deploy and Host Plane Community on Railway

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template/plane-community?utm_medium=integration&utm_source=button&utm_campaign=plane-community)

[Plane](https://plane.so/) is the open-source project tracker: work items, cycles (sprints), modules, a wiki with real-time collaborative pages, saved views, intake and analytics, in a fast keyboard-first interface. This template runs Plane Community Edition 1.4.2 on Plane's official all-in-one image with Postgres, Redis, RabbitMQ and a Railway bucket, and creates your admin account on first boot, so Plane's instance setup page is never open to whoever finds the URL first.

## About Hosting Plane Community

The stack is four services and a bucket: Plane, Postgres, Redis, RabbitMQ and the Uploads bucket.

- **One Plane service, upstream's own image.** The web app, API, background workers, scheduler, real-time editor server and proxy run together in Plane's all-in-one image, pinned to 1.4.2. There is one deploy to watch and one set of logs.
- **Admin ready, god mode closed.** Plane's instance settings at `/god-mode` belong to whoever opens them first. Here the first boot creates the admin from your email and a generated password, so there is nothing to claim.
- **Uploads in a Railway bucket.** Attachments, images and covers go straight from the browser to the bundled bucket. There is no MinIO service to size, back up or keep an image for.
- **Sized for Railway.** Upstream starts one background worker process per CPU the container can see: dozens on Railway's hosts, about 150 MB each. This template runs two, so Plane idles around 0.8 GB instead of several GB.
- **Logs where you look for them.** The all-in-one image writes every process's log to files inside the container; here they go to Railway's log view.
- **Closed sign-up.** Only people you invite to a workspace can create an account.
- **Upgrades that migrate themselves.** Every boot runs Plane's database migrations before serving.

## Common Use Cases

- Issue tracking and sprints for a software team, replacing Jira or Linear
- Roadmaps with modules and a project wiki in Pages, edited together in real time
- A shared backlog for agencies and small companies that don't want per-seat pricing

## Dependencies for Plane Community Hosting

- Postgres 17 (included, private network only)
- Redis 8 (included, private network only)
- RabbitMQ 4.1 (included, private network only)
- A Railway bucket for uploads (included)

### Deployment Dependencies

- [Plane documentation](https://docs.plane.so/)
- [Plane self-hosting guide](https://developers.plane.so/self-hosting/overview)
- [Template source on GitHub](https://github.com/nomideusz/plane-railway)

### Implementation Details

**Sign in** at the Plane service's Railway domain with the email you entered at deploy time and the `PLANE_ADMIN_PASSWORD` value from the Plane service's Variables tab. The first boot runs the database migrations, so give it two or three minutes. Plane then asks you to create your first workspace. The same account manages the instance at `/god-mode`. Change the password afterwards under Profile settings; the variable is only read on first boot.

**Teammates.** Invite them under Workspace settings → Members. Railway only allows outbound SMTP on the Pro plan, so on other plans the invitation email is not sent: tell your teammates the URL, and they sign up with the invited address and accept the invitation. Anyone who wasn't invited gets "sign up disabled". To open sign-up to everyone, or to add SMTP on Pro, use `/god-mode` → Authentication and Email. `ENABLE_SIGNUP` only applies on first boot; after that the setting lives in god mode.

**Memory.** Around 1 GB at idle: about 800 MB for Plane, 100 MB for RabbitMQ, 80 MB for Postgres and 10 MB for Redis. That is more than the Trial plan gives, so deploy on Hobby or above. If background jobs (notifications, imports, exports) queue up for a large team, raise `CELERY_WORKER_CONCURRENCY`; each worker adds about 150 MB.

**Files and backups.** Uploads live in the bucket and everything else in Postgres, so enable Railway's volume backups on the Postgres volume. The largest attachment is 50 MB, set by `FILE_SIZE_LIMIT` in bytes.

**Custom domain.** Add it in the Plane service's Settings → Networking, then set `DOMAIN_NAME` to the bare domain (`plane.example.com`). Plane picks it up on the next boot.

**Telemetry.** Plane reports anonymous usage statistics to its developers by default. Turn it off in `/god-mode` → General.

## Why Deploy Plane Community on Railway?

Railway is a singular platform to deploy your infrastructure stack. Railway will host your infrastructure so you don't have to deal with configuration, while allowing you to vertically and horizontally scale it.

By deploying Plane Community on Railway, you are one step closer to supporting a complete full-stack application with minimal burden. Host your servers, databases, AI agents, and more on Railway.
