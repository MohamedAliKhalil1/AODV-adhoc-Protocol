from guizero import App, Text, TextBox, PushButton, ListBox

app = App(title="adhoc")
welcome_message = Text(app, text="Welcome to my app", size=40, font="Times New Roman", color="lightblue")
sentCommandsListbox = ListBox(app,width="fill", scrollbar=True)
commandTextBox = TextBox(app, width=70)
sendButton = PushButton(app, text="SEND")
receivedCommandsListBox = ListBox(app,width="fill", scrollbar=True)

