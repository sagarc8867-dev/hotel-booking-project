# Grand Meridian Hotels — Updated Project

This build restructures your project to match the template layout you asked
for, and adds a full login system for both guests and staff.

## What changed

### 1. Templates — now exactly under `templates/admin/` and `templates/user/`

```
templates/
    admin/
        dashboard.html
        hotels.html
        rooms.html
        guests.html
        reservations.html
        billing.html
        housekeeping.html
        login.html          <- staff login (extra, needed for auth)
        _shell.html          <- shared sidebar layout the admin pages extend (extra)
    user/
        home.html
        hotel_detail.html
        room_detail.html
        search.html
        booking.html
        payment.html
        confirmation.html
        my_bookings.html
        login.html           <- guest login (extra, needed for auth)
        register.html        <- guest sign-up (extra, needed for auth)
    base.html, navbar.html, footer.html   <- shared site chrome (unchanged location)
    forms.html, confirm_delete.html       <- shared add/edit & delete-confirm screens
```

All the templates that used to live inside `hotels/templates/`,
`rooms/templates/`, `reservations/templates/` and `billing/templates/` have
been moved into the two folders above and wired up in the views.

### 2. Two logins

- **Guest login** — `/accounts/login/` (template `user/login.html`), plus
  `/accounts/register/` to create an account. Regular guests see "Login /
  Sign Up" in the navbar, and once signed in see "My Bookings".
- **Staff login** — `/accounts/admin-login/` (template `admin/login.html`).
  Only accounts with `is_staff=True` can sign in here; everyone else gets
  an error. Staff see "Admin Panel" in the navbar instead of "My Bookings".
- `/accounts/logout/` logs either type of user out.

Both logins use Django's built-in `User` model — no separate "admin"
model was needed. A guest's bookings are linked to their account through
a new `Guest.user` field, so **My Bookings** can show only their own
reservations.

### 3. New staff dashboard (`/manage/...`)

A new `adminpanel` app powers the whole `templates/admin/` section:

| URL | Page |
|---|---|
| `/manage/` | Dashboard — key stats + recent reservations |
| `/manage/hotels/` | Hotel list, add, edit, delete |
| `/manage/rooms/` | Room list, add, edit, delete |
| `/manage/guests/` | Guest list, add, edit, delete |
| `/manage/reservations/` | Reservation list with Confirm / Check-In / Check-Out / Cancel actions |
| `/manage/billing/` | Payment history + totals |
| `/manage/housekeeping/` | Housekeeping tasks, add/edit/delete |

Every one of these is protected — only logged-in staff (`is_staff=True`)
can reach them; everyone else is bounced to the staff login page.

Checking a reservation out automatically flips the room to `cleaning` and
creates a housekeeping task, same as the flow in `PROJECT_PLAN.md`.

Django's own built-in admin (for raw database editing) is still there,
just moved to `/django-admin/` so it doesn't collide with the new
`/manage/` staff dashboard.

### 4. Model changes

- `guests.Guest` gained a `user` field (one-to-one, nullable) linking a
  guest profile to a login account.
- `housekeeping.Housekeeping` — this model didn't exist yet, so it's been
  added (`room`, `staff_name`, `status`, `remarks`, timestamps) with its
  first migration.

Both come with their migration files already written — you just need to
run `migrate` (see below), your existing `db.sqlite3` data is untouched.

## Running it

```bash
cd hotel-project
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # this account can log in at BOTH
                                    # /django-admin/ and /accounts/admin-login/
python manage.py runserver
```

Then visit:
- `http://127.0.0.1:8000/` — the public site
- `http://127.0.0.1:8000/accounts/login/` — guest login
- `http://127.0.0.1:8000/accounts/register/` — guest sign-up
- `http://127.0.0.1:8000/accounts/admin-login/` — staff login
- `http://127.0.0.1:8000/manage/` — staff dashboard (after staff login)

To make an existing regular user a staff member later (so they can use
the dashboard without being a full superuser), tick "Staff status" for
their account in `/django-admin/`.

## Note

The `venv/` folder from your upload was not included in this zip (virtual
environments are OS-specific and shouldn't be shipped) — recreate it with
the commands above.

## Royal Stay redesign (latest update)

The homepage, navbar, and footer have been re-themed to match the
"Royal Stay" luxury design (gold/navy palette, crown branding, Playfair
Display headings). What changed:

- `static/css/theme.css` — **new** file with the site-wide brand colors,
  navbar, user dropdown, and footer styles. It's loaded on every page via
  `base.html`, so the whole site (not just the homepage) shares the same
  gold/navy branding — including buttons and table headers on the admin
  and login pages, which now pick up the gold accent automatically.
- `static/css/home.css` — trimmed down to just the homepage sections
  (hero, floating search bar, amenities row, featured rooms, "why choose
  us", testimonial, gallery). The navbar/footer rules that used to live
  here were moved into `theme.css` so they apply everywhere, not just on
  `/`.
- `templates/navbar.html` / `templates/footer.html` — rebuilt with the
  crown logo and "ROYAL STAY" branding, and every link now points at a
  URL that actually exists in the project (a couple of links in an
  earlier draft — Billing history, Account settings — pointed at pages
  that were never built, so they've been removed to keep things honest;
  happy to build those out properly if you want them).
- `templates/user/home.html` — the featured rooms section now pulls real
  `Room`/`RoomType` data (name, capacity, floor, price) instead of
  placeholder fields that didn't exist on the model, and cycles through
  your `room1.jpg`/`room2.jpg`/`room3.jpg` photos.
- `hotels/views.py` — the homepage view now passes `featured_rooms`
  (the 4 most recently added available rooms) to the template.

Everything else (booking flow, staff dashboard, login system) is
unchanged — this was a front-end reskin only.

## Background still showing white — fix (latest)

Two likely causes, both fixed:

1. **The background image was 6.5MB** (`hero3.jpg`) — on a slower
   connection it could take a moment to appear, looking blank in the
   meantime. All site images have been compressed (resized to a sane
   max width, JPEG-optimized) — `hero3.jpg` alone went from 6.3MB to
   ~340KB, and the whole `static/images` folder from ~36MB to ~3MB.
   Pages should load close to instantly now.
2. **Hardened the CSS** — the background was set with a combined
   shorthand (`background: <gradient>, <image> center/cover no-repeat
   fixed;`), which is valid but can be finicky. Switched to explicit
   `background-color` / `background-image` / `background-size` /
   `background-position` / `background-repeat` properties instead, and
   added a dark-navy `background-color` fallback — so even in a worst
   case where an image fails to load, you'd see navy, not white.

If it's still showing white after unzipping this version, it's almost
certainly a browser cache from testing the previous version — a hard
refresh (Ctrl/Cmd + Shift + R) on the login/register pages should
clear it up.
