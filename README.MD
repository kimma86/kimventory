📦 kImventory System

A lightweight inventory management system built with Flask + SQLite.
Supports barcode/EAN scanning, automatic item creation via external API, and live stock warnings.

🚀 Features

Add and edit inventory items

Scan items using EAN/barcode input (keyboard scanner supported)

Automatically fetch product data (Artikelnr & Description) from external API

Configurable "autosave scanned items" toggle (state stored in session)

Dynamic table highlighting:

table-danger when stock = 0 (red)

table-warning when stock < 3 (yellow)

table-success otherwise (green)

Supports manual adds, edits, and deletes

Clean Bootstrap 5 UI

🛠️ Requirements

Python 3.9+

Flask

Flask-SQLAlchemy

Requests
