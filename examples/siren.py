import pikudhaoref


client = pikudhaoref.SyncClient(update_interval=2)
print(client.history)
print(client.current_sirens)


@client.event()
def on_siren(sirens):
    print(f"Siren alert! started sirens: {sirens}")


@client.event()
def on_siren_end(sirens):
    print(f"Sirens {sirens} have ended.")
