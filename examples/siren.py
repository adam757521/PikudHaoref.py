from datetime import datetime

import pikudhaoref


client = pikudhaoref.SyncClient(update_interval=2)

history_range = client.get_history(
    date_range=pikudhaoref.Range(
        datetime(
            year=2014,
            month=7,
            day=24
        ),
        datetime.now()
    )
)
history_month = client.get_history(mode=pikudhaoref.HistoryMode.LAST_MONTH)

print(history_month)
print(history_range)
# The get_history method does not create a city object as it might take a long time.
# In case you need the city information, you can use the get_city method.

print(client.current_sirens)
# The current_sirens property returns the list of current sirens, and gets the city automatically.


@client.event()
def on_siren(sirens):
    print(f"Siren alert! started sirens: {sirens}")


@client.event()
def on_siren_end(sirens):
    print(f"Sirens {sirens} have ended.")


while True:
    pass  # To make sure the script doesnt stop
