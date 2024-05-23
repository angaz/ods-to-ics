from pyexcel_ods import get_data
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from pprint import pprint
from ical.calendar import Calendar
from ical.event import Event
from ical.calendar_stream import IcsCalendarStream
from aiohttp import web


ods_file = "ETHBerlin04-Volunteer-Schedule.ods"
start_date = datetime(2024, 5, 24, tzinfo=ZoneInfo("Europe/Berlin"))
jobs_start_row = 2
experiances_start_row = 16
slot_cols = [
    (1, 6, timedelta(hours=12), timedelta(hours=16)),
    (7, 12, timedelta(hours=16), timedelta(hours=20)),
    (13, 18, timedelta(hours=20), timedelta(hours=24)),
]


def get_jobs(day_num, row):
    jobs = []

    if len(row) == 0:
        return jobs

    job = row[0]
    if job == "":
        return jobs

    for slot in slot_cols:
        for col in range(slot[0], slot[1]):
            try:
                name = row[col]
                if name == "":
                    continue

                slot_start = start_date + timedelta(days=day_num) + slot[2]
                slot_end = start_date + timedelta(days=day_num) + slot[3]

                jobs.append({
                    "job": job,
                    "start": slot_start,
                    "end": slot_end,
                    "name": name.lower(),
                })
            except IndexError:
                break

    return jobs


jobs = []


def startup():
    ods = get_data(ods_file)

    for day_num, day_name in enumerate(ods):
        day = ods[day_name]

        for row_num in range(jobs_start_row, 100):
            try:
                jobs.extend(get_jobs(day_num, day[row_num]))
            except IndexError:
                break

        for row_num in range(experiances_start_row, 100):
            try:
                jobs.extend(get_jobs(day_num, day[row_num]))
            except IndexError:
                break


async def handle(request):
    name = request.match_info.get('name').lower()

    if name == "":
        return web.Response(status=404)

    my_jobs = [
        job for job in jobs
        if job["name"] == name
    ]

    calendar = Calendar()

    for job in my_jobs:
        calendar.events.append(
            Event(summary=job["job"], start=job["start"], end=job["end"]),
        )

    ics = IcsCalendarStream.calendar_to_ics(calendar)

    return web.Response(text=ics)


def main():
    startup()

    app = web.Application()
    app.add_routes([
        web.get('/{name}', handle)
    ])

    web.run_app(app)


if __name__ == "__main__":
    main()
