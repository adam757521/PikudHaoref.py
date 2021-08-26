import pikudhaoref


client = pikudhaoref.Client(update_interval=2)
print(client.history())  # client.history returns sirens that happened in the last 24 hours.
print(client.get_current_sirens())  # Returns the current sirens


@client.event()
def on_siren(sirens):
    print(f"Siren alert! started sirens: {sirens}")


@client.event()
def on_siren_end(sirens):
    print(f"Sirens {sirens} have ended.")