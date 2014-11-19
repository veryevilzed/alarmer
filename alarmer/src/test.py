from alarmer import Main

main = Main()

email = main.Informer(
    message = "Hello!"
)

main.Checker(
    name="demo", 
    run="",
    informers = [email]
)

main.run()