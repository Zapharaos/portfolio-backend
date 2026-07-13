# Media & files

Uploaded files (images, resume…) are stored as [`File`](models.md#file) records
and served under `/media/`. A few behaviours are worth knowing.

## Uploads overwrite by name

`File.file` uses a custom `OverwriteStorage`: uploading a file whose name is
already taken **overwrites** it instead of Django's default (appending a random
suffix like `cv_a1B2c3.pdf`).

Why: it keeps **stable URLs** (your resume always lives at the same path) and
stops orphaned copies from piling up on disk. The API returns **absolute** media
URLs so the front‑end can load them cross‑origin.

## The admin warns before overwriting

When you upload a file in the admin whose name is already used by **another**
`File` record, the form blocks the save with a message naming the record that
would be overwritten:

> A file named "cv.pdf" is already used by "Resume" (id 5). Uploading it would
> overwrite that file. Rename your file, or edit that record instead.

Re‑uploading a same‑named file **on the same record** is allowed — that's an
intentional replacement.

## Deleting files never deletes content

The foreign keys pointing at `File` are **not** `CASCADE` (a past footgun where
deleting a File deleted the User that referenced it):

| Reference | On delete |
|---|---|
| Optional (`Project.image`, `User.resume`, `About.imageResponsive`) | `SET_NULL` — the reference is cleared, the record survives. |
| Required (`User.logo`, `Hero.backgroundImage`, `About.image`, `Social.image`) | `PROTECT` — you **can't** delete a File still in use; unlink it first. |

When a `File` record is deleted, its file is removed from disk (a `post_delete`
signal). Replacing a File's upload with a **differently‑named** one also deletes
the old file, so it doesn't become an orphan.

## Clean up orphaned media

Files can still be orphaned on disk (e.g. left over from before the overwrite
storage, or from records deleted by an older version). The management command
removes any media file that **no `File` record references**:

```bash
# List what would be removed (safe)
python manage.py clean_orphan_media --dry-run

# Actually delete the orphans
python manage.py clean_orphan_media
```

In production, run it inside the container:

```bash
docker compose -f docker-compose.prod.yml exec portfolio-backend \
  python manage.py clean_orphan_media --dry-run
```

## CDN caching caveat

If media is served behind a CDN (e.g. Cloudflare), responses are cached at the
edge (often a few hours). Combined with the **stable URLs** above, this means:

- Immutable files (images) benefit from long caching — good.
- A **replaced** file (e.g. a new resume at the same URL) keeps serving the old
  version from the CDN until the cache expires or is **purged**.

After updating such a file, **purge the CDN cache** for its URL (or the whole
zone). To check the *origin* (bypassing the edge cache), append a random query
string and look at the cache‑status header:

```bash
curl -sI "https://api.example.com/media/cv.pdf?nocache=$RANDOM" | grep -i cache
```

## Files are not baked into the Docker image

`.dockerignore` excludes `media/` and `db.sqlite3` from the build context, so
runtime data is never copied into the image (which would resurrect old files on
every rebuild). Persistence relies on the volume / bind‑mount — see
[Deployment](deployment.md).
