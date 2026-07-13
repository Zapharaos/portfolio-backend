# Data model

Everything on the site is an admin record. This page is the reference for every
editable table. Colour fields accept a `#RRGGBB` hex value and are validated.

!!! tip "Ordering & hiding"
    Most collections have an **`index`** (sort order, ascending) and a
    **`hidden`** flag. Hidden records are filtered out of the API. In the
    **Projects** admin list, `index` and `hidden` are editable inline for quick
    reordering.

## User

The site is a **singleton** — exactly one `User`. Creating a second one raises a
validation error.

| Field | Description |
|---|---|
| Name | Your name. |
| Email | Public contact email (shown in the footer). |
| Location | Free text, e.g. `Paris, France`. |
| Locale | BCP‑47 locale driving date/time formatting, e.g. `fr-FR`. |
| Timezone | IANA timezone for the footer clock, e.g. `Europe/Paris`. Empty = visitor's local time. Validated against the IANA database. |
| Logo | Header logo [File](#file). |
| Resume | Optional resume [File](#file). |
| Theme | Optional [Theme](#theme). Empty = front‑end default palette. |
| Hero / About / Work / Footer | The one‑to‑one sections below. |

## Theme

A palette applied to the whole front‑end (it overrides 3 CSS tokens; every other
colour is derived from them). Create several, link one to the user.

| Field | Description |
|---|---|
| Name | Unique label. |
| Background | `--color-background` token (`#RRGGBB`). |
| Text | `--color-text` token (`#RRGGBB`). |
| Primary | `--color-primary` accent token (`#RRGGBB`). |

## Hero

| Field | Description |
|---|---|
| Content type | **Do not edit** (defaults to `hero`). |
| Title | Main heading. |
| Tagline | Short phrase under the title (HTML allowed). |
| CallToActionContent | Label of the hero button — it links to the **Projects** page. |
| BackgroundImage | Hero [File](#file) image. |

## About

| Field | Description |
|---|---|
| Content type | **Do not edit** (defaults to `about`). |
| Image | Main [File](#file) image. |
| ImageResponsive | Optional mobile [File](#file) image. |
| Description | About text (HTML allowed). |

## Footer

| Field | Description |
|---|---|
| Content type | **Do not edit** (defaults to `footer`). |
| Title / SubTitle | Footer heading and subtitle. |
| ShowLocation / ShowSocials / ShowEmail / ShowResume | Toggle each footer block. |

## Work & Work items

**Work** selects which **Work items** to display. Each **Work item** holds
either projects **or** experiences (never both).

| Work item field | Description |
|---|---|
| Index / Hidden | Order / visibility. |
| Title | Section title (e.g. `Projects`, `Education`). |
| Projects | [Projects](#project) in this item. |
| Experiences | [Experiences](#experience) in this item. |
| ShowProjects / ShowExperiences | Which of the two to render (exactly one). |

!!! note
    Projects now have their own dedicated page (`/projects/`). The home "Work"
    section is typically used for experiences.

## Project

The projects catalogue. Fields marked *(read‑only)* are managed by the health
system.

| Field | Description |
|---|---|
| Index / Hidden | Order / visibility. |
| Title | Project name. |
| Description | Project text (HTML allowed). |
| Category | Short badge shown top‑right of the card (e.g. `LEGO`). Empty = none. |
| Metric | Short metric under the description (e.g. `~6k € ARR`). Empty = none. |
| IsNew | Show a **New** badge. |
| InProgress | Show a **Work in progress** badge. |
| IconFramed | Frame the icon (tile + border). Uncheck for a frameless icon. |
| ImageFit | `cover` (fill, may crop) or `contain` (whole image, padded). |
| Image | The card [File](#file) icon/image. |
| Technologies | Ordered tech tags (via **ProjectTechnology**, see below). |
| Links | Buttons on the card (see [ProjectLink](#projectlink)). |
| HealthUrl | Optional endpoint probed periodically ([Health checks](health-checks.md)). Empty = no check. |
| HealthUp / HealthCheckedAt / HealthFailures | *(read‑only)* current health state. |

### ProjectTechnology (ordering)

Technologies are attached through a `ProjectTechnology` row so their **order is
explicit**. Edit them inline on the project (the `position` field, lower first).
Same pattern exists for experiences (`ExperienceTechnology`).

### ProjectLink

A button rendered on the project card. The first link (lowest `index`) becomes
the primary call‑to‑action; the rest are secondary buttons.

| Field | Description |
|---|---|
| Kind | `github`, `website`, `appstore`, `playstore`, `docs`, `other` (used for analytics). |
| Url | Target URL. |
| Label | Button text. Empty = **View**. |
| Icon | Optional icon [File](#file) (SVG is tinted to the link colour; PNG shown as‑is). Empty = no icon. |
| IconPosition | `before` or `after` the label. |
| Color | Optional link hue `#RRGGBB` (tints text, border, background, SVG icon). Empty = default style. |
| Index | Order (0 = primary CTA). |

## Experience

| Field | Description |
|---|---|
| Index / Hidden | Order / visibility. |
| Title | Role / title. |
| Organisation | Where it took place. |
| Period | Free text, e.g. `2020–2022`. |
| Location | Free text. |
| Url / UrlShort | Link and its display alias. |
| Description | Details (HTML allowed). |
| Technologies | Ordered tech tags (via `ExperienceTechnology`). |

## Technology

| Field | Description |
|---|---|
| Name | Technology name. |
| Color | Optional tag hue `#RRGGBB`. Empty = default style. |

## Social

Social links shown in the footer.

| Field | Description |
|---|---|
| IdUser | The [User](#user). |
| Index / Hidden | Order / visibility. |
| Name | Platform name. |
| Pseudo | Your handle. |
| Url | Profile URL. |
| Image | Monochrome icon [File](#file) (tinted to the theme text colour). |

## File

Uploaded files (images, resume…). Referenced by many records. Storage,
overwrite behaviour, deletion rules and cleanup are covered in
[Media & files](media.md).

| Field | Description |
|---|---|
| Name | Display name / alt text. |
| File | The uploaded file. Served under `/media/`; the API returns an **absolute** URL. Same‑name uploads overwrite (stable URLs). |
| CreditsUrl / CreditsShortUrl | Attribution link (used by hero images). |
