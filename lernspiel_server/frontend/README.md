Lernspiel Online Frontend
=========================

This is the JavaScript / TypeScript code for the Lernspiel Online Core Frontend. It is mainly used
to pull external libraries from the NPM package index and build a distribution bundle.
It also defines an in-browser API for game developers. But except for the games, all other
content is rendered server-side with little to no JavaScript code running in the browser.

The source code is split between two distinct directories:

* `admin`: JS/CSS bundle for the Django Admin
* `website`: JS/CSS bundle for the public website

The admin bundle is used in a few templates that extend the Django Admin. It is separate from
the rest of the website as the Django Admin evolves independently of our public website.
