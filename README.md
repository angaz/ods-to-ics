# ODS to ICS

Takes a schedule in ODS (Open Document Sheets) format and runs a service to
export the data as ICS calendars which can be imported into your calendar
via a URL.

Each day should be on a consecutive sheet.

The `example.ods` file shows how to format the spreadsheet.

The schedule for a specific person can be queried with `GET /name`, with `name`
being the name of the person in the sheet. The name is case insensitive.

Nothing special is needed for any reverse proxies. The default port is 8080.

The project comes with a [Nix][nixos] flake. Use `nix develop`, then
`python3 main.py` to run the server.

[nixos]: https://nixos.org
